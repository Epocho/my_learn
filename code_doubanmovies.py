# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup  #网页解析
import re
import urllib.request
import xlwt #Excel操作
import sqlite3 #sqlite数据库操作

def main():
    baseurl = 'https://movie.douban.com/top250?start='
    datalist = getData(baseurl)
    savepath = 'E:\Python\my_python\豆瓣电影top250.xls'
    saveData(datalist,savepath)
    

def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50"
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
    for i in range(0,10):  # 走循环，访问玩豆瓣电影top250
        url = baseurl + str(i*25)  # 将int转换成str与str连接
        html = askURL(url)

        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_='item'):  #class 是python的关键字，不加下划线会产生歧义
            # print(item)
            # break
            data = []
            item = str(item)

            link = re.findall(r'<a href="(.*?)">',item)[0]
            data.append(link)

            img = re.findall(r'<img.* src="(.*?)".*>', item, re.S)[0]
            data.append(img)

            title = re.findall(r'<span class="title">(.*?)</span>',item)
            if len(title) == 2:  #中文名和英文名
                data.append(title[0])
                data.append((title[1].replace("/","")))
            else:
                data.append(title[0])
                data.append("None")

            score = re.findall(r'<span.* property=.*>(.*)</span>', item)[0]
            data.append(score)

            judge = re.findall(r'<span>(\d*)人评价</span>', item)[0]
            data.append(judge)

            inq = re.findall(r'<span class="inq">(.*?)</span>',item)
            if len(inq) != 0:
                data.append(inq[0])
            else:
                data.append("None")
            
            # IndexError: list index out of range原因：list是空的，没有一个元素，进行list[0] 就会出现这个错误
            bd = re.findall(r'<p class="">(.*?)</p>', item, re.S)[0]
            bd = re.sub(r'\n', ' ', bd)  # 去掉换行符
            bd = re.sub(r'<br(\S+)?/>(\S+)?', '', bd)  # 替换<br>为空格
            data.append(bd.strip())  # 去掉空格

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
    col = ("序号（排名）","链接","海报","中文名","英文名","评分","评分人数","引言","概况")
    for i in range(0,9):
        sheet.write(0,i,col[i])
    for j in range(0,250):
        print(f"爬取第{j+1}条")
        movie_data = datelist[j]
        sheet.write(j+1,0,j+1)
        for n in range(0,8):
            sheet.write(j+1,n+1,movie_data[n])
    document.save(savepath)


if __name__ == '__main__':
    main()
