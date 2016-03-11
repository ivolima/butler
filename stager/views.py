#coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.text import slugify
from models import *
from django.core.urlresolvers import reverse

from requests_oauthlib import OAuth1

import ipdb
import json
import requests

def login(request):
    return render(request, 'stager/login.html', {})

@login_required
def dashboard(request):
    #ipdb.set_trace()
    projects = Project.objects.filter(owner=request.user)
    webhooks = Webhook.objects.filter(owner=request.user)
    if not projects:
        projects = fetch_repositories(request.user)
    context = {'projects':projects, 'webhooks': webhooks}
    return render(request, 'stager/dashboard.html', context)

@require_POST
def add_repository(request):
    ipdb.set_trace()
    print request
    return HttpResponse("To be implemented")

@login_required
def create_webhook(request, project_uuid):
    """Given an object User and a project UUID, it creates a webhook for this project via API"""
    ipdb.set_trace()
    user = request.user
    project = Project.objects.get(cod_uuid=project_uuid)
    extra_data = json.loads(user.social_auth.values()[0]['extra_data'])
    webhook_url = settings.BUTLER_DEV_URL + project_uuid + "/"
    oauth = OAuth1(
                    settings.SOCIAL_AUTH_BITBUCKET_KEY,
                    settings.SOCIAL_AUTH_BITBUCKET_SECRET,
                    extra_data['access_token']['oauth_token'],
                    extra_data['access_token']['oauth_token_secret']
                )
    payload = {
                "description": "Butler Alert",
                "url": webhook_url,
                "active": True,
                "events": ["pullrequest:created", "pullrequest:updated", "pullrequest:fulfilled"]
            }

    project_slug = slugify(project.name)
    response = requests.post(settings.BITBUCKET_CREATE_WEBHOOK.format(owner=user.username, repo_slug=project_slug), auth=oauth, data=json.dumps(payload))
    ipdb.set_trace()
    if response.ok:
        data = json.loads(response.text)
        # persist webhook
        hook = Webhook()
        hook.url = data.get("url", webhook_url)
        hook.project = project
        hook.owner = user
        hook.description = data.get("description", "")
        hook.scope = str(data.get("events", ""))
        hook.save()
        # TODO: add a success message and redirect to stager/dashboard
        return HttpResponseRedirect(reverse('dashboard'))

    # TODO: add an error message here
    context = {}
    return render(request, 'stager/dashboard.html', context)

@csrf_exempt
@require_POST
def webhooks(request, user_id, project_id):
    """Parses webhooks requests and persists info into db"""
    body = json.loads(request.body)

    if request.META.get("HTTP_USER_AGENT", "") == settings.BITBUCKET_USER_AGENT:
        print "Webhook received from Bitbucket"
        return parse_bitbucket_webhook(body, project_id)
    elif request.META.get("HTTP_USER_AGENT", "") == settings.GITHUB_USER_AGENT:
        print "Webhook received from Github. It needs to be implemented"
        return parse_github_webhook(body)
    else:
        print "Couldn't recognize this service"
        return HttpResponseForbidden("Couldn't recognize this service",content_type="text/plain")

def parse_bitbucket_webhook(json_content, project_id):
    #ipdb.set_trace()
    project = Project.objects.get(cod_uuid=project_id)
    pullrequest = json_content.get('pullrequest', False)
    repository = json_content.get('repository', {})
    actor = json_content.get('actor', {})
    try:
        repository_from_webhook = repository['links']['html']['href']
    except:
        repository_from_webhook = "ERROR"

    # Checks if repository url matches with repository sent via webhook
    repo_verified = (project.repository_url == repository_from_webhook)

    if repo_verified and pullrequest:
        webhook = Webhook()
        webhook.pull_request = json.dumps(pullrequest)
        webhook.repository = json.dumps(repository)
        webhook.actor = json.dumps(actor)
        webhook.project = project
        webhook.save()

        # TODO: We need to decide what exactly should be persisted. By now, I'm considering to persist these 3 dictionaries as plain text
        return HttpResponse("CHEGOU EM PAZ")
    return HttpResponseForbidden("We only support pull request webhooks. Please verify yours",content_type="text/plain")

def fetch_repositories(user, role="owner", persist=False):
    """Given an object User, it gets all repositories owned by this user"""

    extra_data = json.loads(user.social_auth.values()[0]['extra_data'])
    oauth = OAuth1(
                    settings.SOCIAL_AUTH_BITBUCKET_KEY,
                    settings.SOCIAL_AUTH_BITBUCKET_SECRET,
                    extra_data['access_token']['oauth_token'],
                    extra_data['access_token']['oauth_token_secret']
                    )
    response = requests.get(settings.BITBUCKET_REPOSITORIES_URL.format(username=user.username), auth=oauth)

    #ipdb.set_trace()
    data = json.loads(response.text)
    projects = data.get("values")
    result = []
    for proj in projects:
        d = {
                "name": proj["name"],
                "scm": proj["scm"],
                "is_private": proj["is_private"],
                "language": proj["language"],
                "repository_url": proj["links"]["html"]["href"]
            }
        result.append(d)
        # TODO: verify if project already exists and update it
        obj = Project(**d)
        obj.owner = user
        obj.raw = json.dumps(proj)
        obj.save()
    return result

def parse_github_webhook(json_content):
    return HttpResponseForbidden("It needs to be implemented",content_type="text/plain")
