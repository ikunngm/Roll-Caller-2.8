from chardet.universaldetector import UniversalDetector
import pyttsx3,pygame,random,time,sys,os,re
from tkinter import filedialog
from random import choice
from 变量 import*
#默认背景
def build_background():
	pygame.draw.rect(screen,(239,136,190),(photo_background_x,photo_background_y,1000,500),0)
#名单兼容性检查工具
def names_list_utf_8_tool():  
    global text_names_list,names_list_last,list_already,names_list_utf_8#声明全局变量
    names_list_name = os.path.basename(names_list)#截取文件名
    text_names_list = font_30_size.render(("当前的名单是:" + names_list_name),True,(0,0,0))
    #检测名单文件字体类型
    try_text = UniversalDetector()
    try_text.reset()
    for test_txt in open(names_list,"rb"):
        try_text.feed(test_txt)
        if try_text.done:
            break
    try_text.close()
    #判断名单文件是否需要更改为utf-8
    if try_text.result["encoding"] != "utf-8":
		#打开名单文件+将内容写入列表中
        with open(names_list,"r") as open_names_list:
            names_list_read = open_names_list.readlines()
		#创建临时文件+将列表(名单文件)内容以utf-8格式写入临时文件
        with open("用户数据/临时名单.txt","w",encoding = "utf-8") as names_list_utf_8:
            names_list_utf_8.writelines(names_list_read)
            names_list_utf_8 = "用户数据/临时名单.txt"
    else:
        names_list_utf_8 = names_list  
    names_list_last = names_list#保存选择的路径  
    list_already = True#已选择名单
#创建文件夹
if not os.path.exists(names_list_folder):
	os.makedirs(names_list_folder)
if not os.path.exists(music_folder):
	os.makedirs(music_folder)
if not os.path.exists(background_folder):
	os.makedirs(background_folder)
if not os.path.exists(start_music_folder):
	os.makedirs(start_music_folder)
if not os.path.exists("用户数据/"):
	os.makedirs("用户数据/")
#检测音乐文件名称
music_list = os.listdir(music_folder)
for music in music_list:
	if music.endswith(".mp3") or music.endswith(".wav"):
		text_music_name = font_30_size.render(("当前的音乐是:" + music),True,(0,0,0))
		music = music_folder + music#喂给播放器的音乐路径
		music_last = music#保存选择的路径
#检测启动音乐文件名称
start_music_list = os.listdir(start_music_folder)
for start_music in start_music_list:
	if start_music.endswith(".mp3") or start_music.endswith(".wav"):
		start_music = start_music_folder + start_music#喂给播放器的音乐路径		
		start_music_switch = True#允许播放启动音乐
		#播放启动音乐
		pygame.mixer.music.load(start_music)
		pygame.mixer.music.set_volume(0.5)
		pygame.mixer.music.play()
#检测背景文件名称
background_list = os.listdir(background_folder)
for background in background_list:
	if background.endswith(".jpg") or background.endswith(".png"):
		background = background_folder + background#喂给pygame的背景路径
		#用户自定义背景
		photo_background = pygame.image.load(background).convert()
		def build_background():
			screen.blit(photo_background,(photo_background_x,photo_background_y))
#检测名单文件名称
names_list_list = os.listdir(names_list_folder)
for names_list in names_list_list:
	if names_list.endswith(".txt"):
		names_list = names_list_folder + names_list#喂给pygame的名单路径
		names_list_utf_8_tool()#名单兼容性检查
try:
	with open("用户数据/名单路径.txt",encoding = "utf-8") as names_list_data:
		names_list = names_list_data.readline()
		if names_list != "" and os.path.exists(names_list):				
			names_list_utf_8_tool()#名单兼容性检查
