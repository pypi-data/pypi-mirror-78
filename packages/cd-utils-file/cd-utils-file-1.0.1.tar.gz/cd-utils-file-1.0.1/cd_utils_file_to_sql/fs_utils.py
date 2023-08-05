import datetime as dt
from os import path
import sys
import re
from cd_utils_logger import Logger

class FsUtilsSql:

    def __init__(self, str_path_file):
        '''Contrutor fo this class'''
        self._logger = Logger()
        self._isExist = False
        self.str_path_file = str_path_file
        self._str_file = None

        if path.exists(str_path_file) == False:
            msg_error = 'Arquivo ou Caminho não existe'
            self._logger.error(msg_error)
            sys.exit(0)

        elif path.isfile(str_path_file) == False:
            msg_error = 'Arquivo não existe no caminho especificado'
            self._logger.error(msg_error)
        else:
            self._logger.info('Tentando abrir arquivo para leitura')
            try:
                with open(str_path_file, 'r') as file:
                    self._logger.info('Iniciando leitura do arquivo')
                    self._str_file = file.read()
                    self._logger.info('Leitura de arquivo realizada com sucesso')

            except IOError as e:
                self._logger.error("I/O Erro({0}): {1}".format(e.errno, e.strerror))
            except:  # handle other exceptions such as attribute errors
                self._logger.error('Cheque se possui acesso ao arquivo que está tentando fazer leitura')
                self._logger.error("Erro Inesperado:", sys.exc_info()[0])

    def is_exist(self):
        self._logger.info('is_exist::{}'.format(self._isExist))
        return self._isExist

    def get_str_file(self):
        self._logger.info('Obtendo a string do arquivo')
        return self._str_file

    def get_str_query_file(self):
        self._logger.info('get_str_query_file')
        self._logger.info('Removendo comentários e caracteres que não são utilizados em query')
        data = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "",
                      self.get_str_file())  # remove all occurrences streamed comments (/*COMMENT */) from string

        data = re.sub(re.compile("//.*?\n"), "",
                      data)  # remove all occurrence single-line comments (//COMMENT\n ) from string
        data = re.sub(re.compile("--.*?\n"), "",
                      data)  # remove all occurrence single-line comments (//COMMENT\n ) from string

        data = data.replace('\n', ' ')
        data = data.replace('\t', ' ')
        data = data.replace('  ', ' ')
        data = data.replace('   ', ' ')
        self._logger.info('Caracteres e comentarios removidos com sucesso')
        return data
