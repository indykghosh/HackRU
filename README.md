# HackRU
"""
RU Prepared?
An SMS push notification system for upcoming academic Rutgers events using information from their online calendar. 
Users can text our active Twilio number to opt in or out of this service.

Inspiration
Many times, we and other Rutgers students find ourselves caught off guard when an important event seems to appear out of nowhere. 
To help us and those students who feel the same, we wanted to put together some sort of notification system 
that would inform us of these upcoming dates and events. After the short demonstration of Twilio's SMS messaging API, 
we were inspired to incorporate it into our idea, thus creating RU Prepared?

What it does
Our code first reads from the Rutgers academic calendar website to extract the listed events and corresponding dates. 
Then, we set up an active number on Twilio's website to accept SMS messages and respond to them 
as well as put together a notification service set to inform subscribers of upcoming academic events a week in advance. 
Our number understands 4 commands:

'JOIN' : opts the user into the notification service for upcoming academic events
'LEAVE' : opts the user out of the notification service
'LIST' : provides a list of the next six upcoming events from the Rutgers academic calendar and their corresponding dates
'SUPPORT' : provides a list of the previous commands

Text 732 743 7062 to start!

How we built it
We coded using Python to read the Rutgers academic calendar and extract the listed events and their corresponding dates into a .csv file. 
Using Pandas, we were able to make use of the information we extracted to build the notification system and format 
the next six upcoming events into a list to be read by the user. We made use of the Twilio SMS messaging API to be able to read
the user's text messages in order to create automated responses. Our program stores the user's number in a .txt file
to keep track of all the numbers opted into the notification service, and removes their number if they choose to opt out of the service. 
The notification service will send an automated message one week before a scheduled event at 10 a.m. to each number recorded
in the notification list detailing the event and its date.

Challenges we ran into
This was our first Hackathon and most of our first times utilizing Python to this extent, so many of our challenges stemmed from 
familiarizing ourselves with the language. We were also inexperienced with working in teams through GitHub and ran into several 
technical difficulties that we eventually overcame with the help of the mentors here at HackRU. The Twilio SMS messaging API also 
took a considerable amount of time to understand and properly incorporate into our program, but guidance from the Twilio 
representative allowed us to figure it out.

Accomplishments that we're proud of
We are proud of completing our first hack at our first Hackathon and creating a functional SMS messaging system. 
It was a fulfilling and enriching experience to work as a team and to use our collective knowledge and research to build our program. 
We are proud of how much we have learned and improved our skills during this 24-hour period.

What we learned
This was a great learning experience for all of us, especially in regards to working through GitHub with collaborators on a project. 
We became much more acquainted with Python as well as the data manipulation and analysis abilities of Pandas. 
Additionally, we did research into Twilio's API in order to understand how to use the SMS messaging system through Python.

What's next for RU Prepared?
Future improvements to the program would include incorporating more Rutgers events listed on other websites into the system
and adding more features to the response system. We could also improve the program's functionality by creating a second thread
in which to constantly check and update the current time in order to properly run the notification system separately from the rest of the code. 
At the moment, our Twilio account is only a trial account, and thus cannot accept from or send messages to unverified phone numbers. 
If we wish to maintain the service and make it publicly available, we would need to upgrade our account and provide it with funding.

Built With
ngrok
pandas
python
twilio
"""
