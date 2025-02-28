import json

from django.http import HttpResponse
from django.shortcuts import reverse
from django.http.response import HttpResponseRedirect


def allow_manager(fuction):
    def wrapper(request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_manager:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                response_data = {
                    "status": "error",
                    "title": "Unauthorized Access",
                    "message": "You can't perform this action"
                }
                return HttpResponse(json.dumps(response_data),content_type="application/json")

            else:
                return HttpResponseRedirect(reverse("managers:logout"))

        
        return fuction(request, *args, **kwargs)

    return wrapper
def allow_customer(fuction):
    def wrapper(request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_customer:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                response_data = {
                    "status": "error",
                    "title": "Unauthorized Access",
                    "message": "You can't perform this action"
                }
                return HttpResponse(json.dumps(response_data),content_type="application/json")

            else:
                return HttpResponseRedirect(reverse("customers:logout"))

        
        return fuction(request, *args, **kwargs)

    return wrapper
def allow_provider(fuction):
    def wrapper(request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_provider:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                response_data = {
                    "status": "error",
                    "title": "Unauthorized Access",
                    "message": "You can't perform this action"
                }
                return HttpResponse(json.dumps(response_data),content_type="application/json")

            else:
                return HttpResponseRedirect(reverse("providers:logout"))

        
        return fuction(request, *args, **kwargs)

    return wrapper