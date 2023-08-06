import cloudinary
import os
from io import BytesIO
from django.core.cache import InvalidCacheBackendError, caches
from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.images.image_operations import MinMaxOperation
from wagtail.images.models import (
    Image,
    AbstractImage,
    AbstractRendition,
    Filter,
    get_upload_to,
)

from cloudinary_storage.storage import MediaCloudinaryStorage


class AbstractCloudinaryImage(AbstractImage):
    file = models.ImageField(
        verbose_name=_("file"),
        upload_to=get_upload_to,
        width_field="width",
        height_field="height",
        storage=MediaCloudinaryStorage(),
    )
    admin_form_fields = Image.admin_form_fields

    class Meta(AbstractImage.Meta):
        abstract = True

    def get_rendition(self, filter):
        if isinstance(filter, str):
            filter = Filter(spec=filter)

        cache_key = filter.get_cache_key(self)
        Rendition = self.get_rendition_model()

        try:
            rendition_caching = True
            cache = caches["renditions"]
            rendition_cache_key = Rendition.construct_cache_key(
                self.id, cache_key, filter.spec
            )
            cached_rendition = cache.get(rendition_cache_key)
            if cached_rendition:
                return cached_rendition
        except InvalidCacheBackendError:
            rendition_caching = False

        try:
            rendition = self.renditions.get(
                filter_spec=filter.spec, focal_point_key=cache_key,
            )
        except Rendition.DoesNotExist:
            # Generate filename
            input_filename = os.path.basename(self.file.name)
            input_filename_without_extension, input_extension = os.path.splitext(
                input_filename
            )

            # A mapping of image formats to extensions
            FORMAT_EXTENSIONS = {
                "jpeg": ".jpg",
                "png": ".png",
                "gif": ".gif",
                "webp": ".webp",
            }

            output_extension = (
                filter.spec.replace("|", ".")
                # + FORMAT_EXTENSIONS[generated_image.format_name]
            )
            if cache_key:
                output_extension = cache_key + "." + output_extension

            # Truncate filename to prevent it going over 60 chars
            output_filename_without_extension = input_filename_without_extension[
                : (59 - len(output_extension))
            ]
            output_filename = output_filename_without_extension + "." + output_extension

            width = self.width
            height = self.height
            # Every filter operation needs implemented as a Cloudinary transform
            # Only MinMax is supported at this time.
            for operation in filter.operations:
                if isinstance(operation, MinMaxOperation):
                    image_width = self.width
                    image_height = self.height
                    horz_scale = operation.width / image_width
                    vert_scale = operation.height / image_height

                    if operation.method == "min":
                        if (
                            image_width <= operation.width
                            or image_height <= operation.height
                        ):
                            break

                        if horz_scale > vert_scale:
                            width = operation.width
                            height = int(image_height * horz_scale)
                        else:
                            width = int(image_width * vert_scale)
                            height = operation.height

                    elif operation.method == "max":
                        if (
                            image_width <= operation.width
                            and image_height <= operation.height
                        ):
                            break

                        if horz_scale < vert_scale:
                            width = operation.width
                            height = int(image_height * horz_scale)
                        else:
                            width = int(image_width * vert_scale)
                            height = operation.height

            rendition, created = self.renditions.get_or_create(
                filter_spec=filter.spec,
                focal_point_key=cache_key,
                defaults={"width": width, "height": height,},
            )

        if rendition_caching:
            cache.set(rendition_cache_key, rendition)

        return rendition


class AbstractCloudinaryRendition(AbstractRendition):
    file = None  # No need for actual file

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
        abstract = True

    @property
    def url(self):
        url, _ = cloudinary.utils.cloudinary_url(
            self.image.file.name, height=self.height, width=self.width
        )
        return url
