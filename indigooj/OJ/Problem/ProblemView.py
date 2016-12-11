# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from OJ.models import *
from OJ.OJcore import HojControl
from OJ.User.UserSession import sessionGetUserInfo
from OJ.Contest.ContestView import *
from django import forms
from django.forms.models import model_to_dict
import json


def trim(s):
    if s == '':
        return ''
    else:
        return s  # s[2:][:-2]


def trim2(s):
    if s == '':
        return ''
    else:
        return s


class SubmitForm(forms.Form):
    number = forms.IntegerField(widget=forms.HiddenInput)
    id = forms.IntegerField(widget=forms.HiddenInput)
    contest = forms.IntegerField(widget=forms.HiddenInput)
    lan = forms.ChoiceField(label="选择语言", choices=(
        ('C++', 'C++'),
        ('C89', 'C89'),
        ('Java', 'Java'),
    ))
    code = forms.CharField(label='', widget=forms.Textarea(
        attrs={"id": "code", "class": "hidden", "placeholder": "在这里输入"}), max_length=2000)


def savestatus(status, contest_id, uid):
    if contest_id == 0:
        print "未进入竞赛"
        status.save()
    else:
        contest = Contest.objects.get(pk=contest_id)
        user = User.objects.get(pk=uid)
        if user in contest.candidates.all():
            print "attend"
            p = status.problem
            constprob = ContestProblem.objects.filter(
                contest=contest, problem=p)
            if constprob.count == 0:
                print "unattend"
                status.save()
            else:
                print "problemin"
                contestproblem = constprob[0]
                print contestproblem
                cps = ContestProblemStatus.objects.filter(
                    problem=contestproblem, candidate=user)
                if cps.count() == 0:
                    print "nocps"
                    cpsn = ContestProblemStatus(
                        problem=contestproblem, candidate=user)
                else:
                    print "arucps"
                    cpsn = cps[0]
                if cpsn.status == 1:
                    print "accepted"
                    status.save()
                else:
                    print "notaccept"
                    if status.status == "Accepted":
                        print "accpet"
                        cpsn.status = 1
                        cpsn.laststatus = status.status
                        cpsn.endtime = datetime.datetime.now()
                        cpsn.save()
                        cl = ContestLog.objects.filter(
                            contest=contest, candidate=user)[0]
                        cl.problemsolved.add(contestproblem)
                        cl.point += contestproblem.point
                        cl.save()
                    else:
                        print "yetnot"
                        cpsn.laststatus = status.status
                        cpsn.save()
                    status.save()
        else:
            status.save()

def pager(page, lastpage):
    a = {}
    first = 1
    if lastpage <= 9:
        for i in range(1, lastpage + 1):
            a[str(i)] = i

    else:
        if page <= 5:
            for i in range(1, 8):
                a[str(i)] = i
            if lastpage >= 19:
                a["8"] = 0
                a["9"] = 19
            else:
                a["8"] = 0
                a["9"] = lastpage
        elif page < lastpage - 4:
            first = page - 4
            for i in range(1, 8):
                a[str(i)] = first + i - 1
            if lastpage >= page + 14:
                a["8"] = 0
                a["9"] = page + 14
            else:
                a["8"] = 0
                a["9"] = lastpage
        else:
            first = lastpage - 8
            for i in range(1, 10):
                a[str(i)] = first + i - 1

    for i in a:
        a[i] = str(a[i])

    return a


