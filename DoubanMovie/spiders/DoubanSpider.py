#coding=utf-8
import sys
reload(sys)        #设置python默认环境编码格式（默认为ascii），设置成utf8后，爬到的内容就是utf-8的
sys.setdefaultencoding('utf-8')

from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from DoubanMovie.items import DBMovieItem

class DoubanSpider(BaseSpider):
	name='douban'
	allowed_domains=['movie.douban.com']
	start_urls=[]
	#file_object=None
	
	def start_requests(self):
		
		try:
			file_object=open('movie_name.txt','r')
	
		except IOError,e:
			print '打开电影名文件失败...',e.reason
		else:
			url_head="http://movie.douban.com/subject_search?search_text="
			for line in file_object:
				print line
				self.start_urls.append(url_head+line)
			for url in self.start_urls:
				yield self.make_requests_from_url(url.strip())
		finally:
			file_object.close()
	def parse(self,response):
		hxs=HtmlXPathSelector(response)
		movie_link=hxs.select('//*[@id="content"]/div/div[1]/div[2]/table[1]/tr/td[1]/a/@href').extract()

		if movie_link:
			yield Request(movie_link[0],callback=self.parse_item)
	
	def parse_item(self,response):
		hxs=HtmlXPathSelector(response)
		movie_name=hxs.select('//*[@id="content"]/h1/span[1]/text()').extract()
	
		movie_director=hxs.select('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
		movie_writer=hxs.select('//*[@id="info"]/span[2]/span[2]/a/text()').extract()
		movie_description_paths=hxs.select('//*[@id="link-report"]')
		for movie_description_path in movie_description_paths:
			movie_description=movie_description_path.select('.//*[@property="v:summary"]/text()').extract()
		movie_roles_paths=hxs.select('//*[@id="info"]/span[3]/span[2]')
		movie_roles=[]
		for movie_roles_path in movie_roles_paths:
			movie_roles=movie_roles_path.select('.//*[@rel="v:starring"]/text()').extract()
		print 'movie_name---------------',movie_writer
		item=DBMovieItem()
		return item
		#print movie_director
		#print movie_writer	
		#movie_language=re.search(pattern_)
