# -*- coding: utf-8 -*-

#from models import problems, problemslist
import requests
from lxml import etree
import sys

	
class HojSpider(object):

    def __init__(self):
        pass

    def Allpages(self):
        for page_number in range(1, 2): #总页数
            self.Problemlist(page_number)

    def Problemlist(self, page_number):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        url = "http://acm.hit.edu.cn/hoj/problem/volume?page=%d"%page_number
        html = requests.get(url)
        pro_lst_page = etree.HTML(html.text)
        for i in range(1, 10):
            ID = pro_lst_page.xpath('//*[@id="content"]/table//tr[%d]/td[2]/text()'%i)
            href = pro_lst_page.xpath('//*[@id="content"]/table//tr[%d]/td[3]/a/@href'%i)
            _title = pro_lst_page.xpath('//*[@id="content"]/table//tr[%d]/td[3]/a/ins/text()'%i)
            _ratio = pro_lst_page.xpath('//*[@id="content"]/table//tr[%d]/td[5]'%i)
            title = _title[0] if _title else ""
            ratio = _ratio[0].xpath('string(.)') if _ratio else ""
            #print ratio
            SID=ID[0] if ID else ""
            self.Problem(SID, ID ,ratio)

    def Problem(self, SID, proid, ratio):
        url = 'http://acm.hit.edu.cn/hoj/problem/view?id=%s'%SID
        html = requests.get(url)
        problem_page = etree.HTML(html.text, parser=etree.HTMLParser(encoding='utf-8'))
        number = SID
		#submitted_on_oringin = problem_page.xpath('//*[@id="ratio_detail"]/p/')
        title = problem_page.xpath('//*[@id="content"]/h1/text()')
        _time_limit = problem_page.xpath('//*[@id="request"]/table//tr[2]/td[2]')
        _mem_limit = problem_page.xpath('//*[@id="request"]/table//tr[2]/td[4]')
        _detail = problem_page.xpath('//*[@id="problem-detail"]/p/text()')
        _input = ""
        _output = ""
        _sample_input = problem_page.xpath('//*[@id="problem-detail"]/pre[1]')
        _sample_output = problem_page.xpath('//*[@id="problem-detail"]/pre[2]')

        print number
        mem_limit = _mem_limit[0].xpath('string(.)') if _mem_limit else ""
        time_limit = _time_limit[0].xpath('string(.)') if _time_limit else ""
        detail = _detail[0] if _detail else "" #.xpath('string(.)') if _detail else ""
        sample_input = _sample_input[0].xpath('string(.)') if _sample_input else ""
        sample_output =  _sample_output[0].xpath('string(.)') if _sample_output else ""
        problem ={'number': number,
                  'ratio' : ratio,
                  'title' : title,
                  'time_limit' : time_limit,
				  'mem_limit' : mem_limit,
                  'detail': detail,
				  'sample_input' : sample_input,
				  'sample_output' : sample_output}
        print problem 
		
if __name__ == '__main__':
	HojSpider().Allpages()