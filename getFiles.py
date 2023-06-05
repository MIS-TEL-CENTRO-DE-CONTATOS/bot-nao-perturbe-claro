from datetime import datetime
from importFiles import importFile

import pysftp
import patoolib
import os
import locale


locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


class Rpa_Ftp:
    def __init__(self, ftpHost: str, ftpUser: str, ftpPass: str):

        if ftpHost is None:
            raise ValueError("O parâmetro 'host' não pode ser None.")
        else:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None  # Desativa a verificação de chave de host
            self.ftp = pysftp.Connection(
                ftpHost, username=ftpUser, password=ftpPass, cnopts=cnopts)

            self.ftp.chdir('/app/sftp/bloqueio')

            # self.filename = 'NAO_PERTURBE_20230530.zip'
            self.filename = f'NAO_PERTURBE_{datetime.today().year}{str(datetime.today().month).zfill(2)}{str(datetime.today().day).zfill(2)}.zip'

    def getFile(self):
        mes_str = datetime.today().strftime('%B').upper()
        mes_num = datetime.today().month
        dia_num = datetime.today().day
        ano_num = datetime.today().year

        # caminho que irá salvar o arquivo zipado
        path_blacklist = rf'\\TELFSBAR01\Planejamento$\{ano_num}\43 - MIS\06 - GC_CLARO\{mes_num}-{mes_str}\01-NAOPERTURBE\{dia_num}'

        # verifica se o caminho existe
        try:
            # tenta criar os diretórios
            os.makedirs(path_blacklist)
        except OSError:
            # em caso de erro, criar somente a última pasta
            if not os.path.isdir(path_blacklist):
                os.mkdir(path_blacklist)
            else:
                pass

        path_blacklist_p = rf'{path_blacklist}\{self.filename}'

        print(self.ftp.listdir())

        # executa o processo de captura do arquivo
        try:
            self.ftp.get(self.filename, path_blacklist_p)
            self.ftp.close()
        except Exception as e:
            print(e)

        print(
            f"{datetime.today().strftime('%d/%m/%Y %H:%M:%S')} - Processo de extração iniciado.")
        patoolib.extract_archive(path_blacklist_p, outdir=path_blacklist)

        all_files = os.listdir(path_blacklist)
        txt_files = [file for file in all_files if file.endswith('.txt')]
        txt_file = txt_files[0].replace('.txt', '')

        # Cria um arquivo schema para importação.
        fileconfig = open(rf'{path_blacklist}\schema.ini', 'a')

        listconfig = list()
        listconfig.append(f'[{txt_files[0]}]\n')
        listconfig.append('Format=Delimited(;)\n')
        listconfig.append('CHARACTER SET=ANSI\n')
        listconfig.append('ColNameHeader=TRUE\n')

        fileconfig.writelines(listconfig)

        print(txt_file)
        importFile(txt_file)

        # os.remove(rf'{path_blacklist}\{txt_file}')
