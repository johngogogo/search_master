# -*- UTF-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import json
import csv
import wx
import urllib.request
import webbrowser

def GetKeyWord(keyWord,pageNum):
    fileList = []
    urlFront = 'https://www.yunpanjingling.com/search/'
    url = urlFront + keyWord + '?page=' + str(pageNum)
    pages = requests.get(url)
    pages.encoding = 'utf-8'
    #print(pages.text)
    soup = bs(pages.text,'html.parser')
    searchList = soup.find_all("div", class_="item")
    for i in range(0,len(searchList)):
        name = searchList[i].find_all("div", class_="name")
        urlOri = name[0].a.get('href')
        #url = urlOri.split('=')[1].replace('%3A',':').replace('%2F','/')
        fileName = name[0].a.text
        sizeSpan = searchList[i].find_all("span", class_="size")
        size = sizeSpan[0].find_all("strong")
        code = searchList[i].find("span", class_="code")
        item=[]
        item.append(str(i+1))
        item.append(urlOri)
        item.append(fileName)
        if size:
            item.append(size[0].string)
        else:
            item.append('0')
        if code==None:
            item.append('-')
        else:
            item.append(code.string)
        fileList.append(item)
    return fileList



def PresentResult():
    pass

class Frame(wx.Frame):
    keyWord = ''
    basicText = []
    pageNum = 1
    list=[]
    fileList=[]
    def __init__(self, parent=None, id=-1,pos=wx.DefaultPosition,title='Hello, wxPython!'):
        wx.Frame.__init__(self, None, -1, '网盘搜索大师', size=(740, 600))
        newUrl = 'http://papodq2is.bkt.clouddn.com/new01.txt'
        html = requests.get(newUrl)
        if html.text:
            wx.MessageBox('立即更新最新版本！','提示')
            webbrowser.open(html.text)
        else:
            panel = wx.Panel(self, -1)
            basicLabel = wx.StaticText(panel, -1, "输入搜索关键词:",pos=(10, 13))
            basicText = wx.TextCtrl(panel, -1, "",size = (500, -1),pos=(100, 10))
            self.basicText.append(basicText)
            self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT|wx.LC_HRULES,size = (700,235),pos=(10, 50))
            self.list.InsertColumn(0, "序号", format=wx.LIST_FORMAT_LEFT, width=50)
            self.list.InsertColumn(1, "链接", format=wx.LIST_FORMAT_LEFT, width=250)
            self.list.InsertColumn(2, "文件名称", format=wx.LIST_FORMAT_LEFT, width=260)
            self.list.InsertColumn(3, "大小", format=wx.LIST_FORMAT_LEFT, width=70)
            self.list.InsertColumn(4, "密码", format=wx.LIST_FORMAT_LEFT, width=70)
            self.buttonSearch = wx.Button(panel, -1, '搜索', pos=(610, 7))
            self.buttonLast = wx.Button(panel, -1, '上一页', pos=(250, 300))
            self.buttonNext = wx.Button(panel, -1, '下一页', pos=(350, 300))
            self.buttonTips = wx.Button(panel, -1, '使用帮助', pos=(600, 300))
            self.Bind(wx.EVT_BUTTON, self.OnSearch, self.buttonSearch)
            self.Bind(wx.EVT_BUTTON, self.LastPage, self.buttonLast)
            self.Bind(wx.EVT_BUTTON, self.NextPage, self.buttonNext)
            self.Bind(wx.EVT_BUTTON, self.GetTips, self.buttonTips)
            self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.CopyText, self.list)
            self.picUrl = 'http://papodq2is.bkt.clouddn.com/ad02.jpg'
            urllib.request.urlretrieve(self.picUrl, "ad.jpg")
            #self.bmp = wx.Image(name)
            image = wx.Image("ad.jpg", wx.BITMAP_TYPE_JPEG)
            self.tmp = image.ConvertToBitmap()
            self.bmp = wx.StaticBitmap(panel, bitmap=self.tmp,pos=(10,340))

            self.buttonSearch.SetDefault()



    def OnSearch(self, event):
        self.keyWord = self.basicText[-1].GetValue()
        if self.keyWord:
            fileList=GetKeyWord(self.keyWord,self.pageNum)
            self.ShowList(fileList)
            PresentResult()
        else:
            wx.MessageBox('请输入搜索关键词！', '提示')

    def LastPage(self,event):
        if self.pageNum==1:
            wx.MessageBox('当前页面已经是第一页！', '提示')
        else:
            self.pageNum-=1
            fileList = GetKeyWord(self.keyWord, self.pageNum)
            self.ShowList(fileList)

    def NextPage(self,event):
        self.pageNum+=1
        fileList = GetKeyWord(self.keyWord, self.pageNum)
        self.ShowList(fileList)

    def ShowList(self,fileList):
        self.list.DeleteAllItems()
        for row,item in enumerate(fileList):
            index = self.list.InsertItem(len(fileList), item[0])
            for col, text in enumerate(item[1:]):
                self.list.SetItem(index, col+1, text)
        self.fileList = fileList

    def CopyText(self,event):
        text_obj = wx.TextDataObject()
        text_obj.SetText(self.fileList[int(event.GetText())-1][1])
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text_obj)  # 将数据放置到剪贴板上
            wx.TheClipboard.Close()
            wx.MessageBox('链接已复制到剪贴板！','提示')

    def GetTips(self,event):
        wx.MessageBox('版本信息：V2018.1.0\n作者：无知红（微信公众号）\n使用方法：\n1.输入搜索关键词\n2.鼠标点击链接\n3.到浏览器粘贴', '使用帮助')



class App(wx.App):
    def OnInit(self):
        self.frame = Frame(parent=None,title='网盘搜索大师')
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()