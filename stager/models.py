from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import uuid


def generate_uuid4():
    return str(uuid.uuid4().hex)

class Project(models.Model):
    cod_uuid = models.CharField(max_length=40, primary_key=False, default=generate_uuid4, editable=False)
    repository_url = models.URLField(default="")
    name = models.CharField(max_length=40, default="")
    owner = models.ForeignKey(User)
    is_private = models.BooleanField(default=None)
    scm = models.CharField(max_length=10)
    language = models.CharField(max_length=40, default="")
    raw_json = models.TextField(default="")

class Webhook(models.Model):
    url = models.URLField(default="")
    project = models.ForeignKey(Project)
    owner = models.ForeignKey(User)
    description = models.CharField(max_length=40, default="Butler Alert")
    scope = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)

class WebhookRequest(models.Model):
    pull_request = models.TextField()
    repository = models.TextField()
    actor = models.TextField()
    project = models.ForeignKey(Project)

