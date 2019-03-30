#!/usr/bin/python
#coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2099 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 黄文良 <287962566@qq.com>
# +-------------------------------------------------------------------
#+--------------------------------------------------------------------
#|   宝塔系统加固程序
#+--------------------------------------------------------------------
import os ,sys ,json ,time ,re ,psutil #line:2
from datetime import datetime #line:3
os .chdir ('/www/server/panel')#line:4
sys .path .append ('class/')#line:5
import public #line:6
class syssafe_main :#line:7
    __OOO0O00O0O0O0OOOO ='plugin/syssafe/'#line:8
    __O0OOO0O00OOOO000O ={True :'开启',False :'关闭'}#line:9
    __O0O0O0O00O0O0OO00 =u'系统加固'#line:10
    __OOOO0O0OO00O000O0 ='/etc/hosts.deny'#line:11
    __OOOO000000O00000O ='/etc/hosts.allow'#line:12
    __O0O000000OOOOO00O ={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}#line:13
    __OO0OOO00000OO0000 =None #line:14
    __OO00OO0OOO00OOOO0 =None #line:15
    def check_sys_write (OO0O00OOO00OO0OO0 ):#line:16
        O0OO0O0O000OOOOOO ='/etc/init.d/bt_10000100.pl'#line:17
        public .writeFile (O0OO0O0O000OOOOOO ,'True')#line:18
        if os .path .exists (O0OO0O0O000OOOOOO ):#line:19
            os .remove (O0OO0O0O000OOOOOO )#line:20
            return True #line:21
        return False #line:22
    def get_safe_status (OOOO0000O0OO0OOOO ,OO00O0OOO00OO000O ):#line:23
        OO0OO000OO0OO0O0O =OOOO0000O0OO0OOOO .__OO00OO00O0O00OO0O ()#line:24
        if not OO0OO000OO0OO0O0O ['open']:#line:25
            if not OOOO0000O0OO0OOOO .check_sys_write ():#line:26
                OOOO0000O0OO0OOOO .set_open (None ,0 )#line:27
                if not OOOO0000O0OO0OOOO .check_sys_write ():#line:28
                    return public .returnMsg (False ,'检测到第三方系统加固软件,无需再使用本插件!');#line:29
        O000OO000000OOO0O =[]#line:30
        for OO00OO00OOO00O000 in OO0OO000OO0OO0O0O .keys ():#line:31
            if type (OO0OO000OO0OO0O0O [OO00OO00OOO00O000 ])==bool :continue #line:32
            if not 'name'in OO0OO000OO0OO0O0O [OO00OO00OOO00O000 ]:continue ;#line:33
            O0OO0OO0O0OO0OOO0 ={}#line:34
            O0OO0OO0O0OO0OOO0 ['key']=OO00OO00OOO00O000 #line:35
            O0OO0OO0O0OO0OOO0 ['name']=OO0OO000OO0OO0O0O [OO00OO00OOO00O000 ]['name']#line:36
            O0OO0OO0O0OO0OOO0 ['open']=OO0OO000OO0OO0O0O [OO00OO00OOO00O000 ]['open']#line:37
            O0OO0OO0O0OO0OOO0 ['ps']=OO0OO000OO0OO0O0O [OO00OO00OOO00O000 ]['ps']#line:38
            O000OO000000OOO0O .append (O0OO0OO0O0OO0OOO0 )#line:39
        OOOOOOO0OOOOO0OOO ={}#line:40
        OOOOOOO0OOOOO0OOO ['open']=OO0OO000OO0OO0O0O ['open']#line:41
        OOOOOOO0OOOOO0OOO ['list']=O000OO000000OOO0O #line:42
        return OOOOOOO0OOOOO0OOO #line:43
    def set_safe_status (O00O0OOO000O000OO ,O0O00O0O000OOOOOO ):#line:44
        OOOOO0OOOO000O0OO =O00O0OOO000O000OO .__OO00OO00O0O00OO0O ()#line:45
        OOOOO0OOOO000O0OO [O0O00O0O000OOOOOO .s_key ]['open']=not OOOOO0OOOO000O0OO [O0O00O0O000OOOOOO .s_key ]['open']#line:46
        O00O0OOO000O000OO .__OO00OOO0OO0O0O000 (OOOOO0OOOO000O0OO )#line:47
        if type (OOOOO0OOOO000O0OO [O0O00O0O000OOOOOO .s_key ])!=bool :#line:48
            if 'paths'in OOOOO0OOOO000O0OO [O0O00O0O000OOOOOO .s_key ]and OOOOO0OOOO000O0OO ['open']:O00O0OOO000O000OO .__OOOOOOOO0OOOO0000 (OOOOO0OOOO000O0OO [O0O00O0O000OOOOOO .s_key ]['paths'],OOOOO0OOOO000O0OO [O0O00O0O000OOOOOO .s_key ]['open'])#line:49
        if O0O00O0O000OOOOOO .s_key in ['ssh','process']and OOOOO0OOOO000O0OO ['open']:public .ExecShell ("/etc/init.d/bt_syssafe restart")#line:50
        OO0OO00O000OOO00O =u'已将[%s]状态设置为[%s]'%(OOOOO0OOOO000O0OO [O0O00O0O000OOOOOO .s_key ]['name'],O00O0OOO000O000OO .__O0OOO0O00OOOO000O [OOOOO0OOOO000O0OO [O0O00O0O000OOOOOO .s_key ]['open']])#line:51
        public .WriteLog (O00O0OOO000O000OO .__O0O0O0O00O0O0OO00 ,OO0OO00O000OOO00O )#line:52
        return public .returnMsg (True ,OO0OO00O000OOO00O )#line:53
    def set_open (OO0OO00O0O0000000 ,OOO00OOO0OOO00OO0 ,is_hit =-1 ):#line:54
        O0O0O0OOOOOO00OOO =OO0OO00O0O0000000 .__OO00OO00O0O00OO0O ()#line:55
        if not O0O0O0OOOOOO00OOO ['open']and is_hit ==1 :return True #line:56
        if is_hit !=-1 :#line:57
            if is_hit ==0 :#line:58
                O0O0O0OOOOOO00OOO ['open']=True #line:59
            else :#line:60
                O0O0O0OOOOOO00OOO ['open']=False #line:61
        O0O0O0OOOOOO00OOO ['open']=not O0O0O0OOOOOO00OOO ['open']#line:62
        OOO0O0OOO0OOO0OOO ={True :'start',False :'stop'}#line:63
        if is_hit ==-1 :OO0OO00O0O0000000 .__OO00OOO0OO0O0O000 (O0O0O0OOOOOO00OOO )#line:64
        for OO00OOO000000OOOO in O0O0O0OOOOOO00OOO .keys ():#line:65
            if type (O0O0O0OOOOOO00OOO [OO00OOO000000OOOO ])==bool :continue ;#line:66
            if not 'name'in O0O0O0OOOOOO00OOO [OO00OOO000000OOOO ]:continue ;#line:67
            if not 'paths'in O0O0O0OOOOOO00OOO [OO00OOO000000OOOO ]:continue ;#line:68
            if not O0O0O0OOOOOO00OOO ['open']:O0O0O0OOOOOO00OOO [OO00OOO000000OOOO ]['open']=False #line:69
            OO0OO00O0O0000000 .__OOOOOOOO0OOOO0000 (O0O0O0OOOOOO00OOO [OO00OOO000000OOOO ]['paths'],O0O0O0OOOOOO00OOO [OO00OOO000000OOOO ]['open'])#line:70
        OOOOO0OO00O0OOO00 =u'已[%s]宝塔系统加固功能'%OO0OO00O0O0000000 .__O0OOO0O00OOOO000O [O0O0O0OOOOOO00OOO ['open']]#line:71
        public .WriteLog (OO0OO00O0O0000000 .__O0O0O0O00O0O0OO00 ,OOOOO0OO00O0OOO00 )#line:72
        O00OOOO00OOO0OO00 ='/etc/init.d/bt_syssafe %s'%OOO0O0OOO0OOO0OOO [O0O0O0OOOOOO00OOO ['open']]#line:73
        public .ExecShell (O00OOOO00OOO0OO00 )#line:74
        return public .returnMsg (True ,OOOOO0OO00O0OOO00 )#line:75
    def get_safe_config (O0OO0OO00000000O0 ,OOO000OOO0OOO0OO0 ):#line:76
        OOO0OOOOO00O000O0 =O0OO0OO00000000O0 .__OO00OO00O0O00OO0O ()#line:77
        OOO0OOOOO00O000O0 [OOO000OOO0OOO0OO0 .s_key ]['paths']=O0OO0OO00000000O0 .__OO0O00000000OO0O0 (OOO0OOOOO00O000O0 [OOO000OOO0OOO0OO0 .s_key ]['paths'])#line:78
        return OOO0OOOOO00O000O0 [OOO000OOO0OOO0OO0 .s_key ]#line:79
    def add_safe_path (OO00000O00OO00O0O ,OOO0OOOOO0OOO000O ):#line:80
        if not os .path .exists (OOO0OOOOO0OOO000O .path ):return public .returnMsg (False ,u'指定文件或目录不存在!')#line:81
        O00000OO0OOOOO0OO =OO00000O00OO00O0O .__OO00OO00O0O00OO0O ()#line:82
        for OO000O00O00OO0OO0 in O00000OO0OOOOO0OO [OOO0OOOOO0OOO000O .s_key ]['paths']:#line:83
            if OOO0OOOOO0OOO000O .path ==OO000O00O00OO0OO0 ['path']:return public .returnMsg (False ,u'指定文件或目录已经添加过了!')#line:84
        OO0O000OO0OO0O000 ={}#line:85
        OO0O000OO0OO0O000 ['path']=OOO0OOOOO0OOO000O .path #line:86
        OO0O000OO0OO0O000 ['chattr']=OOO0OOOOO0OOO000O .chattr #line:87
        OO0O000OO0OO0O000 ['s_mode']=int (oct (os .stat (OOO0OOOOO0OOO000O .path ).st_mode )[-3 :],8 )#line:88
        if OOO0OOOOO0OOO000O .d_mode :#line:89
            OO0O000OO0OO0O000 ['d_mode']=int (OOO0OOOOO0OOO000O .d_mode ,8 )#line:90
        else :#line:91
            OO0O000OO0OO0O000 ['d_mode']=OO0O000OO0OO0O000 ['s_mode']#line:92
        O00000OO0OOOOO0OO [OOO0OOOOO0OOO000O .s_key ]['paths'].insert (0 ,OO0O000OO0OO0O000 )#line:93
        if 'paths'in O00000OO0OOOOO0OO [OOO0OOOOO0OOO000O .s_key ]:#line:94
            public .ExecShell ('chattr -%s %s'%(OO0O000OO0OO0O000 ['chattr'],OO0O000OO0OO0O000 ['path']))#line:95
            OO00000O00OO00O0O .__OOOOOOOO0OOOO0000 ([OO0O000OO0OO0O000 ],O00000OO0OOOOO0OO [OOO0OOOOO0OOO000O .s_key ]['open'])#line:96
        OO00000O00OO00O0O .__OO00OOO0OO0O0O000 (O00000OO0OOOOO0OO )#line:97
        OOO0O0OO0OOOO00O0 =u'添加防护对象[%s]到[%s]'%(OOO0OOOOO0OOO000O .path ,O00000OO0OOOOO0OO [OOO0OOOOO0OOO000O .s_key ]['name'])#line:98
        public .WriteLog (OO00000O00OO00O0O .__O0O0O0O00O0O0OO00 ,OOO0O0OO0OOOO00O0 )#line:99
        return public .returnMsg (True ,OOO0O0OO0OOOO00O0 )#line:100
    def remove_safe_path (OO0OOOOOO0OOOO0O0 ,OO00OOOO0OOO0OO0O ):#line:101
        OO0O0O0O0OO0OO00O =OO0OOOOOO0OOOO0O0 .__OO00OO00O0O00OO0O ()#line:102
        OO0000O0OO0O000OO =False #line:103
        for OOO0O0O0OO000OOO0 in OO0O0O0O0OO0OO00O [OO00OOOO0OOO0OO0O .s_key ]['paths']:#line:104
            if OO00OOOO0OOO0OO0O .path ==OOO0O0O0OO000OOO0 ['path']:#line:105
                OO0000O0OO0O000OO =True #line:106
                OO0O0O0O0OO0OO00O [OO00OOOO0OOO0OO0O .s_key ]['paths'].remove (OOO0O0O0OO000OOO0 )#line:107
                if os .path .exists (OO00OOOO0OOO0OO0O .path ):OO0OOOOOO0OOOO0O0 .__OOOOOOOO0OOOO0000 ([OOO0O0O0OO000OOO0 ],False )#line:108
                break ;#line:109
        if not OO0000O0OO0O000OO :return public .returnMsg (False ,'指定保护对象不存在!')#line:110
        OO0OOOOOO0OOOO0O0 .__OO00OOO0OO0O0O000 (OO0O0O0O0OO0OO00O )#line:111
        O000O00000OOOO00O =u'从[%s]删除保护对象[%s]'%(OO0O0O0O0OO0OO00O [OO00OOOO0OOO0OO0O .s_key ]['name'],OO00OOOO0OOO0OO0O .path )#line:112
        public .WriteLog (OO0OOOOOO0OOOO0O0 .__O0O0O0O00O0O0OO00 ,O000O00000OOOO00O )#line:113
        return public .returnMsg (True ,O000O00000OOOO00O )#line:114
    def add_process_white (OOOOOOO0O0O0OOO00 ,O0O00O0000OOOO0OO ):#line:115
        OO0O00OO0OO0000OO =OOOOOOO0O0O0OOO00 .__OO00OO00O0O00OO0O ()#line:116
        O0O00O0000OOOO0OO .process_name =O0O00O0000OOOO0OO .process_name .strip ()#line:117
        if O0O00O0000OOOO0OO .process_name in OO0O00OO0OO0000OO ['process']['process_white']:return public .returnMsg (False ,'指定进程名已在白名单')#line:118
        OO0O00OO0OO0000OO ['process']['process_white'].insert (0 ,O0O00O0000OOOO0OO .process_name )#line:119
        OOOOOOO0O0O0OOO00 .__OO00OOO0OO0O0O000 (OO0O00OO0OO0000OO )#line:120
        O00O00OOO0OOOOOO0 =u'添加进程名[%s]到进程白名单'%O0O00O0000OOOO0OO .process_name #line:121
        public .WriteLog (OOOOOOO0O0O0OOO00 .__O0O0O0O00O0O0OO00 ,O00O00OOO0OOOOOO0 )#line:122
        public .ExecShell ('/etc/init.d/bt_syssafe restart')#line:123
        return public .returnMsg (True ,O00O00OOO0OOOOOO0 )#line:124
    def remove_process_white (O0O000O0OO00O0O00 ,OOO00000O00OO00O0 ):#line:125
        O0O000OOOOO0O0OO0 =O0O000O0OO00O0O00 .__OO00OO00O0O00OO0O ()#line:126
        OOO00000O00OO00O0 .process_name =OOO00000O00OO00O0 .process_name .strip ()#line:127
        if not OOO00000O00OO00O0 .process_name in O0O000OOOOO0O0OO0 ['process']['process_white']:return public .returnMsg (False ,'指定进程名不存在')#line:128
        O0O000OOOOO0O0OO0 ['process']['process_white'].remove (OOO00000O00OO00O0 .process_name )#line:129
        O0O000O0OO00O0O00 .__OO00OOO0OO0O0O000 (O0O000OOOOO0O0OO0 )#line:130
        O00OO000OO000OO0O =u'从进程白名单删除进程名[%s]'%OOO00000O00OO00O0 .process_name #line:131
        public .WriteLog (O0O000O0OO00O0O00 .__O0O0O0O00O0O0OO00 ,O00OO000OO000OO0O )#line:132
        public .ExecShell ('/etc/init.d/bt_syssafe restart')#line:133
        return public .returnMsg (True ,O00OO000OO000OO0O )#line:134
    def add_process_rule (OOO0OOOO0OOOO0000 ,O0O0OO0000O0000OO ):#line:135
        OO0O0000000OO0000 =OOO0OOOO0OOOO0000 .__OO00OO00O0O00OO0O ()#line:136
        O0O0OO0000O0000OO .process_key =O0O0OO0000O0000OO .process_key .strip ()#line:137
        if O0O0OO0000O0000OO .process_key in OO0O0000000OO0000 ['process']['process_rule']:return public .returnMsg (False ,'指定关键词已在白名单')#line:138
        OO0O0000000OO0000 ['process']['process_rule'].insert (0 ,O0O0OO0000O0000OO .process_key )#line:139
        OOO0OOOO0OOOO0000 .__OO00OOO0OO0O0O000 (OO0O0000000OO0000 )#line:140
        OOO00O0000OOO0OOO =u'添加关键词[%s]到进程关键词白名单'%O0O0OO0000O0000OO .process_key #line:141
        public .WriteLog (OOO0OOOO0OOOO0000 .__O0O0O0O00O0O0OO00 ,OOO00O0000OOO0OOO )#line:142
        return public .returnMsg (True ,OOO00O0000OOO0OOO )#line:143
    def remove_process_rule (O0O0O00O0OOO00OO0 ,O0O0OOOOOOO0000O0 ):#line:144
        OO0OOOOO0000OO000 =O0O0O00O0OOO00OO0 .__OO00OO00O0O00OO0O ()#line:145
        O0O0OOOOOOO0000O0 .process_key =O0O0OOOOOOO0000O0 .process_key .strip ()#line:146
        if not O0O0OOOOOOO0000O0 .process_key in OO0OOOOO0000OO000 ['process']['process_rule']:return public .returnMsg (False ,'指定关键词不存在')#line:147
        OO0OOOOO0000OO000 ['process']['process_rule'].remove (O0O0OOOOOOO0000O0 .process_key )#line:148
        O0O0O00O0OOO00OO0 .__OO00OOO0OO0O0O000 (OO0OOOOO0000OO000 )#line:149
        OOO00O0OO0OOO00O0 =u'从进程关键词白名单删除关键词[%s]'%O0O0OOOOOOO0000O0 .process_key #line:150
        public .WriteLog (O0O0O00O0OOO00OO0 .__O0O0O0O00O0O0OO00 ,OOO00O0OO0OOO00O0 )#line:151
        return public .returnMsg (True ,OOO00O0OO0OOO00O0 )#line:152
    def get_process_white (O000OOO0OO00OOO00 ,O00O0OOOO000OO0O0 ):#line:153
        OO0OO0O00O00O0OOO =O000OOO0OO00OOO00 .__OO00OO00O0O00OO0O ()#line:154
        return OO0OO0O00O00O0OOO ['process']['process_white']#line:155
    def get_process_rule (O00O0OOO0OO000OO0 ,O0OO0O0OOO00OOOOO ):#line:156
        O00O0OO0OO00O0O00 =O00O0OOO0OO000OO0 .__OO00OO00O0O00OO0O ()#line:157
        return O00O0OO0OO00O0O00 ['process']['process_white_rule']#line:158
    def get_process_exclude (O000O0OOO0O0O00O0 ,OO0OOOOO0O000O000 ):#line:159
        OO00O0OO0OOOO00OO =O000O0OOO0O0O00O0 .__OO00OO00O0O00OO0O ()#line:160
        return OO00O0OO0OOOO00OO ['process']['process_exclude']#line:161
    def get_ssh_config (OOO00OOOOOOO0O000 ,O0OOOO00OOO0O0OO0 ):#line:162
        O0OO0OO0000O00O0O =OOO00OOOOOOO0O000 .__OO00OO00O0O00OO0O ()#line:163
        return O0OO0OO0000O00O0O ['ssh']#line:164
    def save_ssh_config (O0000O0O0O0OOO00O ,OO0OOOO00000OO00O ):#line:165
        OO0OOOO00000OO00O .cycle =int (OO0OOOO00000OO00O .cycle )#line:166
        OO0OOOO00000OO00O .limit =int (OO0OOOO00000OO00O .limit )#line:167
        OO0OOOO00000OO00O .limit_count =int (OO0OOOO00000OO00O .limit_count )#line:168
        if OO0OOOO00000OO00O .cycle >OO0OOOO00000OO00O .limit :return public .returnMsg (False ,'封锁时间不能小于检测周期!');#line:169
        if OO0OOOO00000OO00O .cycle <30 or OO0OOOO00000OO00O .cycle >1800 :return public .returnMsg (False ,'检测周期的值必需在30 - 1800秒之间!');#line:170
        if OO0OOOO00000OO00O .limit <60 :return public .returnMsg (False ,'封锁时间不能小于60秒');#line:171
        if OO0OOOO00000OO00O .limit_count <3 or OO0OOOO00000OO00O .limit_count >100 :return public .returnMsg (False ,'检测阈值必需在3 - 100秒之间!');#line:172
        O0OOO00O0O0OO0O0O =O0000O0O0O0OOO00O .__OO00OO00O0O00OO0O ()#line:173
        O0OOO00O0O0OO0O0O ['ssh']['cycle']=OO0OOOO00000OO00O .cycle #line:174
        O0OOO00O0O0OO0O0O ['ssh']['limit']=OO0OOOO00000OO00O .limit #line:175
        O0OOO00O0O0OO0O0O ['ssh']['limit_count']=OO0OOOO00000OO00O .limit_count #line:176
        O0000O0O0O0OOO00O .__OO00OOO0OO0O0O000 (O0OOO00O0O0OO0O0O )#line:177
        O0OO0000OO000O00O =u'修改SSH策略: 在[%s]秒内,登录错误[%s]次,封锁[%s]秒'%(O0OOO00O0O0OO0O0O ['ssh']['cycle'],O0OOO00O0O0OO0O0O ['ssh']['limit_count'],O0OOO00O0O0OO0O0O ['ssh']['limit'])#line:178
        public .WriteLog (O0000O0O0O0OOO00O .__O0O0O0O00O0O0OO00 ,O0OO0000OO000O00O )#line:179
        public .ExecShell ('/etc/init.d/bt_syssafe restart')#line:180
        return public .returnMsg (True ,'配置已保存!')#line:181
    def get_ssh_login_logs (O00OO0O0O000O0OO0 ,O0O0000OO0OOOO0OO ):#line:182
        import page #line:183
        page =page .Page ();#line:184
        O00O0OOOOOO0O0O0O =public .M ('logs').where ('type=?',(u'SSH登录',)).count ();#line:185
        OO000O0OOO0O000O0 =12 ;#line:186
        OO0O000O0O000OOOO ={}#line:187
        OO0O000O0O000OOOO ['count']=O00O0OOOOOO0O0O0O #line:188
        OO0O000O0O000OOOO ['row']=OO000O0OOO0O000O0 #line:189
        OO0O000O0O000OOOO ['p']=1 #line:190
        if hasattr (O0O0000OO0OOOO0OO ,'p'):#line:191
            OO0O000O0O000OOOO ['p']=int (O0O0000OO0OOOO0OO ['p'])#line:192
        OO0O000O0O000OOOO ['uri']={}#line:193
        OO0O000O0O000OOOO ['return_js']=''#line:194
        if hasattr (O0O0000OO0OOOO0OO ,'tojs'):#line:195
            OO0O000O0O000OOOO ['return_js']=O0O0000OO0OOOO0OO .tojs #line:196
        OOOO0O00O0O00O00O ={}#line:197
        OOOO0O00O0O00O00O ['page']=page .GetPage (OO0O000O0O000OOOO ,'1,2,3,4,5');#line:198
        OOOO0O00O0O00O00O ['data']=public .M ('logs').where ('type=?',(u'SSH登录',)).order ('id desc').limit (str (page .SHIFT )+','+str (page .ROW )).field ('log,addtime').select ();#line:199
        return OOOO0O00O0O00O00O ;#line:200
    def __O0O0OOOO0000OO0O0 (OOO0OO000OO0000OO ,O0O00O0OO00O00O00 ):#line:201
        OOOO000O00000O00O =O0O00O0OO00O00O00 .split (' ')#line:202
        O0OOO0OO00O00OOO0 =str (datetime .now ().year )+'-'+OOO0OO000OO0000OO .__O0O000000OOOOO00O .get (OOOO000O00000O00O [0 ])+'-'+OOOO000O00000O00O [1 ]+' '+OOOO000O00000O00O [2 ]#line:203
        O0OOOO0O0O00OOO0O =time .strptime (O0OOO0OO00O00OOO0 ,"%Y-%m-%d %H:%M:%S")#line:204
        OOOO00O00O0O0O0OO =int (time .mktime (O0OOOO0O0O00OOO0O ))#line:205
        return OOOO00O00O0O0O0OO #line:206
    def add_ssh_limit (OO00O0OOO000O0000 ,OOOO0O00OOO00OOOO ):#line:207
        if OOOO0O00OOO00OOOO :#line:208
            OO0O0O0OO00O000OO =OOOO0O00OOO00OOOO .ip ;#line:209
        else :#line:210
            OO0O0O0OO00O000OO =OO00O0OOO000O0000 .ip ;#line:211
        if OO0O0O0OO00O000OO in OO00O0OOO000O0000 .get_ssh_limit ():return public .returnMsg (True ,'指定IP黑名单已存在!');#line:212
        O0OOOOOOOOO00OO00 =public .readFile (OO00O0OOO000O0000 .__OOOO0O0OO00O000O0 ).strip ();#line:213
        while O0OOOOOOOOO00OO00 [-1 :]=="\n"or O0OOOOOOOOO00OO00 [-1 :]==" ":O0OOOOOOOOO00OO00 =O0OOOOOOOOO00OO00 [:-1 ];#line:214
        O0OOOOOOOOO00OO00 +="\nsshd:"+OO0O0O0OO00O000OO +":deny\n";#line:215
        public .writeFile (OO00O0OOO000O0000 .__OOOO0O0OO00O000O0 ,O0OOOOOOOOO00OO00 );#line:216
        if OO0O0O0OO00O000OO in OO00O0OOO000O0000 .get_ssh_limit ():#line:217
            O0000O0O00O00O000 =u'添加IP[%s]到SSH-IP黑名单'%OO0O0O0OO00O000OO #line:218
            public .WriteLog (OO00O0OOO000O0000 .__O0O0O0O00O0O0OO00 ,O0000O0O00O00O000 )#line:219
            OO00O0OOO000O0000 .get_deny_list ()#line:220
            if not OO0O0O0OO00O000OO in OO00O0OOO000O0000 .__OO0OOO00000OO0000 :OO00O0OOO000O0000 .__OO0OOO00000OO0000 [OO0O0O0OO00O000OO ]=0 #line:221
            OO00O0OOO000O0000 .save_deay_list ()#line:222
            return public .returnMsg (True ,'添加成功!');#line:223
        return public .returnMsg (False ,'添加失败!');#line:224
    def remove_ssh_limit (OOO00OOOOO0O00OOO ,O00O000O00O0O00O0 ):#line:225
        if O00O000O00O0O00O0 :#line:226
            O0O000O0O0O0O0000 =O00O000O00O0O00O0 .ip ;#line:227
        else :#line:228
            O0O000O0O0O0O0000 =OOO00OOOOO0O00OOO .ip ;#line:229
        if not OOO00OOOOO0O00OOO .__OO0OOO00000OO0000 :OOO00OOOOO0O00OOO .get_deny_list ()#line:230
        if O0O000O0O0O0O0000 in OOO00OOOOO0O00OOO .__OO0OOO00000OO0000 :del (OOO00OOOOO0O00OOO .__OO0OOO00000OO0000 [O0O000O0O0O0O0000 ])#line:231
        OOO00OOOOO0O00OOO .save_deay_list ()#line:232
        if not O0O000O0O0O0O0000 in OOO00OOOOO0O00OOO .get_ssh_limit ():return public .returnMsg (True ,'指定IP黑名单不存在!');#line:233
        OOO00000OO000O0O0 =public .readFile (OOO00OOOOO0O00OOO .__OOOO0O0OO00O000O0 ).strip ();#line:234
        while OOO00000OO000O0O0 [-1 :]=="\n"or OOO00000OO000O0O0 [-1 :]==" ":OOO00000OO000O0O0 =OOO00000OO000O0O0 [:-1 ];#line:235
        OOO00000OO000O0O0 =re .sub ("\nsshd:"+O0O000O0O0O0O0000 +":deny\n?","\n",OOO00000OO000O0O0 );#line:236
        public .writeFile (OOO00OOOOO0O00OOO .__OOOO0O0OO00O000O0 ,OOO00000OO000O0O0 +"\n");#line:237
        OOO0O000OO00000O0 =u'从SSH-IP黑名单中解封[%s]'%O0O000O0O0O0O0000 #line:238
        public .WriteLog (OOO00OOOOO0O00OOO .__O0O0O0O00O0O0OO00 ,OOO0O000OO00000O0 )#line:239
        return public .returnMsg (True ,'解封成功!');#line:240
    def get_ssh_limit (OOOOO00OO000O00OO ,get =None ):#line:241
        O0O00O000O00O0000 =public .readFile (OOOOO00OO000O00OO .__OOOO0O0OO00O000O0 );#line:242
        return re .findall ("sshd:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):deny",O0O00O000O00O0000 );#line:243
    def get_ssh_limit_info (OOOO0OO00OO0000OO ,O000O00O00O000O0O ):#line:244
        OOOO0OO00OO0000OO .get_deny_list ()#line:245
        OOOOO0OO000OO0O0O =OOOO0OO00OO0000OO .get_ssh_limit (None )#line:246
        OO00OO00O000O0O00 =[]#line:247
        for OOOOOO000O0OO00OO in OOOOO0OO000OO0O0O :#line:248
            O0O000OOOOOOOOOO0 ={}#line:249
            O0O000OOOOOOOOOO0 ['address']=OOOOOO000O0OO00OO #line:250
            O0O000OOOOOOOOOO0 ['end']=0 #line:251
            if OOOOOO000O0OO00OO in OOOO0OO00OO0000OO .__OO0OOO00000OO0000 :O0O000OOOOOOOOOO0 ['end']=OOOO0OO00OO0000OO .__OO0OOO00000OO0000 [OOOOOO000O0OO00OO ]#line:252
            OO00OO00O000O0O00 .append (O0O000OOOOOOOOOO0 )#line:253
        return OO00OO00O000O0O00 #line:254
    def get_deny_list (OO0O00O0O00OOOOO0 ):#line:255
        OOOO0OO000OOO0O0O =OO0O00O0O00OOOOO0 .__OOO0O00O0O0O0OOOO +'deny.json'#line:256
        if not os .path .exists (OOOO0OO000OOO0O0O ):public .writeFile (OOOO0OO000OOO0O0O ,'{}')#line:257
        OO0O00O0O00OOOOO0 .__OO0OOO00000OO0000 =json .loads (public .readFile (OO0O00O0O00OOOOO0 .__OOO0O00O0O0O0OOOO +'deny.json'))#line:258
    def save_deay_list (OOO000O00OOOO0OOO ):#line:259
        O00OOO0OO000OO0O0 =OOO000O00OOOO0OOO .__OOO0O00O0O0O0OOOO +'deny.json'#line:260
        public .writeFile (O00OOO0OO000OO0O0 ,json .dumps (OOO000O00OOOO0OOO .__OO0OOO00000OO0000 ))#line:261
    def get_logs (OOOOOO0O00OO00OO0 ,O00OOO0O0OO0O00OO ):#line:262
        import page #line:263
        page =page .Page ();#line:264
        OOOO0O000OO0OO00O =public .M ('logs').where ('type=? or type=?',(OOOOOO0O00OO00OO0 .__O0O0O0O00O0O0OO00 ,u'SSH登录')).count ();#line:265
        OOOOOO000O0O0OO0O =12 ;#line:266
        O0O00000O000O0OO0 ={}#line:267
        O0O00000O000O0OO0 ['count']=OOOO0O000OO0OO00O #line:268
        O0O00000O000O0OO0 ['row']=OOOOOO000O0O0OO0O #line:269
        O0O00000O000O0OO0 ['p']=1 #line:270
        if hasattr (O00OOO0O0OO0O00OO ,'p'):#line:271
            O0O00000O000O0OO0 ['p']=int (O00OOO0O0OO0O00OO ['p'])#line:272
        O0O00000O000O0OO0 ['uri']={}#line:273
        O0O00000O000O0OO0 ['return_js']=''#line:274
        if hasattr (O00OOO0O0OO0O00OO ,'tojs'):#line:275
            O0O00000O000O0OO0 ['return_js']=O00OOO0O0OO0O00OO .tojs #line:276
        OOO0O0000000OOO00 ={}#line:277
        OOO0O0000000OOO00 ['page']=page .GetPage (O0O00000O000O0OO0 ,'1,2,3,4,5');#line:278
        OOO0O0000000OOO00 ['data']=public .M ('logs').where ('type=? or type=?',(OOOOOO0O00OO00OO0 .__O0O0O0O00O0O0OO00 ,u'SSH登录')).order ('id desc').limit (str (page .SHIFT )+','+str (page .ROW )).field ('log,addtime').select ();#line:279
        return OOO0O0000000OOO00 ;#line:280
    def __O00OOOO000000O0O0 (O0OO0O0O0O000OOO0 ,OO0O00O0000O0O00O ):#line:281
        try :#line:282
            if not os .path .exists (OO0O00O0000O0O00O ['path']):return False #line:283
            if OO0O00O0000O0O00O ['d_mode']:os .chmod (OO0O00O0000O0O00O ['path'],OO0O00O0000O0O00O ['d_mode'])#line:284
            if OO0O00O0000O0O00O ['chattr']:public .ExecShell ('chattr +%s %s'%(OO0O00O0000O0O00O ['chattr'],OO0O00O0000O0O00O ['path']))#line:285
            return True #line:286
        except :return False #line:287
    def __OO0O0O0O0OO0O0OO0 (O0O0O00O0O0O0OO0O ,O00O0000OOO000OOO ):#line:288
        try :#line:289
            if not os .path .exists (O00O0000OOO000OOO ['path']):return False #line:290
            if O00O0000OOO000OOO ['chattr']:public .ExecShell ('chattr -%s %s'%(O00O0000OOO000OOO ['chattr'],O00O0000OOO000OOO ['path']))#line:291
            if O00O0000OOO000OOO ['s_mode']:os .chmod (O00O0000OOO000OOO ['path'],O00O0000OOO000OOO ['s_mode'])#line:292
            return True #line:293
        except :return False #line:294
    def __O000OOO00O00OO00O (OO0O0O0000OO0O000 ,O0O0O00O00O000000 ):#line:295
        if os .path .isfile (O0O0O00O00O000000 ):#line:296
            OO00000000OOOOOO0 ="lsattr %s|awk '{print $1}'"%O0O0O00O00O000000 #line:297
        else :#line:298
            OO00000000OOOOOO0 ="lsattr %s |grep '%s$'|awk '{print $1}'"%(os .path .dirname (O0O0O00O00O000000 ),O0O0O00O00O000000 )#line:299
        OO00O00O000O0O0OO =public .ExecShell (OO00000000OOOOOO0 )[0 ]#line:300
        if OO00O00O000O0O0OO .find ('-i-')!=-1 :return 'i'#line:301
        if OO00O00O000O0O0OO .find ('-a-')!=-1 :return 'a'#line:302
        return False #line:303
    def __OO0O00000000OO0O0 (OOOO0O0O00000OO0O ,OOOO0O00000O00000 ):#line:304
        for OOOOO00OOO0OOO0OO in range (len (OOOO0O00000O00000 )):#line:305
            OOO0O0OO00OO00O00 =OOOO0O0O00000OO0O .__O000OOO00O00OO00O (OOOO0O00000O00000 [OOOOO00OOO0OOO0OO ]['path'])#line:306
            OOOO0O00000O00000 [OOOOO00OOO0OOO0OO ]['state']=OOO0O0OO00OO00O00 ==OOOO0O00000O00000 [OOOOO00OOO0OOO0OO ]['chattr']#line:307
            OOOO0O00000O00000 [OOOOO00OOO0OOO0OO ]['s_mode']=oct (OOOO0O00000O00000 [OOOOO00OOO0OOO0OO ]['s_mode'])#line:308
            OOOO0O00000O00000 [OOOOO00OOO0OOO0OO ]['d_mode']=oct (OOOO0O00000O00000 [OOOOO00OOO0OOO0OO ]['d_mode'])#line:309
        return OOOO0O00000O00000 #line:310
    def __OOOOOOOO0OOOO0000 (O0OOOOOOOO0OO0OO0 ,OOOOOOOOO00OOOOO0 ,lock =True ):#line:311
        for O0OO0OO0OOO00O0OO in OOOOOOOOO00OOOOO0 :#line:312
            if lock :#line:313
                O0OOOOOOOO0OO0OO0 .__O00OOOO000000O0O0 (O0OO0OO0OOO00O0OO )#line:314
            else :#line:315
                O0OOOOOOOO0OO0OO0 .__OO0O0O0O0OO0O0OO0 (O0OO0OO0OOO00O0OO )#line:316
        return True #line:317
    def __OO00OOO0OO0O0O000 (O0O0OOOO0OOO0O0OO ,O00OOOO00O0O0OOO0 ):#line:318
        public .writeFile (O0O0OOOO0OOO0O0OO .__OOO0O00O0O0O0OOOO +'config.json',json .dumps (O00OOOO00O0O0OOO0 ))#line:319
        return True #line:320
    def __OO00OO00O0O00OO0O (O000O0O0OOOO00O00 ):#line:321
        return json .loads (public .readFile (O000O0O0OOOO00O00 .__OOO0O00O0O0O0OOOO +'config.json'))#line:322
    __O00O0000OOO0OOOO0 =30 ;#line:323
    __O0OO0O0OOOO0OOO0O =1048576 *1000 ;#line:324
    __O0000OO0O00O0OO00 =None #line:325
    __OO0OO00000OO0O000 =None #line:326
    __O00O0OO0O0OOOOO00 =None #line:327
    def check_main (OOOO0O00O0O0OOOOO ):#line:328
        O00OOOOO0OO0O00OO =psutil .pids ()#line:329
        for OO0OO000OO0OOO0O0 in O00OOOOO0OO0O00OO :#line:330
            if OO0OO000OO0OOO0O0 <1100 :continue #line:331
            O00OO0O0OO0O0O00O ='/proc/'+str (OO0OO000OO0OOO0O0 )+'/comm'#line:332
            if not os .path .exists (O00OO0O0OO0O0O00O ):continue #line:333
            OO0O00O00O00OOO0O =public .readFile (O00OO0O0OO0O0O00O ).strip ()#line:334
            if OOOO0O00O0O0OOOOO .check_white (OO0O00O00O00OOO0O ):continue ;#line:335
            try :#line:336
                O0OOO0O0OO0O0O0OO =psutil .Process (OO0OO000OO0OOO0O0 );#line:337
                OOO0000000000OOOO =O0OOO0O0OO0O0O0OO .cpu_percent (interval =0.1 );#line:338
                OO00O00OO0O0000O0 =O0OOO0O0OO0O0O0OO .memory_info ().vms #line:339
                if OOO0000000000OOOO >OOOO0O00O0O0OOOOO .__O00O0000OOO0OOOO0 or OO00O00OO0O0000O0 >OOOO0O00O0O0OOOOO .__O0OO0O0OOOO0OOO0O :#line:340
                    if str (O0OOO0O0OO0O0O0OO .cmdline ()).find ('/www/server/cron')!=-1 :continue #line:341
                    if OO0O00O00O00OOO0O .find ('kworker')!=-1 :continue #line:342
                    O0OOO0O0OO0O0O0OO .kill ();#line:343
                    public .WriteLog (OOOO0O00O0O0OOOOO .__O0O0O0O00O0O0OO00 ,"已强制结束异常进程:[%s],PID:[%s],CPU:[%s]"%(OO0O00O00O00OOO0O ,OO0OO000OO0OOO0O0 ,OOO0000000000OOOO ))#line:344
            except :continue #line:345
    def check_white (OOO00OO000OOOOOO0 ,O0O00OOOOO0OO000O ):#line:346
        if not OOO00OO000OOOOOO0 .__O00O0OO0O0OOOOO00 :OOO00OO000OOOOOO0 .__O00O0OO0O0OOOOO00 =OOO00OO000OOOOOO0 .get_process_exclude (None )#line:347
        if not OOO00OO000OOOOOO0 .__O0000OO0O00O0OO00 :OOO00OO000OOOOOO0 .__O0000OO0O00O0OO00 =OOO00OO000OOOOOO0 .get_process_white (None )#line:348
        if not OOO00OO000OOOOOO0 .__OO0OO00000OO0O000 :OOO00OO000OOOOOO0 .__OO0OO00000OO0O000 =OOO00OO000OOOOOO0 .get_process_rule (None )#line:349
        if O0O00OOOOO0OO000O in OOO00OO000OOOOOO0 .__O00O0OO0O0OOOOO00 :return True #line:350
        if O0O00OOOOO0OO000O in OOO00OO000OOOOOO0 .__O0000OO0O00O0OO00 :return True #line:351
        for O00000O0000OOOO0O in OOO00OO000OOOOOO0 .__OO0OO00000OO0O000 :#line:352
            if O0O00OOOOO0OO000O .find (O00000O0000OOOO0O )!=-1 :return True #line:353
        return False #line:354
    def start (OO000O00OO0O00O00 ):#line:355
        import threading #line:356
        O0OOOO0O0000O0OOO =threading .Thread (target =OO000O00OO0O00O00 .ssh_task )#line:357
        O0OOOO0O0000O0OOO .setDaemon (True )#line:358
        O0OOOO0O0000O0OOO .start ()#line:359
        OO000O00OO0O00O00 .process_task ()#line:360
    def process_task (O0000000OO00O0000 ):#line:361
        time .sleep (600 )#line:362
        if not O0000000OO00O0000 .__OO00OO0OOO00OOOO0 :O0000000OO00O0000 .__OO00OO0OOO00OOOO0 =O0000000OO00O0000 .__OO00OO00O0O00OO0O ()#line:363
        while True :#line:364
            if O0000000OO00O0000 .__OO00OO0OOO00OOOO0 ['process']['open']:O0000000OO00O0000 .check_main ()#line:365
            time .sleep (3 )#line:366
    def ssh_task (OOO00O0O00OOOOOOO ):#line:367
        if not OOO00O0O00OOOOOOO .__OO00OO0OOO00OOOO0 :OOO00O0O00OOOOOOO .__OO00OO0OOO00OOOO0 =OOO00O0O00OOOOOOO .__OO00OO00O0O00OO0O ()#line:368
        while True :#line:369
            if OOO00O0O00OOOOOOO .__OO00OO0OOO00OOOO0 ['ssh']['open']:OOO00O0O00OOOOOOO .ssh_login_task ()#line:370
            time .sleep (5 )#line:371
    def ssh_login_task (OO0O00000OOO0000O ,get =None ):#line:372
        O0OOO00O0O000O00O =public .GetNumLines ('/var/log/secure',500 ).split ('\n')#line:373
        OOO0O0OO00O0O0000 ='/dev/shm/ssh_total_time.pl'#line:374
        if not os .path .exists (OOO0O0OO00O0O0000 ):public .writeFile (OOO0O0OO00O0O0000 ,str (int (time .time ())))#line:375
        O000O00OO00O00OOO =int (public .readFile (OOO0O0OO00O0O0000 ))#line:376
        O00O00O00OO000OO0 =int (time .time ())#line:377
        O0OO0O0O000O0OO0O =O00O00O00OO000OO0 -O000O00OO00O00OOO #line:378
        OO0O00000OOO0000O .__OO00OO0OOO00OOOO0 =OO0O00000OOO0000O .__OO00OO00O0O00OO0O ()#line:379
        OOO0OO0O0OOOOO0OO =OO0O00000OOO0000O .__OO00OO0OOO00OOOO0 ['ssh']#line:380
        OO0O00000OOO0000O .get_deny_list ()#line:381
        OOO0O0000OOOO00O0 =False #line:382
        for O0O00OO00OO00O00O in OO0O00000OOO0000O .__OO0OOO00000OO0000 .keys ():#line:383
            if OO0O00000OOO0000O .__OO0OOO00000OO0000 [O0O00OO00OO00O00O ]>O00O00O00OO000OO0 or OO0O00000OOO0000O .__OO0OOO00000OO0000 [O0O00OO00OO00O00O ]==0 :continue #line:384
            OO0O00000OOO0000O .ip =O0O00OO00OO00O00O #line:385
            OO0O00000OOO0000O .remove_ssh_limit (None )#line:386
        OOOOOOOO00O0OOO0O ={}#line:387
        for O0000O00O00O00O00 in O0OOO00O0O000O00O :#line:388
            if O0000O00O00O00O00 .find ('Failed password for')!=-1 :#line:389
                OOOOOO0O0000O0000 =OO0O00000OOO0000O .__O0O0OOOO0000OO0O0 (re .search ('^\w+\s+\d+\s+\d+:\d+:\d+',O0000O00O00O00O00 ).group ())#line:390
                if O00O00O00OO000OO0 -OOOOOO0O0000O0000 >OOO0OO0O0OOOOO0OO ['cycle']:continue #line:391
                O00OOOO0OO00O0O00 =re .search ('(\d+\.)+\d+',O0000O00O00O00O00 ).group ()#line:392
                if O00OOOO0OO00O0O00 in OO0O00000OOO0000O .__OO0OOO00000OO0000 :continue #line:393
                if not O00OOOO0OO00O0O00 in OOOOOOOO00O0OOO0O :OOOOOOOO00O0OOO0O [O00OOOO0OO00O0O00 ]=0 #line:394
                OOOOOOOO00O0OOO0O [O00OOOO0OO00O0O00 ]+=1 #line:395
                if OOOOOOOO00O0OOO0O [O00OOOO0OO00O0O00 ]<OOO0OO0O0OOOOO0OO ['limit_count']:continue #line:396
                OO0O00000OOO0000O .__OO0OOO00000OO0000 [O00OOOO0OO00O0O00 ]=O00O00O00OO000OO0 +OOO0OO0O0OOOOO0OO ['limit']#line:397
                OO0O00000OOO0000O .save_deay_list ()#line:398
                OO0O00000OOO0000O .ip =O00OOOO0OO00O0O00 #line:399
                OO0O00000OOO0000O .add_ssh_limit (None )#line:400
                public .WriteLog (u'SSH登录',u"[%s]在[%s]秒内连续[%s]次登录SSH失败,封锁[%s]秒"%(O00OOOO0OO00O0O00 ,OOO0OO0O0OOOOO0OO ['cycle'],OOO0OO0O0OOOOO0OO ['limit_count'],OOO0OO0O0OOOOO0OO ['limit']))#line:401
            elif O0000O00O00O00O00 .find ('Accepted p')!=-1 :#line:402
                OOOOOO0O0000O0000 =OO0O00000OOO0000O .__O0O0OOOO0000OO0O0 (re .search ('^\w+\s+\d+\s+\d+:\d+:\d+',O0000O00O00O00O00 ).group ())#line:403
                if OOOOOO0O0000O0000 <O000O00OO00O00OOO :continue ;#line:404
                O00OOOO0OO00O0O00 =re .search ('(\d+\.)+\d+',O0000O00O00O00O00 ).group ()#line:405
                O0000OOOOOO0O0O00 =re .findall ("(\w+)\s+from",O0000O00O00O00O00 )[0 ]#line:406
                public .WriteLog (u'SSH登录',u"用户[%s]成功登录服务器,用户IP:[%s],登录时间:[%s]"%(O0000OOOOOO0O0O00 ,O00OOOO0OO00O0O00 ,time .strftime ('%Y-%m-%d %X',time .localtime (OOOOOO0O0000O0000 ))))#line:407
        public .writeFile (OOO0O0OO00O0O0000 ,str (int (time .time ())))#line:408
        return 'success'#line:409
if __name__ =="__main__":#line:410
    c =syssafe_main ();#line:411
    if len (sys .argv )==1 :#line:412
        c .start ();#line:413
    else :#line:414
        c .set_open (None ,int (sys .argv [1 ]));#line:415
