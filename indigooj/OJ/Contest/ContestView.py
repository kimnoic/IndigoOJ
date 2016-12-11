# -* encoding: UTF-8 *-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from OJ.models import *
from OJ.OJcore import HojControl
from OJ.User.UserSession import sessionGetUserInfo
from django import forms
from django.forms.models import model_to_dict
from django.utils.timezone import localtime


def awaretonaive(aware):
    aware = localtime(aware)
    aware = aware.replace(tzinfo=None)
    return aware


def contestoutofdate(contestid):
    if contestid == 0:
        return True
    try:
        con = Contest.objects.get(pk=contestid)
    except:
        return False
    dic = model_to_dict(con)
    dic["assignlimit"] = awaretonaive(dic["assignlimit"])
    dic["starttime"] = awaretonaive(dic["starttime"])
    dic["endtime"] = awaretonaive(dic["endtime"])
    dic["pk"] = con.pk
    if datetime.datetime.now() <= dic["assignlimit"]:
        dic["status"] = "unopen"
    elif datetime.datetime.now() <= dic["starttime"]:
        dic["status"] = "pending"
    elif datetime.datetime.now() <= dic["endtime"]:
        dic["status"] = "contesting"
    else:
        dic["status"] = "colsed"
    if dic["status"] != "contesting":
        return False
    else:
        return True


class ContestForm(forms.Form):
    title = forms.CharField(max_length=50, widget=forms.TextInput())
    assignlimit = forms.DateTimeField


def contestlist(request):
    uid = sessionGetUserInfo(request)["uid"]
    account = sessionGetUserInfo(request)["account"]
    if uid == '':
        return HttpResponseRedirect('/login/')
    con = Contest.objects.all()
    contest = []
    for i in con:
        dic = model_to_dict(i)
        dic["assignlimit"] = awaretonaive(dic["assignlimit"])
        dic["starttime"] = awaretonaive(dic["starttime"])
        dic["endtime"] = awaretonaive(dic["endtime"])
        dic["pk"] = i.pk
        if datetime.datetime.now() <= dic["assignlimit"]:
            if(User.objects.get(pk=uid) in i.candidates.all()):
                dic["status"] = "signed"
            else:
                dic["status"] = "unopen"
        elif datetime.datetime.now() <= dic["starttime"]:
            dic["status"] = "pending"
        elif datetime.datetime.now() <= dic["endtime"]:
            if(User.objects.get(pk=uid) in i.candidates.all()):
                dic["status"] = "contesting"
            else:
                dic["status"] = "unsinged"
        else:
            dic["status"] = "colsed"
        contest.append(dic)

    return render(request, "OJ/contestlist.html", {"uid": uid, "account": account, "contestlist": contest})


def contestsign(request):
    if request.method == "POST":
        uid = sessionGetUserInfo(request)["uid"]
        if uid == '':
            return HttpResponse("请先登录")
        contest = Contest.objects.get(pk=request.POST["pk"])
        candidate = User.objects.get(pk=uid)
        con = ContestLog(contest=contest, candidate=candidate)
        con.save()
        return HttpResponse("报名成功！")
    else:
        return HttpResponseRedirect('/contest/')


def contest(request, id):
    uid = sessionGetUserInfo(request)["uid"]
    account = sessionGetUserInfo(request)["account"]
    if uid == '':
        return HttpResponseRedirect('/login/')
    contest = Contest.objects.get(pk=id)
    problems = ContestProblem.objects.filter(contest=contest)
    candidates = contest.candidates.all()
    contestlg = ContestLog.objects.filter(
        candidate=User.objects.get(pk=uid), contest=contest)
    if contestlg.count() == 0:
        attend = False
        contestlog = {}
    else:
        contestlog = contestlg[0]
        attend = True
    con = model_to_dict(contest)
    con["template"] = "OJ/Contests/" + str(id) + ".html"
    contestrank = []
    for i in candidates:
        b = ContestLog.objects.get(candidate=i,contest = contest)
        a = model_to_dict(b)
        a["account"] = b.candidate.accountname
        contestrank.append(a)

    return render(request, "OJ/contest.html", {"contestrank": contestrank, "uid": uid, "account": account, "contest": con, "candidates": candidates,
                                               "problems": problems, "pk": id, "contestlog": contestlog, "attend": attend})


def addcontest(request):

    return "OK"
