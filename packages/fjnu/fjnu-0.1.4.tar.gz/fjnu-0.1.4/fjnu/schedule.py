try:
    from . import xuexitong
except:
    import xuexitong
# from re import findall
# import json
# from datetime import datetime,timedelta
# from threading import Thread
from time import strftime,strptime,mktime

timeStamp = lambda day,time:int(mktime( strptime(day +" "+ time, "%Y-%m-%d %H:%M") )*1000)
       
class Schedule(xuexitong.Xuexitong):

    def __init__(self):
        
        super(Schedule, self).__init__()

    def getSchedule(self):

        schedule = [
            {"roomId":"3925","seats":["137","161"]},
        ]

        return schedule

    def isReserved(self,roomId,day,startTime,endTime,seats={"roomId":"3925","seats":["001"]},**a):
        
        # 匹配未被预约的位置
        """
            同一个楼层的指定位置检测预约情况，返回平铺式的 字典数据的列表 房间号：座位号
        """

        url = self.baseurl + '/data/apps/seat/getusedseatnums'
        data = {"roomId": roomId, "startTime":startTime ,"endTime":endTime, "day": day}

        res = self.requests.get(url,params=data)

        #  res.text = {"data":{"seatNums":["009","005","033","021","001"]},"success":true}

        reservdSeats = res.json().get("data").get("seatNums",[]) 

        result = []
        print("已经被预约的座位号",reservdSeats)

        for seat in seats.get("seats"):
            if seat not in reservdSeats and seat not result:
                data["seatNum"] = seat
                
                result.append( data )

        print("符合需求的座位号",result,"\n")

        return result

if __name__ == '__main__':
    Man = Schedule()
    Man.login()

    schedules = Man.getSchedule()

    base = {"day":'2020-09-03',"startTime":'8:00',"endTime":'11:30' }
    for i in schedules:
        base["seats"] = i
        base["roomId"] = i.get("roomId")
        Man.isReserved(**base)
