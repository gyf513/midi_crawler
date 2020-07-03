import requests
from bs4 import BeautifulSoup
import os
import time
from time import sleep
import random
from collections import Counter
import csv


def midiworld_crawler():
	BASE_URL = 'https://www.midiworld.com/search/'
	headers = {
		# 自行添加
	}
	styles = ['blues', 'jazz', 'pop', 'rock', 'movie%20themes', 'christmas%20carols', 'disney%20themes', 'country', 'rap', 'punk', 'dance', 'video%20game%20themes']
	
	# 新建目录
	if not os.path.exists('./midiworld'):
		os.mkdir('./midiworld')
	for style in styles:
		if not os.path.exists('./midiworld/' + style):
			os.mkdir('./midiworld/' + style)
	
	# 爬取记录
	csv_file = open('./midiworld/record.csv', 'a')
	csv_writer = csv.writer(csv_file)
	song_num = Counter()
	
	# 数据爬取
	for style in styles:
		print('===== 开始爬取:', style)
		
		for i in range(1, 1000): # page number
			url = BASE_URL + str(i) + '/?q=' + style
			r = requests.get(url, headers=headers, timeout=20)
			if (r.status_code != 200):
				print('获取网页失败: ',r)
				sleep(random.random()*10)
				continue
				
			sleep(random.random()/5)
			bs = BeautifulSoup(r.text, 'html.parser')
			hrefs = bs.select('a[target="_blank"]')
			
			if len(hrefs) == 0:
				break
				
			for href in hrefs:
				name = href.parent.next_element.strip('\n').strip(' - ').replace('/', '_')
				url = href['href']
				id = url.split('/')[-1]
				r = requests.get(url, headers=headers, timeout=30)
				sleep(random.random()/5)
				
				if (r.status_code != 200):
					print('下载失败: ',href)
					sleep(random.random()*10)
					continue
				
				try:
					with open('./midiworld/' + style + '/' + str(id) + '_' + name + '.midi', 'wb') as f:
						f.write(r.content)
						csv_writer.writerow( (id, style, name, url) )
						song_num[style] += 1
				except:
					print('保存失败: ', './midiworld/' + style + '/' + str(id) + '_' + name + '.midi')
					
				
			print('========== ' + style + '第' + str(i) + '页已完成, 累计数目: ' + str(song_num[style]))	
				
		print('===== ' + style + '爬取完成, 共计' + str(song_num[style]) + '首\n\n')
		
	csv_file.close()
	
	
	
	

if __name__ == '__main__':
	midiworld_crawler()
			
	
	