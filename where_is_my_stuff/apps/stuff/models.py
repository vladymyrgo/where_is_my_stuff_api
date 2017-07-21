from django.db import models
from django.contrib.gis.db import models as geo_models
from django.utils.translation import ugettext_lazy as _

from base.utils.files_storage import upload_to

from base.models import TimeStampedUUIDModel


class Stuff(TimeStampedUUIDModel):
    user = models.ForeignKey('users.User', verbose_name=_('User'), related_name="stuffs")
    title = models.CharField(_('Title'), max_length=120)
    photo = models.ImageField(_('Photo'), upload_to=upload_to, max_length=500, blank=True)
    location = geo_models.PointField(_('Location'), blank=True, null=True, geography=True)

    class Meta:
        verbose_name = _("Stuff")
        verbose_name_plural = _("Stuffs")
        ordering = ['-created']

    def __str__(self):
        return str(self.created)
