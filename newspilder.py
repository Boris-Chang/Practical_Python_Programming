import requests
import re
from lxml import html
'''
1.采：从网页采集信息
2.抽：信息的抽取。非结构化 - 结构化   
3.取：保存采集的结构
'''



class MyCrawler:
    def __init__(self,filename):
        self.filename = filename
        self.headers = {
    
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}
    
    def download(self,url):
        req = requests.get(url,headers=self.headers)
        return req.text
     
    def extract(self,content,pattern):
        result = re.findall(pattern,content)
        return result
        
    def save(self,info):
        with open(self.filename,'a',encoding='utf-8') as f:
            for item in info:
                f.write('\n'.join(item) + '\n')
    
    def crawl(self,url,pattern,headers=None):
        if headers:
            self.headers.update(headers)
        content = self.download(url)
        info = self.extract(content,pattern)
        self.save(info)
        
class My_douban_Crwaler(MyCrawler):
#二级采集    
    def extract(self, content, pattern_main, pattern_star):
        result = re.findall(pattern_main, content)
        for index in range(len(result)):
#         for book_info in result:
            if 'allstar' in result[index][4]:
                items = re.findall(pattern_star, result[index][4])
            else:
                items = [['0', '0', '0']]
            result[index] = list(result[index])
            del result[index][4]
            result[index].extend(items[0])
#             print(result[index])
        return result
    
    def crawl(self, url, pattern_main, pattern_star, headers=None):
        if headers:
            self.headers.update(headers)
        content = self.download(url)
        info = self.extract(content, pattern_main, pattern_star)
        self.save(info)

#正则抽取：
'''
热门手机排行榜：
crawler = MyCrawler('mobile.txt')
crawler.crawl('http://top.zol.com.cn/compositor/57/cell_phone.html',
                         '<div class="rank__name"><a href=".*?">(.*?)<\/a><\/div>') 
'''

'''
豆瓣图书（神经网络）排行榜（正则法）：

b_douban_crawler = My_douban_Crwaler('douban.txt')

b_douban_crawler.crawl(
    'https://book.douban.com/tag/%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C',
    'src="(.*?\d+.jpg)"[\S\s]*?<a\shref="(https:\/\/book.douban.com/subject\/\d+/)"\stitle="(.*?)"[\S\s]*?<div class="pub">\s*(.*?)\s*<\/div>[\S\s]*?<div class="star\sclearfix">\s*([\S\s]*?)\s*<\/div>',
    'allstar(\d+)"[\S\s]*?rating_nums">([^<]*?)<\/span>[\S\s]*?\((\d+)'
)
with open('douban.txt',encoding='utf-8') as f:
    print(f.read())
'''    

'''
bilibili排行榜：

bilibili_crawler = MyCrawler('bilibili.txt')
bilibili_crawler.crawl('https://www.bilibili.com/v/popular/rank/all',
'<title>(.*?)</title>')
'''

#Xpath路径爬取：
'''
#书名：
book_names = douban_tree.xpath('//li/div[2]/h2/a')
book_names = list(map(lambda x:x.text.strip(),book_names))
#出版信息：
book_pub_infos = douban_tree.xpath('//li/div[2]/div[1]')
book_pub_infos = list(map(lambda x:x.text.strip(),book_pub_infos))
#书籍介绍：
book_intros = douban_tree.xpath('//li/div[2]/p')
book_intros= list(map(lambda x:x.text.strip(),book_intros))
#书名URL：
book_name_elem = douban_tree.xpath('//li/div[2]/h2/a')
book_url = book_name_elem[0].attrib['href']
'''

page_id = 1
last__start = 0

while 1:
    #页码提取
    start_id = 20*(page_id - 1)
    url = 'https://book.douban.com/tag/%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C?start={}&type=T'.format(start_id)
    douban_crawler = MyCrawler('douban.txt')
    content = douban_crawler.download(url)
    douban_tree = html.fromstring(content)
    book_infos = douban_tree.xpath('//*[@id="subject_list"]/ul/li')
    print(url)
    #找到页码链接并提取最后一页的关键字
    if page_id == 1:
        page_link = douban_tree.xpath("//div[@class='paginator']/a[last()]/@href")
        if page_link:
            last_start = int(re.findall('start=(\d+)',page_link[0])[0])
            print('Last_start ID:',last_start)
    for book_info in book_infos:
        book_name_elem = book_info.xpath('.//h2/a')[0]
        #书名：
        book_name = re.sub('\s{2,}','',book_name_elem.text_content().replace('\n',''))                                                          
        book_url = book_name_elem.attrib['href']
        #出版信息：
        book_pub_info = book_info.xpath(".//div[@class='pub']")[0].text.strip()
        #评分：
        book_review_elem = book_info.xpath("//li[@class='subject-item']/div[@class='info']/div[@class='star clearfix']")
        book_grade_elem = book_review_elem[0].xpath("//li[@class='subject-item']/div[@class='info']/div[@class='star clearfix']/span[@class='rating_nums']")
        book_grade = '0'
        if book_grade_elem:
            book_grade = book_grade_elem[0].text.strip()
        #书籍信息：
        '''
        由于个别书籍没有书籍信息介绍，所以需要把这部分书籍跳过
        '''
        book_intro = 'N/A'
        book_intro_elem = book_info.xpath(".//div[@class='info']/p")
        if book_intro_elem:
            book_intro = book_intro_elem[0].text.strip()
        print(book_name,book_url,'\n')
        #break
    page_id += 1
    if start_id == last_start:
        break