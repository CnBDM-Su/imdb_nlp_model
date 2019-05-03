#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys
import csv
import json
import redis


def connectRedis():
    conn = redis.StrictRedis(host='localhost', port=6379, password='kNlTR2nPrv')
    return conn

def main():
    redis_conn = connectRedis()
    csvfile = open('csvfile.csv', 'a')
    writer = csv.writer(csvfile)
    writer.writerow(['id','content','rate'])
    while True:
        try:
            source, data = redis_conn.blpop(['movieContent:items'],\
                    timeout=1)
        except:
            break
        item = json.loads(data)
        data = [item['CommentId'],\
                item['Content'],\
                item['Rate']]
        writer.writerow(data)
    csvfile.close()

main()