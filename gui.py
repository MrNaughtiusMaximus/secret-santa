from tkinter import *
from os import path, getcwd
from playsound import playsound
from random import randint
from random import choice
import webbrowser

from sql import SQL


# TODO Add for Windows only
# def play():
#     playsound("wow/wow-%s.wav" % randint(0,9))


def create_listbox(master: Tk):
    ls = Listbox(master)
    ls.pack(fill=BOTH, expand=TRUE)
    return ls


def raise_frame(frame: Frame):
    frame.tkraise()

# TODO Move main code to App and just start it once in the __init__ = "__main__"
# class App():
#     if __name__ == '__main__':
#
#     def start(self):
#         self.root.mainloop()


class StartPage(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)
        lbl = Label(self, text="Welcome to the Yordan's Secret Santa app!\nWhat do you want to do today?")
        lbl.pack(fill=BOTH, expand=TRUE)
        opt = IntVar()
        r1 = Radiobutton(self, text="Add participants manually", variable=opt, value=1)
        r1.pack(anchor=W)
        r2 = Radiobutton(self, text="Import participants", variable=opt, value=2)
        r2.pack(anchor=W)
        r3 = Radiobutton(self, text="Leave feedback", variable=opt, value=3)
        r3.pack(anchor=W)
        btn = Button(self, text="Continue", command=lambda: self.command(opt), width=10)
        btn.pack(side=BOTTOM, anchor=E, pady=5, padx=5)

    def command(self, i):
        print("option selected is " + str(i.get()))
        try:
            if i.get() == 1:
                raise_frame(hmp)

            elif i.get() == 2:
                raise_frame(ip)

            elif i.get() == 3:
                # TODO Open feedback page and send email to myself
                raise_frame(lf)

        except Exception as e:
            # TODO Add an error bar saying they need to select an option
            print("The user did not select an option")

class HowManyParticipants(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW, padx=5, pady=5)
        Label(self, text="How many participants do you want to enter?").pack(fill=X)
        # TODO Check if file already exists and, if it does, ask whether to use or delete
        self.lbl = Label(self)
        self.lbl.pack(fill=BOTH, expand=TRUE)
        f = Frame(self)
        f.pack(side=BOTTOM, fill=X, expand=TRUE, anchor=SW)
        Label(f, text="Enter number here:").pack(fill=X, side=LEFT, anchor=W)
        p = Entry(f)
        p.pack(fill=X, side=LEFT, expand=TRUE, anchor=W)
        btn = Button(f, text="Continue", command=lambda: self.command(p), width=10)
        btn.pack(fill=X, side=RIGHT, anchor=SE)

    def command(self, i):
        try:
            if int(i.get()) < 5:
                self.lbl.configure(text="You need to enter at least 5 participants!")
            else:
                print("Expected participants are %s before the update" % str(ep.exp_part))
                ep.exp_part = i.get()
                ep.exp.configure(text="You have entered 0 out of %s participants" % i.get())
                print("Expected participants are %s after the update" % str(ep.exp_part))
                raise_frame(ep)
        except Exception as e:
            self.lbl.configure(text="Please enter a number!")


class EnterParticipants(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW, padx=5, pady=5)

        (self.exp_part, self.ent_part) = 0, 0
        Label(self, text="Expecting " + str(self.exp_part) + " more participants")
        self.exp = Label(self, text="You have entered %s out of %s participants" % (self.exp_part, self.ent_part))
        self.err = Label(self)
        info = Label(self, text="Enter the participant’s details:")
        f = Frame(self)
        for a in (self.exp, self.err, info, f):
            a.pack(fill=BOTH, expand=TRUE, side=TOP)

        labels = ["Name: ", "Email: ", "Address number: ", "Postcode: ", "Wishlist URL (optional): "]
        name = Entry(f)
        email = Entry(f)
        house = Entry(f)
        post = Entry(f)
        wish = Entry(f)
        entries = [name, email, house, post, wish]
        # Positioning everything accordingly
        for i in range(len(labels)):
            print("Row number is: " + str(i))
            Label(f, text=labels[i]).grid(row=i, column=0, sticky=W)
            f.rowconfigure(i, weight=1)
            entries[i].grid(row=i, column=1, columnspan=4, sticky=NSEW)
        f.columnconfigure(1, weight=1)
        btn = Button(self, text="Continue",
                     command=lambda: self.add_user(name, email, house, post, wish),
                     width=10)
        btn.pack(side=BOTTOM, expand=TRUE, anchor=SE)

    def update_bar_re_adding_user(self):
        self.err.configure(text="User added!")
        self.ent_part = self.ent_part + 1
        self.exp.configure(text="You have entered %s out of %s participants" % (self.ent_part, self.exp_part))

    # TODO Check error handling
    def add_user(self, name, email, house, post, wish):
        try:
            print("Adding user " + name.get())
            db.add_user(name.get(), email.get(), house.get(), post.get(), wish.get())

            name.delete(0, 'end')
            email.delete(0, 'end')
            house.delete(0, 'end')
            post.delete(0, 'end')
            wish.delete(0, 'end')

            self.update_bar_re_adding_user()
            print("Expected participants are %s and entered ones are %s" % (self.exp_part, self.ent_part))
            if int(self.exp_part) == int(self.ent_part):
                sep.update_label()
                raise_frame(sep)
            # play()

        # TODO Add error for duplicate email or empty input
        except Exception as e:
            print("The error is: " + str(e))
            self.err.configure(text="There was an error while adding the user. Try again!")


