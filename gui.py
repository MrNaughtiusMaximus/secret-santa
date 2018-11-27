from tkinter import *


class StartPage(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)
        lbl = Label(self, text="Welcome to the Yordan's Secret Santa app!\nWhat do you want to do today?")
        lbl.pack(fill=BOTH, expand=TRUE)
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
        p = Entry(self)
        p.grid(row=1, column=1, sticky=E)
        btn = Button(self, text="Continue", command=lambda: self.command(p), width=10)
        btn.grid(row=3, column=1, sticky=SE)

    def command(self, i):
        print("WIP")


class EnterParticipants(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        # Grid.columnconfigure(self, 0, weight=1)
        # Grid.rowconfigure(self, 0, weight=1)
        # Make below say: You have enter X participants so far
        exp = Label(self, text="").grid(row=0, column=0)
        ent = Label(self, text="You have enter 0 participants so far").grid(row=0, column=0)
        Label(self, text="Enter the participant’s details:").grid(row=0, column=0)
        Label(self, text="Enter the participant’s details:").grid(row=0, column=0)
        lbl = Label(self, text="")
        lbl.grid(row=1, column=0)
        Label(self, text="Name: ").grid(row=2, column=0, sticky=W, padx=5)
        name = Entry(self)
        name.grid(row=2, column=1, columnspan=2, sticky=NSEW, padx=5)
        Label(self, text="Email: ").grid(row=3, column=0, sticky=W, padx=5)
        email = Entry(self)
        email.grid(row=3, column=1, columnspan=2, sticky=NSEW, padx=5)
        Label(self, text="Address number: ").grid(row=4, column=0, sticky=W, padx=5)
        house = Entry(self)
        house.grid(row=4, column=1, sticky=NSEW, padx=5)
        Label(self, text="Postcode: ").grid(row=5, column=0, sticky=W, padx=5)
        post = Entry(self)
        post.grid(row=5, column=1, sticky=NSEW, padx=5)
        btn = Button(self, text="Continue", command=lambda: self.command(e, lbl), width=10)
        btn.grid(row=6, column=2, sticky=E, padx=5, pady=5)

    def write_details(self, name, email, house, postcode):
        file_path = os.path.join(os.getcwd(), "participants.txt")
        file = open(file_path, "a+")
        file.write("\n" + name + ", " + email + ", " + house + ", " + postcode)

    def command(self, i, a):
        import os
        file_path = os.path.join(os.getcwd(), str(i.get()))
        if not os.path.exists(file_path):
            a.configure(text="File cannot be found!\nImport the file and try again.")
        else:
            a.configure(text="File found!")


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
        import os
        file_path = os.path.join(os.getcwd(), str(i.get()))
        if not os.path.exists(file_path):
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
        db.close()
        exit()

class WorkInProgress(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)
        Label(self, text="SYCHE! YOU THOUGHT IT WAS COMPLETED!").pack(fill=BOTH, expand=TRUE)


if __name__ == '__main__':
    def raise_frame(frame):
        frame.tkraise()

    root = Tk()
    opt = IntVar()
    root.title("Secret Santa")
    # TODO Mess with design later
    # root.configure(bg="gray")
    # Only works with .ico files

    # Works on Windows 10
    # root.iconbitmap("santa.ico")
    root.resizable(width=False, height=False)

    s = StartPage(root)
    hmp = HowManyParticipants(root)
    ep = EnterParticipants(root)
    ip = ImportParticipants(root)
    wip = WorkInProgress(root)
    nav = Navigation(root)

    for frame in (s, ep, ip, hmp, wip):
        frame.grid(row=0, column=0, sticky='news')

    nav.grid(row=1, column=0, sticky='news')

    raise_frame(s)

    root.mainloop()
