#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys ,json, datetime

from collections import OrderedDict

reload(sys)
sys.setdefaultencoding("utf-8")

# Open a file
path = "javbus"
dirs = os.listdir( path )

json_list = []
base_time = 1422105062

image_list = []
# This would print all the files and directories
for file in dirs:

    common_path = os.path.join(path, file,file);
    json_path = common_path+ ".json"

    json_data=open(json_path).read()


    data = json.loads(json_data)

    data['fanhao'] = file

    if os.path.exists(common_path+"l.jpg"):
        data['image'] = 'data/img/jav/'+file+"l.jpg"
        image_list.append(common_path+"l.jpg")
    elif os.path.exists(common_path+"s.jpg"):
        data['image'] = 'data/img/jav/'+file+"s.jpg"
        image_list.append(common_path+"s.jpg")

    try:
        with open(os.path.join(path, file, file+"-magnet.txt") ) as f:
            data['magnets'] = f.read().splitlines()
    except IOError:
        pass

    json_list.append(data)


json_list.sort(key=lambda data: datetime.datetime.strptime(data['date'],'%Y-%m-%d'),reverse=True)

post_list = []

for idx,json_object in enumerate(json_list):


    pic="配图暂缺\n"

    if 'image' in json_object.keys():
        pic="![]("+json_object['image']+")\n"

    body = pic + \
            '发布日期:'+json_object['date'] + '\n'+ \
            '系列:'+json_object['series'] + '\n' + \
            '分类:'+','.join(json_object['category']) + '\n' +  \
            '女优:' + ','.join( json_object['actress']) + '\n' +\
            'downloads:' 

    if 'magnets' in json_object.keys():
        for i,url in enumerate(json_object['magnets']):
            body = body + '[磁力链接%d](%s)\n'%(i+1,url)
    else:
        body = body + '暂缺'



    post = OrderedDict([('post_id',len(json_list)-idx),
            ('title',json_object['title']),
            ('date_published', base_time - idx),
            ('body', body)])
    post_list.append(post)

all_object=OrderedDict([
        ("title", "ZeroBlog"),
	("description", "Demo for decentralized, self publishing blogging platform."),

	("links", "- [Create new blog](?Post:3:How+to+have+a+blog+like+this)\n\n- [How does ZeroNet work?](?Post:34:Slides+about+ZeroNet)\n- Site development tutorial: [Part1](?Post:43:ZeroNet+site+development+tutorial+1), [Part2](?Post:46:ZeroNet+site+development+tutorial+2)\n- [ZeroNet documents](http://zeronet.readthedocs.org/)\n- [Source code](https://github.com/HelloZeroNet)"),
	("next_post_id", len(post_list)+1),
	("demo", False),
	("modified", base_time+len(post_list)+1),
        ('post',post_list)])
        
    
json_str = json.dumps(all_object,ensure_ascii=False,indent=4).encode('utf8')

out_file = open('data.json',"w")
out_file.write(json_str)


for i in image_list:
    print (i)

