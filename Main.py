import Logger
import Service
import logging
import until.smtp as smtp
import until.tools as tol

# 打卡函数

logger = logging.getLogger("logger")

def sendMail():
    print(tol.file2str("log.txt")) 
    for i in range(3):
        try:
            # print(tol.file2str("log.txt")) 
            smtp.smtp_tran( tol.file2str("log.txt") )
        except:
            logging.debug("The %d of mail send errors."%(i))
        else:
            logging.info("Success send logs to QQ mail.")
            return True
    return False

def run():
    res = Service.login()
    if not res:
        logger.error("Failed to login in.")
        return False
    res = Service.send()
    if not res:
        logger.error("Failed to finish this clock.")
        res = sendMail() # 即使打卡失败也要发邮件
        return False
    logger.info("Success to finish clocking in.")
    # 把打卡日志发到我邮箱就行了  最多尝试发送三次
    res = sendMail()
    if not res:
        logger.error("Failed to send the mail.")
        return False
    return True

if __name__ == "__main__":
    Logger.createLogger("logger")
    run()
    
    