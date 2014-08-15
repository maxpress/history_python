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
APP_KEY = '1107621715'
APP_SECRET = 'fc2759a863af2de9058fad1555b8cb86'
CALLBACK_URL = 'http://apps.weibo.com/kjasdsssh'
client = APIClient(app_key = APP_KEY, app_secret = APP_SECRET, redirect_uri = CALLBACK_URL)
access_token = "2.006g_eBD4ATxMBb77e8ef7a2j2bC9C"
expires_in = "1554269252"
client.set_access_token(access_token,expires_in)

db_conn = sqlite3.connect('weibo-msg2.db')
db_cursor = db_conn.cursor()              #connect to the database

db_cursor.execute('select id from msg2')
res=db_cursor.fetchall()
print 'desc',db_cursor.description

num2=5000
def total_number(mid):
    try:
        comment_info=client.comments.show.get(id = mid) #query weibo
    except:
        traceback.print_exc()
        logger.warning('api query error:5')
        time.sleep(3660)
        num=comment_info=client.comments.show.get(id = mid)
    else:
        num=comment_info['total_number']
        time.sleep(25)
    return num

mids=[]
for line in res:
    for f in line:
        mids.append(f)      #find mid and write it into a list
for i in range(9440,9513):        #consider 150 per account 1000 per ip,we can use 6 scripts and accounts
    print 'START'           #per account get 1600 id(total num is 9513)
    m=mids[i]
    print"ID:",m,"NO:",i+1
    j=total_number(m)
    print"comment num:",j
    total_page=j//50+1
    print"total page:",total_page
    if total_page>40:
        num2=num2+1
        logger.warning(num2)
    k=1
    while (k<41)&(j>0):
        try:
            print"page:",k
            comment_info=client.comments.show.get(id = m,page=k) #query weibo
        except:
            traceback.print_exc()
            logger.info('api query error:5')
            time.sleep(3600)
        else:
            j=j-50
            jsonFile = open('./Data/%d-%d.json'%(m, k),'w')
            jsonFile.write(json.dumps(comment_info,ensure_ascii=False))
            jsonFile.close()
            logger.info('SUCCESS:5'+str(i))
            k=k+1
            time.sleep(25)
print num2
logger.info('OVER:5')




    
              
        
