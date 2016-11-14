#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from OJ.models import *
from OJ.OJcore import HojControl
from django import forms

def trim(s):
	if s=='':
		return ''
	else:
		return s #s[2:][:-2]

def trim2(s):
	if s=='':
		return ''
	else:
		return s[2:][:-2]

class SubmitForm(forms.Form):
	number = forms.IntegerField(widget = forms.HiddenInput)
	id = forms.IntegerField(widget = forms.HiddenInput)
	lan = forms.ChoiceField(label= "选择语言",choices = (
			('C++','C++'),
			('C89','C89'),
			('Java','Java'),
		))
	code = forms.CharField(widget = forms.Textarea,max_length = 2000)


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
	l = a[50*eval(page)-50:50*eval(page)]

	for i in l:
		print i.submitted
		if(i.submitted != 0):
			ratio = str(i.accepted*100.0/i.submitted)[:5]
			print ratio
		else:
			ratio = '0';

		if(i.submitted_on_oringin != 0):
			ratio_on_oringin = str(i.accepted_on_oringin*100.0/i.submitted_on_oringin)[:5]
			print ratio_on_oringin
		else:
			ratio_on_oringin = '0';

		dic = {'oj':i.oj.name,'number':i.number,'submitted':i.submitted,'accepted':i.accepted,
				'submitted_on_oringin':i.submitted_on_oringin,'accepted_on_oringin':i.accepted_on_oringin,
				'ratio_on_oringin':ratio_on_oringin,'ratio':ratio,'id':i.id, 'title':trim2(i.title)}
		problem_list.append(dic)


	return render(request,"OJ/problemset.html",{'page':page,'problem_list':problem_list})

def problem(request,id):
	try:
		refer = request.META['HTTP_REFERER']
	except KeyError:
		refer = "/Problem/"

	try:
		i = Problem.objects.get(pk=id)
	except Problem.DoesNotExist:
		return HttpResponseRedirect(refer)

	if(i.submitted != 0):
		ratio = str(i.accepted*100.0/i.submitted)[:5]
		#print ratio
	else:
		ratio = '0';

	if(i.submitted_on_oringin != 0):
		ratio_on_oringin = str(i.accepted_on_oringin*100.0/i.submitted_on_oringin)[:5]
		#print ratio_on_oringin
	else:
		ratio_on_oringin = '0';

	dic = {'oj':i.oj.name,'number':i.number,'submitted':i.submitted,'accepted':i.accepted,
				'submitted_on_oringin':i.submitted_on_oringin,'accepted_on_oringin':i.accepted_on_oringin,
				'ratio_on_oringin':ratio_on_oringin,'ratio':ratio,'id':i.id, 'title':trim2(i.title),
				'time_limit':i.time_limit,'mem_limit':i.mem_limit,'detail':trim(i.detail),'sample':trim(i.sample),
				'sampleinput':trim(i.sampleinput),'sampleoutput':trim(i.sampleoutput),'test':'IJIJI\n\rdfdfd'}


	if request.method == "POST":
		form = SubmitForm(request.POST)
		try:
			uid = request.session['uid']
			account = request.session['accountname']
		except KeyError:
			uid = ''
			account = ''
		
		if form.is_valid():
			if uid=='':
				msg = u'请先登陆'
				form._errors['code']=form.error_class([msg])
				return render(request,"OJ/problem.html",{'problem':dic,'form':form})
			data = form.cleaned_data
			result = HojControl.Submit().Submit(str(data['number']),data['lan'],data['code'])
			i.submitted += 1
			if result[0] == 'Accepted':
				i.accepted += 1
			i.save()
			user = User.objects.get(pk=uid)
			status = Status(problem = i,status = result[0],
				time = int(eval(result[1][:-2])*1000),mem = eval(result[2][:-2]),
				user = user,codelength = eval(result[3][:-2]),lan=data['lan'])
			status.save()
			return HttpResponse("girigiri")
		else:
			return render(request,"OJ/problem.html",{'problem':dic,'form':form})
	else:
		form = SubmitForm({'number':i.number,'id':i.id,'lan':'C++','code':'在这里输入'})

	return render(request,"OJ/problem.html",{'problem':dic,'form':form})





