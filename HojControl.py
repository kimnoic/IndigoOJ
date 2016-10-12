#coding=utf-8
import time
import base64
import urllib
import urllib2
import cookielib
import re

class Submit(object):
    def __init__(self):
        self.WaitingStatus = ['Queuing', 'Compiling', 'Running & Judging', 'Running'] #�������ڲ�����״̬
        self.SubmitAdd = 'http://acm.hit.edu.cn/hoj/problem/submit'
        self.LoginAdd = 'http://acm.hit.edu.cn/hoj/system/login'
        self.StatusAdd = 'http://acm.hit.edu.cn/hoj/problem/status'
        cj = cookielib.LWPCookieJar() #����һ��CookieJar����ʵ��������cookie
        ck = urllib2.HTTPCookieProcessor(cj)  #����urllib2���HTTPCookieProcessor����������cookie������
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
                    'submit': 'Login'} # submit Ĭ��submit
        postData = urllib.urlencode(postData) #urlencode ����ת��
        request = urllib2.Request(self.LoginAdd, postData, self.header)
        try:
            response = urllib2.urlopen(request, timeout= 5)
        except:
            return False
        if response.getcode() != 200 :  #200 ����ɹ�
            print 'login web error!'
            return False 
        ans = response.read()
        if ans.find("Logout") == -1: #��¼�ɹ�����ʾLogout,������û���������¼����
            print 'login fail'
            return False 
        print ' login successful'
        return True 
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
    fin = open('a.txt', 'r')
    code = fin.read()
    Submit().Submit('1001', 'C++', code)