class ImportParticipants(Frame):

    # TODO Ask users to provide a .txt file in the specified format OR a sqlite database with the necessary specs
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW, padx=5, pady=5)
        lbl = Label(self, text="To import participants successfully, use the following format:\n\n"
                               ".csv or .txt files: name, email, house number or name, postcode\n"
                               "Example: John Doe, john@email.com, 25, BN10 3PF\n"
                               "See example.txt if unsure.\n\n"
                               "SQLite .db files: create a table with columns in same order as above\n\n"
                               "Note: unique email addresses are necessary for the app to work")
        lbl.pack(side=TOP, fill=X)
        lbl2 = Label(self)
        lbl2.pack(side=TOP, fill=X, expand=TRUE)
        f = Frame(self)
        f.pack(side=BOTTOM, fill=X, expand=TRUE, anchor=SW)
        self.lbl3 = Label(f, text="Enter the file name: ")
        self.lbl3.pack(side=LEFT, anchor=W, fill=X)
        self.e = Entry(f)
        self.e.pack(side=LEFT, anchor=W, padx=5, fill=X, expand=TRUE)
        self.btn = Button(f, text="Import", command=lambda: self.imp(lbl2), width=10)
        self.btn.pack(side=RIGHT, anchor=SE)

    def imp(self, a):
        file_path = path.join(getcwd(), str(self.e.get()))
        if not path.exists(file_path):
            a.configure(text="File cannot be found!\nImport the file and try again.")
        else:
            # TODO Add check whether filed ends in .csv or .txt and extract data accordingly
            # TODO Add error handling try/except
            file = open(file_path, "r")
            users = []
            # Getting all users
            for l in file:
                users.append(l)
                print("User %s found" % l)

            # Sanitizing the input
            pattern = '[a-zA-Z@\.0-9/: ]'
            san_users = []
            db.reset_records()
            for u in users:
                ls = u.split(",")
                usr = []
                for each in ls:
                    usr.append(''.join(re.findall(pattern, each)))
                print("Sanitised user is %s" % str(usr))
                if len(usr) == 4:
                    db.add_user(usr[0], usr[1], usr[2], usr[3])
                elif len(usr) == 5:
                    db.add_user(usr[0], usr[1], usr[2], usr[3], usr[4])
                else:
                    print("Error encountered! User does not have the expected values.")
                print("Adding sanitized user to DB:"
                      "name %s, email %s, house %s, post %s, wish %s" % (usr[0], usr[1], usr[2], usr[3], usr[4]))
                db.add_user(usr[0], usr[1], usr[2], usr[3], usr[4])
                san_users.append(usr)
            # TODO Give them option to retry
            sep.update_label()
            raise_frame(sep)


class Navigation(Frame):

    def __init__(self, master):
        Frame.__init__(self, master, bd=1, relief=RAISED)
        self.grid(sticky=NSEW)
        btn = Button(self, text="Home", command=lambda: self.home(), width=10)
        btn.pack(side=LEFT, anchor=E, pady=5, padx=5)
        btn1 = Button(self, text="Exit", command=lambda: self.close(), width=10)
        btn1.pack(side=LEFT, anchor=E, pady=5, padx=5)
        btn2 = Button(self, text="Reset DB", command=lambda: self.clear_db(), width=10)
        btn2.pack(side=LEFT, anchor=E, pady=5, padx=5)
        # TODO Link below with GitHub release version
        Label(self, text="v0.9 Yordan Angelov Copyright 2018").pack(side=RIGHT, padx=5)

    @staticmethod
    def home():
        raise_frame(s)

    @staticmethod
    def close():
        db.close()
        exit()

    @staticmethod
    def clear_db():
        print("DB dropped!")
        db.reset_records()
        raise_frame(s)


class LeaveFeedback(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)
        Label(self, text="If you've enjoyed using the app (or even used it at all!)\n"
                         "and you're feeling generous, make sure\n you drop me an email "
                         "on y_angelov@hotmail.com with a brief feedback!\n\n"
                         "If you're feeling even more generous, you can send me a quick "
                         "code review.\n\nFinally, for the true Santas among you,\n"
                         "feel free to submit pull requests with suggestions for improvements!\n\n"
                         "Repo can be found below:").pack(fill=BOTH, expand=TRUE)
        link = Label(self, text="GitHub repo", fg="blue", cursor="hand2")
        link.pack(expand=TRUE)
        link.bind("<Button-1>", self.go_to_repo)
        Label(self, text="This is definitely not a virus.").pack(fill=BOTH, expand=TRUE)

    @staticmethod
    def go_to_repo(event):
        webbrowser.open_new(r"https://github.com/n4ught1us-max1mus/secret-santa")


