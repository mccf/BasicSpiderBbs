import re
from urllib import request
from http.cookiejar import CookieJar
from urllib import parse
import time
# import requests

#抛错： UnicodeEncodeError: 'ascii' codec can't encode characters in position 96-97: ordinal not in range(128)
"""默认编码ascii问题尚未解决"""
#抛错位置line138,爬取114页世界大战时 //opener.open(login_url_response)//此处
#py3.x
# import importlib,sys
# importlib.reload(sys)



"""创建opener保存cookie"""
# 创建cookie对象

cookiejar = CookieJar()
# 创建一个握手
handler = request.HTTPCookieProcessor(cookiejar)
# 创建一个opener
opener = request.build_opener(handler)
# print(opener)

"""访问所需必要参数"""
# 目标页
des_url = 'url1'
# for login
login_url = "url2"
# 主页
des_ur2 = "url3"
# headers
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    # 若headers = { "Accept-Encoding": "gzip, deflate"}
    # 注意headers中如有 ：Accept-Encoding 将导致获取到的html无法解码

}


class LoginVisitSave():
    """创建自动登录访问类"""

    def __init__(self):
        pass

    def VisitLogin(s):
        # 1访问login页
        login_url_response = request.Request(login_url, headers=headers)
        # login_url_response = requests.get(login_url, headers=headers)
        # print(type(login_url_response))
        login_url_response_content = opener.open(login_url_response)
        s.login_url_decode_content = login_url_response_content.read().decode("gbk")
        time.sleep(0.2)

        # 1.1 # 通过html获取 formhash隐藏域值
        regex = "cookies&formhash=(.+?)\'"
        regex_result = re.search(regex, s.login_url_decode_content)
        s.formhash = regex_result.group(1)
        print(" When VisitLogin formhash:", s.formhash)
        # 1.1 # 通过html获取 loginhash

        regex = "loginhash=(\S{5})"
        regex_result = re.search(regex, s.login_url_decode_content)
        loginhash = regex_result.group(1)
        s.loginning_url = "urlx" % loginhash
        # print(" When VisitLogin loginhash:", loginhash)
        # print(s.loginning_url)

        s.Loginning()

    # 2开始login
    def Loginning(s):
        # usr = input("请输入登录名：")
        # pw = input("请输入登录密码：")
        usr = "xxx"
        pw = "xxx"
        data = {"formhash": s.formhash,
                "referer": "http://www.url/",
                "loginfield": "username",
                "username": usr,
                "password": pw,
                "questionid": 0,
                "answer": ""
                }
        data = parse.urlencode(data).encode("gbk")
        login_url = s.loginning_url
        logined_response = request.Request(login_url, data=data, headers=headers)
        # print(logined_response.has_proxy())
        loging_response_obj = opener.open(logined_response)
        s.loging_response_decode_content = loging_response_obj.read().decode("gbk")
        time.sleep(0.01)
        print("登录成功 请开始你的操作")

        s.VisitDes()

    # 3登录后访问url

    def VisitDes(s):
        desurl_response_obj = request.Request(des_url, headers=headers)
        desurl_response_bytes = opener.open(desurl_response_obj)
        s.desurl_response_decode_content = desurl_response_bytes.read().decode("gbk")
        regex = "formhash.{18}"

        # regex_result = re.search(regex, s.desurl_response_decode_content)
        # formhash = regex_result.group()
        # print("When VisitDes:", formhash)

        s.SaveHtml()

    # 4 保存页面
    def SaveHtml(s):
        with open("test_login.html", "w", encoding="gbk") as fd:
            fd.write(s.loging_response_decode_content)

        with open("test_des.html", "w", encoding="gbk") as fd:
            fd.write(s.desurl_response_decode_content)


