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
        r3 = Radiobutton(self, text="Exit", variable=opt, value=3)
        r3.pack(anchor=W)
        btn = Button(self, text="Continue", command=lambda: command(opt), width=10)
        btn.pack(side=BOTTOM, anchor=E, pady=5, padx=5)


class ImportParticipants(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)
        Label(self, text="To import participants, please put the file in the same directory as the app.")\
            .pack(fill=X, expand=TRUE)
        Label(self, text="Enter the file name: ").pack(side=LEFT, fill=BOTH, expand=TRUE)
        e = Entry(self)
        e.pack(side=LEFT, pady=5, padx=5, expand=TRUE, fill=X)
        btn = Button(self, text="Continue", command=lambda: command(e), width=10)
        btn.pack(side=BOTTOM, anchor=E, pady=5, padx=5)


class WorkInProgress(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)
        Label(self, text="SYCHE! YOU THOUGHT IT WAS COMPLETED!").pack(fill=BOTH, expand=TRUE)


if __name__ == '__main__':
    def raise_frame(frame):
        frame.tkraise()

    def command(i):
        print("option selected is " + str(i.get()))
        if i.get() == 1:
            raise_frame(wip)

        elif i.get() == 2:
            raise_frame(ip)

        elif i.get() == 3:
            exit()

        else:
            print("The option is " + i.get())

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

    for frame in (s, ip, wip):
        frame.grid(row=0, column=0, sticky='news')

    # Button(f1, text='Go to frame 2', command=lambda: raise_frame(f2)).pack()
    # Label(f1, text='FRAME 1').pack()
    #
    # Label(f2, text='FRAME 2').pack()
    # Button(f2, text='Go to frame 3', command=lambda: raise_frame(f3)).pack()
    #
    # Label(f3, text='FRAME 3').pack()
    # Button(f3, text='Go to frame 4', command=lambda: raise_frame(f4)).pack()
    #
    # Label(f4, text='FRAME 4').pack()
    # Button(f4, text='Goto to frame 1', command=lambda: raise_frame(s)).pack()

    raise_frame(s)

    root.mainloop()
