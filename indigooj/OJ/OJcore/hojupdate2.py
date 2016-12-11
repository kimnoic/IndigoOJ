import requests
from lxml import etree
import sys
import re
from OJ.models import *


def trim(a):
    if len(a) == 0:
        return ""
    else:
        return a[0]


class Spider(object):

    def __init__(self):
        self.oj = OnlineOJ.objects.get(name="HOJ")

    def solve(self):
        for page_number in range(1, 23):
            reload(sys), sys.setdefaultencoding("utf-8")
            url = "http://acm.hit.edu.cn/hoj/problem/volume?page=%d" % page_number
            html = requests.get(url)
            Path = etree.HTML(html.text)
            for i in range(2, 102):
                ID = Path.xpath(
                    '//*[@id="content"]/table//tr[%d]/td[2]/text()' % i)
                _title = Path.xpath(
                    '//*[@id="content"]/table//tr[%d]/td[3]/a/ins/text()' % i)
                _ratio = Path.xpath(
                    '//*[@id="content"]/table//tr[%d]/td[5]' % i)
                title = _title[0] if _title else ""
                ratio = _ratio[0].xpath('string(.)') if _ratio else ""
                m = re.findall(r'[0-9]+', ratio)
                accepted_on_oringin = m[0]
                submitted_on_oringin = m[1]
                SID = ID[0] if ID else ""
                url = 'http://acm.hit.edu.cn/hoj/problem/view?id=%s' % SID
                html = requests.get(url)
                ppage = etree.HTML(
                    html.text, parser=etree.HTMLParser(encoding='utf-8'))
                number = SID
                title = ppage.xpath('//*[@id="content"]/h1/text()')
                _time_limit = ppage.xpath(
                    '//*[@id="request"]/table//tr[2]/td[2]')
                _mem_limit = ppage.xpath(
                    '//*[@id="request"]/table//tr[2]/td[4]')
                _source = ppage.xpath(
                    '//*[@id="request"]/table//tr[1]/td[2]/a')
                _detail = ppage.xpath('//*[@id="problem-detail"]/p/text()')
                if (_detail):
                    detail = _detail
                else:
                    detail = ppage.xpath('//*[@id="problem-detail"]/text()')
                sample_input = ppage.xpath(
                    '//*[@id="problem-detail"]/pre[1]/text()')
                sample_output = ppage.xpath(
                    '//*[@id="problem-detail"]/pre[2]/text()')
                print number
                mem_limit = re.findall(
                    r'[0-9]+', _mem_limit[0].xpath('string(.)'))[0] + " M" if _mem_limit else ""
                time_limit = re.findall(
                    r'[0-9]+', _time_limit[0].xpath('string(.)'))[0] + " sec" if _time_limit else ""

                source = _source[0].xpath('string(.)')
                problem = {'number': number, 'ratio': ratio, 'title': title, 'time_limit': time_limit, 'mem_limit': mem_limit,
                           'detail': detail, 'sample_input': sample_input, 'sample_output': sample_output, 'source': source}

                p = Problem(oj=self.oj, id=eval('1' + SID), number=number, submitted_on_oringin=submitted_on_oringin,
                            accepted_on_oringin=accepted_on_oringin, title=trim(title), time_limit=time_limit, mem_limit=mem_limit,
                            detail=trim(detail), sampleinput=trim(sample_input), sampleoutput=trim(sample_output), source=source)
                p.save()

                print number + "saved"

if __name__ == '__main__':
    Spider().solve()
