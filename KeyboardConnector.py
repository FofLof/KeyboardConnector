import string

from networktables import NetworkTables
import tkinter
import customtkinter
from tkinter import *
from networktables import NetworkTablesInstance
from pynput import keyboard

ntInstance = NetworkTablesInstance.getDefault()

commandsReceived = False
addedCommands = False
receivedCommands = []
released = False
hasClearedTables = False

characters = list(string.__all__)


# list(string.ascii_uppercase, string.digits)
nt = ntInstance.getTable("Keyboard")


def on_press(key):
    global released
    print(format(key).upper())
    if (released == False):
        nt.getEntry(format(key).upper()[1]).setBoolean(not nt.getEntry(format(key).upper()[1]).getBoolean(False))
        released = True


def on_release(key):
    global released
    released = False
    pass


def task():
    global receivedCommands
    global addedCommands
    # print(NetworkTables.isConnected())
    if not NetworkTables.isConnected():
        connectedLabel.configure(text="Connecting...")
        connectedLabel.place(relx=0.5, rely=0.05, anchor=tkinter.N)
        receivedCommands = []
        textbox.configure(state="normal")
        textbox.delete('1.0', "end")
        addedCommands = False
        global hasClearedTables
        hasClearedTables = False
        if len(ipEntry.get()) >= 9: #and (
                #ipEntry.get() == "127.0.0.1" or ("10." in ipEntry.get() and ".2" in ipEntry.get())):
            NetworkTables.initialize(server=ipEntry.get())
    else:
        getCommandList()

        if not hasClearedTables:
            for x in characters:
                nt.getEntry(str(x)).delete()
            hasClearedTables = TRUE
        # connectedLabel.configure(master= customtkinter.CTk,
        #                          text="Connecting...",
        #            aaaaaabbba              font=("Exo", 60))
        connectedLabel.configure(text="Connected-Commands found")
        connectedLabel.place(relx=0.5, rely=0.05, anchor=tkinter.N)
        if not len(receivedCommands) == 0 and not addedCommands:
            for x in range(len(receivedCommands)):
                textbox.insert(END, receivedCommands[x] + '\n')
            addedCommands = True
            textbox.configure(state="disabled")
            listener = keyboard.Listener(
                on_press=on_press,
                on_release=on_release)
            listener.start()

    app.after(20, task)


def getCommandList():
    global commandsReceived
    global receivedCommands
    if not commandsReceived or len(receivedCommands) == 0:
        receivedCommands = ntInstance.getTable('SmartDashboard').getSubTable('Commands').getStringArray(
            'ListOfCommands', [])
        commandsReceived = True


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        global characters
        global numbers
        for x in range(10):
            characters.append(x)
        photo = PhotoImage(file="teamLogo.png")
        self.title("Keyboard Connector")
        self.iconphoto(False, photo)
        self.minsize(400, 360)
        self.maxsize(400, 360)
        customtkinter.set_appearance_mode("dark")

        global connectedLabel
        connectedLabel = customtkinter.CTkLabel(master=self, text="Connected!", font=("Exo", 30))

        global textbox
        textbox = customtkinter.CTkTextbox(self)
        textbox.grid(row=0, column=0, padx=(100, 0), pady=(60, 0))
        textbox.configure(state = NORMAL)


        global ipEntry
        ipEntry = customtkinter.CTkEntry(master=self, placeholder_text="Enter IP:")
        ipEntry.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        ipLabel = customtkinter.CTkLabel(master=self, text="Sim IP = 127.0.0.1, Real IP = 10.XX.XX.2", font=("Exo", 20))
        ipLabel.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = App()
    app.after(20, task)
    app.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
