from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from models import *

import ipdb, json

def dashboard(request):
    return HttpResponse("Pagina inicial!")

@require_POST
def add_repository(request):
    ipdb.set_trace()
    print request
    return HttpResponse("To be implemented")

@csrf_exempt
@require_POST
def webhooks(request, user_id, project_id):
    BITBUCKET_USER_AGENT = 'Bitbucket-Webhooks/2.0'
    GITHUB_USER_AGENT = 'TO BE IMPLEMENTED'

    #ipdb.set_trace()
    body = json.loads(request.body)

    if request.META.get("HTTP_USER_AGENT", "") == BITBUCKET_USER_AGENT:
        print "Webhook received from Bitbucket"
        return parse_bitbucket_webhook(body, project_id)
    elif request.META.get("HTTP_USER_AGENT", "") == GITHUB_USER_AGENT:
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

        # We need to decide what exactly should be persisted. By now, I'm considering to persist these 3 dictionaries as plain text
        return HttpResponse("CHEGOU EM PAZ")
    return HttpResponseForbidden("We only support pull request webhooks. Please verify yours",content_type="text/plain")


def parse_github_webhook(json_content):
    return HttpResponseForbidden("It needs to be implemented",content_type="text/plain")
