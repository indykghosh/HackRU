import os
from twilio.rest import Client
import datetime
import pandas as pd

key = "SKd9a607a5573a97dc32002e2b43648675"
secret = "gjyVH0EUvl3I8XXVJ4W3s4zfgwVoZly5"
twilio_sid = "AC6e7f493586c79a5c3cf3a8e85305af4d"
mg_sid = "MGbc475ef0b56418fd500454d524e52384"

# twilio_sid = os.environ['TWILIO_SID']
# key = os.environ['TWILIO_API_KEY']
# secret = os.environ['TWILIO_API_SECRET']

notif_list = ['+18482473420', '+19084337325', '+18562063267']
events = {}
sends = {}

client = Client(key, secret, twilio_sid)

month_dict = {
    'january': 1, 'february' : 2, 'march' : 3, 'april' : 4,
    'may' : 5, 'june' : 6, 'july' : 7, 'august' : 8, 'september' : 9,
    'october' : 10, 'november' : 11, 'december' : 12
}


def schedule_notifs(event, dateStart, dateSend):
    send_date = dateSend
    for number in notif_list:
        mess_body = event + ' will be in a week on ' + dateStart.strftime("%A, %B %d")
        message = client.messages \
            .create(
                messaging_service_sid = mg_sid,
                body = mess_body,
                send_at = send_date,
                schedule_type='fixed',
                to=number
            )



def interpret_csv(file):
    df = pd.read_csv(file)
    for i in range(len(df)):
        for col in range(1, 4):
          event_name = df.loc[i, 'Event']
          dateLine = df.loc[i][col]
          dateLine = dateLine.replace(',',"")
          dateLine = dateLine.replace("'", " ")
          date_numbers = dateLine.split(' ', 4)
          
          date_numbers[4] = date_numbers[4].replace(' ', '')
          event_name += str(" " + date_numbers[4])
          event_date = datetime.datetime(int(date_numbers[4]), month_dict[date_numbers[2]], int(date_numbers[3]))
          events.update({event_name : event_date})
          date_numbers.clear()


def sends_to_event():
  for event in events:
    dateStart = events[event]
    send_day = int(dateStart.strftime("%d"))
    send_month = int(dateStart.strftime("%m"))
        
    for i in range(7):
        if send_day == 1:
            send_month -= 1
            if send_month == 2:
                send_day = 28
            elif send_month == 4 or send_month == 6 or send_month == 9 or send_month == 11:
                send_day = 30
            else:
                send_day = 31
        else:
            send_day -= 1

    send_date = datetime.datetime(int(dateStart.strftime("%Y")), send_month, send_day, 14, 00)
    sends.update({send_date : event})


interpret_csv('calendar.csv')

sends_to_event()


today = datetime.date.today()
for send in sends:
    if today == send.date():
      eventforNotif = sends[send]
      schedule_notifs(eventforNotif, events[eventforNotif], send)
