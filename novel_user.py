import requests
from lxml import etree
import time
from fake_useragent import UserAgent
from queue import Queue
import pymysql

class Novel_Get:
    def __init__(self):
        self.headers = {'User-Agent':UserAgent().random}
        self.one_url = 'https://www.qisuu.la/soft/sort{}/index_1.html'
        self.url_queue = Queue()
        self.db = pymysql.connect('127.0.0.1','root','123456','nov',charset='utf8')
        self.cursor = self.db.cursor()

    def get_list(self,url):
        html = requests.get(url=url,headers=self.headers).text
        res = etree.HTML(html)
        link_list = res.xpath('//div[@class="tspage"]/select//@value')
        for link in link_list:
            two_link = 'https://www.qisuu.la'+link
            self.url_queue.put(two_link)
        # while True:
            # 当队列不为空时,获取url地址
        for x in range(1):
            if not self.url_queue.empty():
                url = self.url_queue.get()
                html = requests.get(url, headers=self.headers).content.decode('utf-8')
                self.parse_link(html)
            else:
                break

    def parse_link(self,html):
        res = etree.HTML(html)
        three_list = res.xpath('/html/body/div[4]/div[2]/div/ul/li/a/@href')
        for link in three_list:
            three_link = 'https://www.qisuu.la' + link
            html = requests.get(url=three_link, headers=self.headers).text
            self.parse_mysql(html)

    def parse_mysql(self,html):
        res = etree.HTML(html)
        link = res.xpath('//div[@class="showDown"]/ul/li/script/text()')[0].split(',')[1]
        name = link.split('/')[-1][:-5]
        print(name)
        ins = 'insert into novel values(%s,%s)'
        self.cursor.execute(ins,[name,link])
        self.db.commit()

    def main(self):
        print('''01--玄幻奇幻|02--武侠仙侠|03--女频言情|04--现代都市|05--历史军事|06--游戏竞技|07--科幻灵异|08--美文同人|09--剧本教程|010--名著杂志|''')
        type = input("请输入类型序号:")
        url = self.one_url.format(type)
        self.get_list(url)
        name = input("请输入需要下载的小说名字:")
        sel = 'select link from novel where name=%s'
        self.cursor.execute(sel,name)
        link = self.cursor.fetchone()[0].strip("'")
        print(link)
        html = requests.get(url=link, headers=self.headers).text
        filename = "%s.txt"%name
        with open(filename,'w') as f:
            f.write(html)
        print("下载成功")



if __name__ == '__main__':
    no = Novel_Get()
    no.main()

