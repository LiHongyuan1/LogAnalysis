# -*- coding: utf-8 -*-
# Android Logging Tool
# This tool help tester analyse Android Logging
# Version : beta
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REGEX_EXP_RE = re.compile(r"([^ =]*) *= *[\"|'](.*)[\"|']")
ALL_SUPPORT_KEY = ["Severity", "Timestamp", "Process", "Thread", "Level", "Tag", "Message"]
DEPRECATED_DATE_KEY = "data"
timestamp_regex = re.compile(r'(0?[0-9]|1[0-9]|2[0-3]):(0?[0-9]|[1-5][0-9]):([0-9]{2})\.([0-9]{3})')


class DataProcess:
    key_order = list()

    regex = None

    @staticmethod
    def loading_logfile(file):
        with open(file[0], "r", encoding="utf-8", errors="ignore") as infile:
            for line in infile:
                logger.debug("Line debug :" + line)
                return line

    # 对读入的每一行数据进行规则匹配
    @staticmethod
    def parse_linedata(line):
        return_data = []
        line = line.strip("\n")
        timetmp = re.search(timestamp_regex, line)
        if timetmp is None:
            return return_data
        else:
            timestamp = timetmp.group()
        severity = line.split(timestamp)[0]
        return_data.append(severity)
        return_data.append(timestamp)
        data = re.sub(' +', ' ', line.split(timestamp)[1].split(":", 1)[0].strip(" "))
        process = data.split(" ")[0]
        thread = data.split(" ")[1]
        level = data.split(" ")[2]
        return_data.append(process)
        return_data.append(thread)
        return_data.append(level)
        if int(data.count(" ")) > 3:
            tag = data.split(" ", 3).pop(-1)
            return_data.append(tag)
        elif 3 == int(data.count(" ")):
            tag = data.split(" ")[3]
            return_data.append(tag)
        elif 2 == int(data.count(" ")):
            tag = " "
            return_data.append(tag)
        else:
            pass
        message = line.split(timestamp)[1].split(":", 1)[1]
        return_data.append(message)
        return return_data
