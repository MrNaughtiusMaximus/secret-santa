import os

print("""Hello!
Welcome to the Secret Santa app!
Follow the instructions below and have a jolly good time!
Hint: If you want to avoid inputting 100s of people manually,
just add a file called "participants.txt" in the following format:
name, email, house name or number, postcode

Cheerio!
""")

file_path = os.path.join(os.getcwd(), "participants.txt")

if not os.path.exists(file_path):
    print("Creating a list with participants!")
    open(file_path, 'a+')
    print("Created!")
else:
    print("There is a list with participants present!")


def write_details(name, email, house, postcode):
    file_path = os.path.join(os.getcwd(), "participants.txt")
    file = open(file_path, "a+")
    file.write("\n" + name + ", " + email + ", " + house + ", " + postcode)


def ask_participant():
    print("\n")
    name = input("What's the name of the participant?")
    email = input("What's their email")
    house = input("What's their house name/number?")
    postcode = input("What's their postcode?")
    write_details(name, email, house, postcode)


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

print("Well, let's get started, shall we?")
num_of_participants = int(input("How many participants are there? (Use numbers only) "))
for x in range(0, num_of_participants):
    ask_participant()
print("You have now added %d participants! Prepare for all hell to be let loose! Mwahahahha" % num_of_participants)

if input("Do you want to send the emails? (Y/N) ").lower() == "y":
    send_emails()

exit()
