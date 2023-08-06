from requests import session
from re import findall
import json
from datetime import datetime,timedelta
from threading import Thread
from time import sleep

class Xuexitong():

    def __init__(self):
        self.requests = session()

        self.requests.headers.update( {
            "User-Agent":"Mozilla/5.0 (Linux; Android 9; Redmi Note 5 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36",
        } )

        self.index()

    def todayInfo(self,specialId="7973"):
    
        url = "http://rgyy.xmlib.net:8786/mb/activity/actEnterFor/%s"%specialId
        
        res = self.requests.get(url)
        result = "".join( findall(r"dateList.*?\[(.*?)\]",res.text) )
        if not result: result = "".join( findall(r"var reader =.*?({.*?})",res.text) )

        if not result: print("请重新登陆！！！"); return

        result = json.loads(result)
        # print(json.dumps(result,ensure_ascii=False,indent=4))
        return result

    def index(self):
        
        url = "http://rgyy.xmlib.net:8786/mb?libcode=XMLIB"
        res = self.requests.head(url)

    def notify(self,msg,wxid):
        data = {"sender":wxid or "L8d99458","data":msg}
        print(data)
        try:response = self .requests.post("http://47.114.173.71:9002/send_msg",data=data)
        except Exception as e: print(e)

    def book(self,specialId="7973",dateids="58144",msg=""):

        url = "http://rgyy.xmlib.net:8786/mb/activity/entry"
        data = {
            "specialId":specialId,"dateids":dateids,"attachDesc":"","carryNum":"0"
        }
        headers = self.requests.headers.copy()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        res = self.requests.post(url,data=data,headers=headers)

        result = res.json().get("msg")
        print(msg,"正在预约中。。。。。")
        print(msg,result)

        return msg,result

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

    def login(self,name,personId,phone="18159887546",openid=""):
        
        url = "http://rgyy.xmlib.net:8786/mb/reader/registration"
        
        data = {
            "rdid":personId,
            "rdname":name,
            "rdcertify":personId,
            "rdloginid":phone,
            "openid":""
        }
        
        try:
            res = self.requests.post(url,data=data)
            msg = "%s,登陆%s"%(name,res.json().get("msg"))

            person = self.person(msg,openid)
        except Exception as e:
            print(e)
            sleep(2)
            return self.login(name,personId,phone,openid)
        return res.json()

    def check(self,key="自助图书馆"):

        url = "http://rgyy.xmlib.net:8786/mb/activity/myFutureActivity"
        res = self.requests.get(url).text
        # print(key in res)
        return key in res

def getDetail():
    
    main = Xuexitong()

    with open("detail.txt","a") as f: pass 
    with open("detail.txt","r+") as f: default = f.read() or "6299" 
    print(default)

    target = main.getTarget("自助图书馆")
    main.login("郑八妹","352625196702132227")
    specialId = int(target.get("specialId",default))

    for i in range(20):
        try:
            detail = main.todayInfo( specialId )
            sign = detail.get("enterForEndTime")

            if sign and sign > datetime.now().strftime("%Y-%m-%d") and "自助" in detail.get("departName"):
                with open("detail.txt","w") as f: f.write(str(specialId)) 
                break
            else: specialId += 1
        except Exception as e:print(e); specialId += 1

    detail.update( target )

    return detail

def main( name="",personId="350824199711082213",detail={},wxid="",openid="",times=1 ):
    
    if DEBUG: wxid = "L8d99458"

    man = Xuexitong()
    man.login( name ,personId ,openid=openid )

    if delta()>0 : 
        print(name,"正在等待预约")
        sleep( delta() )

    msg,result = man.book( detail.get("specialId"),detail.get("id"),"%s 预约 %s"%(name,detail.get("departName")) )

    if "不足" in result: man.notify("%s\n%s"%(msg,"名额不足,预约失败"),wxid) ; return  
    if "成功" in result: man.notify("%s\n%s"%(msg,"预约成功，加油！！！"),wxid) ; return 
    elif not man.check(): 
        if times > 2: return man.notify("%s\n%s"%(msg,"很遗憾,预约了%d次都没成功，宣告预约失败"%times),wxid) ; return 
        sleep(10)
        return main( name=name,personId=personId,detail=detail,wxid=wxid,openid=openid,times=times+1)
    else:
        man.notify("%s\n%s"%(msg,"预约成功，加油！！！"),wxid) ; return 

    print(result)
    

def delta(string="17:59:35"):

    strTime = datetime.now().strftime("%Y-%m-%d ") + string
    now = datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")-datetime.now()
    #print(now)
    return now.days*24*3600+now.seconds

if __name__ == "__main__":

    DEBUG = False

    print(delta())

    startTime = "16:58:00"

    if delta(startTime)<600:
        
        detail = getDetail()

        persons = [
                ("刘裕","350824199711082213",detail, "L8d99458","oCbcPt2_VUJUejMiYZF5Q7pbSpe0") , 
                ("曹武豪","332527199804283517",detail ,"scanf_z" ), 
                ("吕周灿","350725199905014017",detail ,"wxid_41ixy9r5rdv622","oCbcPtyDGkL4CPnQBLt2Ruoqcs_I"),
                ("张宁","41282719970318353X",detail ,"printf__c")  ,
                ("杨焜","350825199711104538",detail,"wxid_41ixy9r5rdv622","oCbcPt6Coun1Clncb4NKkU6hWuZM")
        ]

        if delta(startTime)>0 : sleep( delta(startTime) )

        for man in persons:
            try: 
                target = Thread(target=main,args=man).start()
            except Exception as e:print(e)

    else:
        print("时间还早",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
