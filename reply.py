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
"""
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    # Get the user's telephone number
    userNumber = request.values.get('From', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'hello':
        resp.message("Hi!")
    elif body == 'bye':
        resp.message("Goodbye")

    return str(resp)

app.run(debug=True)
