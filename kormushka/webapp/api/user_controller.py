from django.shortcuts import render
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
import webapp.repository.user_repository as user_repository
import json
from django.http import HttpResponse, Http404

### departs page
@login_required(login_url="/login/")
def getUsers(request):
    if request.is_ajax() and request.POST:
        depart_pk = request.POST.get('departId')

        users = user_repository.getUsersByDeparts([depart_pk])
        data = [{"id": u.pk, "fullName": u.get_full_name()} for u in users]
        # data = {"s": "s"}
        return HttpResponse(json.dumps(data))
    raise Http404