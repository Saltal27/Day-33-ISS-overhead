import requests
from datetime import datetime
import smtplib

MY_LAT = 33.510414
MY_LONG = 36.278336


def check_pos():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LONG - 5 <= iss_longitude <= MY_LONG + 5 and MY_LAT - 5 <= iss_latitude <= MY_LAT + 5:
        return True


def check_dark():
    time_now = datetime.now()
    this_hour = time_now.hour

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    if this_hour < sunrise or this_hour > sunset:
        return True


def send_iss_mail():
    my_email = "pythontest32288@gmail.com"
    my_password = "gsrfzucledwimgqp"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs="omarmobarak53@gmail.com",
                            msg="Subject:ISS!\n\nLook up!\nYou can see the ISS in the sky right now"
                            )


minute_check = 0


def keep_checking():
    global minute_check

    time_now = datetime.now()
    this_minute = time_now.minute

    if this_minute != minute_check:
        if check_dark() and check_pos():
            send_iss_mail()
        minute_check = this_minute
    keep_checking()