class Spider(object):

    def __init__(self):
        self.model_url = "urlx&page=%d"

    def UseRequests(self, url):
        # time.sleep(0.02)
        login_url_response = request.Request(url, headers=headers)
        # print(login_url_response)
        # time.sleep(3)
        #114页世界大战
        try:
            login_url_response_content = opener.open(login_url_response)
        except Exception as e:
            # raise
            print(e)
            # continue
        else:
            rescontent1 = login_url_response_content.read()
            return rescontent1
        # finally:
        #     pass
        
        
        

    def singlerun(self, MaxNum=20):
        MaxNum=MaxNum
        MaxNum=int(input("请输入到多少页："))
        for Num in range(MaxNum-10,MaxNum):
            self.RequestUrl(Num + 1)
            pass


    def RequestUrl(self, Num):
        
        self.PageUrl = (self.model_url) % (Num)
        login_url_response_content=self.UseRequests(self.PageUrl)
        self.PageContent = login_url_response_content.decode("gbk")
        self.resu1 = self.AnalyzeUrl()

    def AnalyzeUrl(self):
        str1 = str(self.PageContent)
        # print(str1)
        reg1 = r"精华影视.*?百度网盘资源"
        reg11 = r"<strong>(\d+)</strong>"
        self.reg11 = re.search(reg11, str1).group(1)
        self.resu0 = re.findall(reg1, str1)
        # print(self.resu0)
        for r1 in self.resu0:
            # print(r1)
            # time.sleep(self.sleep_num * 0.01)
            self.DoResUrl(r1)

    def DoResUrl(self, str2):
        # print(str2)
        reg2 = r'(http.*)(amp;)(.*)(amp;)(.*D\d)'
        everyindex = re.search(reg2, str2)
        self.lasturl = everyindex.group(1) + everyindex.group(3) + everyindex.group(5)
        # time.sleep(0.02)
        content1 = self.UseRequests(self.lasturl)  # 为何urlopen打不开 #因为ip被封了
        # 一直断不足3200是因为此处访问的无效地址过多
        self.SaveContent(content1)

    def SaveContent(self, content1):
        if content1 != None   :         
            # print(last_html)
            self.last_html2 = content1.decode("gbk")
            # print(self.last_html2)
            regex = "<title>(((.*)\[百度网盘资源](.*))?])"
            html_name_obj = re.search(regex, self.last_html2)
            if html_name_obj != None:
                self.html_name = str(self.reg11) + html_name_obj.group(3)
                # print(self.html_name)
            else:
                print("本机ip直接访问又开始无效了")
                path1 = "C:/python3src/PycharmProjects/test spider/log/" + "log1.txt"
                with open(path1, "a") as fd:
                    fd.write(self.last_html2)
                    return
            if "/"or "*" in self.html_name:
                regx1 = r"/+"
                self.html_name = re.sub(regx1, "_", self.html_name)
                regx1 = r"\*+"
                self.html_name = re.sub(regx1, "_", self.html_name)
                regx1 = r"\:+" #为何：可以通过命名选项？？？？
                self.html_name = re.sub(regx1, "_", self.html_name)
                

            print(self.html_name)
            self.StoreToHtml()  # 关闭存储html打开网页数则变多

    def StoreToHtml(self):
    	#保存到单页html
        store_path = "C:/python3src/PycharmProjects/test spider/singlehtmls" + "/" + str(self.html_name) + ".html"
        write_html = open(store_path, "w")
        written_content=self.last_html2
        write_html.write(written_content)
        write_html.close()
        #保存所有内容到一个html文件
        path2 = "C:/python3src/PycharmProjects/test spider/comtentfeed/" + "comtentfeed.html"
        with open(path2, "a") as fd:
            fd.write(self.last_html2)






def main():
    lv = LoginVisitSave()
    lv.VisitLogin()
    sp1=Spider()
    sp1.singlerun()

if __name__ == '__main__':
    main()

"""HTML请求流程"""

# #首次访问 登录页面 reuqest
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
# Accept-Encoding: gzip, deflate
# Accept-Language: zh-CN,zh;q=0.9
# Connection: keep-alive
# Host: url
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36

# #首次访问 登录页面 respose
# Cache-Control: no-store, private, post-check=0, pre-check=0, max-age=0
# Connection: keep-alive
# Content-Encoding: gzip
# Content-Type: text/html; charset=gbk
# Date: Fri, 07 Sep 2018 02:49:40 GMT
# Expires: -1
# Pragma: no-cache
# Server: nginx
# Set-Cookie: T7ml_f39a_lastvisit=1536284980; expires=Sun, 07-Oct-2018 02:49:40 GMT; path=/; domain=.url
# Set-Cookie: T7ml_f39a_invite_auth=deleted; expires=Thu, 07-Sep-2017 02:49:39 GMT; path=/; domain=.url
# Set-Cookie: T7ml_f39a_saltkey=r44Oq7A7; expires=Sun, 07-Oct-2018 02:49:40 GMT; path=/; domain=.url; httponly
# Set-Cookie: T7ml_f39a_lastact=1536288580%09member.php%09logging; expires=Sat, 08-Sep-2018 02:49:40 GMT; path=/; domain=.url


# Transfer-Encoding: chunked
# Vary: Accept-Encoding
# Vary: Accept-Encoding
# X-Powered-By: PHP/5.2.17

# #首次访问登录页面 respose hidden:
# <input type="hidden" name="formhash" value="a4b73664">

# """首次开始登录request_header"""
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
# Accept-Encoding: gzip, deflate
# Accept-Language: zh-CN,zh;q=0.9
# Cache-Control: max-age=0
# Connection: keep-alive
# Content-Length: 154
# Content-Type: application/x-www-form-urlencoded
# Cookie: T7ml_f39a_saltkey=r44Oq7A7; T7ml_f39a_lastvisit=1536284980; T7ml_f39a_lastact=1536288580%09plugin.php%09; Hm_lvt_bab7d9af18c858d9b8fa3ae5935aa762=1536288586; Hm_lpvt_bab7d9af18c858d9b8fa3ae5935aa762=1536288586
# Host: www.url
# Origin: http://www.url
# Referer: url
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36

# #首次开始登录data值
# formhash: a4b73664
# referer: url
# loginfield: username
# username: 123
# password: 5fa72358f0b4fb4f2
# questionid: 0
# answer:
