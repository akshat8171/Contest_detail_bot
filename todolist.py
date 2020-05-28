import requests
import json
import time
import urllib
import sqlite3
from datetime import datetime
import pytz
from dbhelper import dbhelper
from upcoming_details import get_upcoming,today_contest
db=dbhelper("todolist.sqlite")
au=dbhelper("all_usser.sqlite")
feedback=dbhelper("feedback.sqlite")
upcoming=[]
live=[]
TOKEN = "<YOUR-BOT-TOKEN>"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def send_contest_details(upcoming,chat):
    if(len(upcoming)==0):
        send_message("There is no scheduled contest in upcoming dates ",chat)
        return
    send_txt=[]
    upcoming=upcoming[:-6:-1]
    for i in upcoming:
        t=i["start"].split('T')
        e=i["end"].split('T')
        t,e=" ".join(t)," ".join(e)
        date_str,date_str1 = t,e
        d,d1 = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S'),datetime.strptime(date_str1, '%Y-%m-%d %H:%M:%S')
        d,d1 = pytz.UTC.localize(d),pytz.UTC.localize(d1)
        ist = pytz.timezone('Asia/Kolkata')
        s,s1=d.astimezone(ist),d1.astimezone(ist)
        t,e=s.strftime('%d/%m/%Y %H:%M:%S'),s1.strftime('%d/%m/%Y %H:%M:%S')
        t,e=t.split(' '),e.split(' ')
        send_txt.append(i["event"]+"\n"+"Start Date :  " +t[0]+"    "+t[1][:5]+"\n"+"End Date :    "+e[0]+"    "+e[1][:5]+"\n"+"Register :"+i["href"]+"\n \n")
    send_message(''.join(send_txt),chat)



def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        items = db.get_items()
        if text.lower()=="/start":
            send_message("Welcome "+ str(update["message"]["chat"]["first_name"])+
                          " i will provide u every information regarding upcoming contests \n type /help to kow more options"
                          , chat)
            au_item=au.get_items()
            if (str(chat) not in au_item):
                au.add_item(chat)
            print("this person started :",str(update["message"]["chat"]["first_name"]))
        elif text.lower()=="/help":
            send_txt=' /start             Start the bot \n\
/list                 List all the coding websites \n\
/enable          Enable the notification \n\
/disable         Diable the notification  \n\
/help               Display the help \n\
/feedback      Give your comments. \n\
/credits          Creator info  '
            send_message(send_txt,chat)
        elif text.lower()=="/credits":
            send_txt="Akshat Garg \n Btech 3rd Year \n Malaviya National Institute of Technology Jaipur"
            send_message(send_txt,chat)
        elif text.lower()=="/feedback":
            send_txt="Give your feedback."
            send_message(send_txt,chat)
        elif text.lower()=="/enable":
            db_item=db.get_items()
            if (str(chat) not in db_item):
                db.add_item(chat)
            db_item=db.get_items()
            print(db_item)
            send_message("You will recieve notification every morning of all contests of that day", chat)
        elif text.lower()=="/disable":
            db_item=db.get_items()
            if (str(chat) in db_item):
                db.delete_item(chat)
            send_message("You will not recieve notification of every contest", chat)
        elif text.lower() == "/list":
            items=["Codechef","Codeforces","HackerEarth","leetcode","AtCoder","Spoj","Hackerrank","Google_coding_competitions"]
            keyboard = build_keyboard(items)
            send_message("Chosse one option", chat, keyboard)
        elif text.lower()=="codeforces":
            upcoming=[]
            get_upcoming(1,live,upcoming)
            send_contest_details(upcoming,chat)
        elif text.lower()=="codechef":
            upcoming=[]
            get_upcoming(2,live,upcoming)
            send_contest_details(upcoming,chat)
        elif text.lower()=="hackerearth":
            upcoming=[]
            get_upcoming(73,live,upcoming)
            send_contest_details(upcoming,chat)
        elif text.lower()=="leetcode":
            upcoming=[]
            get_upcoming(102,live,upcoming)
            send_contest_details(upcoming,chat)
        elif text.lower()=="atcoder":
            upcoming=[]
            get_upcoming(93,live,upcoming)
            send_contest_details(upcoming,chat)
        elif text.lower()=="spoj":
            upcoming=[]
            get_upcoming(26,live,upcoming)
            send_contest_details(upcoming,chat)
        elif text.lower()=="hackerrank":
            upcoming=[]
            get_upcoming(63,live,upcoming)
            send_contest_details(upcoming,chat)
        elif text.lower()=="google_coding_competitions":
            upcoming=[]
            get_upcoming(35,live,upcoming)
            send_contest_details(upcoming,chat)
        else:
            xx=str(chat)+str(update["message"]["chat"]["first_name"]) +":"+str(text)
            feedback.add_item(xx)
            print(feedback.get_items())
def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def enabled_notifications():
    s=str(datetime.now())
    rid=['1','2','73','102']
    result=[]
    if(s[11:13]=="12" and s[14:16]=="50"):
        for i in rid:
            today_contest(i,result)
        item=db.get_items()
        t=i["start"].split('T')
        e=i["end"].split('T')
        t,e=" ".join(t)," ".join(e)
        date_str,date_str1 = t,e
        d,d1 = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S'),datetime.strptime(date_str1, '%Y-%m-%d %H:%M:%S')
        d,d1 = pytz.UTC.localize(d),pytz.UTC.localize(d1)
        ist = pytz.timezone('Asia/Kolkata')
        s,s1=d.astimezone(ist),d1.astimezone(ist)
        t,e=s.strftime('%d/%m/%Y %H:%M:%S'),s1.strftime('%d/%m/%Y %H:%M:%S')
        t,e=t.split(' '),e.split(' ')
        send_txt.append(i["event"]+"\n"+"Start Date :  " +t[0]+"    "+t[1][:5]+"\n"+"End Date :    "+e[0]+"    "+e[1][:5]+"\n"+"Register :"+i["href"]+"\n \n")
        for i in item:
                send_message(''.join(send_txt),i)




def main():
    db.setup()
    feedback.setup()
    au.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
