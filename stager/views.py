from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_POST

def index(request):
    return HttpResponse("Pagina inicial")

@require_POST
def add_repository(request):
    import ipdb; ipdb.set_trace()
    print request


