import logging

def createLogger(name):
    with open("./log.txt","w") as w:  # 为了清空内容
        pass
    logging.basicConfig(level=logging.DEBUG,
                     format='%(levelname)s %(asctime)s [%(filename)s:%(lineno)d] %(message)s',
                     datefmt='%Y.%m.%d. %H:%M:%S',
                     filename="./log.txt")
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)       # 小于Level会被忽略 