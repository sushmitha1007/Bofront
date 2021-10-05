import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from config.config import email_credentials


# move to config
email_credentials = {
    "sender": "svpai969@gmail.com",
    "password": "ibncduvadmpljiwm"
}

def send_mail(text, subject='Complaint Details', to_emails=None, html=None):
    assert isinstance(to_emails, list) ,"Parameter 'to_emails' always takes a list of values "
    msg = MIMEMultipart()
    msg['From'] = email_credentials['sender']
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)
    if html is not None:
        html_part = MIMEText(html, 'html')
        msg.attach(html_part)
    msg_str = msg.as_string()
    # login to my smtp server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(email_credentials['sender'], email_credentials['password'])
    server.sendmail(email_credentials['sender'], to_emails, msg_str)
    server.quit()
