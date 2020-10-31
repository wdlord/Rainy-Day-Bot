# Rainy Day Project
# William Lord
# Program that gets the next days forecast from the national weather service and sends me a text
#   if there is a chance of rain.

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# WEB SCRAPING STUFF
# --------------------------------

# paste the link for a particular city instead of this one
# tempe
page = requests.get('https://forecast.weather.gov/MapClick.php?lat=33.4255&lon=-111.9372')

# printing status hoping for a 200 (successful import)
print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser')

# get the list of forecast items
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")

# move along until we find the correct item
for element in forecast_items:

    # get short description for the forecast
    period = element.find(class_="period-name").get_text()
    short_desc = element.find(class_="short-desc").get_text()

    # break if the item is the one we want
    if (short_desc != "Excessive Heat Warning") and (period != "Tonight"):
        break

# get temperature and full forecast
temperature = element.find(class_="temp").get_text()
description = element.find('img', alt=True)

# output to console so I can see forecast when the program runs if I want
print(period)
print(short_desc)
print(temperature)

# REFORMAT DESCRIPTION
# ---------------------
forecast = ""
quotes = 0

# the description we want is between quotes, this extracts it
for char in str(description):

    if quotes == 2:
        break

    if char == "\"":
        quotes += 1

    elif quotes == 1:
        forecast += char

# SMS CODE
# -------------

# only send text if there is a chance of rain
if ("rain" in forecast) or ("shower" in forecast):

    print(forecast)  # print to console

    # used soon to login to server
    email = "email goes here"
    password = "password goes here"

    # this is for t-mobile, different carriers use something different
    sms_gateway = 'phonenumberhere@tmomail.net'

    # server for sending text over email
    smtp = "smtp.gmail.com"
    port = 587

    # start server and login
    server = smtplib.SMTP(smtp, port)
    server.starttls()
    server.login(email, password)

    # prepare mail fields
    message = MIMEMultipart()
    message['From'] = email
    message['To'] = sms_gateway

    # subject line and body
    message['Subject'] = "FORECAST \n"
    body = forecast + "\n"

    # we're just sending plain text, attach it to message
    message.attach(MIMEText(body, 'plain'))

    # send the text over email
    server.sendmail(email, sms_gateway, message.as_string())

    # quit the server
    server.quit()
