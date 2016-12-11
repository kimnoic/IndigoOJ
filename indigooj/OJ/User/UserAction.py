# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django import forms
from OJ.models import User
from OJ.User.UserSession import sessionGetUserInfo


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    password = forms.CharField(
        label="密码", max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control"}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    password = forms.CharField(
        label="密码", max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    name = forms.CharField(label="昵称", max_length=20, widget=forms.TextInput(
        attrs={"class": "form-control"}))


def login(request):
    uid = sessionGetUserInfo(request)["uid"]
    account = sessionGetUserInfo(request)["account"]

    if uid != '':
        return HttpResponseRedirect("/")  # 待修复:当登陆后重复提交登录应该被屏蔽掉

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = User.objects.get(accountname=data['username'])
            except User.DoesNotExist:
                msg = u'用户不存在'
                form._errors['username'] = form.error_class([msg])
                return render(request, "OJ/login.html", {'form': form, "uid": uid, "account": account})
            if user.password == data['password']:
                request.session['accountname'] = user.accountname
                request.session['uid'] = user.id
                return HttpResponseRedirect("/")
            else:
                msg = u'密码不正确'
                form._errors['password'] = form.error_class([msg])
                return render(request, "OJ/login.html", {'form': form, "uid": uid, "account": account})
        else:
            return render(request, "OJ/login.html", {'form': form, "uid": uid, "account": account})

    form = LoginForm()

    return render(request, "OJ/login.html", {'form': form, "uid": uid, "account": account})


def logout(request):
    try:
        del request.session['uid']
        del request.session['accountname']
        print "UserLogOut"
    except KeyError:
        pass

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def register(request):
    uid = sessionGetUserInfo(request)["uid"]
    account = sessionGetUserInfo(request)["account"]

    if uid != '':
        return HttpResponseRedirect("/")  # 待修复:当登陆后重复提交注册应该被屏蔽掉

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = User.objects.get(accountname=data['username'])
            except User.DoesNotExist:
                user = 'null'

            if user != 'null':
                msg = u'用户已存在'
                form._errors['username'] = form.error_class([msg])
                return render(request, "OJ/register.html", {'form': form})
            else:
                user = User(accountname=data['username'], password=data[
                            'password'], name=data['name'])
                user.save()
                return HttpResponseRedirect("/login/")
        else:
            return render(request, "OJ/register.html", {'form': form, "uid": uid, "account": account})
    else:
        form = RegisterForm()
        return render(request, "OJ/register.html", {'form': form, "uid": uid, "account": account})
