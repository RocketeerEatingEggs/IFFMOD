from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext
from datetime import datetime
def convMOD():
    blankString = ""
    openedFilename = filedialog.askopenfilename(filetypes=['"ProTracker and compatible" {.mod}'])
    if openedFilename == "":
        return 0
    modName = nameObject.get("1.0", "end").strip("\x0A")
    modArtist = artistObject.get("1.0", "end").strip("\x0A")
    modComment = commentObject.get("1.0", "end")
    modTempo = tempoObject.get()
    modVolume = volumeObject.get()
    useVBlank = vBlankCheckVal.get()
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
    newModFile.write(bytes(modName.ljust(32, "\x00"), encoding="iso-8859-1"))
    newModFile.write(b"\x00\x1F")
    ordrs = int(numOrders).to_bytes(2, byteorder='big')
    newModFile.write(bytes(ordrs))
    ptrns = int(numPtrns).to_bytes(2, byteorder='big')
    newModFile.write(bytes(ptrns))
    volume = int(modVolume).to_bytes(2, byteorder='big')
    tempo = int(modTempo).to_bytes(2, byteorder='big')
    newModFile.write(bytes(volume))
    newModFile.write(bytes(tempo))
    flags = int(128)
    if useVBlank == 0:
        flags = flags + 1
    newModFile.write(flags.to_bytes(2, byteorder='little'))
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
        commentsTable.append(line.ljust(40, "\x00"))
    newCmnt = blankString.join(commentsTable)
    commentLen = len(newCmnt) + 40
    newModFile.write(commentLen.to_bytes(4, byteorder='big'))
    newModFile.write(bytes(modArtist.ljust(32, "\x00"), encoding="iso-8859-1"))
    newModFile.write(bytes(newCmnt, encoding="iso-8859-1"))
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
frm = Frame(mainWindow, padding=4)
frm.grid()
Label(frm, text='Song Name').grid(column=0, row=0, sticky="e")
nameObject = Text(frm, width=32, height=1)
nameObject.grid(column=1, row=0, sticky="w")
Label(frm, text='Song Artist').grid(column=0, row=1, sticky="e")
artistObject = Text(frm, width=32, height=1)
artistObject.grid(column=1, row=1, sticky="w")
Label(frm, text='Comment').grid(column=0, row=2, sticky="ne")
commentObject = scrolledtext.ScrolledText(frm, width=40, height=16)
commentObject.grid(column=1, row=2, sticky="w")
Label(frm, text='Tempo').grid(column=0, row=3, sticky="e")
Label(frm, text='(125 is required for most old MODs)').grid(column=1, row=3, sticky="e")
tempoSpinVal = StringVar()
tempoObject = Spinbox(frm, from_=32, to=255, textvariable=tempoSpinVal)
tempoObject.set(125)
tempoObject.grid(column=1, row=3, sticky="w")
Label(frm, text='Volume').grid(column=0, row=4, sticky="e")
Label(frm, text='(64 is okay for most 4-channel MODs)').grid(column=1, row=4, sticky="e")
volumeSpinVal = StringVar()
volumeObject = Spinbox(frm, from_=0, to=64, textvariable=volumeSpinVal)
volumeObject.set(48)
volumeObject.grid(column=1, row=4, sticky="w")
frm.option_add('*tearOff', FALSE)
mainWindow.title("IFFMOD")
mainWindow.resizable(FALSE,FALSE)
def about():
    aboutWindow = Toplevel(mainWindow)
    aboutWindow.resizable(FALSE,FALSE)
    Label(aboutWindow, text='IFFMOD, created by RocketeerEatingEggs').grid(column=0, row=0, sticky="w")
    Label(aboutWindow, text='7/30-8/2/2022').grid(column=0, row=1, sticky="w")
    Label(aboutWindow, text='Help:').grid(column=0, row=2)
    Label(aboutWindow, text='''The "Song name" field overrides the song name.
If you don\'t want it to be overridden, you should leave it blank.''').grid(column=0, row=3, sticky="w")
    Label(aboutWindow, text='''The "Song artist" field is the artist\'s name.
You can leave it blank if you want.''').grid(column=0, row=4, sticky="w")
    Label(aboutWindow, text='''The "Comments" field should contain the comments.
You can, again, leave it blank if you want.''').grid(column=0, row=5, sticky="w")
    Label(aboutWindow, text='''The "Tempo" field overrides the ProTracker default of 125.
Keep it at 125 if you're adding a header to old NoiseTracker MODs.''').grid(column=0, row=6, sticky="w")
    Label(aboutWindow, text='''The "Volume" field overrides the ProTracker default of 64.
You should change it depending on the number of channels that are played at
one time.''').grid(column=0, row=7, sticky="w")
    Label(aboutWindow, text='''The "Use VBlank" checkbox (in the "Checkboxes" menu) is for adding info to
old MODs only, and shouldn't be used in new music.''').grid(column=0, row=8, sticky="w")
    Label(aboutWindow, text='''When you're finished adding the info, go to the "Add or Remove" menu and
select "Add info..."''').grid(column=0, row=9, sticky="w")
menubar = Menu(mainWindow)
menu_file = Menu(menubar)
vBlankCheckVal = IntVar()
menu_file.add_command(label='Add info...', command=convMOD)
menu_file.add_checkbutton(label='Use VBlank', variable=vBlankCheckVal, onvalue=1, offvalue=0)
menu_file.add_command(label='About and Help...', command=about)
def stripHeader():
    blankString = ""
    openedFilename = filedialog.askopenfilename(filetypes=['"ProTracker IFF" {.pt36}'])
    if openedFilename == "":
        return 0
    newModFile = filedialog.asksaveasfile(mode='wb',defaultextension='mod',filetypes=['"ProTracker and compatible" {.mod}'])
    with open(openedFilename, "rb") as openedFile:
        openedFile.seek(8)
        magic = str(openedFile.read(4), encoding="iso-8859-1")
        if magic != "MODL":
            messagebox.showinfo(title='Not a valid file',message='This is not a valid ProTracker IFF file.')
        else:
            if str(openedFile.read(4), encoding="iso-8859-1") != "VERS":
                messagebox.showinfo(title='Not a valid file',message='This file is incorrectly ordered. Chunk should be "VERS".')
                return 0
            openedFile.seek(14, 1)
            if str(openedFile.read(4), encoding="iso-8859-1") != "INFO":
                messagebox.showinfo(title='Not a valid file',message='This file is incorrectly ordered. Chunk should be "INFO".')
                return 0
            openedFile.seek(68, 1)
            if str(openedFile.read(4), encoding="iso-8859-1") != "CMNT":
                messagebox.showinfo(title='Not a valid file',message='This file is incorrectly ordered. Chunk should be "CMNT".')
                return 0
            lenCMNT = int.from_bytes(openedFile.read(4), byteorder='big')
            openedFile.seek(lenCMNT - 8, 1)
            if str(openedFile.read(4), encoding="iso-8859-1") != "PTDT":
                messagebox.showinfo(title='Not a valid file',message='This file is incorrectly ordered. Chunk should be "PTDT".')
                return 0
            openedFile.seek(4, 1)
            newModFile.write(openedFile.read())
            messagebox.showinfo(title='Removal complete',message='The information has been stripped from your file.')
menu_file.add_command(label='Remove info...', command=stripHeader)
menubar.add_cascade(menu=menu_file, label='Menu')
mainWindow['menu'] = menubar
mainWindow.mainloop()
