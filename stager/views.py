from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt, csrf_protect

def index(request):
    return HttpResponse("Pagina inicial!")

@csrf_exempt
@require_POST
def add_repository(request):
    import ipdb; ipdb.set_trace()
    print request


