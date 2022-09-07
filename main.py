from pathlib import Path
from re import sub
import time
import json
import os

path=r"E:\storage\0\tv.danmaku.bili"
# 修改为视频的缓存地址(tv.danmaku.bili文件夹)
# 可以连接手机后直接输入手机中的路径，推荐使用数据线或WLAN连接
# 默认存放在手机根目录下的tv.danmaku.bili无法正常读取，需在b站手动修改缓存路径

path+=r"\download"
path=Path(path)
if not os.path.exists("output"):
    os.makedirs("output") 
videos=[video for video in path.iterdir() if video.is_dir()]
print("\n--共",len(videos),"个视频\n\n")
n=1
for video in videos:
    print("----视频",n,"/",len(videos))
    parts=[part for part in video.iterdir() if part.is_dir()]
    print("----共",len(parts),"p")
    i=1
    for part in parts:
        entry=list(part.glob("**/*entry.json"))[0]
        with open(entry, "r",encoding='UTF-8') as f:
            data = json.load(f)
        title=data[r'title']
        subtitle=data[r'page_data'][r'download_subtitle'].replace(title+' ','')
        p = r"[\/\\\:\*\?\"\<\>\|]"  # 替换不能用于文件名的字符为‘-’
        title=sub(p,'-',title)
        subtitle=sub(p,'-',subtitle)
        if not os.path.exists("output\\"+title):
            os.makedirs("output\\"+title)
        print("--------开始转换",i,"/",len(parts),": ",subtitle,"...")
        if not os.path.exists("output\\"+title+"\\"+subtitle+".mp4"):       
            video=str(list(part.glob("**/*video.m4s"))[0])
            audio=str(list(part.glob("**/*audio.m4s"))[0])
            command=".\\ffmpeg.exe -loglevel quiet -i "+video+" -i "+audio+" -codec copy \"output\\"+title+"\\"+subtitle+".mp4"
            os.system(command)
            print("--------转换完成!\n")
        else:
            print("--------文件已存在，跳过\n")
        i+=1
    n+=1
print("\n全部转换完成！请查看output\n5秒后自动退出......")
time.sleep(5)