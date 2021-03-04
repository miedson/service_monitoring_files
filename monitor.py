import os
import sys
import time
from datetime import datetime
from datetime import timedelta
from pathlib import Path
import smtplib
from email.mime.text import MIMEText


def getConfig():
    params = dict()
    if os.path.exists(f'{os.getcwd()}\config.txt'):
        with open(f'{os.getcwd()}\config.txt', 'r') as config:
            for key, value in dict(map(lambda i: i.split("="), filter(lambda i: i != '\n', filter(lambda i: i.find('//'), config.readlines())))).items():
                params[key] = value.strip()
        return params
    else:
        gravaLog(
            f"[ERRO] {datetime.now().strftime('%H:%M:%S')} --> Arquivo de configuração não encontrado", False)


def decript(valor):
    alfa = 'abcdefghijklmnopqrstuvwxyz1234567890@#$&*()_+-!?{[}]'
    senha = ''
    for l in valor:
        if l in alfa:
            senha += alfa[alfa.find(l)-3]
    return senha


def enviaAlerta(tmpDecorrido):
    smtp_host = getConfig().get('smtp_host')
    smtp_port = getConfig().get('smtp_port')
    user = getConfig().get('user')
    password = decript(getConfig().get('password'))

    if datetime.today().weekday() < 5:
        mailMessageBody = getConfig().get('body').replace(
            'tempo_decorrido', tmpDecorrido).replace('tempo_espera', getConfig().get('tempo'))
    else:
        mailMessageBody = getConfig().get('body').replace(
            'tempo_decorrido', tmpDecorrido).replace('tempo_espera', str(int(getConfig().get('tempo')) * int(getConfig().get('valor'))))

    mailMessage = MIMEText(mailMessageBody)
    mailMessage['subject'] = getConfig().get('subject')
    mailMessage['from'] = getConfig().get('user')
    mailMessage['to'] = getConfig().get('emailTo')

    mailServer = smtplib.SMTP(smtp_host, smtp_port)
    mailServer.starttls()
    mailServer.login(user, password)
    mailServer.sendmail(mailMessage['from'],
                        mailMessage['to'].split(','), mailMessage.as_string())
    mailServer.quit()

    gravaLog(
        f"[ALERTA] {datetime.now().strftime('%H:%M:%S')} --> Alerta enviado às {datetime.now().strftime('%H:%M')}h para {getConfig().get('emailTo')}")


def getFiles():
    files = os.scandir(getConfig().get('path'))
    return list(filter(lambda i: os.path.splitext(i.name)[1] == '.rid', sorted(files, key=lambda i: i.stat().st_mtime, reverse=True)))[0]


def gravaLog(logtext, logpath=True):
    if logpath:
        if not os.path.isdir(getConfig().get('log')):
            os.mkdir(getConfig().get('log'))
        with open(f"{getConfig().get('log')}\{datetime.now().strftime('%d_%m_%Y')}.txt", 'a') as log:
            log.write(f'{logtext}\n')
        log.close()
    else:
        with open(f"{os.getcwd()}\ErrorLog.txt", 'a') as log:
            log.write(f'{logtext}\n')
        log.close()


def getParams():
    if datetime.today().weekday() < 5:
        return {'start': getConfig().get('start'), 'end': getConfig().get('end'), 'tmpEspera': datetime.now() + timedelta(minutes=int(getConfig().get('tempo'))), 'tempo': getConfig().get('tempo')}
    else:
        return {'start': getConfig().get('startFds'), 'end': getConfig().get('endFds'), 'tmpEspera': datetime.now() + timedelta(minutes=int(getConfig().get('tempoFds'))), 'tempo': getConfig().get('tempoFds')}


def startService():
    tmpEspera = getParams().get('tmpEspera')
    tmplastFile = datetime.now().timestamp()
    count = 1
    while True:
        if datetime.now().strftime('%H:%M') >= getParams().get('start') and datetime.now().strftime('%H:%M') <= getParams().get('end'):
            file = getFiles()
            if file.stat().st_mtime > tmplastFile:
                tmpEspera = getParams().get('tmpEspera')
                gravaLog(
                    f"[AVISO] {datetime.now().strftime('%H:%M:%S')} --> Lote {file.name} importado às {datetime.now().strftime('%H:%M')}h")
                tmplastFile = file.stat().st_mtime
                count = 1
            else:
                diffTmp = datetime.now() - datetime.fromtimestamp(tmplastFile)
                gravaLog(
                    f"[AVISO] {datetime.now().strftime('%H:%M:%S')} --> Há {time.strftime('%H:%M:%S', time.gmtime(diffTmp.total_seconds()))} minutos sem importar um novo lote")
                if(datetime.now().timestamp() > tmpEspera.timestamp()):
                    count += 1
                    enviaAlerta(time.strftime(
                        '%H:%M:%S', time.gmtime(diffTmp.total_seconds())))
                    tempo = int(getParams().get('tempo')) * count
                    tmpEspera = datetime.now() + timedelta(minutes=tempo)
        else:
            tmpEspera = getParams().get('tmpEspera')
            tmplastFile = datetime.now().timestamp()


startService()
