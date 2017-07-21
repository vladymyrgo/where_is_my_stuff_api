# -*- coding: utf-8 -*-
import uuid
from os.path import splitext

from django.conf import settings
from django.core.files.storage import get_storage_class
from django.core.files.images import ImageFile


def upload_to(instance, filename):
    """Handler that avoids storing all files in one directory.
    """
    opts = instance._meta
    app_label = opts.app_label
    model_name = instance.__class__.__name__.lower()
    filename, extension = splitext(filename)
    filename = uuid.uuid4().hex
    return "{}/{}/{}/{}{}".format(app_label,
                                  model_name,
                                  instance.id,
                                  filename,
                                  extension)


def get_static_image_file(path):
    storage_class = get_storage_class(settings.STATICFILES_STORAGE)
    storage = storage_class()
    image = ImageFile(storage.open(path))
    image.storage = storage
    return image