class SendEmailsPage(Frame):

    # TODO Add scrollbar if needed
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW, padx=5, pady=5)
        self.part = len(db.fetch_participants())
        self.lbl = Label(self)
        self.lbl.pack(fill=BOTH, expand=TRUE)
        self.lb1 = create_listbox(self)
        self.update_label()
        self.pairs = {}
        self.btn = Button(self, text="Pair participants", command=lambda: self.randomise_santas())
        self.btn.pack(anchor=SE)

    def randomise_santas(self):
        # looping animation while you wait saying "Pairing participants..."
        # Can be restored by just using self.btn.pack(args*)
        self.btn.pack_forget()
        self.lb1.pack_forget()
        self.lbl.configure(text="Randomising pairs...")

        for u in db.fetch_participants():
            # Fetching all participants
            users = db.fetch_participants()
            # Finding index of the current element
            i = users.index(u)
            del users[i]

            # Checking if dict is empty, e.g. whether there are any pairs already assigned
            if bool(self.pairs) is True:
                # If there are, remove the giftee from the list so that they are not allocated two gifters
                for k, v in self.pairs.items():
                    try:
                        del users[users.index(v)]
                    except Exception as e:
                        # Happens whenever the gifter has already been removed from the list
                        print(e)

            # TODO Expain why
            if len(users) > 0:
                self.pairs[u] = choice(users)

        # TODO Remove when app is finished
        for k, v in self.pairs.items():
            print("Key %s has value %s" % (str(k), str(v)))

        self.lbl.configure(text="Pairs have been assigned!\nDo you want to send out emails?")
        self.btn.configure(text="Send emails", command=lambda: self.send_emails(self.pairs))
        self.btn.pack(anchor=SE, padx=5, pady=5)

    def update_label(self):
        users = db.fetch_participants()
        self.part = len(users)
        self.lbl.configure(text="There are %s participants saved" % str(self.part))
        self.lb1.delete(0, END)
        for u in users:
            self.lb1.insert(users.index(u), "%s, %s" % (u[1], u[2]))

    # TODO Can make a new page object with email-related stuff
    def send_emails(self, pairs: dict):
        import smtplib
        self.lbl.configure(text="Sending emails...")
        print("Starting the emails sending sequence...")
        username = "ten10secretsanta@gmail.com"
        password = "jkvryxsvsnrkioww"
        i = 0
        try:
            print("Connecting to server...")
            # server = smtplib.SMTP("smtp.gmail.com", 587)
            # server.set_debuglevel(True)
            # print("Starting TLS...")
            # server.starttls()
            # print("Logging in...")
            # server.login(username, password)

            # TODO Remove file stuff after testing is finished
            file = open("sample-mails", "w")
            for k, v in pairs.items():
                # TODO Add the wishlist if that user has one
                msg = "\r\n".join([
                    "From: " + username,
                    "To:%s" % str(v[2]),
                    "Subject: You have a new Secret Santa pair!",
                    "",
                    "Hi%s,\n\n"
                    "You are the Secret Santa for%s!\n"
                    "Choose your gift and send it off to%s,%s.\n\n"
                    "Have a Merry Christmas and a Happy New Year!"
                    % (str(k[1]), str(v[1]), str(v[3]), str(v[4]))
                ])
                file.write(msg + ",\n")
                try:
                    print("Sending email...")
                    # server.sendmail(username, "y_angelov@hotmail.com", msg)
                    i = i + 1
                    self.lbl.configure(text="%s emails sent out of %s..." % (i, len(pairs)))
                    print("Email sent!")
                except:
                    print("Couldn't send email!")

            # server.quit()
            file.close()
            self.lbl.configure(text="Emails sent!\n"
            "Hope you enjoyed using the app!\n\n"
            "Use the button below to be redirected to the Feedback page.\n")
            self.btn.configure(text="Leave feedback", command=lambda: raise_frame(lf))


        except Exception as e:
            print(e)
            self.lbl.configure(text="Issue encountered while sending emails!")


if __name__ == '__main__':

    # TODO Add submission of Entry fields with Enter
    # TODO Adjust all windows to have the same # of rows and columns
    root = Tk()
    root.title("Secret Santa")
    # TODO Mess with design later
    # root.configure(bg="gray")
    # Only works with .ico files

    # Works on Windows 10
    # root.iconbitmap("santa.ico")
    root.resizable(width=False, height=False)

    db = SQL()

    s = StartPage(root)
    hmp = HowManyParticipants(root)
    ep = EnterParticipants(root)
    ip = ImportParticipants(root)
    lf = LeaveFeedback(root)
    nav = Navigation(root)
    sep = SendEmailsPage(root)

    for frame in (s, ep, ip, hmp, lf, sep):
        frame.grid(row=0, column=0, sticky='news', padx=5, pady=5)

    nav.grid(row=1, column=0, sticky='news')

    raise_frame(s)

    root.mainloop()
