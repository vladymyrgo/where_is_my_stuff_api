# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
import uuid

# Third Party Stuff
from django.db import models
from django.utils.translation import ugettext_lazy as _
from versatileimagefield.fields import PPOIField, VersatileImageField

from .utils.files_storage import upload_to


class UUIDModel(models.Model):
    """
    An abstract base class model that makes primary key `id` as UUID
    instead of default auto incremented number.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class TimeStampedUUIDModel(UUIDModel):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields with UUID as primary_key field.
    """
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class IsActiveModel(models.Model):
    """
    An abstract base class model that provides is_active field
    to avoid deleting instances from DB.
    is_active == False means that instance is 'deleted' from actual list of instances.
    """
    is_active = models.BooleanField(_('Active'), default=True,
                                    help_text=('Designates whether this instance '
                                               'should be treated as active. '
                                               'Unselect this instead of deleting instances.'))

    class Meta:
        abstract = True


class ImageMixin(models.Model):
    """
    An abstract base class model that provides a VersatileImageField Image with POI
    """

    image = VersatileImageField(upload_to=upload_to, blank=True, null=True, ppoi_field='image_poi',
                                verbose_name="image")
    image_poi = PPOIField(verbose_name="image's Point of Interest")  # point of interest

    class Meta:
        abstract = True
