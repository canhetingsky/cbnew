#!/usr/bin/python3
# encoding: utf-8

import time
from typing import Text
import requests
import json
import config
from message import Message


def get_timestamp():
    t = time.time()
    return int(round(t * 1000))  # 毫秒级时间戳


def compare_date(time1, time2):
    s_time = time.mktime(time.strptime(time1, '%Y-%m-%d'))
    e_time = time.mktime(time.strptime(time2, '%Y-%m-%d'))
    delta = int(s_time) - int(e_time)
    return delta


def get_cbnew_pre(pre_date: str) -> list:
    url = "https://www.jisilu.cn/data/cbnew/pre_list/?___jsl=LST___t=%s" % get_timestamp()
    response = requests.get(url)
    result = json.loads(response.text)

    cbnew_list = []
    res = result.get('rows')
    for r in res:
        cbnew = r.get('cell')
        # 申购日期查询
        apply_date = cbnew.get('apply_date')
        if apply_date is not None:
            delta = compare_date(apply_date, pre_date)
            if delta == 0:
                cbnew_list.append({
                    'bond_type': 0,  # 今日申购
                    'date': apply_date,
                    'bond_id': cbnew.get('bond_id'),
                    'bond_nm': cbnew.get('bond_nm'),
                    'rating_cd': cbnew.get('rating_cd')})
            elif delta > 0:
                cbnew_list.append({
                    'bond_type': 2,  # 即将申购
                    'date': apply_date,
                    'bond_id': cbnew.get('bond_id'),
                    'bond_nm': cbnew.get('bond_nm'),
                    'rating_cd': cbnew.get('rating_cd')})

        # 上市日期查询
        list_date = cbnew.get('list_date')
        if list_date is not None:
            delta = compare_date(list_date, pre_date)
            if delta == 0:
                cbnew_list.append({
                    'bond_type': 1,  # 今日上市
                    'date': list_date,
                    'bond_id': cbnew.get('bond_id'),
                    'bond_nm': cbnew.get('bond_nm'),
                    'rating_cd': cbnew.get('rating_cd')})
            elif delta > 0:
                cbnew_list.append({
                    'bond_type': 3,  # 即将上市
                    'date': list_date,
                    'bond_id': cbnew.get('bond_id'),
                    'bond_nm': cbnew.get('bond_nm'),
                    'rating_cd': cbnew.get('rating_cd')})
    return cbnew_list


def main():
    today = time.localtime()

    pre_date = '{0}-{1}-{2}'.format(today.tm_year, today.tm_mon, today.tm_mday)
    # print(pre_date)
    cbnew_list = get_cbnew_pre(pre_date)

    print(cbnew_list)
    msg = ['']*4
    for cbnew in cbnew_list:
        bond_type = cbnew.get('bond_type')
        date = cbnew.get('date')
        bond_id = cbnew.get('bond_id')
        bond_nm = cbnew.get('bond_nm')
        rating_cd = cbnew.get('rating_cd')
        if bond_type == 0 or bond_type == 1:
            msg[bond_type] += '\r\n**{0}**({1})  评级：{2}'.format(bond_nm,
                                                                bond_id, rating_cd)
        elif bond_type == 2 or bond_type == 3:
            msg[bond_type] += '\r\n**{0}**({1})：{2}  评级：{3}'.format(bond_nm,
                                                                    bond_id, date, rating_cd)
    for i in range(len(msg)):
        if msg[i] == '':
            msg[i] = '暂无'

    title = '今日可转债操作详情'
    desp = '''
# {4}可转债操作详情

## 今日可申购可转债：

{0}

## 今日上市可转债：

{1}

## 即将申购可转债：

{2}

## 即将上市可转债：

{3}
'''.format(msg[0], msg[1], msg[2], msg[3], pre_date)

    msg = Message(config.sendkey)
    print(desp)
    msg.send(title, desp)


if __name__ == "__main__":
    main()