def problemset(request):
    if request.method == 'GET':
        try:
            page = request.GET['page']
        except KeyError:
            page = '1'
    else:
        page = '1'

    problem_list = []
    a = Problem.objects.all()
    lastpage = a.count() / 50
    lis = a[50 * eval(page) - 50:50 * eval(page)]
    pagelist = pager(eval(page), lastpage)

    for i in lis:
        # print i.submitted
        if(i.submitted != 0):
            ratio = str(i.accepted * 100.0 / i.submitted)[:5]
            # print ratio
        else:
            ratio = '0'

        if(i.submitted_on_oringin != 0):
            ratio_on_oringin = str(
                i.accepted_on_oringin * 100.0 / i.submitted_on_oringin)[:5]
            # print ratio_on_oringin
        else:
            ratio_on_oringin = '0'

        uid = sessionGetUserInfo(request)["uid"]
        account = sessionGetUserInfo(request)["account"]

        dic = {'oj': i.oj.name, 'number': i.number, 'submitted': i.submitted, 'accepted': i.accepted,
               'submitted_on_oringin': i.submitted_on_oringin, 'accepted_on_oringin': i.accepted_on_oringin,
               'ratio_on_oringin': ratio_on_oringin, 'ratio': ratio, 'id': i.id, 'title': trim2(i.title)}
        problem_list.append(dic)

    return render(request, "OJ/problemset.html", {'page': page, 'problem_list': problem_list, 'pagelist': pagelist, 'lastpage': lastpage, "uid": uid, "account": account})


def problem(request, id, contest_id=0):
    if not contestoutofdate(contest_id):
        contest_id = 0

    try:
        refer = request.META['HTTP_REFERER']
    except KeyError:
        refer = "/Problem/"

    try:
        i = Problem.objects.get(pk=id)
    except Problem.DoesNotExist:
        return HttpResponseRedirect(refer)

    uid = sessionGetUserInfo(request)["uid"]
    account = sessionGetUserInfo(request)["account"]

    if(i.submitted != 0):
        ratio = str(i.accepted * 100.0 / i.submitted)[:5]
        # print ratio
    else:
        ratio = '0'

    if(i.submitted_on_oringin != 0):
        ratio_on_oringin = str(i.accepted_on_oringin *
                               100.0 / i.submitted_on_oringin)[:5]
        # print ratio_on_oringin
    else:
        ratio_on_oringin = '0'

    dic = {'oj': i.oj.name, 'number': i.number, 'submitted': i.submitted, 'accepted': i.accepted,
           'submitted_on_oringin': i.submitted_on_oringin, 'accepted_on_oringin': i.accepted_on_oringin,
           'ratio_on_oringin': ratio_on_oringin, 'ratio': ratio, 'id': i.id, 'title': trim2(i.title),
           'time_limit': i.time_limit, 'mem_limit': i.mem_limit, 'detail': trim(i.detail), 'sample': trim(i.sample),
           'sampleinput': trim(i.sampleinput), 'sampleoutput': trim(i.sampleoutput), 'source': i.source}

    if request.method == "POST":
        # print "进入了Post分支"
        form = SubmitForm(request.POST)
        if form.is_valid():
            if uid == '':
                msg = u'请先登陆'
                form._errors['code'] = form.error_class([msg])
                return render(request, "OJ/problem.html", {'problem': dic, 'form': form, 'uid': uid, 'account': account, 'contest': contest_id})
            data = form.cleaned_data
            result = HojControl.Submit().Submit(
                str(data['number']), data['lan'], data['code'])
            i.submitted += 1
            if result[0] == 'Accepted':
                i.accepted += 1
            i.save()
            user = User.objects.get(pk=uid)
            status = Status(problem=i, status=result[0],
                            time=int(eval(result[1][:-2]) * 1000), mem=eval(result[2][:-2]),
                            user=user, codelength=eval(result[3][:-2]), lan=data['lan'])
            print status
            savestatus(status, data['contest'], uid)
            return HttpResponseRedirect("/status/user/")
        else:
            return render(request, "OJ/problem.html", {'problem': dic, 'form': form, "uid": uid, "account": account, 'contest': contest_id})
    else:
        form = SubmitForm(
            {'number': i.number, 'id': i.id, 'lan': 'C++', 'code': 'null', "contest": contest_id})

    return render(request, "OJ/problem.html", {'problem': dic, 'form': form, 'uid': uid, 'account': account, 'contest': contest_id})
