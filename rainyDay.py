# Rainy Day Project
# William Lord
# Gets tomorrow's forecast from the national weather service and sends me a text if there is a chance of rain.

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# ----------------------------------
# Connecting to the forecast website
# ----------------------------------

tempe = 'https://forecast.weather.gov/MapClick.php?lat=33.4255&lon=-111.9372'       # school
seattle = 'https://forecast.weather.gov/MapClick.php?lat=47.6036&lon=-122.3294'     # for testing
escondido = 'https://forecast.weather.gov/MapClick.php?lat=33.1232&lon=-117.0822'   # home

page = requests.get(tempe)  # I will occasionally change the city
print(page.status_code)     # (200 means successful import)

# ---------------------
# Parsing the web-page
# ---------------------

soup = BeautifulSoup(page.content, 'html.parser')

# get the list of forecast items
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")

# move along until we find the correct item
for element in forecast_items:
    period = element.find(class_="period-name").get_text()
    short_desc = element.find(class_="short-desc").get_text()

    # occasionally an extra element will appear, this ignores it
    if (short_desc != "Excessive Heat Warning") and (period != "Tonight"):
        break

temperature = element.find(class_="temp").get_text()
description = str(element.find('img', alt=True))

# the forecast we want is between quotes; we can split the string along the quotes, then extract the middle item
forecast = description.split('\"')[1]

# output to console so I can see forecast when the program runs if I want
print(period)
print(short_desc)
print(forecast)
print(temperature)

# -------------------------
# Sending the text message
# -------------------------

# only send text if there is a chance of rain
if ("rain" in forecast) or ("shower" in forecast):

    with open('sensitiveInfo', 'r') as file:
        email = file.readline().strip()
        password = file.readline().strip()
        phone = file.readline().strip()

    # this is for t-mobile, different carriers use something different
    sms_gateway = phone + '@tmomail.net'

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

    # exit the server
    server.quit()
