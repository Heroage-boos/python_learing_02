import logging

#设置日志的输出格式
LOG_FORMAT = "%(asctime)s - %(levelname)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S %p"
logging.basicConfig(filename='my.log', 
                    level=logging.DEBUG, 
                    format=LOG_FORMAT, 
                    datefmt=DATE_FORMAT)

logging.basicConfig(level=logging.INFO)
logging.debug("这是调试级别的日志")
logging.info("这是信息级别的日志")
logging.warning("这是警告级别的日志")
logging.error("这是错误级别的日志")
logging.critical("这是严重级别的日志")