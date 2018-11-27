from tkinter import *
from os import path, getcwd

from sql import SQL


def raise_frame(frame: Frame):
    frame.tkraise()


class StartPage(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)
        lbl = Label(self, text="Welcome to the Yordan's Secret Santa app!\nWhat do you want to do today?")
        lbl.pack(fill=BOTH, expand=TRUE)
        opt = IntVar()
        r1 = Radiobutton(self, text="Add participants manually", variable=opt, value=1)
        r1.pack(anchor=W)
        r2 = Radiobutton(self, text="Import participants from a txt file", variable=opt, value=2)
        r2.pack(anchor=W)
        r3 = Radiobutton(self, text="Leave feedback", variable=opt, value=3)
        r3.pack(anchor=W)
        btn = Button(self, text="Continue", command=lambda: self.command(opt), width=10)
        btn.pack(side=BOTTOM, anchor=E, pady=5, padx=5)

    def command(self, i):
        print("option selected is " + str(i.get()))
        if i.get() == 1:
            raise_frame(hmp)

        elif i.get() == 2:
            raise_frame(ip)

        elif i.get() == 3:
            # TODO Open feedback page and send email to myself
            raise_frame(wip)

        else:
            print("The option is " + i.get())


class HowManyParticipants(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW, padx=5, pady=5)
        Label(self, text="How many participants do you want to enter?").grid(row=0, sticky=NS)
        Label(self, text="Enter number here:").grid(row=1, column=0, sticky=W)
        # TODO Check if file already exists and, if it does, ask whether to use or delete
        self.lbl = Label(self)
        self.lbl.grid(row=2, column=0, sticky=W)
        p = Entry(self)
        p.grid(row=1, column=1, sticky=E)
        btn = Button(self, text="Continue", command=lambda: self.command(p), width=10)
        btn.grid(row=3, column=1, sticky=SE)

    def command(self, i):
        print("The user inputted %s" % str(i.get()))
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
        self.grid(sticky=NSEW)
        # Make below say: You have enter X participants so far
        self.exp_part = 0
        self.ent_part = 0
        Label(self, text="Expecting " + str(self.exp_part) + " more participants")
        self.exp = Label(self, text="You have entered %s out of %s participants" % (self.exp_part, self.ent_part))
        self.exp.grid(row=0, column=0, columnspan=3)
        self.err = Label(self)
        self.err.grid(row=1, column=0, columnspan=3)
        Label(self, text="Enter the participant’s details:").grid(row=2, column=0, columnspan=3)
        Label(self, text="Name: ").grid(row=4, column=0, sticky=W, padx=5)
        self.name = Entry(self)
        self.name.grid(row=4, column=1, columnspan=2, sticky=NSEW, padx=5)
        Label(self, text="Email: ").grid(row=5, column=0, sticky=W, padx=5)
        self.email = Entry(self)
        self.email.grid(row=5, column=1, columnspan=2, sticky=NSEW, padx=5)
        Label(self, text="Address number: ").grid(row=6, column=0, sticky=W, padx=5)
        self.house = Entry(self)
        self.house.grid(row=6, column=1, sticky=NSEW, padx=5)
        Label(self, text="Postcode: ").grid(row=7, column=0, sticky=W, padx=5)
        self.post = Entry(self)
        self.post.grid(row=7, column=1, sticky=NSEW, padx=5)
        btn = Button(self, text="Continue", command=lambda: self.add_user(self.name, self.email, self.house, self.post), width=10)
        btn.grid(row=8, column=2, sticky=E, padx=5, pady=5)

    def update_bar_re_adding_user(self):
        self.err.configure(text="User added!")
        self.ent_part = self.ent_part + 1
        self.exp.configure(text="You have entered %s out of %s participants" % (self.ent_part, self.exp_part))

    def clear_text(self):
        self.name.delete(0, 'end')
        self.email.delete(0, 'end')
        self.house.delete(0, 'end')
        self.post.delete(0, 'end')

    def add_user(self, name, email, house, postcode):
        try:
            print("Adding user " + name.get())
            db.add_user(name.get(), email.get(), house.get(), postcode.get())
            self.clear_text()
            self.update_bar_re_adding_user()

        except Exception as e:
            print("The error is: " + str(e))
            self.err.configure(text="There was an error while adding the user. Try again!")



class ImportParticipants(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)
        Label(self, text="To import participants, please put the file in the same directory as the app.")\
            .pack(fill=X)
        lbl = Label(self, text="")
        lbl.pack(fill=X, expand=TRUE)
        Label(self, text="Enter the file name: ").pack(side=LEFT, fill=BOTH, expand=TRUE)
        e = Entry(self)
        e.pack(side=LEFT, pady=5, padx=5, expand=TRUE, fill=X)
        btn = Button(self, text="Continue", command=lambda: self.command(e, lbl), width=10)
        btn.pack(side=BOTTOM, anchor=E, pady=5, padx=5)

    def command(self, i, a):
        file_path = path.join(getcwd(), str(i.get()))
        if not path.exists(file_path):
            a.configure(text="File cannot be found!\nImport the file and try again.")
        else:
            a.configure(text="File found!")


class Navigation(Frame):

    def __init__(self, master):
        Frame.__init__(self, master, bd=1, relief=RAISED)
        self.grid(sticky=NSEW)
        btn = Button(self, text="Home", command=lambda: self.home(), width=10)
        btn.pack(side=LEFT, anchor=E, pady=5, padx=5)
        btn = Button(self, text="Exit", command=lambda: self.close(), width=10)
        btn.pack(side=LEFT, anchor=E, pady=5, padx=5)
        Label(self, text="v0.1 Yordan Angelov Copyright 2018").pack(side=RIGHT, padx=5)

    def home(self):
        raise_frame(s)

    def close(self):
        # db.close()
        exit()


class WorkInProgress(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)
        Label(self, text="SYCHE! YOU THOUGHT IT WAS COMPLETED!").pack(fill=BOTH, expand=TRUE)


if __name__ == '__main__':

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
    wip = WorkInProgress(root)
    nav = Navigation(root)

    num_of_part = 0

    for frame in (s, ep, ip, hmp, wip):
        frame.grid(row=0, column=0, sticky='news')

    nav.grid(row=1, column=0, sticky='news')

    raise_frame(s)

    root.mainloop()
