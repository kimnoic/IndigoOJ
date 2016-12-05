from django.shortcuts import render
from django.http import HttpResponse


def sessionGetUserInfo(request):
	try:
		uid = request.session['uid']
		account = request.session['accountname']
	except KeyError:
		uid = ''
		account = ''

	return {"uid":uid,"account":account}
