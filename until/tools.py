import json
def write2file(text,filename):
    with open(filename,"w") as w:
        w.write(text)

def file2str(filename):
    # 直接这样发邮件显示不太正常
    # with open(filename,"r") as r:
    #     return r.read()
    # 封装成Html再去发
    str = ""
    
    with open(filename,"r") as r:
        while True:
            line = r.readline()
            if not line:
                break
            str += '<p>'+line+'</p>'
    return str

def getConfig(name):
    with open("./config.json","r",encoding = 'utf-8') as configfile:
        config = json.load(configfile)
        try:
            return config[name]
        except:
            return ""