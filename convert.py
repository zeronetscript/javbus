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

# This would print all the files and directories
for file in dirs:
    json_path = os.path.join(path, file,file + ".json")
    #print ('process '+file)
    json_data=open(json_path).read()

    data = json.loads(json_data)

    try:
        with open(os.path.join(path, file, file+"-magnet.txt") ) as f:
            data['magnets'] = f.read().splitlines()
    except IOError:
        pass

    json_list.append(data)


json_list.sort(key=lambda data: datetime.datetime.strptime(data['date'],'%Y-%m-%d'))

post_list = []

for idx,json_object in enumerate(json_list):



    body = '发布日期:'+json_object['date'] + '\n'+ \
            '系列:'+json_object['series'] + '\n' + \
            '分类:'+','.join(json_object['category']) + '\n' +  \
            'actress:' + ','.join( json_object['actress']) + '\n' +\
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
print (json_str)
