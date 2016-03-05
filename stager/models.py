from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    # Unique identifier fieldi
    cod_uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, verbose_name=(u'UUID'))
    user = models.OneToOneField(User, unique=True, verbose_name=('user'), related_name='my_profile')

    class Meta:
        verbose_name = (u'Profile')
        verbose_name_plural = (u'Profiles')
        #ordering = ('user_last_name',)

    def __unicode_(self):
        return unicode(self.user.username)

    def __str__(self):
        return str(self.user.username)

class Project(models.Model):
    cod_uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, verbose_name=(u'UUID'))
    repository_url = models.URLField()
    profile_id = models.ForeignKey(Profile)
