from tkinter import *
from os import path, getcwd
from playsound import playsound
from random import randint
from random import choice
from webbrowser import open_new
from smtplib import SMTP
from platform import platform

from sql import SQL, IntegrityError


def play(scenario):
    if "Windows" in platform():
        if scenario == "err":
            playsound("wow/err-%s.wav" % randint(1, 4))
        if scenario == "wow":
            playsound("wow/wow-%s.wav" % randint(1, 10))


def raise_frame(fr: Frame):
    fr.tkraise()


class StartPage(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)
        Label(self, text="Welcome to the Yordan's Secret Santa app!\nWhat do you want to do today?")\
            .pack(fill=BOTH, expand=TRUE)
        self.err = Label(self, fg="red")
        self.err.pack(fill=BOTH, expand=TRUE)
        opt = IntVar()
        r1 = Radiobutton(self, text="Add participants manually")
        r2 = Radiobutton(self, text="Import participants")
        r3 = Radiobutton(self, text="Leave feedback")
        radio_buttons = [r1, r2, r3]
        for i in range(len(radio_buttons)):
            radio_buttons[i].configure(variable=opt, value=i+1)
            radio_buttons[i].pack(anchor=W)

        Button(self, text="Continue", command=lambda: self.command(opt), width=10).pack(anchor=SE)

    def command(self, i):
        try:
            if i.get() == 1:
                raise_frame(hmp)

            elif i.get() == 2:
                raise_frame(ip)

            elif i.get() == 3:
                raise_frame(lf)

            else:
                self.err.configure(text="Select an option to proceed")
                self.err.pack(fill=BOTH, expand=TRUE)

        except Exception as e:
            print("Got the error: %s" % str(e))
            self.err.configure(text="Select an option to proceed")
            print("The user did not select an option")
            play("err")


class HowManyParticipants(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)
        Label(self, text="How many participants do you want to enter?").pack(fill=X, expand=TRUE)
        self.lbl = Label(self, fg="red")
        self.lbl.pack(fill=BOTH, expand=TRUE)
        f = Frame(self)
        f.pack(side=BOTTOM, fill=X, expand=TRUE, anchor=S)
        Label(f, text="Enter number here:").pack(fill=X, side=LEFT, anchor=W)
        p = Entry(f)
        p.pack(fill=X, side=LEFT, expand=TRUE, anchor=W, padx=5)
        btn = Button(f, text="Continue", command=lambda: self.command(p), width=10)
        btn.pack(fill=X, side=RIGHT, anchor=SE)

    def command(self, i):
        try:
            if int(i.get()) < 5:
                self.lbl.configure(text="You need to enter at least 5 participants!")
            else:
                ep.exp_part = i.get()
                ep.exp.configure(text="You have entered 0 out of %s participants" % i.get())
                raise_frame(ep)
        except Exception as e:
            print("Got the error: %s" % str(e))
            self.lbl.configure(text="Enter a number to proceed")
            play("err")


class EnterParticipants(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)

        (self.exp_part, self.ent_part) = 0, 0
        Label(self, text="Expecting " + str(self.exp_part) + " more participants")
        self.exp = Label(self, text="You have entered %s out of %s participants" % (self.exp_part, self.ent_part))
        self.err = Label(self)
        info = Label(self, text="Enter the participant’s details:")

        # Positioning entry fields and their labels accordingly
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
        for i in range(len(labels)):
            Label(f, text=labels[i]).grid(row=i, column=0, sticky=W)
            f.rowconfigure(i, weight=1)
            entries[i].grid(row=i, column=1, columnspan=4, sticky=NSEW)
        f.columnconfigure(1, weight=1)

        btn = Button(self, text="Continue",
                     command=lambda: self.add_user(name, email, house, post, wish),
                     width=10)
        btn.pack(side=BOTTOM, expand=TRUE, anchor=SE)

    def update_bar_re_adding_user(self):
        self.err.configure(text="User added!", fg="black")
        self.ent_part = self.ent_part + 1
        self.exp.configure(text="You have entered %s out of %s participants" % (self.ent_part, self.exp_part))

    def add_user(self, name, email, house, post, wish):
        try:
            for i in (name, email, house, post):
                if len(i.get()) == 0:
                    raise AttributeError("required field is empty")

            db.add_user(name.get(), email.get(), house.get(), post.get(), wish.get())
            for i in (name, email, house, post, wish):
                i.delete(0, 'end')
            self.update_bar_re_adding_user()
            if int(self.exp_part) == int(self.ent_part):
                sep.update_label()
                raise_frame(sep)
            play("wow")

        except IntegrityError as e:
            print("Got this error while adding users to DB: " + str(e))
            self.err.configure(text="Email is already in use", fg="red")
            play("err")

        except AttributeError as e:
            print("Got this error while adding users to DB: " + str(e))
            self.err.configure(text="Enter name, email and posting address to proceed", fg="red")
            play("err")

        except Exception as e:
            print("Got this error while adding users to DB: " + str(e))
            self.err.configure(text="An unexpected issue occurred while adding the user", fg="red")
            play("err")


