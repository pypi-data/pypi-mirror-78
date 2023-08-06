from requests import session
from base64 import b64encode
# from re import findall
# import json
# from datetime import datetime,timedelta
# from threading import Thread
from time import sleep

class Xuexitong():

    def __init__(self):
        self.requests = session()
        self.baseurl = "http://office.chaoxing.com"

        self.requests.headers.update( {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36'
        } )

        # self.index()

    def index(self,url):

        url = "http://office.chaoxing.com/front/third/apps/seat/index?fidEnc=54459dd2640de2ed"
        res = self.requests.get(url)
        print(res.headers)
        return 

    def notify(self,msg,wxid):
        data = {"sender":wxid or "L8d99458","data":msg}
        print(data)
        try:response = self .requests.post("http://47.114.173.71:9002/send_msg",data=data)
        except Exception as e: print(e)

    def login(self,phone="18159086771",password="liuyu000*"):
        
        url = "https://passport2.chaoxing.com/fanyalogin"
        
        data = {
            "uname":phone,
            "password":b64encode(password.encode()),
            "refer":'http://office.chaoxing.com/front/third/apps/seat/index?fidEnc=54459dd2640de2ed',
            "t":"true"
        }

        # print(data)
        # url = "https://passport2-api.chaoxing.com/v11/loginregister?cx_xxt_passport=json"
        
        # data = {
        #     "uname":phone,
        #     "code":password,
        #     "loginType":"1",
        #     "roleSelect":"true"
        # }
        
        try:
            res = self.requests.post(url,data=data)
            msg = "登陆%s"%(res.json())
            # print(msg,"\n")
            # print(res.headers,"\n")
            # print(self.requests.cookies)

            res = self.requests.head(res.json().get("url","http://office.chaoxing.com/front/third/apps/seat/index?fidEnc=54459dd2640de2ed"))
            # self.index()
            # print(res.headers,"\n")
            # print(res.request.headers,"\n")
            # print(res.text)

            # person = self.person(msg,openid)
        except Exception as e:
            print(e)
            # sleep(2)
            # return self.login(name,personId,phone,openid)
        # return res.json()

if __name__ == '__main__':
    Man = Xuexitong()
    Man.login()


