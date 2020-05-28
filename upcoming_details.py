import requests
import json
import time
import datetime
import urllib
import sqlite3


def get_upcoming(rid,live,upcoming):
    now = datetime.datetime.now()
    now=str(now)
    url = 'https://clist.by/api/v1/json/contest/?&order_by=-start&username=swiggy123&api_key=a0fc6e7ce627ee61b7fced4c976609b97bb65b76&limit=25'
    params = dict({
        'resource__id' : rid
    })
    resp = requests.get(url=url, params=params)
    x = resp.json()
    t = x['objects']
    n=len(t)
    now=str(now)
    for i in range(n):
         if(t[i]['start'][:10:] >now[:10:]):
            upcoming.append(t[i])
         if(t[i]['start'][:10:] == now[:10:]):
              if(t[i]['end'][11::]>=now[11:19] and t[i]['start'][11::]<=now[11:19]):
                   live.append(t[i])
              else:
                   upcoming .append(t[i])
def today_contest(rid,today):
    now = datetime.datetime.now()
    now=str(now)
    url = 'https://clist.by/api/v1/json/contest/?&order_by=-start&username=swiggy123&api_key=a0fc6e7ce627ee61b7fced4c976609b97bb65b76&limit=25'
    params = dict({
        'resource__id' : rid
    })
    resp = requests.get(url=url, params=params)
    x = resp.json()
    t = x['objects']
    n=len(t)
    now=str(now)
    for i in range(n):
         if(t[i]['start'][:10] ==now[:10]):
            today.append(t[i])
    
