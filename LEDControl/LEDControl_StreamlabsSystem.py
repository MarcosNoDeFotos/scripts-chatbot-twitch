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
RGB_ENDPOINT_ANIMACION = "http://192.168.1.189:5000/rgb_establecerAnimacion"

lastTimeExecuted = 0

coloresValidos = {
    "azul": "17,0,255",
    "rojo": "255,0,0",
    "verde": "0,255,0",
    "morado": "168,0,146",
    "amarillo" : "214,179",
    "furcia": "230,0,111",
    "rainbow": "0,0,0",
    "blanco": "255,255,255",
    "apagado": "0,0,0",
}


def http_post(url, data):
    client = WebClient()
    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded")
    # data debe ser string
    form_data = "&".join([str(k) + "=" + str(v) for k, v in data.items()])
    response = client.UploadString(url, "POST", form_data)
    return response


def enviarColor(color, efecto):
    http_post(RGB_ENDPOINT_COLOR, data={"color": color})
    sleep(2)
    http_post(RGB_ENDPOINT_ANIMACION, data={"animacion": efecto})


def Init():
    
    return;




def Execute(data):
    if data.GetParam(0) not in COMANDOS:
        return;
    else:
        global lastTimeExecuted
        if data.GetParamCount() == 1 or (data.GetParamCount() == 2 and data.GetParam(1) == "help"):
            Parent.SendStreamMessage("!leds [color]: ¡Usa este comando para cambiar el color de mi gorro! Colores disponibles: "+(', '.join(coloresValidos.keys())))     
        elif data.GetParamCount() == 2:
            color = data.GetParam(1)
            efecto = "loop"
            if str(color).strip()!="help":
                if lastTimeExecuted == 0 or time()-lastTimeExecuted >= COOLDOWN:
                    lastTimeExecuted = time()
                    colorEsHexa = True
                    try:
                        int(color[1:], 16);
                    except:
                        colorEsHexa = False
                    if color in coloresValidos.keys():
                        if color == "rainbow":
                            enviarColor("0,0,0", "rgbLoco"); 
                        else:
                            enviarColor(coloresValidos[color], efecto); 
                        Parent.SendStreamMessage(data.UserName+" ha cambiado el color de mi gorro!!!")
                    # elif (str(color).__len__()==7 and str(color)[0:1] == "#" and colorEsHexa):
                    #     enviarColor(coloresValidos[color]); 
                    #     bot.send_stream_message(author+" ha cambiado el color de mi gorro!!!")

                else:
                    Parent.SendStreamMessage("Que me vas a fundir las luces!! Espérate un ratico ("+str(int(COOLDOWN-(time()-lastTimeExecuted)))+"s)")
    return;

def Tick():
    return;


