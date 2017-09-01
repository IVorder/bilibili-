#! /usr/bin/python
# coding = utf-8
import jieba 
import requests 
import re,os
import random
from os import path
from scipy.misc import imread
from wordcloud import WordCloud,ImageColorGenerator

class get_bilibili_random_headers(object) :
	
	def __init__(self,user_agent_list):
		self.user_agent_list = [
					"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
					"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
					"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
					"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
					"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
					"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
					"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
					"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
					"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
					"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
					"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
					"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
					"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
					"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
					"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
					"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
					"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
					"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
						]
	def get_html_bilibili(self):
		headers=random.choice(self.user_agent_list)
		return headers
def bili_av(bi_url_av=''): #av号获取cid和把标题
	bi_url='https://www.bilibili.com/video/'+bi_url_av
	html=bilibili_html_get(bi_url)
	reg_title=r'le"><h1 title="(.+?)"'#视频标题
	reg_cid =r'cid=(.+?)&'#弹幕链接
	title="".join(re.findall(re.compile(reg_title),html))
	cid="".join(re.findall(re.compile(reg_cid),html))
	print('视频标题：%s'%title)
	return cid

def bilibili_html_get(html):#得到html
	bilibili_random_headers=get_bilibili_random_headers('self')
	bili_headers ={'User-Agent':bilibili_random_headers.get_html_bilibili()}
	bi_html =requests.get(html,headers=bili_headers,timeout=3).content
	bi_html = str(bi_html,'utf-8')
	return bi_html#得到html

def bilibili_get_danmu(cid) :#得到弹幕
	bili_danmu_html = 'http://comment.bilibili.com/'+cid+'.xml'#构建弹幕网站链接
	html=bilibili_html_get(bili_danmu_html)
	reg_dm =r'">(.+?)</d'
	dm_list=re.findall(re.compile(reg_dm),html)
	dm_list=",".join(dm_list)
	dm_list=" ".join(jieba.lcut(dm_list))
	return dm_list

def creater_wordcloud(dm_list,image='image.jpg',font='叶立群几何体.ttf'):
	if os.path.exists(font)==False :
		font='C:/Windows/Fonts/simsun.ttc'
	if os.path.exists(image)==False :
		print('默认图片丢失，请重新运行尝试输入指定图片')	
		os._exit()
	back_coloring = imread(path.join(image))
	bilibili = WordCloud( font_path=font,#设置字体
	                background_color="#fff", #背景颜色
	                max_words=5000,# 词云显示的最大词数
	                mode='RGBA',#产生透明图层
	                mask=back_coloring,#设置背景图片
	                #max_font_size=100, #字体最大值
	                scale=1.5,
	                random_state= 30 ,
	                )
	bilibili.generate(dm_list)
	image_colors = ImageColorGenerator(back_coloring)
	if os.path.exists('bilibili.png')==False :
		bilibili.to_file(path.join('bilibili.png'))
	else :
		bilibili.to_file(path.join('bilibili_%s.png')%random.randint(1,100))

def check_input():#检测输入数据
	while (True):
		av_ls=input("请输入bilibili AV号：").strip()
		if av_ls[:2]=='av' :
			try :
				int(av_ls[2:])
				av=av_ls
				break
			except :
				print("输入的av号有错\n请重新输入av号:")
		else :
			try :
				int(av_ls)
				av = 'av'+ av_ls
				break
			except :
				print("输入的av号有错\n请重新输入av号:")
	return av

def  get(defa='n'):
	print('是否改变默认图片(y/n)',end='')
	yn = input()
	if yn=='':
		return defa
	return yn

def main():
	av=check_input()
	#av ='av13829826'
	cid=bili_av(av)#av号获取cid和把标题
	text=bilibili_get_danmu(cid)#cid得到弹幕
	yn=get()
	while(True) :
		if yn=='y' or yn=='Y':
			mu=input('请输入图片目录：')
			if mu[4:]=='.jpg' or  mu[4:]=='png':
				try :
					creater_wordcloud(text,mu)
					break
				except :
					print('图片目录不存在')
			else :
				try :
					creater_wordcloud(text,'%s.jpg'%mu)
					break
				except :
					creater_wordcloud(text,'%s.png'%mu)
					break
				else :
					print('图片目录不存在')
		elif yn=='n' or yn=='N':
			creater_wordcloud(text)
			break
		else :
			print('输入图片目录错误,请重新输入')

if __name__ == '__main__':
	main()
