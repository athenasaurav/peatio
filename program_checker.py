import psutil
import os
import schedule
import time
import smtplib, ssl
import config
def job():
    def is_running(script):
        for q in psutil.process_iter():
            if q.name().startswith('python'):
                if len(q.cmdline())>1 and script in q.cmdline()[1] and q.pid !=os.getpid():
                    print("'{}' Process is already running".format(script))
                    return True

        return False


    if not is_running("app.py"):
        print("Program stopped")
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = config.sender_email
        receiver_email = config.receiver_email
        password = config.password
        message = """\
        Subject: Program Stopped

        The Program has encountered an error and has stopped working. Please restart urgently"""
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

schedule.every(1).seconds.do(job)
# schedule.every(config.REFRESH_TIME_BALANCE).seconds.do(balance)

while True:
    schedule.run_pending()
    time.sleep(1)