class ImportParticipants(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)
        Label(self, text="To import participants successfully, use the following format:\n\n"
                         ".csv or .txt files: name, email, house number or name, postcode\n"
                         "Note: avoid including commas at the end of lines for best performance\n\n"
                         "SQLite .db files: create a table with columns in same order as above\n"
                         "Note: unique email addresses are necessary for the app to work")\
            .pack(side=TOP, fill=X)
        example = Label(self, text="See example.txt", fg="blue", cursor="hand2")
        example.pack(side=TOP, fill=X)
        example.bind("<Button-1>", self.see_example)
        lbl2 = Label(self)
        lbl2.pack(side=TOP, fill=X, expand=TRUE)
        f = Frame(self)
        f.pack(side=BOTTOM, fill=X, expand=TRUE, anchor=S)
        Label(f, text="Enter the file name: ").pack(side=LEFT, anchor=W, fill=X)
        self.e = Entry(f)
        self.e.pack(side=LEFT, anchor=W, padx=5, fill=X, expand=TRUE)
        self.btn = Button(f, text="Import", command=lambda: self.imp(lbl2), width=10)
        self.btn.pack(anchor=E)

    @staticmethod
    def see_example(event):
        open_new(path.join(getcwd(), "example.txt"))

    def imp(self, a):
        file_path = path.join(getcwd(), str(self.e.get()))
        if not path.exists(file_path):
            a.configure(text="File cannot be found!\nImport the file and try again.", fg="red")
            play("err")
        else:
            # Getting all users
            file = open(file_path, "r")
            users = []
            for l in file:
                users.append(l)
                print("User %s found" % l)

            if len(users) < 5:
                a.configure(text="File contains less than 5 participants!\n"
                                 "Ensure the file is correctly formatted and try again", fg="red")
                play("err")
            else:
                # Sanitizing the input
                pattern = '[a-zA-Z@\.0-9/: ]'
                san_users = []
                db.reset_records()
                for u in users:
                    ls = u.split(",")
                    usr = []
                    for each in ls:
                        usr.append(''.join(re.findall(pattern, each)).strip())
                    print("Sanitised user is %s" % str(usr))
                    if len(usr) == 4:
                        db.add_user(usr[0], usr[1], usr[2], usr[3], None)
                    elif len(usr) == 5:
                        db.add_user(usr[0], usr[1], usr[2], usr[3], usr[4])
                    else:
                        a.configure(text="File cannot be found!\nImport the file and try again.")
                        print("Error encountered! User does not have the expected values.")
                    san_users.append(usr)
                sep.update_label()
                raise_frame(sep)


class Navigation(Frame):

    def __init__(self, master):
        Frame.__init__(self, master, bd=1, relief=RAISED)
        self.grid(sticky=NSEW)
        btn = Button(self, text="Home", command=lambda: self.home(), width=10)
        btn1 = Button(self, text="Exit", command=lambda: self.close(), width=10)
        btn2 = Button(self, text="Reset DB", command=lambda: self.clear_db(), width=10)
        for i in (btn, btn1, btn2):
            i.pack(side=LEFT, anchor=W, pady=5, padx=5)
        Label(self, text="v1.0 Yordan Angelov Copyright 2018").pack(side=RIGHT, padx=5)

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

    # The event value is used. The function doesn't work otherwise
    @staticmethod
    def go_to_repo(event):
        open_new(r"https://github.com/n4ught1us-max1mus/secret-santa")


