#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
from django import forms
from OJ.models import User

class LoginForm(forms.Form):
	username = forms.CharField(label = "用户名", max_length=20)
	password = forms.CharField(label = "密码", max_length=20,widget=forms.PasswordInput)

class RegisterForm(forms.Form):
	username = forms.CharField(label = "用户名", max_length=20)
	password = forms.CharField(label = "密码", max_length=20,widget=forms.PasswordInput)
	name = forms.CharField(label = "昵称", max_length=20)

def login(request):
	try:
		uid = request.session['uid']
		account = request.session['accountname']
	except KeyError:
		uid = ''
		account = ''

	if uid!='':
		return HttpResponseRedirect("/")#待修复:当登陆后重复提交登录应该被屏蔽掉

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			try:
				user = User.objects.get(accountname=data['username'])
			except User.DoesNotExist:
				msg = u'用户不存在'
				form._errors['username']=form.error_class([msg])  
				return render(request,"OJ/login.html",{'form':form})
			if user.password == data['password']:
				request.session['accountname']=user.accountname
				request.session['uid']=user.id
				return HttpResponseRedirect("/")
			else:
				msg = u'密码不正确'
				form._errors['password']=form.error_class([msg])
				return render(request,"OJ/login.html",{'form':form})
		else:
			return render(request,"OJ/login.html",{'form':form})

	form = LoginForm()

	return render(request,"OJ/login.html",{'form':form})

def logout(request):
	try:
		del request.session['uid']
		del request.session['accountname']
		print "deleted"
	except KeyError:
		pass
	
	return HttpResponseRedirect(request.META['HTTP_REFERER'])

def register(request):
	try:
		uid = request.session['uid']
		account = request.session['accountname']
	except KeyError:
		uid = ''
		account = ''

	if uid!='':
		return HttpResponseRedirect("/")#待修复:当登陆后重复提交注册应该被屏蔽掉

	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			try:
				user = User.objects.get(accountname=data['username'])
			except User.DoesNotExist:
				user = 'null';

			if user!='null':
				msg = u'用户已存在'
				form._errors['username']=form.error_class([msg])
				return render(request,"OJ/register.html",{'form':form})
			else:
				user = User(accountname=data['username'],password=data['password'],name=data['name'])
				user.save()
				return HttpResponseRedirect("/login/")
		else:
			return render(request,"OJ/register.html",{'form':form})
	else:
		form = RegisterForm()
		return render(request,"OJ/register.html",{'form':form})

		