import tkinter as tk
import tkinter.font as tkFont
import steamstore
import steamstoreGmail

class App:
    def __init__(self, root):
        #setting title
        self.GLabel_567 = None
        root.title("undefined")
        #setting window size
        width=574
        height=267
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GCheckBox_571=tk.Checkbutton(root,variable=var)
        GCheckBox_571["bg"] = "#ef8888"
        ft = tkFont.Font(family='Times',size=10)
        GCheckBox_571["font"] = ft
        GCheckBox_571["fg"] = "#333333"
        GCheckBox_571["justify"] = "center"
        GCheckBox_571["text"] = "NSFW Content"
        GCheckBox_571.place(x=40,y=90,width=153,height=38)
        GCheckBox_571["offvalue"] = "0"
        GCheckBox_571["onvalue"] = "1"
        GCheckBox_571["command"] = self.GCheckBox_571_command


        GLabel_612=tk.Label(root)
        GLabel_612["bg"] = "#f99b0c"
        ft = tkFont.Font(family='Times',size=18)
        GLabel_612["font"] = ft
        GLabel_612["fg"] = "#333333"
        GLabel_612["justify"] = "center"
        GLabel_612["text"] = "Extract Data"
        GLabel_612.place(x=40,y=40,width=155,height=30)

        GButton_61=tk.Button(root)
        GButton_61["bg"] = "#2cff15"
        ft = tkFont.Font(family='Times',size=10)
        GButton_61["font"] = ft
        GButton_61["fg"] = "#000000"
        GButton_61["justify"] = "center"
        GButton_61["text"] = "start extraction"
        GButton_61.place(x=60,y=160,width=107,height=50)
        GButton_61["command"] = self.GButton_61_command

        GLabel_276=tk.Label(root)
        GLabel_276["bg"] = "#1768f2"
        ft = tkFont.Font(family='Times',size=18)
        GLabel_276["font"] = ft
        GLabel_276["fg"] = "#f9f9f8"
        GLabel_276["justify"] = "center"
        GLabel_276["text"] = "Email"
        GLabel_276.place(x=340,y=40,width=155,height=30)

        GButton_780=tk.Button(root)
        GButton_780["bg"] = "#4cff0b"
        ft = tkFont.Font(family='Times',size=10)
        GButton_780["font"] = ft
        GButton_780["fg"] = "#000000"
        GButton_780["justify"] = "center"
        GButton_780["text"] = "Schedual Email"
        GButton_780["relief"] = "groove"
        GButton_780.place(x=360,y=110,width=107,height=50)
        GButton_780["command"] = self.GButton_780_command

        GButton_96 = tk.Button(root)
        GButton_96["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_96["font"] = ft
        GButton_96["fg"] = "#000000"
        GButton_96["justify"] = "center"
        GButton_96["text"] = "clear"
        GButton_96.place(x=470, y=220, width=70, height=25)
        GButton_96["command"] = self.GButton_96_command

        GLabel_567 = tk.Label(root)
        GLabel_567["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=10)
        GLabel_567["font"] = ft
        GLabel_567["fg"] = "#333333"
        GLabel_567["justify"] = "center"
        GLabel_567["text"] = "message"
        GLabel_567.place(x=240, y=150, width=311, height=61)

    def GCheckBox_571_command(self):
        print("command")
        status = var.get()
        if status == 1:
            global NSFWGLOBALFLAG
            NSFWGLOBALFLAG = True
        else:
            NSFWGLOBALFLAG = False

    def GButton_61_command(self):
        steamstore.startscraper(NSFWGLOBALFLAG)

    def printmessage(self,str):
        self.GLabel_567["text"]=str

    def GButton_780_command(self):
        steamstoreGmail.readcsvandschedualemail()

    def GButton_96_command(self):
        print("command")


if __name__ == "__main__":
    NSFWGLOBALFLAG = False
    root = tk.Tk()
    var = tk.IntVar()
    app = App(root)
    root.mainloop()
