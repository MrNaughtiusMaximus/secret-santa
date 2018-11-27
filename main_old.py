
# TODO Add a config file which needs to be read to send emails - add the option to either place the file or put it through the GUI
def send_emails():
    import smtplib
    username = "my@email.com"
    password = "my_password"

    server = smtplib.SMTP('smtp.gmail.com:587')
    # server.set_debuglevel(True)
    server.starttls()
    server.login(username, password)
    msg = "\r\n".join([
        "From: " + username,
        "To: " + username,
        "Subject: Just a message",
        "",
        "Why, oh why"
        ])
    try:
        server.sendmail(username, username, msg)
    except:
        print("Couldn't send email!")

    server.quit()
