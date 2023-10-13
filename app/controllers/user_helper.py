import smtplib

from email.mime.text import MIMEText


def send_mail(path, mailid):
    subject = "Set password for you Childcare group account"
    body = "Kindly follow the link to set your password for the Childcare Management System Account " + path + "/setpassword?email=" + mailid
    sender = "chidambaramg.dev@gmail.com"
    password = "baeaqufrwmtosnnr"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = mailid
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, mailid, msg.as_string())

