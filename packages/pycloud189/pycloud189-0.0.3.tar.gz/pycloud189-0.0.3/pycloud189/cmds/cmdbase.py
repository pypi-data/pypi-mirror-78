import os
import subprocess
import platform
from pycloud189.log import logger

log = logger.getLogger(__name__)


class CmdBase:

    def __init__(self):
        self.__workDirPath = os.getcwd()
        self.__logger = log

        self.__outputEncoding = 'utf8'
        if platform.system() == 'Windows':  # windows
            self.__outputEncoding = 'gbk'
        elif platform.system() == 'Darwin':  # macOS
            self.__outputEncoding = 'utf8'

    def setCmdEncoding(self, encoding):
        self.__outputEncoding = encoding

    def setWorkDirPath(self, path):
        if not os.path.exists(path):
            return False
        self.__workDirPath = path
        return True

    def getWorkDirPath(self):
        return self.__workDirPath

    def executeCmdInWorkDir(self, cmd):
        if len(cmd) == 0:
            self.__logger.error('cmd is empty')
            return False

        if not os.path.exists(self.__workDirPath):
            self.__logger.error('the path of the work dir is not existed')
            return False

        curDir = os.getcwd()

        # change dir
        os.chdir(self.__workDirPath)

        # start app
        status = os.system(cmd)

        # backup dir
        os.chdir(curDir)

        return status == 0

    def executeCmdInWorkDirWithOutput(self, cmdList):
        result = {'success': False, 'output': ''}

        backDir = os.getcwd()
        srcCodeDir = self.getWorkDirPath()
        if not os.path.exists(srcCodeDir):
            self.__logger.error('source code path not existed: ' + srcCodeDir)
            return result

        # self.__logger.debug('change work dir: ' + srcCodeDir)
        os.chdir(srcCodeDir)

        try:
            obj = subprocess.check_output(cmdList, stderr=subprocess.STDOUT)
            result['success'] = True
            result['output'] = obj.decode(self.__outputEncoding)
        except subprocess.CalledProcessError as ex:
            result['success'] = False
            result['output'] = ex.output.decode(self.__outputEncoding)

        # back
        os.chdir(backDir)
        return result
