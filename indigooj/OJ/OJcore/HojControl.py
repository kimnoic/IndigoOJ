# -*- coding: utf-8 -*-
import time
import base64
import urllib
import urllib2
import cookielib
import re


class Submit(object):

    def __init__(self):
        self.WaitingStatus = ['Queuing', 'Compiling',
                              'Running & Judging', 'Running']  # 几个还在测评的状态
        self.SubmitAdd = 'http://acm.hit.edu.cn/hoj/problem/submit'
        self.LoginAdd = 'http://acm.hit.edu.cn/hoj/system/login'
        self.StatusAdd = 'http://acm.hit.edu.cn/hoj/problem/status'
        cj = cookielib.LWPCookieJar()  # 声明一个CookieJar对象实例来保存cookie
        # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
        ck = urllib2.HTTPCookieProcessor(cj)
        open = urllib2.build_opener(ck, urllib2.HTTPHandler)
        urllib2.install_opener(open)
        self.header = {'User-Agent': 'IE10'}
        self.username = 'kimnoic'
        self.password = '78456123'

    def Html(self, text):
        HtmlObject = open('res.html', 'wb')
        HtmlObject.write(text)
        HtmlObject.close()

    def Login(self):
        postData = {'user': self.username,
                    'password': self.password,
                    'submit': 'Login'}  # submit 默认submit
        postData = urllib.urlencode(postData)  # urlencode 编码转换
        request = urllib2.Request(self.LoginAdd, postData, self.header)
        try:
            response = urllib2.urlopen(request, timeout=5)
        except:
            return False
        if response.getcode() != 200:  # 200 请求成功
            print 'login web error!'
            return False
        ans = response.read()
        if ans.find("Logout") == -1:  # 登录成功会显示Logout,若爬虫没有爬到则登录错误
            print 'login fail'
            return False
        print ' login successful'
        return True

    def QueryStatus(self):
        postData = {'author': self.username}
        postData = urllib.urlencode(postData)
        request = urllib2.Request(
            self.StatusAdd + '?' + postData, headers=self.header)
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
        ans = {'C++': 'C++',
               'C89': 'C89',
               'Java': 'Java', }
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
        if response.getcode() != 200:
            print 'Submmit Error'
            return ['Submit Failed', '', '']
        # print 'Subbmit Done!'
        time.sleep(3)
        ans = self.QueryStatus()
        print ans[0]
        while ans[0] in self.WaitingStatus:
            time.sleep(1)
            ans = self.QueryStatus()
        # print ans
        return ans

if __name__ == '__main__':
    fin = open('a.txt', 'r')
    code = fin.read()
    Submit().Submit('1001', 'C++', code)
