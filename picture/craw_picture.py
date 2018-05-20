import urllib.request
import re
import time
import socket


socket.setdefaulttimeout(20)
urlCT = 'https://openi.nlm.nih.gov/gridquery.php?q=&it=c'
urlMRI = 'https://openi.nlm.nih.gov/gridquery.php?q=&it=m'
urlUltrasound = 'https://openi.nlm.nih.gov/gridquery.php?q=&it=u'
urlX = 'https://openi.nlm.nih.gov/gridquery.php?q=&it=x'
urlList = [urlCT, urlMRI, urlUltrasound, urlX]  
urlDir = ['CT/', 'MRI/', 'Ultrasound/', 'Xss/']

pngHead ='https://openi.nlm.nih.gov'

Header = {
    "User-Agent":
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
}

# suolue = 'https://openi.nlm.nih.gov/imgs/150/204/1006/MPX1006_synpic52425.png'
# wanzheng = 'https://openi.nlm.nih.gov/imgs/512/204/1006/MPX1006_synpic52425.png'

def craw(url, pages, dir):
    for i in range(0, pages):
        print(i)

        a = i * 100 + 1
        b = a + 99
        url = url + '&m=' + str(a) + '&n=' + str(b)
        request = urllib.request.Request(url, headers=Header)
        try:
            response = urllib.request.urlopen(request)
            html = response.read()
            html = str(html)
            response.close()
            pat1 = '<script language="javascript">.+?Advanced Search- Open-i'
            result1 = re.compile(pat1).findall(html)
            result1 = result1[0]
            pat2 = '"thumbUrl":"(.+?.png)"'
            result2 = re.compile(pat2).findall(result1)

            for imageurl in result2:
                imageurl = imageurl.replace('150', '512')   #  将缩略图转为全图
                imageurl = imageurl.replace('\\','')
                imagename = 'save/' + dir + imageurl[19:].replace('/', '-') # 生成图片保存位置
                imageurl = pngHead + imageurl
                urllib.request.urlretrieve(imageurl, filename=imagename)
                time.sleep(4.63)

        except urllib.error.URLError as e:
            print(e.reason)



if __name__ == "__main__":
    # for index in range(4):
    index = 0
    url = urlList[index]
    dir = urlDir[index]
    print(url)
    craw(url, 200, dir)
