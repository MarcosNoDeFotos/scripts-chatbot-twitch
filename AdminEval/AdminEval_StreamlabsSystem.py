# -*- coding: utf-8 -*-
ScriptName = "Admin Eval"
Website = ""
Description = "Ejecuta python en tiempo real desde el chat"
Creator = "MarcosNoDeFotos"
Version = "1.0.1"

COMANDOS = ["!eval"]


def Execute(data):
    if str(data.GetParam(0)) not in COMANDOS or data.UserName != "marcosnodefotos" and data.IsBroadcaster():
        return
    
    try:
        exec(str(data.Message).replace(COMANDOS[0], "").strip())
        Parent.SendStreamMessage("👌")
    except Exception as e:
        Parent.SendStreamMessage("👎")
        print(e)
        
    
    return
def Init():
    return

def Tick():
    return