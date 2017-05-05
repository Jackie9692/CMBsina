#!/usr/bin/python
# -*- coding: utf-8 -*-


# ***文本情绪判定*****#
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import json

from QcloudApi.qcloudapi import QcloudApi

from os import sys, path

sys.path.append(path.abspath(path.join(path.dirname(__file__), '..')))  # 引入绝对路径

from dao.baseDao import StatusDao


#文智 模块访问配置 授权配置
module = 'wenzhi'
action = 'TextSentiment'
config = {
    'Region': 'sh',
    'secretId': 'AKIDUs6A3kManoeoqgGxUtGSSGtKYaSDBtnV',
    'secretKey': 'iFcpqfKyRirwLfmnsnY7Zs1yjKl283o6',
    'method': 'post'
}

if __name__ == "__main__":
    service = QcloudApi(module, config)
    statusDao = StatusDao()

    # 过滤条件
    filterCondition = {"emotion", None}
    statusItems = statusDao.queryCondition(filterCondition)

    for each in statusItems:
        text = each.text  # 微博文本

        if text is None:
            continue

        params = {"content": text}
        try:
            result = json.loads(service.call(action, params))
            if result:
                if result["codeDesc"] == "Success":
                    each.emotion = str(result["positive"])
                    statusDao.updateByItem(each)

        except Exception, e:
            print 'exception:', e

