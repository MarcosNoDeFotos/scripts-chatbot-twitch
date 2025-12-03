# -*- coding: utf-8 -*-
from time import time
import clr
clr.AddReference("System")
from System.Net import WebClient
from System.Text import Encoding
import json
from time import sleep

ScriptName = "LED Control";
Website = "";
Description = "Los usuarios pueden cambiar el color de los leds";
Creator = "MarcosNoDeFotos";
Version = "1.0.0";


COMANDOS = ["!led", "!leds"]
COOLDOWN = 5*60 #Segundos
# COOLDOWN = 2 #Segundos
RGB_ENDPOINT_COLOR = "http://192.168.1.189:5000/rgb_establecerColor"
STREAMER_NAME = "marcosnodefotos"

lastTimeExecuted = 0

coloresValidos = {
    "azul": "17,0,255",
    "rojo": "255,0,0",
    "verde": "0,255,0",
    "morado": "168,0,146",
    "amarillo" : "214,179",
    "furcia": "230,0,111",
    "blanco": "255,255,255",
    "apagado": "0,0,0",
}

efectosValidos = [
    "static",
    "loop",
    "vuelta",
    "fill",
    "random",
    "destello",
]



def http_post(url, data):
    client = WebClient()
    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded")
    # data debe ser string
    form_data = "&".join([str(k) + "=" + str(v) for k, v in data.items()])
    response = client.UploadString(url, "POST", form_data)
    return response


def enviarColor(color, efecto):
    http_post(RGB_ENDPOINT_COLOR, data={"color": color, "animacion": efecto})


def Init():
    
    return;




def Execute(data):
    if data.GetParam(0) not in COMANDOS:
        return;
    else:
        global lastTimeExecuted
        if data.GetParamCount() == 1 or (data.GetParamCount() == 2 and data.GetParam(1) == "help"):
            Parent.SendStreamMessage("!leds [color] [efecto]: ¡Cambia el color de mi gorro! Efectos válidos: "+(', '.join(efectosValidos))+". Ejemplo: !leds rojo random")     
        elif data.GetParamCount() == 2:
            color = data.GetParam(1)
            efecto = "loop"
            if data.GetParamCount() >= 3:
                if data.GetParam(2) in efectosValidos:
                    efecto = data.GetParam(2)
            if color == "reset" and data.UserName.lower() == STREAMER_NAME.lower():
                lastTimeExecuted = 0
                Parent.SendStreamMessage("👌")
            elif str(color).strip()!="help":
                if lastTimeExecuted == 0 or time()-lastTimeExecuted >= COOLDOWN:
                    lastTimeExecuted = time()
                    if color in coloresValidos.keys():
                        enviarColor(coloresValidos[color], efecto); 
                        Parent.SendStreamMessage(data.UserName+" ha cambiado el color de mi gorro!!!")
                    if color == "multicolor":
                        enviarColor("", "multicolor")
                        Parent.SendStreamMessage(data.UserName+" ha cambiado el color de mi gorro!!!")
                else:
                    Parent.SendStreamMessage("Que me vas a fundir las luces!! Espérate un ratico ("+str(int(COOLDOWN-(time()-lastTimeExecuted)))+"s)")
    return;

def Tick():
    return;


