import requests
import re
'''
1.采：从网页采集信息
2.抽：信息的抽取。非结构化 - 结构化   
3.取：保存采集的结构
'''

class MyCrawler:
    def __init__(self,filename):
        self.filename = filename
    
    def download(self,url):
        req = requests.get(url)
        return req.text
     
    def extract(self,content,pattern):
        result = re.findall(pattern,content)
        return result
        
    def save(self,info):
        with open(self.filename,'a') as f:
            for item in info:
                f.write(''.join(item) + '\n')
    
    def crwal(self,url,pattern):
        content = self.download(url)
        info = self.extract(content,pattern)
        self.save(info)
        
crawler = MyCrawler('mobile.txt')
crawler.crwal('http://top.zol.com.cn/compositor/57/cell_phone.html',
                         '<div class="rank__name"><a href=".*?">(.*?)<\/a><\/div>')