finally:				
	try:
		with open("用户数据/音乐路径.txt",encoding = "utf-8") as music_data:
			music = music_data.readline()
			if music != "" and os.path.exists(music) == True:				
				music_last = music#保存选择的路径				
				music_name = os.path.basename(music)#截取文件名
				text_music_name = font_30_size.render(("当前的音乐是:" + music_name),True,(0,0,0))					
	finally:
		while True:
			for user_input in pygame.event.get():	
				mouse = pygame.mouse.get_pos()
				#退出
				if user_input.type == pygame.QUIT:
					pygame.quit()
					try:
						os.remove(r"用户数据/临时名单.txt")#删除临时名单
					finally:
						sys.exit()
				#点击判定
				if user_input.type == pygame.MOUSEBUTTONDOWN:	
					#选名单
					if 0 <= mouse[0] <= 250 and 400 <= mouse[1] <= 500:
						if set_enter == False:
							if start_music_switch == True:
								pygame.mixer.music.stop()#停止音乐
								start_music_switch = False#不允许播放启动音乐
							#防止三连抽或幸运单抽运行时其他按钮被点击造成卡死
							names_3_fast_switch = False#关闭快速三连抽
							names_3_switch = False#关闭三连抽
							names_3_time = 0#未点击"三连抽"
							name_fast_switch = False#关闭快速幸运单抽
							name_switch = False#关闭幸运单抽
							name_time = 0#未点击"幸运单抽"
							pygame.draw.rect(screen,(255,255,255),(0,400,250,100),1)#绘制白色按钮特效矩形
							pygame.display.update()#更新屏幕
							time.sleep(0.1)#特效延迟
							pygame.draw.rect(screen,(0,0,0),(0,400,250,100),1)#绘制黑色按钮特效矩形
							pygame.display.update()#更新屏幕
							#选名单窗口
							names_list = filedialog.askopenfilename(title = "请选择名单",filetypes = [("文本文档",".txt")])
							if names_list != "":
								#保存名单路径
								with open("用户数据/名单路径.txt","w",encoding = "utf-8") as names_list_data:
									names_list_data.write(names_list)
								names_list_utf_8_tool()#名单兼容性检查
								names_3_already = False#三连抽未完成
								name_already = False#幸运单抽未完成
							else:
								if list_already == True:
									names_list = names_list_last#调用上一次选择的路径
					#三连抽
					if 250 <= mouse[0] <= 500 and 400 <= mouse[1] <= 500:	
						if set_enter == False and list_already == True:
							if start_music_switch == True:
								pygame.mixer.music.stop()#停止音乐
								start_music_switch = False#不允许播放启动音乐
							#防止幸运单抽运行时"三连抽"被点击造成卡死
							name_fast_switch = False#关闭快速幸运单抽
							name_switch = False#关闭幸运单抽
							name_already = False#幸运单抽未完成
							name_time = 0#未点击"幸运单抽"
							names_3_time += 1#第1次点击"三连抽"
							#三连抽特效模式
							names_3_module = random.randint(1,int(1/0.5))
							if names_3_module == 1:
								lucky_names_3_1_x = 130#三连抽第1个名字X轴初始位置
								lucky_names_3_1_y = -60#三连抽第1个名字y轴初始位置
								lucky_names_3_2_x = 430#三连抽第2个名字X轴初始位置
								lucky_names_3_2_y = -60#三连抽第2个名字y轴初始位置
								lucky_names_3_3_x = 730#三连抽第3个名字X轴初始位置 							
								lucky_names_3_3_y = -60#三连抽第3个名字y轴初始位置
							else:
								lucky_names_3_1_x = -300#三连抽第1个名字X轴初始位置
								lucky_names_3_1_y = 145#三连抽第1个名字y轴初始位置
								lucky_names_3_2_x = 430#三连抽第2个名字X轴初始位置
								lucky_names_3_2_y = -60#三连抽第2个名字y轴初始位置
								lucky_names_3_3_x = 1300#三连抽第3个名字X轴初始位置 							
								lucky_names_3_3_y = 145#三连抽第3个名字y轴初始位置
							speak_start = False#停止朗读						
							names_3_speak_time = 3#三连抽朗读次数
							if music_switch == True:
								pygame.mixer.music.unpause()#继续播放
								play = pygame.mixer_music.get_busy()#是否正在播放音乐
								if play == False:    
									#播放音乐
									pygame.mixer.music.load(music)
									pygame.mixer.music.set_volume(0.5)
									pygame.mixer.music.play()
							#第1次点击
							if names_3_time == 1:
								names_3_fast_switch = True#启动快速三连抽
								names_3_switch = False#关闭三连抽
								names_3_already = False#三连抽未完成
							#第2次点击
							if names_3_time >= 2:
								pygame.mixer.music.pause()#暂停音乐
								names_3_switch = True#启动三连抽
								names_3_fast_switch = False#关闭快速三连抽
								names_3_time = 0#未点击"三连抽"
					#幸运单抽
					if 500 <= mouse[0] <= 750 and 400 <= mouse[1] <= 500:
						if set_enter == False and list_already == True:
							if start_music_switch == True:
								pygame.mixer.music.stop()#停止音乐
								start_music_switch = False#不允许播放启动音乐
							#防止三连抽运行时"幸运单抽"被点击造成卡死
							names_3_fast_switch = False#关闭快速三连抽
							names_3_switch = False#关闭三连抽
							names_3_already = False#三连抽未完成
							names_3_time = 0#未点击"三连抽"
							name_time += 1#第1次点击"幸运单抽"
							#幸运单抽特效模式
							name_module = random.randint(1,int(1/0.3))
							if name_module == 1:
								lucky_name_x = 430#幸运单抽名字X轴初始位置
								lucky_name_y = -60#幸运单抽名字y轴初始位置								
							if name_module == 2:
								lucky_name_x = 1300#幸运单抽名字X轴初始位置
								lucky_name_y = 145#幸运单抽名字y轴初始位置
							if name_module == 3:
								lucky_name_x = -300#幸运单抽名字X轴初始位置
								lucky_name_y = 145#幸运单抽名字y轴初始位置
							speak_start = False#停止朗读							
							name_speak_time = 1#幸运单抽朗读次数
							if music_switch == True:
								pygame.mixer.music.unpause()#继续播放
								play = pygame.mixer_music.get_busy()#是否正在播放音乐
								if play == False:    
									#播放音乐
									pygame.mixer.music.load(music)
									pygame.mixer.music.set_volume(0.5)
									pygame.mixer.music.play()
							#第1次点击
							if name_time == 1:
								name_fast_switch = True#启动快速幸运单抽
								name_switch = False#关闭幸运单抽
								name_already = False#幸运单抽未完成
							#第2次点击
							if name_time >= 2:
								pygame.mixer.music.pause()#暂停音乐
								name_switch = True#启动幸运单抽
								name_fast_switch = False#关闭快速幸运单抽
								name_time = 0#未点击"幸运单抽"
					#设置
					if 750 <= mouse[0] <= 1000 and 400 <= mouse[1] <= 500:
						if set_enter == False:
							if start_music_switch == True:
								pygame.mixer.music.stop()#停止音乐
								start_music_switch = False#不允许播放启动音乐
							pygame.mixer.music.pause()#暂停音乐
							#防止三连抽或幸运单抽运行时其他按钮被点击造成卡死							
							names_3_fast_switch = False#关闭快速三连抽						
							names_3_switch = False#关闭三连抽							
							names_3_time = 0#未点击"三连抽"							
							name_fast_switch = False#关闭快速幸运单抽							
							name_switch = False#关闭幸运单抽						
							name_time = 0#未点击"幸运单抽"					
							pygame.draw.rect(screen,(255,255,255),(750,400,250,100),1)#绘制白色按钮特效矩形							
							pygame.display.update()#更新屏幕							
							time.sleep(0.1)#特效延迟							
							pygame.draw.rect(screen,(0,0,0),(750,400,250,100),1)#绘制黑色按钮特效矩形						
							pygame.display.update()#更新屏幕							
							time.sleep(0.1)#特效延迟
							set_enter = True#设置已打开
					#返回				
					if 0 <= mouse[0] <= 100 and 0 <= mouse[1] <= 50:
						if set_enter == True:							
							pygame.mixer.music.pause()#暂停音乐
							pygame.draw.rect(screen,(255,255,255),(0,0,100,50),1)#绘制白色按钮特效矩形							
							pygame.display.update()#更新屏幕							
							time.sleep(0.1)#特效延迟							
							pygame.draw.rect(screen,(0,0,0),(0,0,100,50),1)#绘制黑色按钮特效矩形							
							pygame.display.update()#更新屏幕						
							time.sleep(0.1)#特效延迟							
							set_enter = False#设置已关闭
					#选音乐				
					if 0 <= mouse[0] <= 250 and 90 <= mouse[1] <= 190:
						if set_enter == True and music_switch == True:						
							pygame.draw.rect(screen,(255,255,255),(0,90,250,100),1)#绘制白色按钮特效矩形							
							pygame.display.update()#更新屏幕							
							time.sleep(0.1)#特效延迟							
							pygame.draw.rect(screen,(0,0,0),(0,90,250,100),1)#绘制黑色按钮特效矩形							
							pygame.display.update()#更新屏幕							
							pygame.mixer.music.unload()#卸载掉上一首音乐
							#选音乐窗口
							music = filedialog.askopenfilename(title = "请选择音乐",filetypes = [("音乐",".mp3"),("音乐",".wav")])
							if music != "":
								#保存音乐路径
								with open("用户数据/音乐路径.txt","w",encoding = "utf-8") as music_data:
									music_data.write(music)
								music_last = music#保存选择的路径
								music_name = os.path.basename(music)#截取文件名
								text_music_name = font_30_size.render(("当前的音乐是:" + music_name),True,(0,0,0))
							else:
								music = music_last#调用上一次选择的路径
					#音乐开关
					if 25 <= mouse[0] <= 75 and 242 <= mouse[1] <= 267:
						if set_enter == True:		
							pygame.draw.rect(screen,(255,255,255),(25,242,50,25),1)#绘制白色按钮特效矩形					
							pygame.display.update()#更新屏幕							
							time.sleep(0.1)#特效延迟						
							pygame.draw.rect(screen,(0,0,0),(25,242,50,25),1)#绘制黑色按钮特效矩形						
							pygame.display.update()#更新屏幕	
							if music_switch == True:									
								music_switch = False#音乐开关已关闭			
							else:								
								music_switch = True#音乐开关已打开
					#朗读开关
					if 25 <= mouse[0] <= 75 and 332 <= mouse[1] <= 357:
						if set_enter == True:						
							pygame.draw.rect(screen,(255,255,255),(25,332,50,25),1)#绘制白色按钮特效矩形						
							pygame.display.update()#更新屏幕							
							time.sleep(0.1)#特效延迟							
							pygame.draw.rect(screen,(0,0,0),(25,332,50,25),1)#绘制黑色按钮特效矩形						
							pygame.display.update()#更新屏幕
							if speak_switch == True:									
								speak_switch = False#朗读开关已关闭			
							else:							
								speak_switch = True#朗读开关已打开
					#帮助
					if 0 <= mouse[0] <= 100 and 370 <= mouse[1] <= 420:
						if set_enter == True:							
							pygame.draw.rect(screen,(255,255,255),(0,370,100,50),1)#绘制白色按钮特效矩形						
							pygame.display.update()#更新屏幕							
							time.sleep(0.1)#特效延迟						
							pygame.draw.rect(screen,(0,0,0),(0,370,100,50),1)#绘制黑色按钮特效矩形							
							pygame.display.update()#更新屏幕
							os.system(r"notepad 关于/帮助.txt")#打开"帮助.txt"
					#关于
					if 0 <= mouse[0] <= 100 and 420 <= mouse[1] <= 470:
						if set_enter == True:						
							pygame.draw.rect(screen,(255,255,255),(0,420,100,50),1)#绘制白色按钮特效矩形						
							pygame.display.update()#更新屏幕						
							time.sleep(0.1)#特效延迟							
							pygame.draw.rect(screen,(0,0,0),(0,420,100,50),1)#绘制黑色按钮特效矩形
							pygame.display.update()#更新屏幕
							os.system(r"notepad 关于/关于.txt")#打开"关于.txt"
			#UI绘制
			#绘制主界面
			photo_background_x = 0#背景X轴位置
			photo_background_y = 0#背景y轴位置
			build_background()#绘制背景
			#选名单			
			pygame.draw.rect(screen,(0,0,0),(0,400,250,100),1)#绘制黑色按钮特效矩形			
			pygame.draw.rect(screen,(255,201,13),(1,401,248,98),0)#绘制选名单矩形
			screen.blit(text_choose_list,(55,420))#打印选名单字体
			#三连抽
			pygame.draw.rect(screen,(0,0,0),(250,400,250,100),1)#绘制黑色按钮特效矩形			
			pygame.draw.rect(screen,(237,27,36),(251,401,248,98),0)#绘制三连抽矩形			
			screen.blit(text_names_3,(300,420))#打印三连抽字体
			#幸运单抽			
			pygame.draw.rect(screen,(0,0,0),(500,400,250,100),1)#绘制黑色按钮特效矩形			
			pygame.draw.rect(screen,(35,177,77),(501,401,248,98),0)#绘制幸运单抽矩形
			screen.blit(text_name,(530,420))#打印幸运单抽字体
			#设置			
			pygame.draw.rect(screen,(0,0,0),(750,400,250,100),1)#绘制黑色按钮特效矩形			
			pygame.draw.rect(screen,(255,127,38),(751,401,248,98),0)#绘制设置矩形
			screen.blit(text_set,(820,420))#打印设置字体
			screen.blit(text_music_name,(0,325))#打印音乐文件名
			if music_switch == False:				             
				screen.blit(music_state,(0,320))#状态栏阴影
			if list_already == True:	
				screen.blit(text_names_list,(0,365))#打印名单文件名
			else:
				screen.blit(warn_list,(375,145))#警告
			if speak_switch == True:
				screen.blit(text_speak_switch_on,(850,365))#朗读开关已打开
			else:
				screen.blit(text_speak_switch_off,(850,365))#朗读开关已关闭
			def print_names_3_1():
				global names_3_speak_time#声明全局变量
				screen.blit(text_lucky_names_3_1,(lucky_names_3_1_x,lucky_names_3_1_y))#打印第1个人的姓名
				if names_3_speak_time == 0:
					if speak_switch == True:
						pygame.display.update()#更新屏幕
						pyttsx3.speak(names_3_1)#朗读第1个人的姓名				
					names_3_speak_time += 1#第1次朗读
			def print_names_3_2():
				global names_3_speak_time#声明全局变量
				screen.blit(text_lucky_names_3_2,(lucky_names_3_2_x,lucky_names_3_2_y))#打印第2个人的姓名
				if names_3_speak_time == 1 and lucky_names_3_2_x == 430 and lucky_names_3_2_y == 145:
					if speak_switch == True:
						pygame.display.update()#更新屏幕
						pyttsx3.speak(names_3_2)#朗读第2个人的姓名
					names_3_speak_time += 1#第2次朗读
			def print_names_3_3():
				global names_3_speak_time#声明全局变量
				screen.blit(text_lucky_names_3_3,(lucky_names_3_3_x,lucky_names_3_3_y))#打印第3个人的姓名
				if names_3_speak_time == 2 and lucky_names_3_3_x == 730 and lucky_names_3_3_y == 145:
					if speak_switch == True:
						pygame.display.update()#更新屏幕
						pyttsx3.speak(names_3_3)#朗读第3个人的姓名	
					names_3_speak_time += 1#第3次朗读
			def print_name():
				global name_speak_time#声明全局变量
				screen.blit(text_lucky_name,(lucky_name_x,lucky_name_y))#打印幸运儿的姓名
				if speak_switch == True and name_speak_time == 0:
					pyttsx3.speak(name)#朗读幸运儿的姓名
				name_speak_time += 1#第1次朗读
			#三连抽姓名打印及朗读
			if names_3_already == True and move_set_x != -1000:
				if names_3_module == 1:
					if lucky_names_3_1_y == 145 and speak_start == False:
						names_3_speak_time = 0
						speak_start = True#开始朗读
					if lucky_names_3_1_y != 145:
						lucky_names_3_1_y += 1
					if lucky_names_3_1_y == 145 and lucky_names_3_2_y != 145:
						lucky_names_3_2_y += 1
					if lucky_names_3_2_y == 145 and lucky_names_3_3_y != 145:
						lucky_names_3_3_y += 1
					print_names_3_1()
					print_names_3_2()
					print_names_3_3()
				else:
					if lucky_names_3_1_x == 130 and speak_start == False:
						names_3_speak_time = 0
						speak_start = True#开始朗读
					if lucky_names_3_1_x != 130:
						lucky_names_3_1_x += 1
					if lucky_names_3_1_x == 130 and lucky_names_3_2_y != 145:
						lucky_names_3_2_y += 1
					if lucky_names_3_2_y == 145 and lucky_names_3_3_x != 730:
						lucky_names_3_3_x -= 2
					print_names_3_1()
					print_names_3_2()
					print_names_3_3()
				names_3_switch = False#关闭三连抽
			#幸运单抽姓名打印及朗读
			if name_already == True and move_set_x != -1000:
				if name_module == 1:
					if lucky_name_y == 145 and speak_start == False:
						name_speak_time = 0
						speak_start = True#开始朗读
					if lucky_name_y != 145:
						lucky_name_y += 1
					print_name()
				if name_module == 2:
					if lucky_name_x == 430 and speak_start == False:
						name_speak_time = 0
						speak_start = True#开始朗读
					if lucky_name_x != 430:
						lucky_name_x -= 2
					print_name()
				if name_module == 3:
					if lucky_name_x == 430 and speak_start == False:
						name_speak_time = 0
						speak_start = True#开始朗读
					if lucky_name_x != 430:
						lucky_name_x += 2
					print_name()	
				name_switch = False#关闭幸运单抽
			#绘制设置界面
			photo_background_x = 1000 + move_set_x#背景X轴位置
			photo_background_y = 500 + move_set_y#背景y轴位置
			build_background()#绘制背景
			#返回
			pygame.draw.rect(screen,(0,0,0),(1000 + move_set_x,500 + move_set_y,100,50),1)#绘制黑色按钮特效矩形			
			pygame.draw.rect(screen,(185,122,87),(1001 + move_set_x,501 + move_set_y,98,48),0)#绘制返回矩形		
			screen.blit(text_back,(1020 + move_set_x,507 + move_set_y))#打印返回字体
			#选音乐			
			pygame.draw.rect(screen,(0,0,0),(1000 + move_set_x,590 + move_set_y,250,100),1)#绘制黑色按钮特效矩形			
			pygame.draw.rect(screen,(0,162,234),(1001 + move_set_x,591 + move_set_y,248,98),0)#绘制选音乐矩形		
			screen.blit(text_choose_music,(1050 + move_set_x,610 + move_set_y))#打印选音乐字体
			#帮助		
			pygame.draw.rect(screen,(0,0,0),(1000 + move_set_x,870 + move_set_y,100,50),1)#绘制黑色按钮特效矩形			
			pygame.draw.rect(screen,(106,59,187),(1001 + move_set_x,871 + move_set_y,98,48),0)#绘制帮助矩形		
			screen.blit(text_help,(1020 + move_set_x,877 + move_set_y))#打印帮助字体
			#关于		
			pygame.draw.rect(screen,(0,0,0),(1000 + move_set_x,920 + move_set_y,100,50),1)#绘制黑色按钮特效矩形		
			pygame.draw.rect(screen,(179,229,33),(1001 + move_set_x,921 + move_set_y,98,48),0)#绘制关于矩形	
			screen.blit(text_about,(1020 + move_set_x,927 + move_set_y))#打印关于字体
			#音乐开关	
			if music_switch == True and move_music_switch_x < 24:
				move_music_switch_x += 1#打开音乐开关时开关滑块移动的距离	
			if music_switch == False and move_music_switch_x > 0:
				move_music_switch_x -= 1#关闭音乐开关时开关滑块移动的距离			
			move_music_switch_x_black = 0 - move_music_switch_x#黑色部分移动的距离转换
			if music_switch == True:
				#白色部分	
				music_switch_white = pygame.Surface((move_music_switch_x,23),pygame.SRCALPHA)
				music_switch_white.fill((255,255,255,128))
				screen.blit(music_switch_white,(1026 + move_set_x,743 + move_set_y))
				#黑色部分
				music_switch_black = pygame.Surface((24 + move_music_switch_x_black,23),pygame.SRCALPHA)
				music_switch_black.fill((0,0,0,128))
				screen.blit(music_switch_black,(1050 + move_music_switch_x_black + move_set_x,743 + move_set_y))				
				screen.blit(text_music_switch_on,(1000 + move_set_x,695 + move_set_y))#音乐开关已打开
			else:
				#白色部分
				music_switch_white = pygame.Surface((move_music_switch_x,23),pygame.SRCALPHA)
				music_switch_white.fill((255,255,255,128))
				screen.blit(music_switch_white,(1026,743))
				#黑色部分
				music_switch_black = pygame.Surface((24 + move_music_switch_x_black,23),pygame.SRCALPHA)
				music_switch_black.fill((0,0,0,128))
				screen.blit(music_switch_black,(1050 + move_music_switch_x_black + move_set_x,743 + move_set_y))
				screen.blit(text_music_switch_off,(1000 + move_set_x,695 + move_set_y))#音乐开关已关闭                
				screen.blit(music_state,(1000 + move_set_x,550 + move_set_y))#状态栏阴影   				                   
				screen.blit(choose_music_state,(1000 + move_set_x,590 + move_set_y))#选音乐阴影		   
			pygame.draw.rect(screen,(0,0,0),(1025 + move_set_x,742 + move_set_y,50,25),1)#绘制黑色按钮特效矩形
			pygame.draw.rect(screen,(199,191,230),(1026 + move_music_switch_x + move_set_x,743 + move_set_y,24,23),0)#音乐开关滑块
			#朗读开关		
			if speak_switch == True and move_speak_switch_x < 24:
				move_speak_switch_x += 1#打开朗读开关时开关滑块移动的距离				
			if speak_switch == False and move_speak_switch_x > 0:
				move_speak_switch_x -= 1#关闭朗读开关时开关滑块移动的距离
			move_speak_switch_x_black = 0 - move_speak_switch_x#黑色部分移动的距离转换
			if speak_switch == True:
				#白色部分	
				speak_switch_white = pygame.Surface((move_speak_switch_x,23),pygame.SRCALPHA)
				speak_switch_white.fill((255,255,255,128))
				screen.blit(speak_switch_white,(1026 + move_set_x,833 + move_set_y))
				#黑色部分
				speak_switch_black = pygame.Surface((24 + move_speak_switch_x_black,23),pygame.SRCALPHA)
				speak_switch_black.fill((0,0,0,128))
				screen.blit(speak_switch_black,(1050 + move_speak_switch_x_black + move_set_x,833 + move_set_y))				
				screen.blit(text_speak_switch_on,(1000 + move_set_x,785 + move_set_y))#朗读开关已打开
			else:
				#白色部分
				speak_switch_white = pygame.Surface((move_speak_switch_x,23),pygame.SRCALPHA)
				speak_switch_white.fill((255,255,255,128))
				screen.blit(speak_switch_white,(1026,743))
				#黑色部分
				speak_switch_black = pygame.Surface((24 + move_speak_switch_x_black,23),pygame.SRCALPHA)
				speak_switch_black.fill((0,0,0,128))
				screen.blit(speak_switch_black,(1050 + move_speak_switch_x_black + move_set_x,833 + move_set_y))				
				screen.blit(text_speak_switch_off,(1000 + move_set_x,785 + move_set_y))#朗读开关已关闭		
			pygame.draw.rect(screen,(0,0,0),(1025 + move_set_x,832 + move_set_y,50,25),1)#绘制黑色按钮特效矩形
			pygame.draw.rect(screen,(128,128,255),(1026 + move_speak_switch_x + move_set_x,833 + move_set_y,24,23),0)#朗读开关滑块
			screen.blit(text_music_name,(1000 + move_set_x,555 + move_set_y))#打印音乐文件名
			#逻辑判定
			#打开设置
			if set_enter == True and move_set_x != -1000:
				move_set_x -= 2
				move_set_y -= 1
			#关闭设置
			if set_enter == False and move_set_x != 0:
				move_set_x += 2
				move_set_y += 1
			#三连抽
			#快速三连抽
			if names_3_fast_switch == True and names_3_switch == False:
				pygame.draw.rect(screen,(255,255,255),(250,400,250,100),1)#绘制白色按钮特效矩形
				with open(names_list_utf_8,encoding = "utf-8") as names_list:
					names_lines = names_list.readlines()					
					names_3_fast_1 = choice(names_lines)#抽选第1个人
					names_3_fast_2 = choice(names_lines)#抽选第2个人
					names_3_fast_3 = choice(names_lines)#抽选第3个人
					names_3_fast_1 = re.sub(r"\n","",names_3_fast_1)#第1个人的姓名去除"\n"
					names_3_fast_2 = re.sub(r"\n","",names_3_fast_2)#第2个人的姓名去除"\n"
					names_3_fast_3 = re.sub(r"\n","",names_3_fast_3)#第3个人的姓名去除"\n"
					text_lucky_names_3_fast_1 = font_50_size.render((names_3_fast_1),True,(0,0,255))
					text_lucky_names_3_fast_2 = font_50_size.render((names_3_fast_2),True,(0,0,255))
					text_lucky_names_3_fast_3 = font_50_size.render((names_3_fast_3),True,(0,0,255))
					screen.blit(text_lucky_names_3_fast_1,(130,145))#打印第1个人的姓名									
					screen.blit(text_lucky_names_3_fast_2,(430,145))#打印第2个人的姓名									
					screen.blit(text_lucky_names_3_fast_3,(730,145))#打印第3个人的姓名	
			#真正的三连抽
			if names_3_switch == True:				
				pygame.draw.rect(screen,(0,0,0),(250,400,250,100),1)#绘制黑色按钮特效矩形
				while True:
					with open(names_list_utf_8,encoding = "utf-8") as names_list:
						names_lines = names_list.readlines()#将名单内容加入抽选列表
						names_3_1 = choice(names_lines)#抽选第1个人							
						names_3_2 = choice(names_lines)#抽选第2个人						
						names_3_3 = choice(names_lines)#抽选第3个人						
						names_3_1 = re.sub(r"\n","",names_3_1)#第1个人的姓名去除"\n"						
						names_3_2 = re.sub(r"\n","",names_3_2)#第2个人的姓名去除"\n"						
						names_3_3 = re.sub(r"\n","",names_3_3)#第3个人的姓名去除"\n"
						#防止同时出现的3个相同的名字
						if names_3_1 == names_3_2 or names_3_1 == names_3_3 or names_3_2 == names_3_3:
							continue
						#防重复列表					
						names_lines_max = len(names_lines)#人员名单长度
						#检测人员名单是否是3的倍数
						while True:
							if names_lines_max % 3 == 0:	
								names_lines_max_3 = names_lines_max
								break
							else:
								names_lines_max -= 1 
								continue
						#第1个人的姓名是否在防重复列表中
						if names_3_1 in pass_names_3:	
							continue
						#第2个人的姓名是否在防重复列表中
						if names_3_2 in pass_names_3:	
							continue
						#第3个人的姓名是否在防重复列表中
						if names_3_3 in pass_names_3:	
							continue					
						pass_names_3.append(names_3_1)#抽中的第1个人的姓名加入防重复列表					
						pass_names_3.append(names_3_2)#抽中的第2个人的姓名加入防重复列表
						pass_names_3.append(names_3_3)#抽中的第3个人的姓名加入防重复列表
						#防重复列表长度限制
						pass_names_max = len(pass_names_3)
						if pass_names_max == names_lines_max_3:
							pass_names_3.clear()
						text_lucky_names_3_1 = font_50_size.render((names_3_1),True,(0,0,255))
						text_lucky_names_3_2 = font_50_size.render((names_3_2),True,(0,0,255))
						text_lucky_names_3_3 = font_50_size.render((names_3_3),True,(0,0,255))
						names_3_already = True#三连抽已完成
						break
			#幸运单抽
			#快速幸运单抽
			if name_fast_switch == True and name_switch == False:
				pygame.draw.rect(screen,(255,255,255),(500,400,250,100),1)#绘制白色按钮特效矩形
				with open(names_list_utf_8,encoding = "utf-8") as names_list:
					names_lines = names_list.readlines()#将名单内容加入抽选列表
					name_fast = choice(names_lines)#抽选幸运儿
					name_fast = re.sub(r"\n","",name_fast)#幸运儿的姓名去除"\n"
					text_lucky_name_fast = font_50_size.render((name_fast),True,(0,0,255))
					screen.blit(text_lucky_name_fast,(430,145))#打印幸运儿的姓名
			#真正的幸运单抽
			if name_switch == True:
				pygame.draw.rect(screen,(0,0,0),(500,400,250,100),1)#绘制黑色按钮特效矩形
				while True:
					with open(names_list_utf_8,encoding = "utf-8") as names_list:
						names_lines = names_list.readlines()
						name = choice(names_lines)#抽选幸运儿			
						name = re.sub(r"\n","",name)#幸运儿的姓名去除"\n"
						#防重复列表
						names_lines_max = len(names_lines)#人员名单长度
						#幸运儿的姓名是否在防重复列表中
						if name in pass_names:
							continue
						pass_names.append(name)#幸运儿的姓名加入防重复列表
						#防重复列表长度限制
						pass_names_max = len(pass_names)
						if pass_names_max == names_lines_max:
							pass_names.clear()
						text_lucky_name = font_50_size.render((name),True,(0,0,255))
						name_already = True#幸运单抽已完成				
						break
			pygame.display.update()#更新屏幕