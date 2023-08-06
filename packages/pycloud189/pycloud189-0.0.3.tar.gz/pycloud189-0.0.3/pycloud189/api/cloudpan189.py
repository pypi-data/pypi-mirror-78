import os
import re

from pycloud189.cmds.cmdbase import CmdBase
from pycloud189.log import logger

log = logger.getLogger(__name__)


class Cloudpan189:
    cmd = CmdBase()
    cloudpan189DirPath = ''

    def setCloudpan189GoDirPath(self, dirPath):
        """
        设置 'cloudpan189-go' 可执行文件的所在目录的绝对路径
        如果没有该可执行文件，请到 https://github.com/tickstep/cloudpan189-go/releases 下载
        :param dirPath: cloudpan189-go 执行文件所在目录绝对路径
        :return:
        """
        self.cloudpan189DirPath = dirPath
        self.cmd.setWorkDirPath(dirPath)

    def checkConnection(self):
        """检查是否能正常连接到网盘"""
        result = self.quota()
        return result['totalSpace'] > 0

    def version(self):
        """
        获取可执行文件的版本号
        :return: 返回版本号
        """
        response = self.cmd.executeCmdInWorkDirWithOutput(['./cloudpan189-go', '--version'])
        if 'cloudpan189-go version' in response['output']:
            return response['output'].replace('cloudpan189-go version', '').strip()
        return ''

    def login(self, username, password):
        """
        登录
        :param username: 用户名
        :param password: 密码
        :return: 成功返回True
        """
        response = self.cmd.executeCmdInWorkDirWithOutput(['./cloudpan189-go', 'login', '--username={0}'.format(username), "--password={0}".format(password)])
        if '帐号登录成功' in response['output']:
            return True
        return False

    def isLogin(self):
        """
        检查是否已经登录
        :return: 已经登录返回True
        """
        return self.checkConnection()

    def quota(self):
        """获取配额, 即获取网盘的总储存空间, 和已使用的储存空间"""
        result = {'totalSpace': -1, 'reservedSpace': -1}
        response = self.cmd.executeCmdInWorkDirWithOutput(['./cloudpan189-go', 'quota'])['output']
        if len(response) == 0:
            return result
        pattern = re.compile('([0-9\.]+)[GB|TB]')
        nums = pattern.findall(response)
        if len(nums) == 0:
            return result

        # TB -> B
        ratio = 1024 * 1024 * 1024
        result['totalSpace'] = int(float(nums[0]) * ratio)
        result['reservedSpace'] = int(float(nums[1]) * ratio)
        return result

    def cd(self, dirPath):
        """
        切换工作目录
        :param dirPath: 网盘目录绝对路径
        :return: 成功返回True
        """
        response = self.cmd.executeCmdInWorkDirWithOutput(['./cloudpan189-go', 'cd', dirPath])
        if not response['success']:
            return False
        return '改变工作目录:' in response['output']

    def pwd(self):
        """
        输出当前所在目录 (工作目录)
        :return: 返回当前网盘工作目录
        """
        response = self.cmd.executeCmdInWorkDirWithOutput(['./cloudpan189-go', 'pwd'])
        if not response['success']:
            return False
        return response['output'].strip()

    def mkdir(self, dirPath):
        """
        创建目录
        :param dirPath: 网盘目录路径
        :return: 成功返回True
        """
        response = self.cmd.executeCmdInWorkDirWithOutput(['./cloudpan189-go', 'mkdir', dirPath])
        if not response['success']:
            return False
        return '创建文件夹成功' in response['output']

    def mv(self, srcPath, targetPath):
        """
        移动 文件/目录
        :param srcPath: 源文件路径
        :param targetPath: 目标文件路径
        :return: 成功返回True
        """
        response = self.cmd.executeCmdInWorkDirWithOutput(['./cloudpan189-go', 'mv', srcPath, targetPath])
        if not response['success']:
            return False
        return '操作成功' in response['output']

    def rename(self, oldNamePath, newNamePath):
        """
        重命名 文件/目录，需要绝对路径，并且必须保证新旧的绝对路径在同一个文件夹内，否则重命名失败！
        :param oldNamePath: 旧文件路径
        :param newNamePath: 新文件路径
        :return: 成功返回True
        """
        response = self.cmd.executeCmdInWorkDirWithOutput(['./cloudpan189-go', 'rename', oldNamePath, newNamePath])
        if not response['success']:
            return False
        return '重命名文件成功' in response['output']

    def rm(self, remotePath):
        """
        删除 文件/目录"
        :param remotePath: 网盘文件绝对路径
        :return: 成功返回True
        """
        response = self.cmd.executeCmdInWorkDirWithOutput(['./cloudpan189-go', 'rm', remotePath])
        if not response['success']:
            return False
        return '操作成功' in response['output']

    def ls(self, remoteDirPath=''):
        """
        获取指定目录里的文件列表，不指定路径则获取当前工作目录的文件列表
        :param remoteDirPath: 目录路径，文件夹绝对路径
        """
        if remoteDirPath == "":
            response = self.cmd.executeCmdInWorkDirWithOutput(['./cloudpan189-go', 'ls'])
        else:
            response = self.cmd.executeCmdInWorkDirWithOutput(['./cloudpan189-go', 'ls', remoteDirPath])
        # print(response['output'])
        if not response['success']:
            return False

        output = response['output']
        lines = output.split('\n')
        fileList = []
        for line in lines:
            if line is None or len(line) == 0:
                continue
            fileInfo = self.__parseFileInfoLine(line)
            if len(fileInfo) > 0:
                fileList.append(fileInfo)

        if len(fileList) > 0:
            for file in fileList:
                file['path'] = os.path.join(remoteDirPath, file['name'])
        return fileList

    def __parseFileInfoLine(self, fileInfoLine=''):
        fileInfo = {'name': '', 'createDate': '', 'fileSize': '', 'isDir': False}
        if fileInfoLine is None or len(fileInfoLine) == 0:
            return {}

        # parse
        fileInfoLine = fileInfoLine.strip()

        pattern = re.compile(
            '^([0-9]+)\s+([0-9.mMkKgGtTbB-]+)\s+([1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])\s+(20|21|22|23|[0-1]\d):[0-5]\d:[0-5]\d)\s+')
        rs = pattern.findall(fileInfoLine)
        if len(rs) == 0:
            return {}

        fileInfo['fileSize'] = rs[0][1]
        if fileInfo['fileSize'] == '-':
            fileInfo['isDir'] = True

        fileInfo['createDate'] = rs[0][2]

        # name
        idx = fileInfoLine.find(fileInfo['createDate'])
        if idx <= 0:
            return {}
        fileInfo['name'] = fileInfoLine[idx + len(fileInfo['createDate']):].strip()
        return fileInfo

    def upload(self, localPath, remoteDirPath, overwrite=False):
        """
        上传文件或目录
        :param localPath: 要上传的本地文件绝对路径
        :param remoteDirPath: 文件保存到网盘的文件夹路径
        :param overwrite: 是否覆盖已经存在的网盘同名文件
        :return: 成功返回True
        """

        # refine remoteDirPath
        localPath = localPath.replace('[', '\\[')
        localPath = localPath.replace(']', '\\]')
        if overwrite:
            response = self.cmd.executeCmdInWorkDirWithOutput(
                ['./cloudpan189-go', 'upload', '-np', '-ow', localPath, remoteDirPath])
        else:
            response = self.cmd.executeCmdInWorkDirWithOutput(
                ['./cloudpan189-go', 'upload', '-np', localPath, remoteDirPath])
        # log.info(response['output'])
        if not response['success']:
            return False
        return '秒传成功' in response['output'] or '保存到网盘路径' in response['output'] or '上传文件成功' in response['output']

    def setDownloadSaveDir(self, saveDirPath):
        """
        设置下载保存的本地目录路径，全局设置
        :param saveDirPath: 本地目录绝对路径，该目录必须存在
        :return: 成功返回True
        """
        if not os.path.exists(saveDirPath):
            return False
        response = self.cmd.executeCmdInWorkDirWithOutput(['./cloudpan189-go', 'config', 'set', '-savedir', saveDirPath])
        if not response['success']:
            return False
        return '保存配置成功' in response['output']

    def download(self, remoteFileOrDirPath):
        """
        下载网盘上指定路径的文件，可以是文件夹或者文件
        :param remoteFileOrDirPath: 文件绝对路径
        :return: 成功返回True
        """
        response = self.cmd.executeCmdInWorkDirWithOutput(['./cloudpan189-go', 'download', '-np', remoteFileOrDirPath])
        if not response['success']:
            return False
        if '获取路径信息错误, 获取文件/目录的元信息, 遇到错误, 远端服务器返回错误' in response['output']:
            return False
        return '下载完成, 保存位置' in response['output'] or '文件已经存在' in response['output']
