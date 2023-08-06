import pickle,os,sys

BasePath = os.path.abspath(os.path.join(os.path.abspath(__file__), "../."))
TopPath = os.path.abspath(os.path.join(os.path.abspath(__file__), "../.."))

DataPath = os.path.join(BasePath,"log")
Secret_key = "liuyuaqswde0002*"

if not os.path.isdir(DataPath):
    os.mkdir(DataPath)
    print("新建文件夹",DataPath)

def get_path(path):
    return os.path.join(TopPath,path)

class Local(object):
    """docstring for Local"""
    def __init__(self, path,debug=False):
        super(Local, self).__init__()
        self.path = os.path.join(BasePath,path)
        if debug: print(self.path)

    def write(self,data={}):
        with open(self.path,"wb") as f:
            pickle.dump(data,f)


    def read(self,data={}):
        if os.path.isfile(self.path):
            with open(self.path,"rb") as f:
                try:data = pickle.load(f)
                except Exception as e:print(e),self.write()
        else: self.write()
        return data

    def add(self,data={}):
        initData = self.read()
        initData.update(data)
        self.write(initData)

# from time import time,strftime,localtime
# lastweek = localtime(time()-3600*24*7)
# print( (strftime("%Y-%m-%d",lastweek)) )