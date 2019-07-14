# /usr/bin/python
# coding:utf-8
import urllib
from requests.adapters import HTTPAdapter
import time

import os, shutil
import urllib.request, urllib.error, requests

def convert_file(_path, filename):
    tmp = []
    if '\\' in _path:
      _path=_path.replace('\\','\\\\')
    files = os.listdir(_path)
    for file in files:
      if '.ts' in file:
        tmp.append(_path+"\\"+str(file))
    os.chdir(_path)
    shell_str = '+'.join(tmp)
    shell_strc = 'copy /b '+ shell_str + ' ' + filename+"g.mp4"
    print(shell_strc)
    return
def download_txvideo(_url,_path):
     r = requests.get(url=_url)
     with open(_path+'/videoUrl.txt', 'wb') as f:
        f.write(r.content)

     fo = open(_path+"/videoUrl.txt",'r')
     fc = fo.readlines()
     count=0
     for i in fc:
       if 'ver=4' in i:
         urltemp=_url.split('/')
         urldl=_url.replace(urltemp[urltemp.__len__()-1],i).strip()
         print(urltemp[urltemp.__len__()-1])
         s=requests.session()
         s.mount('https://',HTTPAdapter(max_retries=3))
         r=s.get(urldl,timeout=3)
         with open( _path+'/'+str(count)+'.ts', 'wb') as f:
            f.write(r.content)
         count+=1
         time.sleep(1)
     return


# 打开并读取网页内容
def getUrlData(url):
    try:
        urlData = urllib.request.urlopen(url, timeout=20)  # .read().decode('utf-8', 'ignore')
        # urlData = requests.get(url, timeout=20)  # .read().decode('utf-8', 'ignore')
        return urlData
    except Exception as err:
        print(f'err getUrlData({url})\n', err)
        return -1


# 下载文件-requests
def getDown_reqursts(url, file_path):
    try:
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"}
        response = requests.get(url, timeout=120, headers=header)
        with open(file_path, mode='ab+') as f:
            f.write(response.content)
        # 下载文件较大时，使用循环下载
        # with open(file_path, mode='wb') as f:
        #     for content in response.iter_content(1024):
        #         f.write(content)
        print("down successful!")
    except Exception as e:
        print(e)

def getVideo_requests(url_m3u8, path, videoName):
    print('begin run ~~\n')
    urlData = getUrlData(url_m3u8)
    tempName_video = os.path.join(path, f'{videoName}.ts')  # f'{}' 相当于'{}'.format() 或 '%s'%videoName
    open(tempName_video, "wb").close()
    # print(urlData)
    for line in urlData:

        url_ts = str(line.decode("utf-8","ignore")).strip()
        if not '.ts' in url_ts:
            continue
        else:
            if not url_ts.startswith('http'):

                url_ts = url_m3u8.replace(url_m3u8.split('/')[-1], url_ts)
        print(url_ts)
        getDown_reqursts(url=url_ts, file_path=tempName_video)
    filename = os.path.join(path, f'{videoName}.mp4')
    shutil.move(tempName_video, filename)
    print(f'Great, {videoName}.mp4 finish down!')

if __name__=='__main__':
    _path=input("输入下载路径：\n")
    _url=input("输入下载链接：\n")
    filename=input("输入下载文件名称：\n")
    getVideo_requests(_url,_path,filename)


