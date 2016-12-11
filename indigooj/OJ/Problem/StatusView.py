from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from OJ.models import *
from OJ.User.UserSession import sessionGetUserInfo


def statuslist(request):
    uid = sessionGetUserInfo(request)["uid"]
    account = sessionGetUserInfo(request)["account"]

    if uid == '':
        return HttpResponseRedirect('/login/')

    statuslist = []
    status = Status.objects.all()
    for i in range(status.count() - 1, -1, -1):
        statuslist.append({'id': status[i].id, 'problem': status[i].problem, 'subtime': status[i].subtime, 'status': status[i].status,
                           'time': status[i].time, 'lan': status[i].lan, 'mem': status[i].mem, 'user': status[i].user, 'codelength': status[i].codelength})

    return render(request, "OJ/statuslist.html", {'statuslist': statuslist, "uid": uid, "account": account})


def status(request, id):
    uid = sessionGetUserInfo(request)["uid"]
    account = sessionGetUserInfo(request)["account"]

    if uid == '':
        return HttpResponseRedirect('/login/')

    statuslist = []
    problem = Problem.objects.get(pk=id)
    status = Status.objects.filter(problem=problem)
    for i in range(0, status.count()):
        statuslist.append({'id': status[i].id, 'problem': status[i].problem, 'subtime': status[i].subtime, 'status': status[i].status,
                           'time': status[i].time, 'lan': status[i].lan, 'mem': status[i].mem, 'user': status[i].user, 'codelength': status[i].codelength})

    return render(request, "OJ/statuslist.html", {'statuslist': statuslist, "uid": uid, "account": account})


def userProblemStatus(request):
    uid = sessionGetUserInfo(request)["uid"]
    account = sessionGetUserInfo(request)["account"]
    if uid == '':
        return HttpResponseRedirect('/login/')

    statuslist = []
    user = User.objects.get(pk=uid)
    status = Status.objects.filter(user=user)
    for i in range(0, status.count()):
        statuslist.append({'id': status[i].id, 'problem': status[i].problem, 'subtime': status[i].subtime, 'status': status[i].status,
                           'time': status[i].time, 'lan': status[i].lan, 'mem': status[i].mem, 'user': status[i].user, 'codelength': status[i].codelength})

    return render(request, "OJ/statuslist.html", {'statuslist': statuslist, "uid": uid, "account": account})
