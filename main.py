import json
import os
import smtplib
from email.mime.text import MIMEText

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def send_notification(notification_msg: str):
    notification_phone = os.environ.get("NOTIFICATION_PHONE_NUMBER")
    relay_url = os.environ.get("RELAY_URL")
    if not notification_phone:
        raise ValueError("Missing one or more required environment variables.")

    body = {
        "from_service": "trail-condition-checker",
        "notification_type": "sms",
        "to_number": notification_phone,
        "number_provider_url": "vtext.com",
        "message": notification_msg
    }

    try:
        res = requests.post(relay_url, json=body)
        res_body = res.json()
        if res_body["sent"] == True:
            print("Message sent!")
        else:
            print("Message failed to send.")
    except Exception as e:
        print(f"Failed to send message: {e}")


def main():
    load_dotenv()
    trail_name = "Skyline Trail"
    res = requests.get(
        "https://www.nps.gov/mora/planyourvisit/trails-and-backcountry-camp-conditions.htm")
    bs = BeautifulSoup(res.content, features="html.parser")
    row = bs.find("td", string=trail_name)
    if row:
        cells = row.parent.find_all("td")
        snow_cover_pct = cells[1].text.strip()
        trail_conditions = cells[2].text.strip()
        updated_at = cells[3].text.strip()
        status_string = f"{trail_name}: {snow_cover_pct}% snow cover, {trail_conditions}. Last updated {updated_at}."
        send_notification(status_string)
    else:
        print(f"Trail '{trail_name}' not found.")


if __name__ == "__main__":
    main()
