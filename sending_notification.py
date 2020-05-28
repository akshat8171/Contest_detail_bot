from datetime import datetime
from todolist import send_message
from dbhelper import dbhelper
from upcoming_details import today_contest
import pytz
db=dbhelper("todolist.sqlite")
print(datetime.now())
def enabled_notifications():
    s=str(datetime.now())
    rid=['1','2','73','102','35','63','26','93']
    result=[]
    for i in rid:
        today_contest(i,result)
        #print(result)
    item=db.get_items()
    send_txt=[]
    if(len(result)==0):
        send_txt=["No scheduled contest for today on platforms that i have added, if you do on any other platform type the name below"]
    else:
        send_txt=["Contests scheduled today \n\n"]
        for i in result:
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
enabled_notifications()
