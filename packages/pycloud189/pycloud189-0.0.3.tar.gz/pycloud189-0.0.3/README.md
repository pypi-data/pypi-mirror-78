# Pycloud189
An easy to use Python3 package that interact with the cloud189 cloud disk service.

## Installation  
### Install with pip  
```
pip install pycloud189
```

## Quick Start
1. Add `pycloud189.api.cloudpan189 import Cloudpan189` to the beginning of your code.
2. Initialize a new Cloudpan189 object using `api = Cloudpan189()`.
3. Then specify the `cloudpan189-go` execute file locate folder path call for example `api.setCloudpan189GoDirPath('/Users/tickstep/cloudpan189-go-v0.0.5-darwin-macos-amd64')`.
If you do not has the `cloudpan189-go` file you can download it freely from [here](https://github.com/tickstep/cloudpan189-go/releases).
4. Now everything is get ready, you can do all the thing that cloud189 supports such as: login, ls, upload, download, etc.

## Example 
Here is a example code show how to do
```
from pycloud189.api.cloudpan189 import Cloudpan189

if __name__ == '__main__':
    api = Cloudpan189()

    # set the 'cloudpan189-go' execute file dir path
    api.setCloudpan189GoDirPath('/Users/tickstep/cloudpan189-go-v0.0.5-darwin-macos-amd64')

    # of course, we need login first
    # if you do not has an account, register one from https://cloud.189.cn
    if not api.isLogin():
        print(api.login('usernmae@189.cn', 'password'))

    # version
    print(api.version())

    # get list file of current work dir
    print(api.ls(''))

    # change word dir
    print(api.cd('/folder2020'))

    # show current work dir
    print(api.pwd())

    # upload file
    print(api.upload('/Users/tickstep/Downloads/testfile2020.txt', '/folder2020'))

    # download file
    print(api.download('/folder2020/testfile2020.txt'))
```

## [Change logs](https://github.com/tickstep/python-cloudpan189-api/blob/master/CHANGELOG.md)
