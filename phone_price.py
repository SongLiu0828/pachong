# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re


def shouji_list():
    phonename = dict()
    for i in range(1, 3):#采集1到2页的手机价格
        url = 'https://list.jd.com/list.html?cat=9987,653,655&ev=exprice%5FM2800L4499&page='+str(i)+'&sort=sort%5Frank%5Fasc&trans=1&JL=6_0_0&ms=6#J_main'
        url_session = requests.Session()
        #会话对象requests.Session能够跨请求地保持某些参数，比如cookies，即在同一个Session实例发出的所有请求都保持同一个cookies,而requests模块每次会自动处理cookies
        #这样就很方便地处理登录时的cookies问题。在cookies的处理上会话对象一句话可以顶过好几句urllib模块下的操作。
        req = url_session.get(url).text
        soup = BeautifulSoup(req, 'html.parser')
        phone_html = soup.find_all(name = 'div', attrs = {'class':"p-name"})#查看网页源代码得到的关键信息
        for item in phone_html:
            for link in item.find_all('a'):
                shouji_html = str(link.get('href')[14:-5])#取得每个手机网址的关键信息
                phonename[shouji_html] = link.get_text().strip()#将价格和网址对应，组成一个字典
    return phonename

if __name__ == '__main__':
    price = shouji_list()
    price_txt = open('phone_prcie.txt', 'w')
    for num in price:
        price_url = 'https://p.3.cn/prices/mgets?callback=jQuery6983933&type=1&area=1_72_2799_0&pdtk=&pduid=14995199449641080515414&pdpin=&pin=null&pdbp=0&skuIds=J_'+str(num)+'&ext=11000000&source=item-pc'
        #这个网址是难点，要在后台里面查找
        url_session = requests.Session()
        price_req = url_session.get(price_url).text
        price_soup = re.findall(r'"p":"(.*?)"', price_req)
        for i in price_soup:
            shouji_data = price[num].encode('utf-8')
            price_txt.write(shouji_data+':'+str(i)+'\n')
            print str(shouji_data) + ':' + str(i) + '\n'
    price_txt.close()

