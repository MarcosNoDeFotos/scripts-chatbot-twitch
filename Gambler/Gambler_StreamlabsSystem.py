# -*- coding: utf-8 -*-
ScriptName = "Apuestas"
Website = ""
Description = "Apuesta monedas para conseguir más y conseguir recompensas"
Creator = "MarcosNoDeFotos"
Version = "1.0.1"



import random
import time
import json
import clr
clr.AddReference("System")
from System.Net import WebClient

MONEDA = "Moneda Calva"
MONEDAS = "Monedas Calvas"
AYUDA = "Usa !gamble [cantidad]: Apuesta tus "+MONEDAS+" en la tragaperras 🎰.Si salen 3 ⭐, la recompensa es x2.5 Si salen 3 emojis iguales, la recompensa es x2. Si salen 2 emojis iguales, la recompensa es x1.5, y si no, perderás. Puedes usar los comandos !gamble, !apuesta o !gmb\nPara consultar tus "+MONEDAS+", usa !monedas"
SERVER_REPRODUCCION_SONIDO = "http://192.168.1.189:5000"
SERVER_CONTROL = "http://192.168.1.188:5000"
COMANDO_CANJEAR = "!canjear"
COMANDOS = ["!gamble", "!apuesta", "!gmb", COMANDO_CANJEAR]
COSTES_CANJEOS = {
    "susto" : 200,
    "destacar" : 500
}
COOLDOWN = 60 *5 # Segundos

slots = ["❤️", "😎", "⭐", "👽"]

ultimo_uso = {}
# random.seed(int(time.time() * 1000) % 1000000)



def http_get(url):
    client = WebClient()
    return client.DownloadString(url)


def reproducirSusto(userId, horaEjecucionComando):
    http_get(SERVER_REPRODUCCION_SONIDO+"/reproducirSonido?identificador=susto")
    ultimo_uso[userId] = horaEjecucionComando
    coste = COSTES_CANJEOS["susto"]
    displayName = Parent.GetDisplayName(userId)
    Parent.RemovePointsAll({userId:coste})
    Parent.SendStreamMessage(displayName+" ha canjeado susto por "+str(coste)+" "+MONEDAS)
    

def destacarMensaje(userId, mensaje, horaEjecucionComando):
    http_get(SERVER_CONTROL+"/destacarMensaje?user="+userId+"&mensaje="+mensaje)
    ultimo_uso[userId] = horaEjecucionComando
    coste = COSTES_CANJEOS["destacar"]
    displayName = Parent.GetDisplayName(userId)
    Parent.RemovePointsAll({userId:coste})
    Parent.SendStreamMessage(displayName+" ha canjeado destacar por "+str(coste)+" "+MONEDAS)





def Execute(data):
    if str(data.GetParam(0)) not in COMANDOS:
        return
    userId = str(data.UserName).lower()
    userDisplayName = Parent.GetDisplayName(userId)
    horaEjecucionComando = time.time()
    diferenciaCooldown = 0
    enCooldown = False
    if userId in ultimo_uso.keys():
        diferenciaCooldown = horaEjecucionComando - ultimo_uso[userId]
        enCooldown = diferenciaCooldown < COOLDOWN
    if str(data.GetParam(0)) == COMANDO_CANJEAR: # El funcionamiento es !canjear [recompensa]
        if data.GetParam(1) and (userId not in ultimo_uso.keys() or not enCooldown):
            canjeo = str(data.GetParam(1)).lower()
            puntos = Parent.GetPoints(userId)
            if COSTES_CANJEOS.keys().__contains__(canjeo):
                if puntos >= COSTES_CANJEOS[canjeo]:
                    if canjeo == "susto":
                        reproducirSusto(userId, horaEjecucionComando)
                    if canjeo == "destacar" and data.GetParamCount() > 2:
                        destacarMensaje(userId, str(data.Message).replace(COMANDO_CANJEAR, "").replace("destacar", "").strip(), horaEjecucionComando)
                else:
                    Parent.SendStreamMessage(userDisplayName+", necesitas "+ str(COSTES_CANJEOS[canjeo])+" "+MONEDAS+" para canjearlo, y tienes "+str(puntos))
        if enCooldown:
            Parent.SendStreamMessage("Espera "+str(int(COOLDOWN-round(diferenciaCooldown)))+" segundos antes de volver a canjar o apostar")
    else:
        if str(data.GetParam(1)).lower() in ["help", "?", "ayuda"] or not data.GetParam(1):
            # Si usa !gamble help, !gamble ?, !gamble ayuda o !gamble, se mostrará la ayuda
            Parent.SendStreamMessage(AYUDA)
        else:
            # Si usa !gamble [cantidad], se ejecuta la apuesta
            global ultimo_uso
            
            apuesta = int(data.GetParam(1))
            puntos = Parent.GetPoints(userId)
            if apuesta > 0:
                if apuesta <=puntos and (userId not in ultimo_uso.keys() or not enCooldown):
                    #r = [random.choice(slots) for _ in range(3)] # Random no válido para python 2.7. Siempre saca los 2 primeros valores de la lista slots
                    r = []
                    for _ in range(3):
                        random.shuffle(slots)  # desordena aleatoriamente la lista
                        r.append(slots[0])
                    resultado = "".join(r)
                    multiplicador = 0
                    msg = userDisplayName+" ha apostado "+str(apuesta)+" " + MONEDAS + ". El resultado es ["+resultado+"]. "
                    if r == ["⭐","⭐","⭐"]:
                        multiplicador = 2.5
                        msg += "Apuesta güena güena 😍😍!!"
                    elif r[0] == r[1] and r[0] == r[2]:
                        multiplicador = 2
                        msg += "Olee!! 😘"
                    elif r[0] == r[1] or r[0] == r[2] or r[1] == r[2]:
                        multiplicador = 1.5
                        msg += "Algo es algo... 🤷‍♂️"
                    else:
                        multiplicador = 1
                        msg += "Menudo mojón xd 💩💩"
                    ganancia = int(round(apuesta * multiplicador)) - apuesta  # Ejemplo fijo
                    if multiplicador != 1:
                        Parent.AddPointsAll({userId:ganancia})
                    else:
                        Parent.RemovePointsAll({userId:ganancia})
                        ganancia = -apuesta
                    Parent.SendStreamMessage(msg+ ". Ahora tiene "+ str(puntos+ganancia) + " " + MONEDAS + "🪙")
                    ultimo_uso[userId] = horaEjecucionComando
                elif enCooldown:
                    Parent.SendStreamMessage("Espera "+str(int(COOLDOWN-round(diferenciaCooldown)))+" segundos antes de volver a canjear o apostar")
                else:
                    Parent.SendStreamMessage("No puedes apostar más "+MONEDAS+ " de las que tienes")
            try:
                None
            except Exception as e:
                print(e)
    return
def Init():
    return

def Tick():
    return