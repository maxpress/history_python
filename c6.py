# -*-coding: utf8 -*-
from weibo import APIClient   # 导入weibo的APICient类
import json
import time
import logging
import sqlite3
import time
import sys
import traceback
reload(sys)
sys.setdefaultencoding( "utf-8" ) 

logger=logging.getLogger('get the comments')
formatter=logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s\
                              %(message)s', '%a, %d %b %Y %H:%M:%S',)
file_handler=logging.FileHandler('report1.log')
file_handler.setFormatter(formatter)
stream_handler=logging.StreamHandler(sys.stderr)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

'''Configure AppKey'''
APP_KEY = '1545850093'
APP_SECRET = 'd46a2c4d1a02672c253b45297bb2a6f1'
CALLBACK_URL = 'http://apps.weibo.com/fgfdgdfg'
client = APIClient(app_key = APP_KEY, app_secret = APP_SECRET, redirect_uri = CALLBACK_URL)
access_token = "2.006g_eBDBOOcgB6e032633210Igyl9"
expires_in = "1554269430"
client.set_access_token(access_token,expires_in)

db_conn = sqlite3.connect('weibo-msg2.db')
db_cursor = db_conn.cursor()              #connect to the database

db_cursor.execute('select id from msg2')
res=db_cursor.fetchall()
print 'desc',db_cursor.description

def total_number(mid):
    i=0
    try:
        comment_info=client.comments.show.get(id = mid) #query weibo
    except:
        traceback.print_exc()
    else:
        num=comment_info['total_number']
        if num>2000:
            i=i+1
            logger.warnning(i)
    return num

mids=[]
for line in res:
    for f in line:
        mids.append(f)      #find mid and write it into a list
for i in range(1600):        #consider 150 per account 1000 per ip,we can use 6 scripts and accounts
    print 'START'           #per account get 1600 id(total num is 9513)
    logger.info('START')
    m=mids[i]
    print"ID:",m,"NO:",i+1
    j=total_number(m)
    print"comment num:",j
    total_page=j//50+1
    print"total page:",total_page
    k=1
    while k<41:
        try:
            print"page:",k
            comment_info=client.comments.show.get(id = m,page=k) #query weibo
        except:
            traceback.print_exc()
            time.sleep(3600)
        else:
            j=j-50
            jsonFile = open('./Data/%d-%d.json'%(m, k),'w')
            jsonFile.write(json.dumps(comment_info,ensure_ascii=False))
            jsonFile.close()
            k=k+1
            time.sleep(26)





    
              
        
