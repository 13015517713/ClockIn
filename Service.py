# 登录页   ->login   确认页外页(infourl) ->send   确认页内页(confirmurl)  -> 
import logging
import PageInfo
import requests
import until.tools as tol

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
Info = PageInfo.Info()


# 访问的时候有时候很卡  需要设置定时器如果失败重新login几次
def login():
    # 1.解析出来按钮那个url
    mainUrl = Info.getUrl()
    if mainUrl == "":
        logger.error("main page url is null when logging.")
        return False
    logReq = requests.get(mainUrl)
    logReq.encoding = "utf-8"
    if not logReq.ok:
        logger.error("connect to main page url error when logging.")
        return False
    InfoUrl = ""
    for r in logReq.text.split('\n'):
        if r.find("form") !=-1 and r.find("action") !=-1 and r.find("myform52") != -1:
            str = r
            str = str.strip("").split("action")
            for rr in str:
                if rr != "" and rr.strip()[0] ==   "=" and len(rr.split('"')) >= 2:
                    InfoUrl = rr.split('"')[1]
                    break
            break
    if InfoUrl == "":
        logger.error("unable to find infopage url when logging.")
        return False
    Info.setInfoPageUrl(InfoUrl)
    logger.debug("Successfully parsed the infopageurl.")
    
    # 2.向解析出来的url发登录请求
    data = "uid=%s&upw=%s"%(Info.getUid(),Info.getPwd())
    req = requests.post(InfoUrl,data)
    req.encoding = "utf-8"
    if not req.ok:
        logger.error("connect to url error when logging.")
        return False
    # 2.1密码错误（通过字符串匹配）   
    if req.text.find("密码错误") != -1:
        logger.error("username or password errors.")
        return False
    if req.text.find("验证码") != -1:
        logger.error("login times too more today,just choose other computers to login in.")
        return False
    # 2.2登录成功，把得到的内容和url存储下来
    Info.setInfoPage(req.text)
    logger.info("Successfully login in.")
    tol.write2file(req.text,"out.txt")
    return True

def send():
    stat = sendConfirm()
    if not stat:
        logger.error("send confirm page url errors.")
        return False
    stat = sendOk()
    if stat == 0:
        logger.info("Successful finishing this clock in.")
        return True
    elif stat == 1:
        logger.info("You have already clocked.")
        return True
    elif stat == 2:
        logger.error("Failed to finish this clock in.")
        return False
    else:
        logger.info("Send okpage ReturnCode is undefined.")
        return False
    logger.info("Success to finish clocking in.")
    return True

def sendConfirm():
    # 1.解析确认页面的包装页1
    infoPage = Info.getInfoPage()
    tol.write2file(infoPage,"out.txt")
    confirmUrl = ""
    for r in infoPage.split('\n'):
        if r.find("window.location") != -1 and r.find("http") != -1:
            str = r.strip().split('"')
            for rr in str:
                if rr.find('http') != -1:
                    confirmUrl = rr
                    break
            break
    if confirmUrl == "":
        logger.error("unable to parsing clockpage url when confirming info.")
        return False

    # 2.解析确认页面的包装页2
    req = requests.get(confirmUrl)
    req.encoding = "utf-8"
    if not req.ok:
        logger.error("connect error to confirm package page2.")
        return False
    # tol.write2file(req.text,"out.txt")
    confirmUrl = ""
    for r in req.text.split('\n'):
        if r.find("iframe") != -1 and r.find("zzj_top_6s") != -1:
            str = r.strip().split("src")
            for rr in str:
                if rr != "" and rr.strip()[0] ==   "=" and len(rr.split('"')) >= 2:
                    confirmUrl = rr.split('"')[1]
                    break
            break
    if confirmUrl == "":
        logger.error("unable to parsing clockpage url when confirming info.")
        return false
    Info.setComfirmPageUrl(confirmUrl)

    # 3.得到确认页面
    req = requests.get(confirmUrl)
    req.encoding = "utf-8"
    if not req.ok:
        logger.error("connect error to confirm page.")
        return False
    Info.setConfirmPage(req.text)
    # tol.write2file(req.text,"out.txt")
    logger.info("Success to find inner confirmPage url.")
    okPageUrl = ""
    for r in req.text.split('\n'):
        if r.find("form") !=-1 and r.find("action") !=-1 and r.find("myform52") != -1:
            str = r
            str = str.strip("").split("action")
            for rr in str:
                if rr != "" and rr.strip()[0] ==   "=" and len(rr.split('"')) >= 2:
                    okPageUrl = rr.split('"')[1]
                    break
            break
    if okPageUrl == "":
        logger.error("Failed to parse okPage from inner confirmPage.")
        return False
    Info.setOkPageUrl(okPageUrl)

    # 4.组织信息发到打卡页
    post = PageInfo.PostStruce1() # 先默认构造吧
    # tol.write2file(req.text,"out.txt")
    tmpLazy = getValueFromInput
    post.setAll(tmpLazy(req.text,"day6"),tmpLazy(req.text,"did"),tmpLazy(req.text,"door"),tmpLazy(req.text,"men6"),tmpLazy(req.text,"ptopid"),tmpLazy(req.text,"sid"))
    data = post.serialize()
    req = requests.post(okPageUrl,data)
    req.encoding = "utf-8"
    if not req.ok:
        logger.error("Failed connect to okPage url.")
        return False
    Info.setOkPage(req.text)
    logger.info("Success send data to okPage and go to the end page.")
    # tol.write2file(req.text,"out.txt")
    return True

