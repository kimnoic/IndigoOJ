# -*- coding: utf-8 -*-

#from models import problems, problemslist
import requests
from lxml import etree
import sys

	
class HojSpider(object):

    def __init__(self): 
        pass

    def Allpages(self):
        for page_number in range(1, 2): #×ÜÒ³Êý
            self.Problemlist(page_number)

    def Problemlist(self, page_number):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        url = "http://acm.hit.edu.cn/hoj/problem/volume?page=%d"%page_number
        html = requests.get(url)
        pro_lst_page = etree.HTML(html.text)
        for i in range(1, 100):
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
        detail = problem_page.xpath('//*[@id="problem-detail"]/p[1]/text()')
        _input = ""
        _output = ""
        sample_input = problem_page.xpath('//*[@id="problem-detail"]/pre[1]/text()')
        sample_output = problem_page.xpath('//*[@id="problem-detail"]/pre[2]/text()')

        print number
        mem_limit = _mem_limit[0].xpath('string(.)') if _mem_limit else ""
        time_limit = _time_limit[0].xpath('string(.)') if _time_limit else ""
        problem ={'number': number,
                  'ratio' : ratio,
                  'title' : title,
                  'time_limit' : time_limit,
				  'mem_limit' : mem_limit,
                  'detail': detail,
				  'sample_input' : sample_input,
				  'sample_output' : sample_output}
        print problem 
	def QueryStatus(self):
        postData = {'author' : self.username} 
        postData = urllib.urlencode(postData)
        request = urllib2.Request(self.StatusAdd + '?' + postData, headers=self.header)
        try:
            response = urllib2.urlopen(request, timeout=10)
        except:
            print 'Sorry Query Error'
            return ['Judge Error', '', '', '']
        if response.getcode() != 200:
            print 'Sorry Query Error'
            return ['Judge Error', '', '', '']
        Page = response.read()
        self.Html(Page)
        res = Page.split('<tbody>')[2].split('</tbody>')[0]
        rec = res.split('</tr>')[0]
        rec = re.findall(r'<td(.*?)</td>', rec)
        Result = rec[2].split('>')[1]
        if 'http' in Result:
            Result = 'Compilation Error'
        Time = rec[3].split('>')[1]
        Memory = rec[4].split('>')[1]
        Codelength = rec[6].split('>')[1]
        return [Result, Time, Memory, Codelength] 
    
    def map(self):
        ans = {'C++' : 'C++',
               'C89' : 'C89',
               'Java' : 'Java',}
        return ans 
    
    def Submit(self, Proid, Language, Code):
        if not self.Login():
            return ['Judge Error', '', '']
        Proid = Proid.encode('utf-8')
        Language = self.map()[Language]
        PostData = {'Proid': Proid,
                    'Language': Language,
                    'Source': Code} 
        PostData = urllib.urlencode(PostData)
        request = urllib2.Request(self.SubmitAdd, PostData, self.header)
        try:
            response = urllib2.urlopen(request, timeout=10)
        except:
            return ['Submit Failed', '', '']
        if response.getcode() != 200 :
            print 'Submmit Error'
            return ['Submit Failed', '', '']
        print 'Subbmit Done!'
        time.sleep(3) 
        ans = self.QueryStatus()
        print ans[0]
        while ans[0] in self.WaitingStatus: 
            time.sleep(1)
            ans = self.QueryStatus()
        print ans
        return ans
		
if __name__ == '__main__':
	HojSpider().Allpages()