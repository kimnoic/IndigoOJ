from django.shortcuts import render
from django.http import HttpResponse
from User import UserAction
from Problem import ProblemView, StatusView
from Contest import ContestView

# Create your views here.


def index(request):  # index may be beautiful
    try:
        uid = request.session['uid']
        account = request.session['accountname']
    except KeyError:
        uid = ''
        account = ''

    return render(request, 'OJ/index.html', {'uid': uid, 'account': account})


def login(request):
    return UserAction.login(request)


def logout(request):
    return UserAction.logout(request)
    # return HttpResponse("<h1>Logout</h1>" + request.META['HTTP_REFERER'])


def register(request):
    return UserAction.register(request)


def problemset(request):
    return ProblemView.problemset(request)


def problem(request, id ,contest=0):
    return ProblemView.problem(request, id,contest)


def statuslist(request):
    return StatusView.statuslist(request)


def status(request, id):
    return StatusView.status(request, id)


def userProblemStatus(request):
    return StatusView.userProblemStatus(request)


def contestList(request):
    return ContestView.contestlist(request)


def contestSign(request):
    return ContestView.contestsign(request)


def contest(request, id):
    return ContestView.contest(request, id)