# return status    0：打卡成功    1：已打卡,不用重复打卡   2：打卡失败
def sendOk():  
    # 打卡页面
    # 1.解析确认页面url
    okPage = Info.getOkPage()
    okPageUrl = ""
    tol.write2file(okPage,"out.txt")
    for r in okPage.split('\n'):
        if r.find("form") != -1 and r.find("action") !=-1 and r.find("myform52") != -1:
            str = r
            str = str.strip("").split("action")
            for rr in str:
                if rr != "" and rr.strip()[0] ==   "=" and len(rr.split('"')) >= 2:
                    okPageUrl = rr.split('"')[1]
                    if okPageUrl == '':
                        logger.info("You have already clocked in.")
                        return 1   # 打过卡了 action里面为空
                    break
            break
    if okPageUrl == "":
        logger.error("Failed to parse okPage url.")
        return 2
    

    # 2.打卡
    post = PageInfo.PostStruce2()
    tmpLazy = getValueFromInput
    post.setAll(tmpLazy(okPage,"did"), tmpLazy(okPage,"door"), tmpLazy(okPage,"day6"), tmpLazy(okPage,"men6"),tmpLazy(okPage,"sheng6"),tmpLazy(okPage,"shi6"),tmpLazy(okPage,"fun3"),tmpLazy(okPage,"ptopid"),tmpLazy(okPage,"sid"))
    data = post.serialize()
    # logger.debug("send to okpage : %s"%(data))
    req = requests.post(okPageUrl,data.encode("utf-8"))
    req.encoding = "utf-8"
    if not req.ok:
        logger.error("Failed to connect okPage url:%s"%okPageUrl)
        return 2

    # 3.解析出来最后打卡的结果  可以宣布打卡成功了
    logger.debug(req.text)
    logger.info("Success clock in.")
    return 0
    
# 从text中解析出来name对应input的value，存在radio那种就不行了，不过那些一般都是默认值
def getValueFromInput(text,name):
    
    for r in text.split('\n'):
        if r.find("input") != -1 and r.find(name) != -1 : # 找到每日填报的一行
            str = r.strip().split("input")
            for rr in str:
                if rr.find(name) != -1:
                    for rrr in rr.strip().split('>'):
                        if rrr.find('value') != -1 and rrr.find(name) != -1:
                            strr = ""
                            for rrrr in rrr.split('value'):
                                if rrrr != "" and rrrr.strip()[0] ==   "=" and len(rrrr.split('"')) >= 2:
                                    strr = rrrr.split('"')[1]
                                    return strr
    return ""


# if __name__ == "__main__":
#     sendOk()
