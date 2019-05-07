from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. Welcome to ssh user creation and revoke  app")
