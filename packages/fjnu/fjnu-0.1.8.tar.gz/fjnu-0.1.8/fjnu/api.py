try:
    from . import xuexitong
    from .local import Local
except:
    import xuexitong
    from local import Local

from re import findall
from time import strftime
from urllib import parse
from datetime import datetime
from threading import Thread

import json

Now = lambda : strftime("%Y-%m-%d %R:%S")
# from datetime import datetime,timedelta
# from threading import Thread

class Api(xuexitong.Xuexitong):

    def __init__(self,debug=False):
        
        self.reserveList = []
        self.debug = debug
        self.local = Local("fjnuTSG.pkl")
        super(Api, self).__init__()

    def getToken(self):

        url = "https://office.chaoxing.com/front/apps/seat/select"
        # url = self.baseurl+"/data/apps/seat/select"
        res = self.requests.get(url)
        # if self.debug: print(res.headers)
        reserve = res.text
        # if self.debug: print(reserve)

        token = "".join( findall("token.*?'(.*?)'",reserve) ) 
        if self.debug: print(token)
        return token

    def reservelist(self,tp=0):

        url = "http://office.chaoxing.com/data/apps/seat/reservelist?cpage=1&pageSize=10&type=%s"%tp
        # url = self.baseurl+"/data/apps/seat/select"
        res = self.requests.get(url)
        self.reserveList = res.json().get("data",{}).get("reserveList",[])
        result = self.reserveList

        msg,datamsg = [],[]

        for result in self.reserveList:
            # if self.debug: print(result)

            params = {"name":parse.unquote(self.requests.cookies.get("oa_name","")),
                      "startTime":datetime.fromtimestamp(int(result.get('startTime')/1000)), 
                      "firstLevelName":result.get("firstLevelName") ,
                      "secondLevelName":result.get("secondLevelName") ,
                      "seatNum":result.get("seatNum"),
                      "itemId":result.get("id")
                    }

            resmsg = "%s %s %s-%s 座位号: %s"%(params.get("name"),params.get("startTime"),params.get("firstLevelName"),params.get("secondLevelName"),params.get("seatNum"))
            # resmsg = "%s %s %s-%s 座位号: %s"%(parse.unquote(self.requests.cookies.get("oa_name","")),datetime.fromtimestamp(int(result.get('startTime')/1000)), result.get("firstLevelName") ,result.get("secondLevelName") ,result.get("seatNum"))

            msg.append(resmsg)
            datamsg.append(params)

        # if self.debug: print(self.phone)

        data = self.local.read().get(self.phone)
        data["params"] = datamsg
        # if self.debug: print(data)
        self.local.add({self.phone:data})

        # if self.debug: print(msg)

    def reserve(self,roomId,seatNum,day,token,startTime, endTime,**a):
        # 预约
        
        url = self.baseurl+"/data/apps/seat/submit"
        data = {
            "roomId":roomId,"startTime":startTime ,"endTime":endTime,"day":day,"seatNum":seatNum,"token":token
        }
        res = self.requests.get(url,params=data)

        if "msg" in res.json(): print("请求数据",data,"返回信息",res.json().get("msg")); return  res.json().get("msg"),{}

        # if self.debug: print(res.json(),res.request.url,"\n")

        result = res.json().get("data",{}).get("seatReserve",{})
        resmsg = "%s-%s 座位号: %s 时长: %s小时"%( result.get("firstLevelName") ,result.get("secondLevelName") ,result.get("seatNum"),result.get("duration"))
        params = { "itemId":result.get("id",""), "roomId":result.get("roomId"), "seatNum":result.get("seatNum") , "startTime":result.get("startTime"), "endTime":result.get("endTime"),"signDuration":result.get("signDuration") }
        reserveInfo = {"key":resmsg,"params":json.dumps(params,ensure_ascii=False),"status":True ,"create_time":Now() }

        # if self.debug: print(reserveInfo)
        if self.debug: print("正在预约中。。。。。",resmsg)
        Thread(target=self.reservelist).start()

        # data = self.local.read().get(self.phone+"_msg")
        # if not data.get("msg"): data["msg"] = [resmsg]
        # else: data["msg"].append(resmsg)

        # self.local.add(data)

        return resmsg,reserveInfo

    def leave(self,itemId):
        # 暂离

        url = self.baseurl+'/data/apps/seat/leave'
        data = {
            "id":itemId
        }
        res = self.requests.get(url,params=data)

        result = res.json()
        if self.debug: print("正在暂时离开中。。。。。",result)

    def signback(self,itemId):
        # 退座

        url = self.baseurl+'/data/apps/seat/signback'
        data = {
            "id":itemId
        }
        res = self.requests.get(url,params=data)

        result = res.json()
        if self.debug: print("正在退座中。。。。。",result)
        Thread(target=self.reservelist).start()

    def sign(self,itemId):
        # 签到

        url = self.baseurl+'/data/apps/seat/sign'
        data = {
            "id":itemId
        }
        res = self.requests.get(url,params=data)

        result = res.json()
        if self.debug: print("正在签到中。。。。。",result)


    def cancel(self,itemId):
        # 取消预约

        url = self.baseurl+'/data/apps/seat/cancel'
        data = {
            "id":itemId
        }
        res = self.requests.get(url,params=data)

        # if self.debug: print(res.request.headers)
        # if self.debug: print(res.headers)
        result = res.json()
        if self.debug: print("正在取消预约中。。。。。",result)
        Thread(target=self.reservelist).start()

    def notify(self,msg,wxid):
        data = {"sender":wxid or "L8d99458","data":msg}
        if self.debug: print(data)
        try:response = self .requests.post("http://47.114.173.71:9002/send_msg",data=data)
        except Exception as e: 
            if self.debug: print(e)

    def person(self,msg="",wxid=""):

        url = "http://rgyy.xmlib.net:8786/mb/reader/person"

        res = self.requests.get(url)

        result = ''.join(findall("/mb/reader/setting\">(.*?)<",res.text))
        if self.debug: print(msg,"我是谁",result)

        if wxid: 
            url = "http://rgyy.xmlib.net:8786/mb/reader/getOpenid"
            res = self.requests.post(url,data={"code":"","openid":wxid})
            if self.debug: print(res.text)

        return result

    def index(self):

        # url = "http://office.chaoxing.com/front/apps/seat/index?fidEnc=54459dd2640de2ed"
        url = "http://office.chaoxing.com/front/third/apps/seat/rule?deptIdEnc="
        res = self.requests.get(url)

        try:
            name = parse.unquote(self.requests.cookies.get("oa_name"))
        except: name ="没有名字"

        if self.debug: print("登陆成功，当前登陆的是",name)

        # if self.debug: print(dir(self.requests.cookies))
        return name

    # def login(self,phone="",password="",**a):

    def storeCookie(self,phone):
        cookies = {}
        for i in self.requests.cookies:
            cookies[i.name] = [i.value,i.domain]

        self.local.add( {phone:cookies} )

    def login(self,phone="18159086771",password="liuyu000*",**a):

        self.requests.cookies.clear()
        self.phone = phone

        # if self.debug: print(self.phone)
        cookies = self.local.read().get(phone,{})
        for cookie in cookies:
            if cookie=="params": continue
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
            
            # if self.debug: print(res.request.headers)

            # person = self.person(msg,openid)
        except Exception as e:
            if self.debug: print(e)
            # sleep(2)
            # return self.login(name,personId,phone,openid)

        # if self.debug: print(self.requests.cookies.get_dict())
        self.storeCookie(phone)

        return res.json()

    def check(self,key="自助图书馆"):

        url = "http://rgyy.xmlib.net:8786/mb/activity/myFutureActivity"
        res = self.requests.get(url).text
        # if self.debug: print(key in res)
        return key in res

if __name__ == '__main__':

    # Man = Api()
    # Man.login()
    # Man.login("18159887546","liuyu000*")
    # print( "\n\n",Man.local.read() )
    pass

    # Man.getToken()