class SendEmailsPage(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW, padx=5, pady=5)
        self.part = len(db.fetch_participants())
        self.lbl = Label(self)
        self.lbl.pack(fill=BOTH, expand=TRUE)
        self.lb1 = Listbox(self)
        self.lb1.pack(fill=BOTH, expand=TRUE, pady=5)
        self.update_label()
        self.pairs = {}
        self.btn = Button(self, text="Pair participants", command=lambda: self.randomise_santas())
        self.btn.pack(anchor=SE)

    def randomise_santas(self):
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

            # Allocating a giftee, provided there are giftees to be allocated
            if len(users) > 0:
                self.pairs[u] = choice(users)

        self.lbl.configure(text="Pairs have been assigned!\nDo you want to send out emails?")
        self.btn.configure(text="Send emails", command=lambda: self.send_emails(self.pairs))
        self.btn.pack(anchor=SE)

    def update_label(self):
        users = db.fetch_participants()
        self.part = len(users)
        self.lbl.configure(text="There are %s participants in the database" % str(self.part))
        self.lb1.delete(0, END)
        for u in users:
            self.lb1.insert(users.index(u), "%s, %s" % (u[1], u[2]))

    def send_emails(self, pairs: dict):
        self.lbl.configure(text="Sending emails...")
        print("Starting the emails sending sequence...")
        username = "ten10secretsanta@gmail.com"
        password = "jkvryxsvsnrkioww"
        try:
            print("Connecting to server...")
            server = SMTP("smtp.gmail.com", 587)
            print("Starting TLS...")
            server.starttls()
            print("Logging in...")
            server.login(username, password)

            for k, v in pairs.items():
                headers = ("From: %s\n"
                           "To: %s\n"
                           "Subject: You have a new Secret Santa pair!\n\n"
                           % (str(k[2]), str(v[2])))
                if v[5] is not None:
                    body = ("Hi %s,\n\nYou are the Secret Santa for %s!\n"
                            "Choose your gift and send it off to %s, %s.\n\n"
                            "If you're seeking inspiration, take a look at "
                            "their wishlist: %s\n\n"
                            "Happy holidays!"
                            % (str(k[1]), str(v[1]), str(v[3]), str(v[4]), str(v[5])))
                else:
                    body = ("Hi %s,\n\nYou are the Secret Santa for %s!\n"
                            "Choose your gift and send it off to %s, %s.\n\n"
                            "Happy holidays!"
                            % (str(k[1]), str(v[1]), str(v[3]), str(v[4])))
                try:
                    print("Sending email...")
                    server.sendmail(username, "y_angelov@hotmail.com", headers + body)
                    print("Email sent!")
                except Exception as e:
                    print("Got this error while trying to send out emails: " + str(e))

            server.quit()
            self.lbl.configure(text="Emails sent!\n"
                                    "Get back to work now, we're not paying you to mess around!\n\n"
                                    "Use the button below to be redirected to the Feedback page.\n")
            self.btn.configure(text="Leave feedback", command=lambda: raise_frame(lf))

        except Exception as e:
            print("Got the error: " + str(e))
            self.lbl.configure(text="Issue encountered while sending emails!")


if __name__ == '__main__':

    root = Tk()
    root.title("Secret Santa")
    # Works on Windows 10
    # Only works with .ico files
    root.resizable(width=False, height=False)
    if "Windows" in platform():
        root.iconbitmap("santa.ico")

    # Starting up SQLite
    db = SQL()

    # Creating and positioning the pages
    s = StartPage(root)
    hmp = HowManyParticipants(root)
    ep = EnterParticipants(root)
    ip = ImportParticipants(root)
    lf = LeaveFeedback(root)
    sep = SendEmailsPage(root)
    for frame in (s, ep, ip, hmp, lf, sep):
        frame.grid(row=0, column=0, sticky='news', padx=5, pady=5)

    nav = Navigation(root)
    nav.grid(row=1, column=0, sticky='news')

    raise_frame(s)

    root.mainloop()
