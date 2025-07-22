# -*- coding: utf-8 -*-
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 原有常量保留，不做改名
REGEX_EXP_RE = re.compile(r'([^ =]*) *= *[\'"](.*?)[\'"]')
ALL_SUPPORT_KEY = ["Severity", "Timestamp", "Process", "Thread", "Level", "Tag", "Message"]
DEPRECATED_DATE_KEY = "data"

# 更严谨的 Timestamp 正则：HH:MM:SS.mmm
_TIMESTAMP_REGEX = r'(?:[01]?\d|2[0-3]):[0-5]?\d:[0-5]\d\.\d{3}'
timestamp_regex = re.compile(_TIMESTAMP_REGEX)

# 一次性匹配整行：severity / timestamp / process / thread / level / tag / message
_parse_pattern = re.compile(
    rf'^(?P<severity>.*?)\s*'
    rf'(?P<timestamp>{_TIMESTAMP_REGEX})\s+'
    rf'(?P<process>\S+)\s+'
    rf'(?P<thread>\S+)\s+'
    rf'(?P<level>\S+)\s+'
    rf'(?P<tag>[^:]*):\s*(?P<message>.*)$'
)

class DataProcess:
    """
    提供两大静态方法：
      - loading_logfile(file)：读入整个日志文件并返回行列表
      - parse_linedata(line)：解析单行日志，返回
        [severity, timestamp, process, thread, level, tag, message] 或 []
    """

    @staticmethod
    def loading_logfile(file):
        """
        读取日志文件所有行
        :param file: 文件路径字符串，或可索引结构（如 QFileDialog 返回的 tuple），以 file[0] 为路径
        :return: list of str，每行为文件的一行；出错时返回空列表
        """
        path = file[0] if isinstance(file, (list, tuple)) and file else file
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as infile:
                lines = infile.readlines()
            logger.info(f"Loaded {len(lines)} lines from {path}")
            return lines
        except Exception:
            logger.exception(f"Failed to load logfile: {path}")
            return []

    @staticmethod
    def parse_linedata(line):
        """
        将一行日志拆分为 [Severity, Timestamp, Process, Thread, Level, Tag, Message]
        不匹配时返回 []
        """
        text = line.rstrip('\n')
        m = _parse_pattern.match(text)
        if not m:
            return []

        g = m.groupdict()
        # strip() 防止前后多余空白
        severity  = g.get('severity', '').strip()
        timestamp = g.get('timestamp', '')
        process   = g.get('process', '')
        thread    = g.get('thread', '')
        level     = g.get('level', '')
        tag       = g.get('tag', '').strip()
        message   = g.get('message', '')

        return [severity, timestamp, process, thread, level, tag, message]
