from bs4 import BeautifulSoup
from dotenv import load_dotenv
from email.mime.text import MIMEText
import os
import requests
import smtplib


def send_notification(notification_msg: str):
    notification_phone = os.environ.get("NOTIFICATION_PHONE_NUMBER")
    from_email = os.environ.get("FROM_EMAIL")
    app_pw = os.environ.get("FROM_EMAIL_APP_PW")

    to_number = f"{notification_phone}@vtext.com"

    # Create the message
    msg = MIMEText(notification_msg)
    msg["From"] = from_email
    msg["To"] = to_number
    msg["Subject"] = ""  # SMS doesn't need a subject

    # Send the email (SMS)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_email, app_pw)
        server.sendmail(from_email, to_number, msg.as_string())

    print("Message sent!")


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
