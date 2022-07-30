from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext
from datetime import datetime
def convMOD():
    blankString = ""
    openedFilename = filedialog.askopenfilename(filetypes=['"ProTracker" {.mod}'])
    if openedFilename == "":
        return 0
    modName = nameObject.get("1.0", "end")
    modArtist = artistObject.get("1.0", "end")
    modComment = commentObject.get("1.0", "end")
    modTempo = tempoObject.get()
    modVolume = volumeObject.get()
    newModFile = filedialog.asksaveasfile(mode='wb',defaultextension='pt36',filetypes=['"ProTracker IFF" {.pt36}'])
    with open(openedFilename, "rb") as openedFile:
        oldModFile = openedFile.read()
        oldModSize = openedFile.tell()
        openedFile.seek(950)
        numOrders = int.from_bytes(openedFile.read(1), byteorder='big')
        openedFile.seek(952)
        numPtrns = 0
        for i in range(127):
            patternNumber = int.from_bytes(openedFile.read(1), byteorder='big')
            if patternNumber > numPtrns:
                numPtrns = patternNumber + 1
    numPtrns = numPtrns + 1
    newModFile.write(b"\x46\x4F\x52\x4D\x43\x4D\x4E\x54\x4D\x4F\x44\x4C\x56\x45\x52\x53")
    newModFile.write(b"\x00\x00\x00\x16\x00\x00\x00\x00\x49\x46\x46\x4D\x4F\x44\x49\x4E")
    newModFile.write(b"\x46\x4F\x00\x00\x00\x48")
    newModFile.write(bytes(modName.ljust(32), encoding="utf-8"))
    newModFile.write(b"\x00\x1F")
    ordrs = int(numOrders).to_bytes(2, byteorder='big')
    newModFile.write(bytes(ordrs))
    ptrns = int(numPtrns).to_bytes(2, byteorder='big')
    newModFile.write(bytes(ptrns))
    volume = int(modVolume).to_bytes(2, byteorder='big')
    tempo = int(modTempo).to_bytes(2, byteorder='big')
    newModFile.write(bytes(volume))
    newModFile.write(bytes(tempo))
    newModFile.write(b"\x81\x00")
    day = int(datetime.utcnow().day).to_bytes(2, byteorder='big')
    mon = int(datetime.utcnow().month).to_bytes(2, byteorder='big')
    yr = int(datetime.utcnow().year - 1900).to_bytes(2, byteorder='big')
    hour = int(datetime.utcnow().hour).to_bytes(2, byteorder='big')
    minute = int(datetime.utcnow().minute).to_bytes(2, byteorder='big')
    sec = int(datetime.utcnow().second).to_bytes(2, byteorder='big')
    newModFile.write(bytes(day))
    newModFile.write(bytes(mon))
    newModFile.write(bytes(yr))
    newModFile.write(bytes(hour))
    newModFile.write(bytes(minute))
    newModFile.write(bytes(sec))
    newModFile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x43\x4D\x4E\x54")
    commentsTable = []
    for line in modComment.split('\n'):
        commentsTable.append(line.ljust(40))
    newCmnt = blankString.join(commentsTable)
    commentLen = len(newCmnt) + 40
    newModFile.write(commentLen.to_bytes(4, byteorder='big'))
    newModFile.write(bytes(modArtist.ljust(32), encoding="utf-8"))
    newModFile.write(bytes(newCmnt, encoding="utf-8"))
    newModFile.write(b"\x50\x54\x44\x54\x4F\x44\x49\x4E")
    PTDTPosition = newModFile.tell() - 4
    newModFile.write(oldModFile)
    newModSize = newModFile.tell()
    newModFile.seek(PTDTPosition)
    oldModSizeBytes = int(oldModSize + 16).to_bytes(4, byteorder='big')
    newModSizeBytes = int(newModSize + 16).to_bytes(4, byteorder='big')
    newModFile.write(bytes(oldModSizeBytes))
    newModFile.seek(4)
    newModFile.write(bytes(newModSizeBytes))
    newModFile.close()
    messagebox.showinfo(title='Addition complete',message='The extra information has been added to your file.')
mainWindow = Tk()
frm = Frame(mainWindow, padding=10)
frm.grid()
Label(frm, text='IFFMOD beta by RocketeerEatingEggs').grid(column=0, row=0)
Label(frm, text='Song Name').grid(column=0, row=1)
nameObject = Text(frm, width=32, height=1)
nameObject.grid(column=0, row=2)
Label(frm, text='Song Artist').grid(column=1, row=1)
artistObject = Text(frm, width=32, height=1)
artistObject.grid(column=1, row=2)
Label(frm, text='Comment').grid(column=0, row=3)
commentObject = scrolledtext.ScrolledText(frm, width=40, height=20)
commentObject.grid(column=0, row=4)
Button(frm, text='Add info to MOD', command=convMOD).grid(column=0, row=5)
Label(frm, text='Other Settings').grid(column=1, row=3)
otherSettings = Frame(frm, padding=1)
otherSettings.grid(column=1, row=4)
Label(otherSettings, text='Tempo').grid(column=0, row=0)
tempoSpinVal = StringVar()
tempoObject = Spinbox(otherSettings, from_=32, to=255, textvariable=tempoSpinVal)
tempoObject.set(125)
tempoObject.grid(column=1, row=0)
Label(otherSettings, text='Volume').grid(column=0, row=1)
volumeSpinVal = StringVar()
volumeObject = Spinbox(otherSettings, from_=0, to=64, textvariable=volumeSpinVal)
volumeObject.set(64)
volumeObject.grid(column=1, row=1)
mainWindow.mainloop()
