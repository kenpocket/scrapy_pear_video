import requests
import re
import random
import os


class doit:
    def __init__(self):
        self.__headers = {
            'Host': 'www.pearvideo.com',
            'Referer': 'https://www.pearvideo.com/video_{}'
        }
        self.falseid = 'https://www.pearvideo.com/videoStatus.jsp?contId={}&mrd={}'

    def get_url(self):
        url = 'https://www.pearvideo.com'
        response = requests.get(url)
        response.encoding = 'utf-8'
        text = response.text
        response.close()
        arr = re.findall(r'video_(.*?)"', text)
        return arr

    def get_false_url(self, contid):
        self.__headers['Referer'] = self.__headers['Referer'].format(contid)
        url = self.falseid.format(contid, random.uniform(0.5, 1))
        response = requests.get(url, headers=self.__headers)
        want_url = response.json()['videoInfo']['videos']['srcUrl']
        wanted = response.json()['videoInfo']['videos']['srcUrl'].split('/')[-1].split('-')[0]
        response.close()
        self.__headers = {
            'Host': 'www.pearvideo.com',
            'Referer': 'https://www.pearvideo.com/video_{}'
        }
        return want_url.replace(wanted, 'cont-{}'.format(contid))


if __name__ == '__main__':
    if os.path.exists('./download'):
        pass
    else:
        os.mkdir('./download')
    mydoit = doit()
    arr = mydoit.get_url()
    for i in arr:
        result_url = mydoit.get_false_url(i)
        response = requests.get(result_url)
        print('downloading：'+result_url)
        with open('./download/{}.mp4'.format(i), 'wb')as file:
            file.write(response.content)
        response.close()
    print('complete')
