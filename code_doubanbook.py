# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup  #网页解析
import re
import urllib.request
import xlwt #Excel操作
import sqlite3 #sqlite数据库操作

def main():
    baseurl = 'https://book.douban.com/top250?start='
    datalist = getData(baseurl)
    savepath = '豆瓣读书top250.xls'
    saveData(datalist,savepath)
    

def askURL(url):
    head = {
      #自填
    }
    request = urllib.request.Request(url,headers=head)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):  #判断对象e中是否含有code属性
            print(e.code)  #code被挪到HTTPError里面去了
        if hasattr(e,"reason"):
            print(e.reason)
    
    return html

# askURL('https://movie.douban.com/top250?start=')

def getData(baseurl):
    datalist = []
    for i in range(0,10):  # 走循环，访问玩豆瓣top250
        url = baseurl + str(i*25)  # 将int转换成str与str连接
        html = askURL(url)

        soup = BeautifulSoup(html,"html.parser")
        # class 是python的关键字，不加下划线会产生歧义  <div class="indent">
        for item in soup.find_all('table', width='100%'):
            # print(item)
            # break
            data = []
            item = str(item)

            img = re.findall(r'<img src="(.*?)".*>', item)[0]
            data.append(img)

            link_title = re.findall(r'<a href="(.*?)".*?title="(.*?)">',item)[0]
            data.append(link_title[0])
            data.append(link_title[1])

            bd = re.findall(r'<p class="pl">(.*?)</p>', item)[0]
            data.append(bd)
            
            score = re.findall(r'<span class="rating_nums">(.*)</span>', item)[0]
            data.append(score)

            judge = re.findall(r'<span class="pl">\((.*?)\)</span>', item,re.S)[0]
            judge = re.sub(r'\n',' ',judge)
            data.append(judge.strip())

            inq = re.findall(r'<span class="inq">(.*?)</span>',item)
            if len(inq) != 0:
                data.append(inq[0])
            else:
                data.append("None")
            
            

            # print(link)
            # print(title)
            # print(img)
            # print(bd)
            # print(score)
            # print(judge)

            datalist.append(data)
            
    return datalist


def saveData(datelist,savepath):
    print("爬取中。。。")
    # style_compression=0说明了是否允许改变excel表格样式
    document = xlwt.Workbook(encoding="utf-8", style_compression=0)
    # 第二参数用于确认同一个cell单元是否可以重设值。
    sheet = document.add_sheet('列表', cell_overwrite_ok=True)
    col = ("序号（排名）", "封面", "链接", "标题", "概况", "评分", "评分人数", "引言")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for j in range(0,250):
        print(f"爬取第{j+1}条")
        book_data = datelist[j]
        sheet.write(j+1,0,j+1)
        for n in range(0,7):
            sheet.write(j+1,n+1,book_data[n])
    document.save(savepath)


if __name__ == '__main__':
    main()
