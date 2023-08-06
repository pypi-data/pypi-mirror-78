try:
    from . import xuexitong
    from .local import Local
except:
    import xuexitong
    from local import Local

from re import findall
from time import strftime
from urllib import parse

import json

Now = lambda : strftime("%Y-%m-%d %R:%S")
# from datetime import datetime,timedelta
# from threading import Thread

class Api(xuexitong.Xuexitong):

    def __init__(self):
        
        self.reserveList = []
        self.local = Local("fjnuTSG.pkl")
        super(Api, self).__init__()

    def getToken(self):

        url = "https://office.chaoxing.com/front/apps/seat/select"
        # url = self.baseurl+"/data/apps/seat/select"
        res = self.requests.get(url)
        # print(res.headers)
        reserve = res.text
        # print(reserve)

        token = "".join( findall("token.*?'(.*?)'",reserve) ) 
        print(token)
        return token

    def reservelist(self,tp=0):

        url = "http://office.chaoxing.com/data/apps/seat/reservelist?cpage=1&pageSize=10&type=%s"%tp
        # url = self.baseurl+"/data/apps/seat/select"
        res = self.requests.get(url)
        self.reserveList = res.json().get("data",{}).get("reserveList",[])
        result = self.reserveList
        msg = []

        for result in self.reserveList:
            resmsg = "%s-%s 座位号: %s"%( result.get("firstLevelName") ,result.get("secondLevelName") ,result.get("seatNum"))
            msg.append(resmsg)
        
        print(msg)

    def reserve(self,roomId,seatNum,day,token,startTime, endTime,**a):
        # 预约
        
        url = self.baseurl+"/data/apps/seat/submit"
        data = {
            "roomId":roomId,"startTime":startTime ,"endTime":endTime,"day":day,"seatNum":seatNum,"token":token
        }
        res = self.requests.get(url,params=data)

        if "msg" in res.json(): return  res.json().get("msg"),{}

        print(res.json(),res.request.url,"\n")

        result = res.json().get("data",{}).get("seatReserve",{})
        resmsg = "%s-%s 座位号: %s 时长: %s小时"%( result.get("firstLevelName") ,result.get("secondLevelName") ,result.get("seatNum"),result.get("duration"))
        params = { "itemId":result.get("id",""), "roomId":result.get("roomId"), "seatNum":result.get("seatNum") , "startTime":result.get("startTime"), "endTime":result.get("endTime"),"signDuration":result.get("signDuration") }
        reserveInfo = {"key":resmsg,"params":json.dumps(params,ensure_ascii=False),"status":True ,"create_time":Now() }

        print(reserveInfo)
        print("正在预约中。。。。。",resmsg)

        return resmsg,reserveInfo

    def leave(self,itemId):
        # 暂离

        url = self.baseurl+'/data/apps/seat/leave'
        data = {
            "id":itemId
        }
        res = self.requests.get(url,params=data)

        result = res.json()
        print("正在暂时离开中。。。。。")
        print(result)


    def signback(self,itemId):
        # 退座

        url = self.baseurl+'/data/apps/seat/signback'
        data = {
            "id":itemId
        }
        res = self.requests.get(url,params=data)

        result = res.json()
        print("正在退座中。。。。。")
        print(result)


    def cancel(self,itemId):
        # 取消预约

        url = self.baseurl+'/data/apps/seat/cancel'
        data = {
            "id":itemId
        }
        res = self.requests.get(url,params=data)

        # print(res.request.headers)
        # print(res.headers)
        result = res.json()
        print("正在取消预约中。。。。。")
        print(result)

    def notify(self,msg,wxid):
        data = {"sender":wxid or "L8d99458","data":msg}
        print(data)
        try:response = self .requests.post("http://47.114.173.71:9002/send_msg",data=data)
        except Exception as e: print(e)

    def person(self,msg="",wxid=""):

        url = "http://rgyy.xmlib.net:8786/mb/reader/person"

        res = self.requests.get(url)

        result = ''.join(findall("/mb/reader/setting\">(.*?)<",res.text))
        print(msg,"我是谁",result)

        if wxid: 
            url = "http://rgyy.xmlib.net:8786/mb/reader/getOpenid"
            res = self.requests.post(url,data={"code":"","openid":wxid})
            print(res.text)

        return result

    def index(self):

        # url = "http://office.chaoxing.com/front/apps/seat/index?fidEnc=54459dd2640de2ed"
        url = "http://office.chaoxing.com/front/third/apps/seat/rule?deptIdEnc="
        res = self.requests.get(url)

        try:
            name = parse.unquote(self.requests.cookies.get("oa_name"))
        except: name ="没有名字"

        print("登陆成功，当前登陆的是",name)

        # print(dir(self.requests.cookies))
        return name

    # def login(self,phone="",password="",**a):

    def storeCookie(self,phone):
        cookies = {}
        for i in self.requests.cookies:
            cookies[i.name] = [i.value,i.domain]

        self.local.add( {phone:cookies} )

    def login(self,phone="18159086771",password="liuyu000*",**a):

        self.requests.cookies.clear()
        cookies = self.local.read().get(phone,{})
        for cookie in cookies:
            self.requests.cookies.set(cookie,cookies[cookie][0],domain=cookies[cookie][1])

        if not cookies:
            self.login_by_pd(phone,password)
        else:
            if self.index()=="没有名字":
                self.login_by_pd(phone,password)

        self.reservelist()

    def login_by_pd(self,phone="18159086771",password="liuyu000*"):
        
        url = "https://passport2-api.chaoxing.com/v11/loginregister?cx_xxt_passport=json"
        
        data = {
            "uname":phone,
            "code":password,
            "loginType":"1",
            "roleSelect":"true"
        }
        
        try:
            
            res = self.requests.post(url,data=data)
            self.index()
            
            # print(res.request.headers)

            # person = self.person(msg,openid)
        except Exception as e:
            print(e)
            # sleep(2)
            # return self.login(name,personId,phone,openid)

        print(self.requests.cookies.get_dict())
        self.storeCookie(phone)

        return res.json()

    def check(self,key="自助图书馆"):

        url = "http://rgyy.xmlib.net:8786/mb/activity/myFutureActivity"
        res = self.requests.get(url).text
        # print(key in res)
        return key in res

if __name__ == '__main__':

    Man = Api()
    Man.login()
    Man.login("18159887546","liuyu000*")
    # Man.getToken()
