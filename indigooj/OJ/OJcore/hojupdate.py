from OJ.models import *
import requests
from lxml import etree
import sys
import re

class hojupdate(object):
    def __init__(self):
        self.oj = OnlineOJ.objects.get(name="HOJ")

    def update(self):
        for i in range(1, 23):
            self.dive_page(i)

    def dive_page(self,page):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        url = "http://acm.hit.edu.cn/hoj/problem/volume?page=%d"%page
        html = requests.get(url)
        pro_lst_page = etree.HTML(html.text)
        for i in range(1, 102):
            ID = pro_lst_page.xpath('//*[@id="content"]/table//tr[%d]/td[2]/text()'%i)
            href = pro_lst_page.xpath('//*[@id="content"]/table//tr[%d]/td[3]/a/@href'%i)
            _title = pro_lst_page.xpath('//*[@id="content"]/table//tr[%d]/td[3]/a/ins/text()'%i)
            _ratio = pro_lst_page.xpath('//*[@id="content"]/table//tr[%d]/td[5]'%i)
            title = _title[0] if _title else ""
            ratio = _ratio[0].xpath('string(.)') if _ratio else ""
            SID=ID[0] if ID else ""
            self.dive_problem(SID,ratio)

    def dive_problem(self, SID, ratio):
        if SID == '':
            return
        url = 'http://acm.hit.edu.cn/hoj/problem/view?id=%s'%SID
        html = requests.get(url)
        problem_page = etree.HTML(html.text, parser=etree.HTMLParser(encoding='utf-8'))
        number = SID
        #submitted_on_oringin = problem_page.xpath('//*[@id="ratio_detail"]/p/')
        title = problem_page.xpath('//*[@id="content"]/h1/text()')
        _time_limit = problem_page.xpath('//*[@id="request"]/table//tr[2]/td[2]')
        _mem_limit = problem_page.xpath('//*[@id="request"]/table//tr[2]/td[4]')
        _detail = problem_page.xpath('//*[@id="problem-detail"]/p/text()')
        detail = _detail[0] if _detail else "" #.xpath('string(.)') if _detail else ""
        _input = ""
        _output = ""
        _sample_input = problem_page.xpath('//*[@id="problem-detail"]/pre[1]')
        _sample_output = problem_page.xpath('//*[@id="problem-detail"]/pre[2]')
        sample_input = _sample_input[0].xpath('string(.)') if _sample_input else ""
        sample_output =  _sample_output[0].xpath('string(.)') if _sample_output else ""
        m = re.findall(r'[0-9]+',ratio)
        accepted_on_oringin = m[0]
        submitted_on_oringin = m[1]

        #print number
        mem_limit = re.findall(r'[0-9]+',_mem_limit[0].xpath('string(.)'))[0]+" M" if _mem_limit else ""
        time_limit = re.findall(r'[0-9]+',_time_limit[0].xpath('string(.)'))[0]+" sec" if _time_limit else ""

        p = Problem(oj = self.oj,id = eval('1'+SID),number = number,submitted_on_oringin = submitted_on_oringin,
            accepted_on_oringin = accepted_on_oringin, title = title, time_limit = time_limit, mem_limit = mem_limit,
            detail = detail,sampleinput = sample_input,sampleoutput = sample_output)
        p.save()

        print number+"saved"

        problem ={'number': number,
                  'accepted_on_oringin' : accepted_on_oringin,
                  'submitted_on_oringin' : submitted_on_oringin,
                  'title' : title,
                  'time_limit' : time_limit,
                  'mem_limit' : mem_limit,
                  'detail': detail,
                  'sample_input' : sample_input,
                  'sample_output' : sample_output}
        #print problem 

if __name__ == '__main__':
    hojupdate().update()