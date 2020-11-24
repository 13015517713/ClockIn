# 在这里存储全局信息，并提供访问接口
import Logger
import json
import until.tools as tol

# 全局url信息
class Info:
    # 初始化下url,账号密码
    url = ""
    uid = ""
    pwd = ""
    # 信息确认页
    infoPage = ""
    infoPageUrl = ""
    confirmPage = ""
    confirmPageUrl = ""
    # 打开页
    okPage = ""
    okPageUrl = ""
    
    def __init__(self):
        # 从config中读取
        with open("./config.json","r",encoding = 'utf-8') as configfile:
            config = json.load(configfile)
            self.url = config["url"]
            self.uid = config["uid"]
            self.pwd = config["pwd"]
    def getUrl(self):
        return self.url
    def getUid(self):
        return self.uid
    def getPwd(self):
        return self.pwd

    def setInfoPageUrl(self,url):
        self.infoPageUrl = url
        return 
    def setInfoPage(self,text):
        self.infoPage = text
        return
    def getInfoPage(self):
        return self.infoPage
    def getInfoPageUrl(self):
        return self.infoPageUrl

    def setConfirmPage(self,text):
        self.confirmPage = text
    def setComfirmPageUrl(self,url):
        self.confirmPageUrl = url
    def getConfirmPage(self):
        return self.confirmPage
    def getComfirmPageUrl(self):
        return self.confirmPageUrl

    def setOkPage(self,text):
        self.okPage = text
    def setOkPageUrl(self,url):
        self.okPageUrl = url
    def getOkPage(self):
        return self.okPage
    def getOkPageUrl(self):
        return self.okPageUrl
               


# Post发包的信息  自身提供序列化函数
class PostStruce1:     
    # 不确认需不需要 前面五个在一行   后面一个在一行
    did = "1"
    door = ""
    men6 = "a"
    ptopid = ""    #  这两个需要解析
    sid = ""
    # 确认需要的
    day6 = "b" # 选中每日填报
    def __init__(self):
        pass
    def setAll(self,day6,did,door,men6,ptopid,sid):
        self.did = did
        self.door = door
        self.men6 = men6
        self.ptopid = ptopid
        self.sid = sid
        # 确认需要的
        self.day6 = day6
    def serialize(self):  # 序列化自己
        str = "day6=%s&did=%s&door=%s&men6=%s&ptopid=%s&sid=%s"%(self.day6,self.did,self.door,self.men6,self.ptopid,self.sid)
        return str

class PostStruce2:
    # 这些都是默认的  11个  不知道每天是不是有变化
    did = "2"
    door = ""
    day6 = "b"
    men6 = "a"
    sheng6 = "41"  # 可能这就是省份的
    shi6 = "4101"  # 可能这是市的
    fun3 = ""
    # 这两个不知道是不是
    ptopid = ""
    sid = ""
    
    # 这些每天应该没有变化，如果有变化，也要对自己的身体负责
    myvs_1 = "否"  # 发烧
    myvs_2 = "否"  # 咳嗽
    myvs_3 = "否"  # 是否乏力
    myvs_4 = "否"  # 鼻塞、腹泻
    # Btn3   获取城市  这个是不是没什么用
    myvs_13a = "41"  # 河南省对应的value 
    myvs_13b = "4101"  # 郑州市对应的value
    myvs_13c = "河南省.郑州市.中原区xxxxxx"  # 要填写的家庭住址地区
    myvs_14 = "否"  #  是否当天返郑
    myvs_14b = ""  # 自动测温记录：否

    def __init__(self):
        self.myvs_13c = tol.getConfig("home")

    def setAll(self,did,door,day6,men6,sheng6,shi6,fun3,ptopid,sid):
        self.did = did
        self.door = door
        self.day6 = day6
        self.men6 = men6
        self.sheng6 = sheng6
        self.shi6 = shi6
        self.fun3 = fun3
        self.ptopid = ptopid
        self.sid = sid
        # 确认需要的
    def serialize(self):  # 序列化自己
        str1 = "did=%s&door=%s&day6=%s&men6=%s&sheng6=%s&shi6=%s&fun3=%s&ptopid=%s&sid=%s&"%(self.did,self.door,self.day6,self.men6,self.sheng6,self.shi6,self.fun3,self.ptopid,self.sid)
        str2 = "myvs_1=%s&myvs_2=%s&myvs_3=%s&myvs_4=%s&myvs_13a=%s&myvs_13b=%s&myvs_13c=%s&myvs_14=%s&myvs_14b=%s"%(self.myvs_1,self.myvs_2,self.myvs_3,self.myvs_4,self.myvs_13a,self.myvs_13b,self.myvs_13c,self.myvs_14,self.myvs_14b)
        str = str1+str2
        return str