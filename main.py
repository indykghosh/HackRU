# Send a dynamic reply to an incoming text message
"""
ngrok instructions:
1) connect to Windows terminal
2) set current directory to parent directory of ngrok.exe file [cd Downloads]
3) Type the command "ngrok http 5000"
4) copy and paste the shown url into the twilio website under "A message comes in" (make sure Webhook and HTTP POST is selected)
5) add "/sms" to the end of the url
6) press "Save"
7) run the program
**Note: every time ngrok is ran with the command "ngrok http 5000", a new url is generated,
so these steps must be repeated if you need to launch ngrok again**

GitHub instructions to make changes to repository:
1) git add "filename"
2) git commit -m "message saying what's changed"
3) git push
"""
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

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

# List of user numbers who have texted the service
numbers_list = []
# List of user numbers who have joined the notif system
notif_list = []
events = {}
sends = {}

client = Client(key, secret, twilio_sid)

def writeToTxt():
    with open("notif.txt","w") as f:
        for numbers in notif_list:
            f.write(numbers + '\n')

def readFromTxt():
    global notif_list
    with open("notif.txt","r") as f:
        notif_list = [numbers[:-1] for numbers in f]

readFromTxt()

def writeToAll():
    with open("all.txt","w") as f:
        for numbers in numbers_list:
            f.write(numbers + '\n')

def readFromAll():
    global numbers_list
    with open("all.txt","r") as f:
        numbers_list = [numbers[:-1] for numbers in f]

readFromAll()

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

month_dict = {
    'january': 1, 'february' : 2, 'march' : 3, 'april' : 4,
    'may' : 5, 'june' : 6, 'july' : 7, 'august' : 8, 'september' : 9,
    'october' : 10, 'november' : 11, 'december' : 12
}

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


def list_events():
    event_message = ""
    event_df = pd.DataFrame(columns = ['Event', 'Date'])
    for event in events:
        data = {'Event' : [event], 'Date' : [events[event]]}
        df1 = pd.DataFrame(data)
        event_df = pd.concat([event_df, df1], ignore_index=True)
    event_df['Date'] = pd.to_datetime(event_df['Date'])
    event_df = event_df.sort_values(by='Date')
    event_df = event_df.reset_index(drop=True)
    today = datetime.date.today()
    i = 0
    while event_df.loc[i, 'Date'] < today:
        i += 1
    for n in range(i, i + 6):
        event_message += event_df.loc[n, 'Event'].replace("'", "") + event_df.loc[n, 'Date'].strftime(" %B %d") + "\n"
    return event_message



# Below: sms functionality 
app = Flask(__name__)

commands = ("To join the notification system, type \"JOIN\"\n"
            "To opt out of the notification system, type \"LEAVE\"\n"
            "To show a list of upcoming events, type \"LIST\"\n"
            "To view this list of commands again, type \"SUPPORT\"")
replySupport = " Reply with \"SUPPORT\" for help."
 
@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    global numbers_list
    global notif_list
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    body = body.lower()
  
    # Get the user's telephone number
    userNumber = request.values.get('From', None)
    # Start our TwiML response
    resp = MessagingResponse()
 
    # Determine the right reply for this message
 
    # If the user has never texted the service
    if not userNumber in numbers_list:
        numbers_list.append(userNumber)
        resp.message("Welcome to the Rutgers Academic Calender Notification System: RU Prepared?\n" + commands)
        writeToAll()
 
    # If the user has previously texted the service
    else:
        if body == "join":
            if userNumber in notif_list:
                resp.message("You are already opted into the notification system." + replySupport)
            else:
                notif_list.append(userNumber)
                resp.message("You have been opted into the notification system. Type \"LEAVE\" to opt out at any time." + replySupport)
                writeToTxt()

        elif body == "leave":
            if not userNumber in notif_list:
                resp.message("You are not currently opted into the notification system." + replySupport)
            else:
                notif_list.remove(userNumber)
                resp.message("You have been opted out of the notification system. Type \"JOIN\" to opt in again." + replySupport)
                writeToTxt()

        elif body == "list":
            resp.message(list_events())
 
        elif body == "support":
            resp.message(commands)
 
    return str(resp)
 
app.run(debug=True)
 


