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
            raise_frame(wip)

        elif i.get() == 2:
            raise_frame(ip)

        elif i.get() == 3:
            # TODO Open feedback page and send email to myself
            raise_frame(wip)

        else:
            print("The option is " + i.get())

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
        Label(self, text="v0.1 Yordan Angelov © Copyright 2018").pack(side=RIGHT, padx=5)

    def home(self):
        raise_frame(s)

    def close(self):
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
    root.iconbitmap("santa.ico")
    root.resizable(width=False, height=False)

    s = StartPage(root)
    ip = ImportParticipants(root)
    wip = WorkInProgress(root)
    nav = Navigation(root)

    for frame in (s, ip, wip):
        frame.grid(row=0, column=0, sticky='news')

    nav.grid(row=1, column=0, sticky='news')

    raise_frame(s)

    root.mainloop()
