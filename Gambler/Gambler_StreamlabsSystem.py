# -*- coding: utf-8 -*-
ScriptName = "Apuestas";
Website = "";
Description = "Apuesta monedas para conseguir más y conseguir recompensas";
Creator = "MarcosNoDeFotos";
Version = "1.0.1";



import random
import time

MONEDA = "Moneda Calva"
MONEDAS = "Monedas Calvas"
AYUDA = "Usa !gamble [cantidad]: Apuesta tus "+MONEDAS+" en la tragaperras 🎰.Si salen 3 ⭐, la recompensa es x2.5 Si salen 3 emojis iguales, la recompensa es x2. Si salen 2 emojis iguales, la recompensa es x1.5, y si no, perderás. Puedes usar los comandos !gamble, !apuesta o !gmb\nPara consultar tus "+MONEDAS+", usa !monedas"
COMANDOS = ["!gamble", "!apuesta", "!gmb"]
COOLDOWN = 10 # Segundos

slots = ["❤️", "😎", "⭐", "👽"]

ultimo_uso = {}
# random.seed(int(time.time() * 1000) % 1000000)


def Execute(data):
    if str(data.GetParam(0)) not in COMANDOS:
        return;
    if str(data.GetParam(1)).lower() in ["help", "?", "ayuda"] or not data.GetParam(1):
        Parent.SendStreamMessage(AYUDA);
    else:
        global ultimo_uso
        user = data.UserName
        horaEjecucionComando = time.time()
        apuesta = int(data.GetParam(1))
        puntos = Parent.GetPoints(user)
        if apuesta > 0:
            diferenciaCooldown = 0
            enCooldown = False
            if  user in ultimo_uso.keys():
                diferenciaCooldown = horaEjecucionComando - ultimo_uso[user]
                enCooldown = diferenciaCooldown < COOLDOWN
            if apuesta <=puntos and (user not in ultimo_uso.keys() or not enCooldown):
                #r = [random.choice(slots) for _ in range(3)] # Random no válido para python 2.7. Siempre saca los 2 primeros valores de la lista slots
                r = []
                for _ in range(3):
                    random.shuffle(slots)  # desordena aleatoriamente la lista
                    r.append(slots[0])
                resultado = "".join(r)
                multiplicador = 0
                msg = user+" ha apostado "+str(apuesta)+" " + MONEDAS + ". El resultado es ["+resultado+"]. "
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
                    Parent.AddPoints(user, user, ganancia)
                else:
                    Parent.RemovePoints(user, user, apuesta)
                    ganancia = -apuesta;
                Parent.SendStreamMessage(msg+ ". Ahora tiene "+ str(puntos+ganancia) + " " + MONEDAS + "🪙")
                ultimo_uso[user] = horaEjecucionComando
            elif enCooldown:
                Parent.SendStreamMessage("Espera "+str(int(COOLDOWN-round(diferenciaCooldown)))+" segundos antes de volver a apostar")
            else:
                Parent.SendStreamMessage("No puedes apostar más "+MONEDAS+ " de las que tienes")
        try:
            None
        except Exception as e:
            print(e)
    return;
def Init():
    return;

def Tick():
    return;