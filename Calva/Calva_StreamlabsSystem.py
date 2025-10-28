# -*- coding: utf-8 -*-
import os
ScriptName = "Besos Calva";
Website = "";
Description = "Cuenta los besos en la calva que llevo";
Creator = "MarcosNoDeFotos";
Version = "1.0.0";

COMANDO = "!calva";
CURRENT_PATH = os.path.dirname(__file__).replace("\\", "/") + "/"
FILE_PATH = CURRENT_PATH+"besos.txt"


def Init():
    return;

def Execute(data):
    if data.GetParam(0) != COMANDO:
        return;
    besos = 0
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            f.write("1")
            f.close()
        besos = 1
    else:
        with open(FILE_PATH, "r+") as f:
            besos = int(f.read().strip())+1
            f.seek(0)
            f.write(str(besos))
            f.truncate()
            f.close()
    Parent.SendStreamMessage(data.UserName+" me ha dado un beso en la calva. Ya llevo "+str(besos)+" besos");
    return;

def Tick():
    return;
