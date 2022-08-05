import sys
blankString = ""
openedFilename = sys.argv[1]
if openedFilename != "":
    newFilename = sys.argv[2]
    if newFilename != "":
        with open(openedFilename, "rb") as openedFile:
            with open(newFilename, "wb") as newModFile:
                openedFile.seek(8)
                if str(openedFile.read(4), encoding="iso-8859-1") == "MODL":
                    if str(openedFile.read(4), encoding="iso-8859-1") == "VERS":
                        openedFile.seek(14, 1)
                        if str(openedFile.read(4), encoding="iso-8859-1") == "INFO":
                            openedFile.seek(68, 1)
                            if str(openedFile.read(4), encoding="iso-8859-1") == "CMNT":
                                lenCMNT = int.from_bytes(openedFile.read(4), byteorder='big')
                                openedFile.seek(lenCMNT - 8, 1)
                                if str(openedFile.read(4), encoding="iso-8859-1") == "PTDT":
                                    openedFile.seek(4, 1)
                                    newModFile.write(openedFile.read())
                                    print('The information has been stripped from your file.')
                                else: print('PTDT')
                            else: print('CMNT')
                        else: print('INFO')
                    else: print('VERS')
                else: print('MODL')
