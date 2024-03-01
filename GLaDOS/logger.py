import logging
from pytz import timezone
from datetime import datetime

# 设置时区为亚洲/上海
tz = timezone('Asia/Shanghai')

# 自定义时区转换函数
def convert_timestamp(sec, what):
    return datetime.now(tz).timetuple()

logging.Formatter.converter = convert_timestamp

# 创建 logger 对象
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # 设置日志级别为 INFO

formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")

# 控制台输出 handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)  # 设置日志级别为 INFO
stream_handler.setFormatter(formatter)

# 移除之前的 handler
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# 添加新的 handler
logger.addHandler(stream_handler)
