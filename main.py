from getFiles import Rpa_Ftp

import os
import locale
import schedule
import time

ftpHost = '172.25.64.11'
ftpUser = 'net_telematica'
ftpPass = 'rDuFGam0S@'

# Define a localização do programa como português do Brasil
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


def limpar_console():
    if os.name == 'posix':  # Para Linux/Mac
        _ = os.system('clear')
    else:  # Para Windows
        _ = os.system('cls')


def execProcesso():
    impObj = Rpa_Ftp(ftpHost, ftpUser, ftpPass)
    impObj.getFile()


# Agendar execução
schedule.every().day.at('15:43').do(execProcesso)


# Produção
try:
    while True:
        tempo_restante = schedule.idle_seconds()
        if tempo_restante is not None:
            horas = int(tempo_restante // 3600)
            minutos = int((tempo_restante % 3600) // 60)
            segundos = int(tempo_restante % 60)
            print('Robô Claro, importação de NÃO PERTURBE:\n',
                  f'Próxima execução em {horas} horas, {minutos} minutos e {segundos} segundos.')
        time.sleep(1)
        limpar_console()
        schedule.run_pending()
except KeyboardInterrupt:
    pass
