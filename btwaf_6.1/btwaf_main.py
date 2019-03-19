# coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2099 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 黄文良 <287962566@qq.com>
# | Author: 梁凯强 <1249648969@qq.com>
# +-------------------------------------------------------------------

# +--------------------------------------------------------------------
# |   宝塔网站防火墙
# +--------------------------------------------------------------------
import sys #line:14
sys .path .append ('/www/server/panel/class');#line:16
import json ,os ,time ,public ,string #line:17
os .chdir ('/www/server/panel')#line:19
if __name__ !='__main__':#line:20
    from panelAuth import panelAuth #line:21
class btwaf_main :#line:24
    __O00O00O0OO0O00O0O ='/www/server/btwaf/'#line:25
    __O0OO0O0O000O0OOOO ={True :'开启',False :'关闭',0 :'停用',1 :'启用'}#line:26
    __O0OOOOOOO000OO0OO =None #line:27
    __O0OO0000000O0O000 =["args.json","cookie.json","post.json","url_white.json","url.json","user_agent.json"]#line:28
    __OOOOO0OO0OOO0OO0O ={"EcShop":["/ecshop/api/cron.php","/appserver/public/js/main.js","/ecshop/js/index.js","/ecshop/data/config.php"],"weiqin":["/framework/table/users.table.php","/payment/alipay/return.php","/web/common/bootstrap.sys.inc.php"],"haiyang":["/data/admin/ping.php","/js/history.js","/templets/default/html/topicindex.html"],"canzhi":["/system/module/action/js/history.js","/system/framework/base/control.class.php","/www/data/css/default_clean_en.css"],"pingguo":["/static/js/jquery.pngFix.js","/static/css/admin_style.css","/template/default_pc/js/jquery-autocomplete.js"],"PHPCMS":["/phpsso_server/statics/css/system.css","/phpcms/languages/en/cnzz.lang.php","/api/reg_send_sms.php"],"wordpress":["/wp-content/languages/admin-network-zh_CN.mo","/wp-includes/js/admin-bar.js","/wp-admin/css/colors/ocean/colors.css"],"zhimeng":["/include/calendar/calendar-win2k-1.css","/include/js/jquery/ui.tabs.js","/inc/inc_stat.php","/images/js/ui.core.js"],"Discuz":["/static/js/admincp.js","/api/javascript/javascript.php","/api/trade/notify_invite.php"],"metlnfo":["/admin/content/article/save.php","/app/system/column","/config/metinfo.inc.php"]}#line:46
    def get_zhizu_list (O000OOO00O00O0O0O ):#line:49
        O0O0000O0000OO0O0 =public .httpGet ('http://www.bt.cn/api/panel/get_spider_type')#line:50
        if not O0O0000O0000OO0O0 :return False #line:51
        public .WriteFile (O000OOO00O00O0O0O .__O00O00O0OO0O00O0O +'zhi.json',O0O0000O0000OO0O0 )#line:52
        return json .loads (O0O0000O0000OO0O0 )#line:53
    def get_zhizu_ip_list (OO0O0O0O0O0OOO000 ):#line:56
        from BTPanel import session #line:57
        OOO00O000O00O0000 =OO0O0O0O0O0OOO000 .get_zhizu_list ()#line:58
        if 'types'in OOO00O000O00O0000 :#line:59
            if len (OOO00O000O00O0000 ['types'])>=1 :#line:60
                for O00OO0O0O00OO00OO in OOO00O000O00O0000 ['types']:#line:61
                    OO0O00O00000OO000 =public .httpGet ('http://www.bt.cn/api/panel/get_spider?spider=%s'%str (O00OO0O0O00OO00OO ['id']))#line:62
                    if not OO0O00O00000OO000 :continue #line:63
                    try :#line:64
                        OO0OO0O00O0O0000O =json .dumps (OO0O00O00000OO000 )#line:65
                    except :#line:66
                        if not os .path .exists (OO0O0O0O0O0OOO000 .__O00O00O0OO0O00O0O +str (O00OO0O0O00OO00OO ['id'])+'.json'):#line:67
                            O0000OO000OOO0OOO =[]#line:68
                            public .WriteFile (OO0O0O0O0O0OOO000 .__O00O00O0OO0O00O0O +str (O00OO0O0O00OO00OO ['id'])+'.json',json .dumps (O0000OO000OOO0OOO ))#line:69
                        continue #line:70
                    if os .path .exists (OO0O0O0O0O0OOO000 .__O00O00O0OO0O00O0O +str (O00OO0O0O00OO00OO ['id'])+'.json'):#line:71
                        O0OO0OO00OOO0000O =public .ReadFile (OO0O0O0O0O0OOO000 .__O00O00O0OO0O00O0O +str (O00OO0O0O00OO00OO ['id'])+'.json')#line:72
                        if O0OO0OO00OOO0000O :#line:73
                            O000OOOOO0O000OOO =list (set (json .loads (O0OO0OO00OOO0000O )).union (json .loads (OO0O00O00000OO000 )))#line:74
                            public .WriteFile (OO0O0O0O0O0OOO000 .__O00O00O0OO0O00O0O +str (O00OO0O0O00OO00OO ['id'])+'.json',json .dumps (O000OOOOO0O000OOO ))#line:75
                            O0O000OO00OOO0O0O =list (set (O0OO0OO00OOO0000O ).difference (set (OO0O00O00000OO000 )))#line:76
                            public .httpGet ('https://www.bt.cn/api/panel/add_spiders?address=%s'%json .dumps (O0O000OO00OOO0O0O ))#line:78
                        else :#line:79
                            public .WriteFile (OO0O0O0O0O0OOO000 .__O00O00O0OO0O00O0O +str (O00OO0O0O00OO00OO ['id'])+'.json',OO0O00O00000OO000 )#line:80
                    else :#line:81
                        public .WriteFile (OO0O0O0O0O0OOO000 .__O00O00O0OO0O00O0O +str (O00OO0O0O00OO00OO ['id'])+'.json',OO0O00O00000OO000 )#line:82
        if not 'zhizu'in session :session ['zhizu']=1 #line:83
        return True #line:84
    def get_zhizu_list22 (OOOO0O0OOO0OO0OO0 ,OO0OOO0OO0O0O0000 ):#line:87
        O0O000OOO0O0OO0OO =OOOO0O0OOO0OO0OO0 .get_zhizu_list ()#line:89
        if 'types'in O0O000OOO0O0OO0OO :#line:90
            if len (O0O000OOO0O0OO0OO ['types'])>=1 :#line:91
                for O00OOOO000OO0O0OO in O0O000OOO0O0OO0OO ['types']:#line:92
                    OO00000OOOOOOO0O0 =public .httpGet ('http://www.bt.cn/api/panel/get_spider?spider=%s'%str (O00OOOO000OO0O0OO ['id']))#line:93
                    if not OO00000OOOOOOO0O0 :continue #line:94
                    try :#line:95
                        OOOOOO0O000000OO0 =json .dumps (OO00000OOOOOOO0O0 )#line:96
                    except :#line:97
                        if not os .path .exists (OOOO0O0OOO0OO0OO0 .__O00O00O0OO0O00O0O +str (O00OOOO000OO0O0OO ['id'])+'.json'):#line:98
                            O0O0OOO00O00O00OO =[]#line:99
                            public .WriteFile (OOOO0O0OOO0OO0OO0 .__O00O00O0OO0O00O0O +str (O00OOOO000OO0O0OO ['id'])+'.json',json .dumps (O0O0OOO00O00O00OO ))#line:100
                        continue #line:101
                    if os .path .exists (OOOO0O0OOO0OO0OO0 .__O00O00O0OO0O00O0O +str (O00OOOO000OO0O0OO ['id'])+'.json'):#line:102
                        OO0O0OO00OOO0O000 =public .ReadFile (OOOO0O0OOO0OO0OO0 .__O00O00O0OO0O00O0O +str (O00OOOO000OO0O0OO ['id'])+'.json')#line:103
                        if OO0O0OO00OOO0O000 :#line:104
                            O0OOOOO0000O0OOOO =list (set (json .loads (OO0O0OO00OOO0O000 )).union (json .loads (OO00000OOOOOOO0O0 )))#line:105
                            public .WriteFile (OOOO0O0OOO0OO0OO0 .__O00O00O0OO0O00O0O +str (O00OOOO000OO0O0OO ['id'])+'.json',json .dumps (O0OOOOO0000O0OOOO ))#line:106
                            OO00O00O00O0OO000 =list (set (OO0O0OO00OOO0O000 ).difference (set (OO00000OOOOOOO0O0 )))#line:107
                            public .httpGet ('https://www.bt.cn/api/panel/add_spiders?address=%s'%json .dumps (OO00O00O00O0OO000 ))#line:109
                        else :#line:110
                            public .WriteFile (OOOO0O0OOO0OO0OO0 .__O00O00O0OO0O00O0O +str (O00OOOO000OO0O0OO ['id'])+'.json',OO00000OOOOOOO0O0 )#line:111
                    else :#line:112
                        public .WriteFile (OOOO0O0OOO0OO0OO0 .__O00O00O0OO0O00O0O +str (O00OOOO000OO0O0OO ['id'])+'.json',OO00000OOOOOOO0O0 )#line:113
        return public .returnMsg (True ,'更新蜘蛛成功!')#line:115
    def start_zhuzu (OO0OOOO00000OO000 ):#line:118
        OOOO0OOOO0OO0OO0O =OO0OOOO00000OO000 .get_zhizu_list ()#line:120
        if 'types'in OOOO0OOOO0OO0OO0O :#line:121
            if len (OOOO0OOOO0OO0OO0O ['types'])>=1 :#line:122
                for OO0OO00O00OOOOOO0 in OOOO0OOOO0OO0OO0O ['types']:#line:123
                    O0O0OOO0000O0O00O =public .httpGet ('http://www.bt.cn/api/panel/get_spider?spider=%s'%str (OO0OO00O00OOOOOO0 ['id']))#line:124
                    if not O0O0OOO0000O0O00O :continue #line:125
                    try :#line:126
                        O000OO00O0OO00O0O =json .dumps (O0O0OOO0000O0O00O )#line:127
                    except :#line:128
                        if not os .path .exists (OO0OOOO00000OO000 .__O00O00O0OO0O00O0O +str (OO0OO00O00OOOOOO0 ['id'])+'.json'):#line:129
                            OOO0OOO0O0000O0O0 =[]#line:130
                            public .WriteFile (OO0OOOO00000OO000 .__O00O00O0OO0O00O0O +str (OO0OO00O00OOOOOO0 ['id'])+'.json',json .dumps (OOO0OOO0O0000O0O0 ))#line:131
                        continue #line:132
                    if os .path .exists (OO0OOOO00000OO000 .__O00O00O0OO0O00O0O +str (OO0OO00O00OOOOOO0 ['id'])+'.json'):#line:133
                        OO0O0OOO00000O0O0 =public .ReadFile (OO0OOOO00000OO000 .__O00O00O0OO0O00O0O +str (OO0OO00O00OOOOOO0 ['id'])+'.json')#line:134
                        if OO0O0OOO00000O0O0 :#line:135
                            OOO0O000OO00OO0OO =list (set (json .loads (OO0O0OOO00000O0O0 )).union (json .loads (O0O0OOO0000O0O00O )))#line:136
                            public .WriteFile (OO0OOOO00000OO000 .__O00O00O0OO0O00O0O +str (OO0OO00O00OOOOOO0 ['id'])+'.json',json .dumps (OOO0O000OO00OO0OO ))#line:137
                            OO000O0O00O000OOO =list (set (OO0O0OOO00000O0O0 ).difference (set (O0O0OOO0000O0O00O )))#line:138
                            public .httpGet ('https://www.bt.cn/api/panel/add_spiders?address=%s'%json .dumps (OO000O0O00O000OOO ))#line:140
                        else :#line:141
                            public .WriteFile (OO0OOOO00000OO000 .__O00O00O0OO0O00O0O +str (OO0OO00O00OOOOOO0 ['id'])+'.json',O0O0OOO0000O0O00O )#line:142
                    else :#line:143
                        public .WriteFile (OO0OOOO00000OO000 .__O00O00O0OO0O00O0O +str (OO0OO00O00OOOOOO0 ['id'])+'.json',O0O0OOO0000O0O00O )#line:144
        return True #line:146
    def get_zhizu_ip (O0OO0O0OO000OO00O ,O00O0000O00O0O0O0 ):#line:149
        OOOOOO0O00O0O0OO0 =O0OO0O0OO000OO00O .get_zhizu_list ()#line:150
        if 'types'in OOOOOO0O00O0O0OO0 :#line:151
            if len (OOOOOO0O00O0O0OO0 ['types'])>=1 :#line:152
                for OO0OOOO0OOOOO00O0 in OOOOOO0O00O0O0OO0 ['types']:#line:153
                    O0OOO0O0OOO0000OO =public .httpGet ('http://www.bt.cn/api/panel/get_spider?spider=%s'%str (OO0OOOO0OOOOO00O0 ['id']))#line:154
                    if not O0OOO0O0OOO0000OO :continue #line:155
                    try :#line:156
                        O0OOO0000O00OO00O =json .dumps (O0OOO0O0OOO0000OO )#line:157
                    except :#line:158
                        if not os .path .exists (O0OO0O0OO000OO00O .__O00O00O0OO0O00O0O +str (OO0OOOO0OOOOO00O0 ['id'])+'.json'):#line:159
                            OO000O000O00OOOOO =[]#line:160
                            public .WriteFile (O0OO0O0OO000OO00O .__O00O00O0OO0O00O0O +str (OO0OOOO0OOOOO00O0 ['id'])+'.json',json .dumps (OO000O000O00OOOOO ))#line:161
                        continue #line:162
                    if os .path .exists (O0OO0O0OO000OO00O .__O00O00O0OO0O00O0O +str (OO0OOOO0OOOOO00O0 ['id'])+'.json'):#line:163
                        O0000O0O0000000O0 =public .ReadFile (O0OO0O0OO000OO00O .__O00O00O0OO0O00O0O +str (OO0OOOO0OOOOO00O0 ['id'])+'.json')#line:164
                        if O0000O0O0000000O0 :#line:165
                            O00OOO0O000OO0O0O =list (set (json .loads (O0000O0O0000000O0 )).union (json .loads (O0OOO0O0OOO0000OO )))#line:166
                            public .WriteFile (O0OO0O0OO000OO00O .__O00O00O0OO0O00O0O +str (OO0OOOO0OOOOO00O0 ['id'])+'.json',json .dumps (O00OOO0O000OO0O0O ))#line:167
                            OOOOO0OOOO0OOOOOO =list (set (O0000O0O0000000O0 ).difference (set (O0OOO0O0OOO0000OO )))#line:168
                            public .httpGet ('https://www.bt.cn/api/panel/add_spiders?address=%s'%json .dumps (OOOOO0OOOO0OOOOOO ))#line:170
                        else :#line:171
                            public .WriteFile (O0OO0O0OO000OO00O .__O00O00O0OO0O00O0O +str (OO0OOOO0OOOOO00O0 ['id'])+'.json',json .dumps (O0OOO0O0OOO0000OO ))#line:172
                    else :#line:173
                        public .WriteFile (O0OO0O0OO000OO00O .__O00O00O0OO0O00O0O +str (OO0OOOO0OOOOO00O0 ['id'])+'.json',json .dumps (O0OOO0O0OOO0000OO ))#line:174
        return public .returnMsg (True ,'更新蜘蛛成功!')#line:176
    def get_process_list (OOOO000O0OOO00000 ):#line:179
        import psutil #line:180
        OOO0O0OOO000OOOOO =0 #line:181
        O00O0OOO0O00000O0 =int (public .ExecShell ('cat /proc/cpuinfo |grep "processor"|wc -l')[0 ])#line:182
        OO0O00O0O000OO00O =psutil .pids ();#line:183
        for O0000000OOO0OO0OO in OO0O00O0O000OO00O :#line:184
            O0OOO00O00O0OOO0O ={}#line:185
            try :#line:186
                OO0O0OOOOOOO0OO00 =psutil .Process (O0000000OOO0OO0OO );#line:187
            except :#line:188
                continue #line:189
            if str (OO0O0OOOOOOO0OO00 .name ())=='php-fpm':#line:190
                OOO0O0OOO000OOOOO +=int (OO0O0OOOOOOO0OO00 .cpu_percent (0.1 ))#line:191
        public .ExecShell ("echo '%s' >/dev/shm/nginx.txt"%OOO0O0OOO000OOOOO /O00O0OOO0O00000O0 )#line:192
        return OOO0O0OOO000OOOOO /O00O0OOO0O00000O0 #line:193
    def Start_apache_cc (O0OO000OO0O0OO0O0 ,OO000000OO0000OOO ):#line:197
        OO000O0O0OO0OO000 =O0OO000OO0O0OO0O0 .auto_sync_apache ()#line:198
        return OO000O0O0OO0OO000 #line:199
    def Get_apap_cc (OO0O00O00O00O00OO ,O000O0O00000O00OO ):#line:202
        O00O00O0OO0O00O00 =public .M ('crontab').where ('name=?',(u'Nginx防火墙智能防御CC',)).getField ('id');#line:203
        if O00O00O0OO0O00O00 :return public .returnMsg (True ,'开启!');#line:204
        else :return public .returnMsg (False ,'关闭!');#line:205
    def Stop_apache_cc (OOO0O0OO0O000O00O ,O0OOO00000O0O00OO ):#line:208
        if os .path .exists ('/dev/shm/nginx.txt'):#line:209
            os .remove ('/dev/shm/nginx.txt')#line:210
        OOO000O0O0O0O0O00 =public .M ('crontab').where ('name=?',(u'Nginx防火墙智能防御CC',)).getField ('id');#line:211
        import crontab #line:212
        if OOO000O0O0O0O0O00 :crontab .crontab ().DelCrontab ({'id':OOO000O0O0O0O0O00 })#line:213
        return public .returnMsg (True ,'设置成功!');#line:214
    def auto_sync_apache (OO0OO0O0OO0000OOO ):#line:217
        OO0OOO000O0OOO000 =public .M ('crontab').where ('name=?',(u'Nginx防火墙智能防御CC',)).getField ('id');#line:218
        import crontab #line:219
        if OO0OOO000O0OOO000 :crontab .crontab ().DelCrontab ({'id':OO0OOO000O0OOO000 })#line:220
        OO0OOOO00OOO0OO0O ={}#line:221
        OO0OOOO00OOO0OO0O ['name']=u'Nginx防火墙智能防御CC'#line:222
        OO0OOOO00OOO0OO0O ['type']='minute-n'#line:223
        OO0OOOO00OOO0OO0O ['where1']='1'#line:224
        OO0OOOO00OOO0OO0O ['sBody']='python /www/server/panel/plugin/btwaf/btwaf_main.py start'#line:225
        OO0OOOO00OOO0OO0O ['backupTo']='localhost'#line:226
        OO0OOOO00OOO0OO0O ['sType']='toShell'#line:227
        OO0OOOO00OOO0OO0O ['hour']=''#line:228
        OO0OOOO00OOO0OO0O ['minute']=''#line:229
        OO0OOOO00OOO0OO0O ['week']=''#line:230
        OO0OOOO00OOO0OO0O ['sName']=''#line:231
        OO0OOOO00OOO0OO0O ['urladdress']=''#line:232
        OO0OOOO00OOO0OO0O ['save']=''#line:233
        crontab .crontab ().AddCrontab (OO0OOOO00OOO0OO0O )#line:234
        return public .returnMsg (True ,'设置成功!');#line:235
    def retuen_nginx (O0O000O0OOOO0O0O0 ):#line:238
        import psutil #line:239
        O000O00O0OOOOOOO0 =0 #line:240
        OO0O0O00OOOOO0000 =int (public .ExecShell ('cat /proc/cpuinfo |grep "processor"|wc -l')[0 ])#line:241
        OO000O0OO0OO0O000 =psutil .pids ();#line:242
        for O0OO00OO00000O0OO in OO000O0OO0OO0O000 :#line:243
            O0O00OOO000O0OOOO ={}#line:244
            try :#line:245
                OOO00O0O0O0OO00O0 =psutil .Process (O0OO00OO00000O0OO );#line:246
            except :#line:247
                continue #line:248
            if str (OOO00O0O0O0OO00O0 .name ())=='php-fpm':#line:249
                O000O00O0OOOOOOO0 +=int (OOO00O0O0O0OO00O0 .cpu_percent (0.1 ))#line:250
        public .ExecShell ("echo '%s' >/dev/shm/nginx.txt"%str (O000O00O0OOOOOOO0 /OO0O0O00OOOOO0000 ))#line:252
        return O000O00O0OOOOOOO0 /OO0O0O00OOOOO0000 #line:253
    def get_config (O0O0OOOO00OOO00OO ,O0OOO0OO0O0O00OO0 ):#line:256
        OO000O00OO000000O =json .loads (public .readFile (O0O0OOOO00OOO00OO .__O00O00O0OO0O00O0O +'config.json'))#line:258
        if not 'retry_cycle'in OO000O00OO000000O :#line:259
            OO000O00OO000000O ['retry_cycle']=60 ;#line:260
            O0O0OOOO00OOO00OO .__OO0O00OO0O00O00O0 (OO000O00OO000000O );#line:261
        if OO000O00OO000000O ['start_time']==0 :#line:262
            OO000O00OO000000O ['start_time']=time .time ();#line:263
            O0O0OOOO00OOO00OO .__OO0O00OO0O00O00O0 (OO000O00OO000000O );#line:264
        return OO000O00OO000000O #line:265
    def get_site_config (OOO00OOO000OO00OO ,O0O000O00O0OO0OO0 ):#line:267
        O00O0O00OO0OOOO0O =public .readFile (OOO00OOO000OO00OO .__O00O00O0OO0O00O0O +'site.json');#line:268
        O000000OOO0O0O0O0 =OOO00OOO000OO00OO .__OOOOOO0OO0O0OOO00 (json .loads (O00O0O00OO0OOOO0O ))#line:269
        if O0O000O00O0OO0OO0 :#line:270
            OO000OO0O0OOOOO0O =OOO00OOO000OO00OO .get_total (None )['sites']#line:271
            OOO0O00O0OO0000O0 =[]#line:272
            for OOOOO0O0O0OOOO0OO in O000000OOO0O0O0O0 .keys ():#line:273
                if not OOOOO0O0O0OOOO0OO in OO000OO0O0OOOOO0O :OO000OO0O0OOOOO0O [OOOOO0O0O0OOOO0OO ]={}#line:274
                O000000OOO0O0O0O0 [OOOOO0O0O0OOOO0OO ]['total']=OOO00OOO000OO00OO .__O0O0OOOO00OOOO0O0 (OO000OO0O0OOOOO0O [OOOOO0O0O0OOOO0OO ])#line:275
                O0O0O000OOOOOO000 =O000000OOO0O0O0O0 [OOOOO0O0O0OOOO0OO ];#line:276
                O0O0O000OOOOOO000 ['siteName']=OOOOO0O0O0OOOO0OO ;#line:277
                OOO0O00O0OO0000O0 .append (O0O0O000OOOOOO000 );#line:278
            O000000OOO0O0O0O0 =sorted (OOO0O00O0OO0000O0 ,key =lambda O0OO0O0OO0OO000O0 :O0OO0O0OO0OO000O0 ['log_size'],reverse =True )#line:279
        return O000000OOO0O0O0O0 #line:280
    def get_site_config_byname (OOOO0OO0OOOO00O0O ,O0OO00O0OO00O0000 ):#line:282
        OO0OOOOO00OOOOO00 =OOOO0OO0OOOO00O0O .get_site_config (None );#line:283
        O0OO0O0OOOO0OO0O0 =OO0OOOOO00OOOOO00 [O0OO00O0OO00O0000 .siteName ]#line:284
        O0OO0O0OOOO0OO0O0 ['top']=OOOO0OO0OOOO00O0O .get_config (None )#line:285
        return O0OO0O0OOOO0OO0O0 #line:286
    def set_open (OO0000O0OOO0OO0OO ,OO00O00OOOO00OO00 ):#line:291
        from BTPanel import session ,cache #line:292
        if not 'btwaf'in session :#line:293
            O00O0OOO0000OOOO0 =OO0000O0OOO0OO0OO .get_btwaf ()#line:294
            if O00O0OOO0000OOOO0 ==0 :#line:295
                OO0000O0OOO0OO0OO .stop ()#line:296
                return public .returnMsg (False ,'')#line:297
        OOO0OO000000O00OO =OO0000O0OOO0OO0OO .get_config (None )#line:299
        if OOO0OO000000O00OO ['open']:#line:300
            OOO0OO000000O00OO ['open']=False #line:301
            OOO0OO000000O00OO ['start_time']=0 #line:302
        else :#line:303
            OOO0OO000000O00OO ['open']=True #line:304
            OOO0OO000000O00OO ['start_time']=int (time .time ())#line:305
        OO0000O0OOO0OO0OO .__O0OOOO0000OOOOOOO (OO0000O0OOO0OO0OO .__O0OO0O0O000O0OOOO [OOO0OO000000O00OO ['open']]+'网站防火墙(WAF)');#line:306
        OO0000O0OOO0OO0OO .__OO0O00OO0O00O00O0 (OOO0OO000000O00OO )#line:307
        return public .returnMsg (True ,'设置成功!');#line:308
    def set_obj_open (O0000OO0OO0OO0OOO ,OOOOO0O0OOOO000OO ):#line:310
        O0O0O00O0OO0O00OO =O0000OO0OO0OO0OOO .get_config (None )#line:311
        if type (O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ])!=bool :#line:312
            if O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]['open']:#line:313
                O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]['open']=False #line:314
            else :#line:315
                O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]['open']=True #line:316
            O0000OO0OO0OO0OOO .__O0OOOO0000OOOOOOO (O0000OO0OO0OO0OOO .__O0OO0O0O000O0OOOO [O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]['open']]+'【'+OOOOO0O0OOOO000OO .obj +'】功能');#line:317
        else :#line:318
            if O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]:#line:319
                O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]=False #line:320
            else :#line:321
                O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]=True #line:322
            O0000OO0OO0OO0OOO .__O0OOOO0000OOOOOOO (O0000OO0OO0OO0OOO .__O0OO0O0O000O0OOOO [O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]]+'【'+OOOOO0O0OOOO000OO .obj +'】功能');#line:323
        O0000OO0OO0OO0OOO .__OO0O00OO0O00O00O0 (O0O0O00O0OO0O00OO )#line:325
        return public .returnMsg (True ,'设置成功!');#line:326
    def set_site_obj_open (OO00OO0OOOO00O00O ,OOOOO0O0O000OOO00 ):#line:328
        OOOO00OOO0O0OOO00 =OO00OO0OOOO00O00O .get_site_config (None )#line:329
        if type (OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ])!=bool :#line:330
            if OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]['open']:#line:331
                OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]['open']=False #line:332
            else :#line:333
                OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]['open']=True #line:334
            OO00OO0OOOO00O00O .__O0OOOO0000OOOOOOO (OO00OO0OOOO00O00O .__O0OO0O0O000O0OOOO [OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]['open']]+'网站【'+OOOOO0O0O000OOO00 .siteName +'】【'+OOOOO0O0O000OOO00 .obj +'】功能');#line:336
        else :#line:337
            if OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]:#line:338
                OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]=False #line:339
            else :#line:340
                OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]=True #line:341
            OO00OO0OOOO00O00O .__O0OOOO0000OOOOOOO (OO00OO0OOOO00O00O .__O0OO0O0O000O0OOOO [OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]]+'网站【'+OOOOO0O0O000OOO00 .siteName +'】【'+OOOOO0O0O000OOO00 .obj +'】功能');#line:343
        if OOOOO0O0O000OOO00 .obj =='drop_abroad':OO00OO0OOOO00O00O .__OOO0OOO0O0O0OO0OO ();#line:344
        OO00OO0OOOO00O00O .__OO000O00OOO0OO0O0 (OOOO00OOO0O0OOO00 )#line:345
        return public .returnMsg (True ,'设置成功!');#line:346
    def set_obj_status (O0000OO0OO000OOOO ,O0O00O0O0O0OOOOOO ):#line:348
        OOO0O000O00OO00OO =O0000OO0OO000OOOO .get_config (None )#line:349
        OOO0O000O00OO00OO [O0O00O0O0O0OOOOOO .obj ]['status']=int (O0O00O0O0O0OOOOOO .statusCode )#line:350
        O0000OO0OO000OOOO .__OO0O00OO0O00O00O0 (OOO0O000O00OO00OO )#line:351
        return public .returnMsg (True ,'设置成功!');#line:352
    def set_cc_conf (O0OOOO00OO000O000 ,O000OOOO00OOO0OO0 ):#line:354
        OO00000O000O000OO =O0OOOO00OO000O000 .get_config (None )#line:355
        OO00000O000O000OO ['cc']['cycle']=int (O000OOOO00OOO0OO0 .cycle )#line:356
        OO00000O000O000OO ['cc']['limit']=int (O000OOOO00OOO0OO0 .limit )#line:357
        OO00000O000O000OO ['cc']['endtime']=int (O000OOOO00OOO0OO0 .endtime )#line:358
        OO00000O000O000OO ['cc']['increase']=(O000OOOO00OOO0OO0 .increase =='1')|False #line:359
        O0OOOO00OO000O000 .__OO0O00OO0O00O00O0 (OO00000O000O000OO )#line:360
        O0OOOO00OO000O000 .__O0OOOO0000OOOOOOO ('设置全局CC配置为：'+O000OOOO00OOO0OO0 .cycle +' 秒内累计请求超过 '+O000OOOO00OOO0OO0 .limit +' 次后,封锁 '+O000OOOO00OOO0OO0 .endtime +' 秒'+',增强:'+O000OOOO00OOO0OO0 .increase );#line:362
        return public .returnMsg (True ,'设置成功!');#line:363
    def set_site_cc_conf (OO000OOO00OOOO000 ,O0OO0000O0OO0OOO0 ):#line:365
        O00OOOOO0OOO0O0O0 =OO000OOO00OOOO000 .get_site_config (None )#line:366
        O00OOOOO0OOO0O0O0 [O0OO0000O0OO0OOO0 .siteName ]['cc']['cycle']=int (O0OO0000O0OO0OOO0 .cycle )#line:367
        O00OOOOO0OOO0O0O0 [O0OO0000O0OO0OOO0 .siteName ]['cc']['limit']=int (O0OO0000O0OO0OOO0 .limit )#line:368
        O00OOOOO0OOO0O0O0 [O0OO0000O0OO0OOO0 .siteName ]['cc']['endtime']=int (O0OO0000O0OO0OOO0 .endtime )#line:369
        O00OOOOO0OOO0O0O0 [O0OO0000O0OO0OOO0 .siteName ]['cc']['increase']=(O0OO0000O0OO0OOO0 .increase =='1')|False #line:370
        OO000OOO00OOOO000 .__OO000O00OOO0OO0O0 (O00OOOOO0OOO0O0O0 )#line:371
        OO000OOO00OOOO000 .__O0OOOO0000OOOOOOO ('设置站点【'+O0OO0000O0OO0OOO0 .siteName +'】CC配置为：'+O0OO0000O0OO0OOO0 .cycle +' 秒内累计请求超过 '+O0OO0000O0OO0OOO0 .limit +' 次后,封锁 '+O0OO0000O0OO0OOO0 .endtime +' 秒'+',增强:'+O0OO0000O0OO0OOO0 .increase );#line:373
        return public .returnMsg (True ,'设置成功!');#line:374
    def add_cnip (OO00OOOOOO0O0OO00 ,OO0OO00O00OOO0000 ):#line:376
        O000OOO0000OO000O =[OO00OOOOOO0O0OO00 .__O000O00000O0OOOOO (OO0OO00O00OOO0000 .start_ip ),OO00OOOOOO0O0OO00 .__O000O00000O0OOOOO (OO0OO00O00OOO0000 .end_ip )]#line:377
        if not O000OOO0000OO000O [0 ]or not O000OOO0000OO000O [1 ]:return public .returnMsg (False ,'IP段格式不正确');#line:378
        if not OO00OOOOOO0O0OO00 .__O0OOOOOOOOO0OO00O (O000OOO0000OO000O ):return public .returnMsg (False ,'起始IP不能大于结束IP');#line:379
        OO000OOO00O000OOO =OO00OOOOOO0O0OO00 .__O0000000OO00000O0 ('cn')#line:380
        if O000OOO0000OO000O in OO000OOO00O000OOO :return public .returnMsg (False ,'指定IP段已存在!');#line:381
        OO000OOO00O000OOO .insert (0 ,O000OOO0000OO000O )#line:382
        OO00OOOOOO0O0OO00 .__O0O00O0O0O0O0O000 ('cn',OO000OOO00O000OOO )#line:383
        OO00OOOOOO0O0OO00 .__O0OOOO0000OOOOOOO ('添加IP段['+OO0OO00O00OOO0000 .start_ip +'-'+OO0OO00O00OOO0000 .end_ip +']到国内IP库');#line:384
        return public .returnMsg (True ,'添加成功!');#line:385
    def remove_cnip (O0OO0OO00OOOOOOO0 ,O0OO0O0O0OOOOOOO0 ):#line:387
        O0000000O00000OO0 =int (O0OO0O0O0OOOOOOO0 .index )#line:388
        OO0000OO0OO0O0000 =O0OO0OO00OOOOOOO0 .__O0000000OO00000O0 ('cn')#line:389
        OO0OOOO000O00O0O0 =OO0000OO0OO0O0000 [O0000000O00000OO0 ]#line:390
        del (OO0000OO0OO0O0000 [O0000000O00000OO0 ])#line:391
        O0OO0OO00OOOOOOO0 .__O0O00O0O0O0O0O000 ('cn',OO0000OO0OO0O0000 )#line:392
        O0OO0OO00OOOOOOO0 .__O0OOOO0000OOOOOOO ('从国内IP库删除['+'.'.join (map (str ,OO0OOOO000O00O0O0 [0 ]))+'-'+'.'.join (map (str ,OO0OOOO000O00O0O0 [1 ]))+']');#line:393
        return public .returnMsg (True ,'删除成功!');#line:394
    def add_ip_white (O0O00O0OOO000000O ,OOOOOO0O00O0OO0O0 ):#line:396
        OO00OOOOOOOO0O000 =[O0O00O0OOO000000O .__O000O00000O0OOOOO (OOOOOO0O00O0OO0O0 .start_ip ),O0O00O0OOO000000O .__O000O00000O0OOOOO (OOOOOO0O00O0OO0O0 .end_ip )]#line:397
        if not OO00OOOOOOOO0O000 [0 ]or not OO00OOOOOOOO0O000 [1 ]:return public .returnMsg (False ,'IP段格式不正确');#line:398
        if not O0O00O0OOO000000O .__O0OOOOOOOOO0OO00O (OO00OOOOOOOO0O000 ):return public .returnMsg (False ,'起始IP不能大于结束IP');#line:399
        O0O0OOO0OO000OOO0 =O0O00O0OOO000000O .__O0000000OO00000O0 ('ip_white')#line:400
        if OO00OOOOOOOO0O000 in O0O0OOO0OO000OOO0 :return public .returnMsg (False ,'指定IP段已存在!');#line:401
        O0O0OOO0OO000OOO0 .insert (0 ,OO00OOOOOOOO0O000 )#line:402
        O0O00O0OOO000000O .__O0O00O0O0O0O0O000 ('ip_white',O0O0OOO0OO000OOO0 )#line:403
        O0O00O0OOO000000O .__O0OOOO0000OOOOOOO ('添加IP段['+OOOOOO0O00O0OO0O0 .start_ip +'-'+OOOOOO0O00O0OO0O0 .end_ip +']到IP白名单');#line:404
        return public .returnMsg (True ,'添加成功!');#line:405
    def remove_ip_white (OOOOO00O0OO000OO0 ,O0O000000000OO0O0 ):#line:407
        OOOO0000O0O0OO0O0 =int (O0O000000000OO0O0 .index )#line:408
        OOOOO00OOO0000O00 =OOOOO00O0OO000OO0 .__O0000000OO00000O0 ('ip_white')#line:409
        OOOOO00O0O0OO0O0O =OOOOO00OOO0000O00 [OOOO0000O0O0OO0O0 ]#line:410
        del (OOOOO00OOO0000O00 [OOOO0000O0O0OO0O0 ])#line:411
        OOOOO00O0OO000OO0 .__O0O00O0O0O0O0O000 ('ip_white',OOOOO00OOO0000O00 )#line:412
        OOOOO00O0OO000OO0 .__O0OOOO0000OOOOOOO ('从IP白名单删除['+'.'.join (map (str ,OOOOO00O0O0OO0O0O [0 ]))+'-'+'.'.join (map (str ,OOOOO00O0O0OO0O0O [1 ]))+']');#line:413
        return public .returnMsg (True ,'删除成功!');#line:414
    def import_data (O00O0O000OOO0O0O0 ,OOOOO0OOOO0O0O00O ):#line:416
        O0O0OO0000OO0O0OO =OOOOO0OOOO0O0O00O .s_Name ;#line:417
        O00OOOO0O00OOO0O0 =json .loads (OOOOO0OOOO0O0O00O .pdata )#line:418
        if not O00OOOO0O00OOO0O0 :return public .returnMsg (False ,'数据格式不正确');#line:419
        OO000OOO0O0OO0000 =O00O0O000OOO0O0O0 .__O0000000OO00000O0 (O0O0OO0000OO0O0OO );#line:420
        for OO0O00O0OOOO000OO in O00OOOO0O00OOO0O0 :#line:421
            if OO0O00O0OOOO000OO in OO000OOO0O0OO0000 :continue ;#line:422
            OO000OOO0O0OO0000 .insert (0 ,OO0O00O0OOOO000OO )#line:423
        O00O0O000OOO0O0O0 .__O0O00O0O0O0O0O000 (O0O0OO0000OO0O0OO ,OO000OOO0O0OO0000 )#line:424
        return public .returnMsg (True ,'导入成功!')#line:425
    def output_data (OO0OO0OOOOOOOO0O0 ,O0000OO0OOOO0OOO0 ):#line:427
        O00OOOOO00O00OOOO =OO0OO0OOOOOOOO0O0 .__O0000000OO00000O0 (O0000OO0OOOO0OOO0 .s_Name )#line:428
        return O00OOOOO00O00OOOO ;#line:429
    def add_ip_black (OOO0O000O0OO0O0OO ,O0000O000OO0OOO00 ):#line:431
        OO0OOOOO0000000OO =[OOO0O000O0OO0O0OO .__O000O00000O0OOOOO (O0000O000OO0OOO00 .start_ip ),OOO0O000O0OO0O0OO .__O000O00000O0OOOOO (O0000O000OO0OOO00 .end_ip )]#line:432
        if not OO0OOOOO0000000OO [0 ]or not OO0OOOOO0000000OO [1 ]:return public .returnMsg (False ,'IP段格式不正确');#line:433
        if not OOO0O000O0OO0O0OO .__O0OOOOOOOOO0OO00O (OO0OOOOO0000000OO ):return public .returnMsg (False ,'起始IP不能大于结束IP');#line:434
        O0OO0O000000O000O =OOO0O000O0OO0O0OO .__O0000000OO00000O0 ('ip_black')#line:435
        if OO0OOOOO0000000OO in O0OO0O000000O000O :return public .returnMsg (False ,'指定IP段已存在!');#line:436
        O0OO0O000000O000O .insert (0 ,OO0OOOOO0000000OO )#line:437
        OOO0O000O0OO0O0OO .__O0O00O0O0O0O0O000 ('ip_black',O0OO0O000000O000O )#line:438
        OOO0O000O0OO0O0OO .__O0OOOO0000OOOOOOO ('添加IP段['+O0000O000OO0OOO00 .start_ip +'-'+O0000O000OO0OOO00 .end_ip +']到IP黑名单');#line:439
        return public .returnMsg (True ,'添加成功!');#line:440
    def remove_ip_black (O000OOOO00000O000 ,O0OOOO0OO00000O0O ):#line:442
        OOO000O00OOOOOO00 =int (O0OOOO0OO00000O0O .index )#line:443
        OOO0000O000O00O0O =O000OOOO00000O000 .__O0000000OO00000O0 ('ip_black')#line:444
        O0O000OO000000O0O =OOO0000O000O00O0O [OOO000O00OOOOOO00 ]#line:445
        del (OOO0000O000O00O0O [OOO000O00OOOOOO00 ])#line:446
        O000OOOO00000O000 .__O0O00O0O0O0O0O000 ('ip_black',OOO0000O000O00O0O )#line:447
        O000OOOO00000O000 .__O0OOOO0000OOOOOOO ('从IP黑名单删除['+'.'.join (map (str ,O0O000OO000000O0O [0 ]))+'-'+'.'.join (map (str ,O0O000OO000000O0O [1 ]))+']');#line:448
        return public .returnMsg (True ,'删除成功!');#line:449
    def add_url_white (O00O00OO0O0OO0O00 ,OOO0OO0O0O00OOOO0 ):#line:451
        O00000O0000O0O0OO =O00O00OO0O0OO0O00 .__O0000000OO00000O0 ('url_white')#line:452
        O00OO0OO000O00000 =OOO0OO0O0O00OOOO0 .url_rule .strip ()#line:453
        if OOO0OO0O0O00OOOO0 .url_rule in O00000O0000O0O0OO :return public .returnMsg (False ,'您添加的URL已存在')#line:454
        O00000O0000O0O0OO .insert (0 ,O00OO0OO000O00000 )#line:455
        O00O00OO0O0OO0O00 .__O0O00O0O0O0O0O000 ('url_white',O00000O0000O0O0OO )#line:456
        O00O00OO0O0OO0O00 .__O0OOOO0000OOOOOOO ('添加url规则['+O00OO0OO000O00000 +']到URL白名单');#line:457
        return public .returnMsg (True ,'添加成功!');#line:458
    def remove_url_white (O000O0O00OO0OOOOO ,O000OO00OO0O0O0OO ):#line:460
        OO0OO00000O000000 =O000O0O00OO0OOOOO .__O0000000OO00000O0 ('url_white')#line:461
        O000OOO0000OO00OO =int (O000OO00OO0O0O0OO .index )#line:462
        OO0OO0O0OO0O000O0 =OO0OO00000O000000 [O000OOO0000OO00OO ]#line:463
        del (OO0OO00000O000000 [O000OOO0000OO00OO ])#line:464
        O000O0O00OO0OOOOO .__O0O00O0O0O0O0O000 ('url_white',OO0OO00000O000000 )#line:465
        O000O0O00OO0OOOOO .__O0OOOO0000OOOOOOO ('从URL白名单删除URL规则['+OO0OO0O0OO0O000O0 +']');#line:466
        return public .returnMsg (True ,'删除成功!');#line:467
    def add_url_black (O0000O0OOOOO00O00 ,O0000O0000O00O0OO ):#line:469
        OOO00OO0OOO0OOO00 =O0000O0OOOOO00O00 .__O0000000OO00000O0 ('url_black')#line:470
        O00OO0OOO00O0OO00 =O0000O0000O00O0OO .url_rule .strip ()#line:471
        if O0000O0000O00O0OO .url_rule in OOO00OO0OOO0OOO00 :return public .returnMsg (False ,'您添加的URL已存在')#line:472
        OOO00OO0OOO0OOO00 .insert (0 ,O00OO0OOO00O0OO00 )#line:473
        O0000O0OOOOO00O00 .__O0O00O0O0O0O0O000 ('url_black',OOO00OO0OOO0OOO00 )#line:474
        O0000O0OOOOO00O00 .__O0OOOO0000OOOOOOO ('添加url规则['+O00OO0OOO00O0OO00 +']到URL黑名单');#line:475
        return public .returnMsg (True ,'添加成功!');#line:476
    def remove_url_black (O0O0O0000O00O00OO ,OO00O0O000OOO0O0O ):#line:478
        O0OOO0OOOO0OO00OO =O0O0O0000O00O00OO .__O0000000OO00000O0 ('url_black')#line:479
        OO000OO0OOO0OO0O0 =int (OO00O0O000OOO0O0O .index )#line:480
        OO000OOOO0O0O0OO0 =O0OOO0OOOO0OO00OO [OO000OO0OOO0OO0O0 ]#line:481
        del (O0OOO0OOOO0OO00OO [OO000OO0OOO0OO0O0 ])#line:482
        O0O0O0000O00O00OO .__O0O00O0O0O0O0O000 ('url_black',O0OOO0OOOO0OO00OO )#line:483
        O0O0O0000O00O00OO .__O0OOOO0000OOOOOOO ('从URL黑名单删除URL规则['+OO000OOOO0O0O0OO0 +']');#line:484
        return public .returnMsg (True ,'删除成功!');#line:485
    def save_scan_rule (O000OOO0OO00O0OO0 ,OOOO000OO00O0000O ):#line:487
        O000OO00O000O0O0O ={'header':OOOO000OO00O0000O .header ,'cookie':OOOO000OO00O0000O .cookie ,'args':OOOO000OO00O0000O .args }#line:488
        O000OOO0OO00O0OO0 .__O0O00O0O0O0O0O000 ('scan_black',O000OO00O000O0O0O )#line:489
        O000OOO0OO00O0OO0 .__O0OOOO0000OOOOOOO ('修改扫描器过滤规则');#line:490
        return public .returnMsg (True ,'设置成功')#line:491
    def set_retry (OOOO0OO0O0OOOO000 ,OO0O0O0O0OOO0OO00 ):#line:493
        O0OO00O00OO0O0O00 =OOOO0OO0O0OOOO000 .get_config (None )#line:494
        O0OO00O00OO0O0O00 ['retry']=int (OO0O0O0O0OOO0OO00 .retry )#line:495
        O0OO00O00OO0O0O00 ['retry_cycle']=int (OO0O0O0O0OOO0OO00 .retry_cycle )#line:496
        O0OO00O00OO0O0O00 ['retry_time']=int (OO0O0O0O0OOO0OO00 .retry_time )#line:497
        OOOO0OO0O0OOOO000 .__OO0O00OO0O00O00O0 (O0OO00O00OO0O0O00 )#line:498
        OOOO0OO0O0OOOO000 .__O0OOOO0000OOOOOOO ('设置非法请求容忍阈值: '+OO0O0O0O0OOO0OO00 .retry_cycle +' 秒内累计超过 '+OO0O0O0O0OOO0OO00 .retry +' 次, 封锁 '+OO0O0O0O0OOO0OO00 .retry_time +' 秒');#line:499
        return public .returnMsg (True ,'设置成功!');#line:500
    def set_site_retry (OOOOO000O00O0000O ,OOO000O0OOO00O0O0 ):#line:502
        O0O0OO00O00OOOOO0 =OOOOO000O00O0000O .get_site_config (None )#line:503
        O0O0OO00O00OOOOO0 [OOO000O0OOO00O0O0 .siteName ]['retry']=int (OOO000O0OOO00O0O0 .retry )#line:504
        O0O0OO00O00OOOOO0 [OOO000O0OOO00O0O0 .siteName ]['retry_cycle']=int (OOO000O0OOO00O0O0 .retry_cycle )#line:505
        O0O0OO00O00OOOOO0 [OOO000O0OOO00O0O0 .siteName ]['retry_time']=int (OOO000O0OOO00O0O0 .retry_time )#line:506
        OOOOO000O00O0000O .__OO000O00OOO0OO0O0 (O0O0OO00O00OOOOO0 )#line:507
        OOOOO000O00O0000O .__O0OOOO0000OOOOOOO ('设置网站【'+OOO000O0OOO00O0O0 .siteName +'】非法请求容忍阈值: '+OOO000O0OOO00O0O0 .retry_cycle +' 秒内累计超过 '+OOO000O0OOO00O0O0 .retry +' 次, 封锁 '+OOO000O0OOO00O0O0 .retry_time +' 秒');#line:509
        return public .returnMsg (True ,'设置成功!');#line:510
    def set_site_cdn_state (O00OOOO0OOO00O00O ,O00OO0O00OO0OO000 ):#line:512
        O0O000O000OO00OO0 =O00OOOO0OOO00O00O .get_site_config (None )#line:513
        if O0O000O000OO00OO0 [O00OO0O00OO0OO000 .siteName ]['cdn']:#line:514
            O0O000O000OO00OO0 [O00OO0O00OO0OO000 .siteName ]['cdn']=False #line:515
        else :#line:516
            O0O000O000OO00OO0 [O00OO0O00OO0OO000 .siteName ]['cdn']=True #line:517
        O00OOOO0OOO00O00O .__OO000O00OOO0OO0O0 (O0O000O000OO00OO0 )#line:518
        O00OOOO0OOO00O00O .__O0OOOO0000OOOOOOO (O00OOOO0OOO00O00O .__O0OO0O0O000O0OOOO [O0O000O000OO00OO0 [O00OO0O00OO0OO000 .siteName ]['cdn']]+'站点【'+O00OO0O00OO0OO000 .siteName +'】CDN模式');#line:519
        return public .returnMsg (True ,'设置成功!');#line:520
    def get_site_cdn_header (OOO0O0O00O00O0O00 ,OOO0000O0O0OO00OO ):#line:522
        OOOOOOOOO0O0OO00O =OOO0O0O00O00O0O00 .get_site_config (None )#line:523
        return OOOOOOOOO0O0OO00O [OOO0000O0O0OO00OO .siteName ]['cdn_header']#line:524
    def add_site_cdn_header (O0OOOOO00O0O00000 ,OOO00O00000000O0O ):#line:526
        OO00O0O00000000OO =O0OOOOO00O0O00000 .get_site_config (None )#line:527
        OOO00O00000000O0O .cdn_header =OOO00O00000000O0O .cdn_header .strip ().lower ();#line:528
        if OOO00O00000000O0O .cdn_header in OO00O0O00000000OO [OOO00O00000000O0O .siteName ]['cdn_header']:return public .returnMsg (False ,'您添加的请求头已存在!');#line:529
        OO00O0O00000000OO [OOO00O00000000O0O .siteName ]['cdn_header'].append (OOO00O00000000O0O .cdn_header )#line:530
        O0OOOOO00O0O00000 .__OO000O00OOO0OO0O0 (OO00O0O00000000OO )#line:531
        O0OOOOO00O0O00000 .__O0OOOO0000OOOOOOO ('添加站点【'+OOO00O00000000O0O .siteName +'】CDN-Header【'+OOO00O00000000O0O .cdn_header +'】');#line:532
        return public .returnMsg (True ,'添加成功!');#line:533
    def remove_site_cdn_header (O0000O0OOOO00OOO0 ,O00O0000O0000OO00 ):#line:535
        OO000000OOO0O00O0 =O0000O0OOOO00OOO0 .get_site_config (None )#line:536
        O00O0000O0000OO00 .cdn_header =O00O0000O0000OO00 .cdn_header .strip ().lower ();#line:537
        if not O00O0000O0000OO00 .cdn_header in OO000000OOO0O00O0 [O00O0000O0000OO00 .siteName ]['cdn_header']:return public .returnMsg (False ,'指定请求头不存在!');#line:538
        for O00OO0O00000O00OO in range (len (OO000000OOO0O00O0 [O00O0000O0000OO00 .siteName ]['cdn_header'])):#line:539
            if O00O0000O0000OO00 .cdn_header ==OO000000OOO0O00O0 [O00O0000O0000OO00 .siteName ]['cdn_header'][O00OO0O00000O00OO ]:#line:540
                O0000O0OOOO00OOO0 .__O0OOOO0000OOOOOOO ('删除站点【'+O00O0000O0000OO00 .siteName +'】CDN-Header【'+OO000000OOO0O00O0 [O00O0000O0000OO00 .siteName ]['cdn_header'][O00OO0O00000O00OO ]+'】');#line:542
                del (OO000000OOO0O00O0 [O00O0000O0000OO00 .siteName ]['cdn_header'][O00OO0O00000O00OO ])#line:543
                break ;#line:544
        O0000O0OOOO00OOO0 .__OO000O00OOO0OO0O0 (OO000000OOO0O00O0 )#line:545
        return public .returnMsg (True ,'删除成功!');#line:546
    def get_site_rule (OO00OO0OOO00O000O ,O000000OOO00OOO0O ):#line:548
        O0O0OO0OOO0000O00 =OO00OO0OOO00O000O .get_site_config (None )#line:549
        return O0O0OO0OOO0000O00 [O000000OOO00OOO0O .siteName ][O000000OOO00OOO0O .ruleName ]#line:550
    def add_site_rule (OO00OO00O0OO0OO00 ,OO0OO0OO000OOOOOO ):#line:552
        O0OO0OOO00O0000OO =OO00OO00O0OO0OO00 .get_site_config (None )#line:553
        if not OO0OO0OO000OOOOOO .ruleName in O0OO0OOO00O0000OO [OO0OO0OO000OOOOOO .siteName ]:return public .returnMsg (False ,'指定规则不存在!');#line:554
        OO0O0OOOO0OO0000O =type (O0OO0OOO00O0000OO [OO0OO0OO000OOOOOO .siteName ][OO0OO0OO000OOOOOO .ruleName ])#line:555
        if OO0O0OOOO0OO0000O ==bool :return public .returnMsg (False ,'指定规则不存在!');#line:556
        if OO0O0OOOO0OO0000O ==str :O0OO0OOO00O0000OO [OO0OO0OO000OOOOOO .siteName ][OO0OO0OO000OOOOOO .ruleName ]=OO0OO0OO000OOOOOO .ruleValue #line:557
        if OO0O0OOOO0OO0000O ==list :#line:558
            if OO0OO0OO000OOOOOO .ruleName =='url_rule'or OO0OO0OO000OOOOOO .ruleName =='url_tell':#line:559
                for O0OOOO00000000OOO in O0OO0OOO00O0000OO [OO0OO0OO000OOOOOO .siteName ][OO0OO0OO000OOOOOO .ruleName ]:#line:560
                    if O0OOOO00000000OOO [0 ]==OO0OO0OO000OOOOOO .ruleUri :return public .returnMsg (False ,'指定URI已存在!');#line:561
                OOO0OO0O0O0OOO0O0 =[]#line:562
                OOO0OO0O0O0OOO0O0 .append (OO0OO0OO000OOOOOO .ruleUri )#line:563
                OOO0OO0O0O0OOO0O0 .append (OO0OO0OO000OOOOOO .ruleValue )#line:564
                if OO0OO0OO000OOOOOO .ruleName =='url_tell':#line:565
                    OO00OO00O0OO0OO00 .__O0OOOO0000OOOOOOO ('添加站点【'+OO0OO0OO000OOOOOO .siteName +'】URI【'+OO0OO0OO000OOOOOO .ruleUri +'】保护规则,参数【'+OO0OO0OO000OOOOOO .ruleValue +'】,参数值【'+OO0OO0OO000OOOOOO .rulePass +'】');#line:567
                    OOO0OO0O0O0OOO0O0 .append (OO0OO0OO000OOOOOO .rulePass )#line:568
                else :#line:569
                    OO00OO00O0OO0OO00 .__O0OOOO0000OOOOOOO ('添加站点【'+OO0OO0OO000OOOOOO .siteName +'】URI【'+OO0OO0OO000OOOOOO .ruleUri +'】过滤规则【'+OO0OO0OO000OOOOOO .ruleValue +'】');#line:570
                O0OO0OOO00O0000OO [OO0OO0OO000OOOOOO .siteName ][OO0OO0OO000OOOOOO .ruleName ].insert (0 ,OOO0OO0O0O0OOO0O0 )#line:571
            else :#line:572
                if OO0OO0OO000OOOOOO .ruleValue in O0OO0OOO00O0000OO [OO0OO0OO000OOOOOO .siteName ][OO0OO0OO000OOOOOO .ruleName ]:return public .returnMsg (False ,'指定规则已存在!');#line:573
                O0OO0OOO00O0000OO [OO0OO0OO000OOOOOO .siteName ][OO0OO0OO000OOOOOO .ruleName ].insert (0 ,OO0OO0OO000OOOOOO .ruleValue )#line:574
                OO00OO00O0OO0OO00 .__O0OOOO0000OOOOOOO ('添加站点【'+OO0OO0OO000OOOOOO .siteName +'】【'+OO0OO0OO000OOOOOO .ruleName +'】过滤规则【'+OO0OO0OO000OOOOOO .ruleValue +'】');#line:575
        OO00OO00O0OO0OO00 .__OO000O00OOO0OO0O0 (O0OO0OOO00O0000OO )#line:576
        return public .returnMsg (True ,'添加成功!');#line:577
    def remove_site_rule (OOOOOO0OO0O00O0O0 ,O0OOO0O0000000OO0 ):#line:579
        OOO0000OO0OO00OO0 =OOOOOO0OO0O00O0O0 .get_site_config (None )#line:580
        O0O0OO0OOO0OOOOO0 =int (O0OOO0O0000000OO0 .index )#line:581
        if not O0OOO0O0000000OO0 .ruleName in OOO0000OO0OO00OO0 [O0OOO0O0000000OO0 .siteName ]:return public .returnMsg (False ,'指定规则不存在!');#line:582
        O0O0O0O0OO0O00OOO =OOO0000OO0OO00OO0 [O0OOO0O0000000OO0 .siteName ][O0OOO0O0000000OO0 .ruleName ][O0O0OO0OOO0OOOOO0 ]#line:583
        del (OOO0000OO0OO00OO0 [O0OOO0O0000000OO0 .siteName ][O0OOO0O0000000OO0 .ruleName ][O0O0OO0OOO0OOOOO0 ])#line:584
        OOOOOO0OO0O00O0O0 .__OO000O00OOO0OO0O0 (OOO0000OO0OO00OO0 )#line:585
        OOOOOO0OO0O00O0O0 .__O0OOOO0000OOOOOOO ('删除站点【'+O0OOO0O0000000OO0 .siteName +'】【'+O0OOO0O0000000OO0 .ruleName +'】过滤规则【'+json .dumps (O0O0O0O0OO0O00OOO )+'】');#line:586
        return public .returnMsg (True ,'删除成功!');#line:587
    def get_rule (OOOOOO0OO0O00O0OO ,OO0000OOO00OO00O0 ):#line:589
        O00O000O00OOO0OOO =OOOOOO0OO0O00O0OO .__O0000000OO00000O0 (OO0000OOO00OO00O0 .ruleName )#line:590
        if not O00O000O00OOO0OOO :return [];#line:591
        return O00O000O00OOO0OOO #line:592
    def add_rule (O0000O00OOO0O000O ,OOOO00OOOOOO0OOOO ):#line:594
        O00OO0OO00O000OO0 =O0000O00OOO0O000O .__O0000000OO00000O0 (OOOO00OOOOOO0OOOO .ruleName )#line:595
        O0O0OO0OO00OO0OOO =[1 ,OOOO00OOOOOO0OOOO .ruleValue .strip (),OOOO00OOOOOO0OOOO .ps ,1 ]#line:596
        for OO0OOOO000O00OO00 in O00OO0OO00O000OO0 :#line:597
            if OO0OOOO000O00OO00 [1 ]==O0O0OO0OO00OO0OOO [1 ]:return public .returnMsg (False ,'指定规则已存在，请勿重复添加');#line:598
        O00OO0OO00O000OO0 .append (O0O0OO0OO00OO0OOO )#line:599
        O0000O00OOO0O000O .__O0O00O0O0O0O0O000 (OOOO00OOOOOO0OOOO .ruleName ,O00OO0OO00O000OO0 )#line:600
        O0000O00OOO0O000O .__O0OOOO0000OOOOOOO ('添加全局规则【'+OOOO00OOOOOO0OOOO .ruleName +'】【'+OOOO00OOOOOO0OOOO .ps +'】');#line:601
        return public .returnMsg (True ,'添加成功!');#line:602
    def remove_rule (OOOO000O0O0O0O0O0 ,O0OOOOOOOOOO000O0 ):#line:604
        O00OO0O0000OO0O0O =OOOO000O0O0O0O0O0 .__O0000000OO00000O0 (O0OOOOOOOOOO000O0 .ruleName )#line:605
        OOO00OOO0000OOOO0 =int (O0OOOOOOOOOO000O0 .index )#line:606
        OOOOOOO0OO0O00OOO =O00OO0O0000OO0O0O [OOO00OOO0000OOOO0 ][2 ]#line:607
        del (O00OO0O0000OO0O0O [OOO00OOO0000OOOO0 ])#line:608
        OOOO000O0O0O0O0O0 .__O0O00O0O0O0O0O000 (O0OOOOOOOOOO000O0 .ruleName ,O00OO0O0000OO0O0O )#line:609
        OOOO000O0O0O0O0O0 .__O0OOOO0000OOOOOOO ('删除全局规则【'+O0OOOOOOOOOO000O0 .ruleName +'】【'+OOOOOOO0OO0O00OOO +'】');#line:610
        return public .returnMsg (True ,'删除成功!');#line:611
    def modify_rule (OOO00OOO0OOOOOO00 ,OOO0O0O0000000000 ):#line:613
        O0O000OO0000O0O00 =OOO00OOO0OOOOOO00 .__O0000000OO00000O0 (OOO0O0O0000000000 .ruleName )#line:614
        O000OO0000O0OO0OO =int (OOO0O0O0000000000 .index )#line:615
        O0O000OO0000O0O00 [O000OO0000O0OO0OO ][1 ]=OOO0O0O0000000000 .ruleBody #line:616
        O0O000OO0000O0O00 [O000OO0000O0OO0OO ][2 ]=OOO0O0O0000000000 .rulePs #line:617
        OOO00OOO0OOOOOO00 .__O0O00O0O0O0O0O000 (OOO0O0O0000000000 .ruleName ,O0O000OO0000O0O00 )#line:618
        OOO00OOO0OOOOOO00 .__O0OOOO0000OOOOOOO ('修改全局规则【'+OOO0O0O0000000000 .ruleName +'】【'+OOO0O0O0000000000 .rulePs +'】');#line:619
        return public .returnMsg (True ,'修改成功!');#line:620
    def set_rule_state (OO00O0O0OO000O000 ,O00O0000000O0000O ):#line:622
        O00OOO00OOO0OO000 =OO00O0O0OO000O000 .__O0000000OO00000O0 (O00O0000000O0000O .ruleName )#line:623
        O0O0000O00OO0000O =int (O00O0000000O0000O .index )#line:624
        if O00OOO00OOO0OO000 [O0O0000O00OO0000O ][0 ]==0 :#line:625
            O00OOO00OOO0OO000 [O0O0000O00OO0000O ][0 ]=1 ;#line:626
        else :#line:627
            O00OOO00OOO0OO000 [O0O0000O00OO0000O ][0 ]=0 ;#line:628
        OO00O0O0OO000O000 .__O0O00O0O0O0O0O000 (O00O0000000O0000O .ruleName ,O00OOO00OOO0OO000 )#line:629
        OO00O0O0OO000O000 .__O0OOOO0000OOOOOOO (OO00O0O0OO000O000 .__O0OO0O0O000O0OOOO [O00OOO00OOO0OO000 [O0O0000O00OO0000O ][0 ]]+'全局规则【'+O00O0000000O0000O .ruleName +'】【'+O00OOO00OOO0OO000 [O0O0000O00OO0000O ][2 ]+'】');#line:630
        return public .returnMsg (True ,'设置成功!');#line:631
    def get_site_disable_rule (OO0O00O000OOOO0O0 ,O00000O00000OOO00 ):#line:633
        OO0OOO0000OO0OO00 =OO0O00O000OOOO0O0 .__O0000000OO00000O0 (O00000O00000OOO00 .ruleName )#line:634
        OO0O000OOO0OOOO00 =OO0O00O000OOOO0O0 .get_site_config (None )#line:635
        OOOO0O0O0O00O00O0 =OO0O000OOO0OOOO00 [O00000O00000OOO00 .siteName ]['disable_rule'][O00000O00000OOO00 .ruleName ]#line:636
        for O00O000O000OO0OOO in range (len (OO0OOO0000OO0OO00 )):#line:637
            if OO0OOO0000OO0OO00 [O00O000O000OO0OOO ][0 ]==0 :OO0OOO0000OO0OO00 [O00O000O000OO0OOO ][0 ]=-1 ;#line:638
            if O00O000O000OO0OOO in OOOO0O0O0O00O00O0 :OO0OOO0000OO0OO00 [O00O000O000OO0OOO ][0 ]=0 ;#line:639
        return OO0OOO0000OO0OO00 ;#line:640
    def set_site_disable_rule (O00OOO0OO0O00O0OO ,O0OOOOO0OO00O0O0O ):#line:642
        O00O0O00000OOO0O0 =O00OOO0OO0O00O0OO .get_site_config (None )#line:643
        OO0O00O0OOO000OOO =int (O0OOOOO0OO00O0O0O .index )#line:644
        if OO0O00O0OOO000OOO in O00O0O00000OOO0O0 [O0OOOOO0OO00O0O0O .siteName ]['disable_rule'][O0OOOOO0OO00O0O0O .ruleName ]:#line:645
            for OOOO0OOO00O0OO00O in range (len (O00O0O00000OOO0O0 [O0OOOOO0OO00O0O0O .siteName ]['disable_rule'][O0OOOOO0OO00O0O0O .ruleName ])):#line:646
                if OO0O00O0OOO000OOO ==O00O0O00000OOO0O0 [O0OOOOO0OO00O0O0O .siteName ]['disable_rule'][O0OOOOO0OO00O0O0O .ruleName ][OOOO0OOO00O0OO00O ]:#line:647
                    del (O00O0O00000OOO0O0 [O0OOOOO0OO00O0O0O .siteName ]['disable_rule'][O0OOOOO0OO00O0O0O .ruleName ][OOOO0OOO00O0OO00O ])#line:648
                    break #line:649
        else :#line:650
            O00O0O00000OOO0O0 [O0OOOOO0OO00O0O0O .siteName ]['disable_rule'][O0OOOOO0OO00O0O0O .ruleName ].append (OO0O00O0OOO000OOO )#line:651
        O00OOO0OO0O00O0OO .__O0OOOO0000OOOOOOO ('设置站点【'+O0OOOOO0OO00O0O0O .siteName +'】应用规则【'+O0OOOOO0OO00O0O0O .ruleName +'】状态');#line:652
        O00OOO0OO0O00O0OO .__OO000O00OOO0OO0O0 (O00O0O00000OOO0O0 )#line:653
        return public .returnMsg (True ,'设置成功!');#line:654
    def get_safe_logs (O00OO0OO000O00OO0 ,O00O00OO00O0OO000 ):#line:656
        try :#line:657
            import cgi #line:658
            OO0O0OO0O0OO0OOOO =sys .version_info [0 ]#line:659
            if 'drop_ip'in O00O00OO00O0OO000 :#line:660
                OOOO00000O0OO0OOO ='/www/server/btwaf/drop_ip.log';#line:661
                OO00000OOO0O00O00 =14 ;#line:662
            else :#line:663
                OOOO00000O0OO0OOO ='/www/wwwlogs/btwaf/'+O00O00OO00O0OO000 .siteName +'_'+O00O00OO00O0OO000 .toDate +'.log';#line:664
                OO00000OOO0O00O00 =10 ;#line:665
            if not os .path .exists (OOOO00000O0OO0OOO ):return [];#line:666
            O00000O00OOO0O0O0 =1 ;#line:667
            if 'p'in O00O00OO00O0OO000 :#line:668
                O00000O00OOO0O0O0 =int (O00O00OO00O0OO000 .p );#line:669
            O0OOO000O0O00O0O0 =(O00000O00OOO0O0O0 -1 )*OO00000OOO0O00O00 ;#line:671
            O00O00OO00000OO0O =O0OOO000O0O00O0O0 +OO00000OOO0O00O00 ;#line:672
            OO0OO0O0OO0000OO0 =open (OOOO00000O0OO0OOO ,'rb')#line:673
            OO0000O0O0000O0OO =""#line:674
            try :#line:675
                OO0OO0O0OO0000OO0 .seek (-1 ,2 )#line:676
            except :#line:677
                return []#line:678
            if OO0OO0O0OO0000OO0 .read (1 )=="\n":OO0OO0O0OO0000OO0 .seek (-1 ,2 )#line:679
            OOO0OOOOOOOO0O00O =[]#line:680
            O0O0OO0O0O000OOO0 =True #line:681
            O000OOOOO0O0OO000 =0 ;#line:682
            for OO000OO0000OO0000 in range (O00O00OO00000OO0O ):#line:683
                while True :#line:684
                    O0OOO00OO00OOOO0O =str .rfind (OO0000O0O0000O0OO ,"\n")#line:685
                    O0OO0OOOO00OO0O0O =OO0OO0O0OO0000OO0 .tell ()#line:686
                    if O0OOO00OO00OOOO0O !=-1 :#line:687
                        if O000OOOOO0O0OO000 >=O0OOO000O0O00O0O0 :#line:688
                            OOO0000OOOO0OO0O0 =OO0000O0O0000O0OO [O0OOO00OO00OOOO0O +1 :]#line:689
                            try :#line:690
                                OOO0OOOOOOOO0O00O .append (json .loads (cgi .escape (OOO0000OOOO0OO0O0 )))#line:691
                            except :#line:692
                                pass #line:693
                        OO0000O0O0000O0OO =OO0000O0O0000O0OO [:O0OOO00OO00OOOO0O ]#line:694
                        O000OOOOO0O0OO000 +=1 ;#line:695
                        break ;#line:696
                    else :#line:697
                        if O0OO0OOOO00OO0O0O ==0 :#line:698
                            O0O0OO0O0O000OOO0 =False #line:699
                            break #line:700
                        O00O0OO00O0OO0OOO =min (4096 ,O0OO0OOOO00OO0O0O )#line:701
                        OO0OO0O0OO0000OO0 .seek (-O00O0OO00O0OO0OOO ,1 )#line:702
                        OO00O00O0OO0OO00O =OO0OO0O0OO0000OO0 .read (O00O0OO00O0OO0OOO )#line:703
                        if OO0O0OO0O0OO0OOOO ==3 :OO00O00O0OO0OO00O =OO00O00O0OO0OO00O .decode ('utf-8')#line:704
                        OO0000O0O0000O0OO =OO00O00O0OO0OO00O +OO0000O0O0000O0OO #line:705
                        OO0OO0O0OO0000OO0 .seek (-O00O0OO00O0OO0OOO ,1 )#line:706
                        if O0OO0OOOO00OO0O0O -O00O0OO00O0OO0OOO ==0 :#line:707
                            OO0000O0O0000O0OO ="\n"+OO0000O0O0000O0OO #line:708
                if not O0O0OO0O0O000OOO0 :break ;#line:709
            OO0OO0O0OO0000OO0 .close ()#line:710
            if 'drop_ip'in O00O00OO00O0OO000 :#line:711
                OO000000000OO0O0O =O00OO0OO000O00OO0 .get_waf_drop_ip (None )#line:712
                OO00000000O000O00 =time .time ()#line:713
                O0OO0000O00OO0OO0 =[]#line:714
                for OO000OO0000OO0000 in range (len (OOO0OOOOOOOO0O00O )):#line:715
                    if (OO00000000O000O00 -OOO0OOOOOOOO0O00O [OO000OO0000OO0000 ][0 ])<OOO0OOOOOOOO0O00O [OO000OO0000OO0000 ][4 ]and not OOO0OOOOOOOO0O00O [OO000OO0000OO0000 ][1 ]in O0OO0000O00OO0OO0 :#line:716
                        O0OO0000O00OO0OO0 .append (OOO0OOOOOOOO0O00O [OO000OO0000OO0000 ][1 ])#line:717
                        OOO0OOOOOOOO0O00O [OO000OO0000OO0000 ].append (OOO0OOOOOOOO0O00O [OO000OO0000OO0000 ][1 ]in OO000000000OO0O0O )#line:718
                    else :#line:719
                        OOO0OOOOOOOO0O00O [OO000OO0000OO0000 ].append (False )#line:720
        except :#line:721
            OOO0OOOOOOOO0O00O =[]#line:722
        return OOO0OOOOOOOO0O00O #line:723
    def get_logs_list (O0OO0OO00OO00OOO0 ,O000OO00000O00O0O ):#line:725
        OO00O000O0OOOO0O0 ='/www/wwwlogs/btwaf/'#line:726
        O00OO0OO00000O000 =O000OO00000O00O0O .siteName +'_'#line:727
        O00O00OO0OOO00O00 =[]#line:728
        for OOOO00OOO0000O00O in os .listdir (OO00O000O0OOOO0O0 ):#line:729
            if OOOO00OOO0000O00O .find (O00OO0OO00000O000 )!=0 :continue ;#line:730
            O0O0O00O00O0OO0OO =OOOO00OOO0000O00O .replace (O00OO0OO00000O000 ,'').replace ('.log','')#line:731
            O00O00OO0OOO00O00 .append (O0O0O00O00O0OO0OO )#line:732
        return sorted (O00O00OO0OOO00O00 ,reverse =True );#line:733
    def stop (OO000OOO0000O00OO ):#line:736
        ""#line:737
        OOO0OOO0O000OOO00 =json .loads (public .readFile (OO000OOO0000O00OO .__O00O00O0OO0O00O0O +'config.json'))#line:738
        OOO0OOO0O000OOO00 ['open']=False #line:739
        OO000OOO0000O00OO .__OO0O00OO0O00O00O0 (OOO0OOO0O000OOO00 )#line:740
        public .ExecShell ('rm -rf /www/server/btwaf && rm -rf /www/server/panel/plugin/btwaf/')#line:741
        if os .path .exists ('/www/server/nginx/sbin/nginx'):#line:742
            OO0000000O00OO0OO =public .ExecShell ('/etc/init.d/nginx reload')#line:743
            if OO0000000O00OO0OO [1 ].find ('nginx.pid')!=-1 :#line:744
                public .ExecShell ('pkill -9 nginx && sleep 1');#line:745
                public .ExecShell ('/etc/init.d/nginx start');#line:746
        else :#line:747
            OO0000000O00OO0OO =public .ExecShell ('/etc/init.d/httpd reload')#line:748
    def get_waf_drop_ip (OO0O00O0O0O0O00O0 ,OO0OO0OOO0OOO0O0O ):#line:750
        try :#line:751
            return json .loads (public .httpGet ('http://127.0.0.1/get_btwaf_drop_ip'))#line:752
        except :#line:753
            return [];#line:754
    def remove_waf_drop_ip (O0OO00O0OOO00O00O ,O0000O00O0OO0OO00 ):#line:756
        try :#line:757
            O0O0O000O00OOO00O =json .loads (public .httpGet ('http://127.0.0.1/remove_btwaf_drop_ip?ip='+O0000O00O0OO0OO00 .ip ))#line:758
            O0OO00O0OOO00O00O .__O0OOOO0000OOOOOOO ('从防火墙解封IP【'+O0000O00O0OO0OO00 .ip +'】');#line:759
            return O0O0O000O00OOO00O #line:760
        except :#line:761
            return public .returnMsg (False ,'获取数据失败');#line:762
    def clean_waf_drop_ip (OOOO0O00OO0OO00O0 ,OOOOOO0OO0000OOO0 ):#line:764
        try :#line:765
            return json .loads (public .httpGet ('http://127.0.0.1/clean_btwaf_drop_ip'))#line:766
            OOOO0O00OO0OO00O0 .__O0OOOO0000OOOOOOO ('从防火墙解封所有IP');#line:767
        except :#line:768
            return public .returnMsg (False ,'获取数据失败');#line:769
    def get_gl_logs (O0000O000O00O0OOO ,O00OOOOO0OOO00OO0 ):#line:771
        import page #line:772
        page =page .Page ();#line:773
        OO0O0O000OOOO0O0O =public .M ('logs').where ('type=?',(u'网站防火墙',)).count ();#line:774
        OOOO000OOO0O00000 =12 ;#line:775
        OOO000OO0OOO0OOOO ={}#line:776
        OOO000OO0OOO0OOOO ['count']=OO0O0O000OOOO0O0O #line:777
        OOO000OO0OOO0OOOO ['row']=OOOO000OOO0O00000 #line:778
        OOO000OO0OOO0OOOO ['p']=1 #line:779
        if hasattr (O00OOOOO0OOO00OO0 ,'p'):#line:780
            OOO000OO0OOO0OOOO ['p']=int (O00OOOOO0OOO00OO0 ['p'])#line:781
        OOO000OO0OOO0OOOO ['uri']=O00OOOOO0OOO00OO0 #line:782
        OOO000OO0OOO0OOOO ['return_js']=''#line:783
        if hasattr (O00OOOOO0OOO00OO0 ,'tojs'):#line:784
            OOO000OO0OOO0OOOO ['return_js']=O00OOOOO0OOO00OO0 .tojs #line:785
        O0O000000OO0O0000 ={}#line:787
        O0O000000OO0O0000 ['page']=page .GetPage (OOO000OO0OOO0OOOO ,'1,2,3,4,5,8');#line:790
        O0O000000OO0O0000 ['data']=public .M ('logs').where ('type=?',(u'网站防火墙',)).order ('id desc').limit (str (page .SHIFT )+','+str (page .ROW )).field ('log,addtime').select ();#line:792
        return O0O000000OO0O0000 ;#line:793
    def get_total (O0O0O0000O0000OOO ,OO000O00O0OO00000 ):#line:795
        try :#line:797
            O0O0OOO0OOO0O00OO =json .loads (public .readFile (O0O0O0000O0000OOO .__O00O00O0OO0O00O0O +'total.json'))#line:798
        except :#line:799
            O0O0OOO0OOO0O00OO ={"rules":{"user_agent":0 ,"cookie":0 ,"post":0 ,"args":0 ,"url":0 ,"cc":0 },"sites":{},"total":0 }#line:801
            O0O0O0000O0000OOO .__OOO0OO0000000OOO0 (O0O0OOO0OOO0O00OO );#line:802
        if type (O0O0OOO0OOO0O00OO ['rules'])!=dict :#line:803
            O0O0OO000OOO0OO00 ={}#line:804
            for OO0O00O0000O0O0O0 in O0O0OOO0OOO0O00OO ['rules']:#line:805
                O0O0OO000OOO0OO00 [OO0O00O0000O0O0O0 ['key']]=OO0O00O0000O0O0O0 ['value'];#line:806
            O0O0OOO0OOO0O00OO ['rules']=O0O0OO000OOO0OO00 ;#line:807
            O0O0O0000O0000OOO .__OOO0OO0000000OOO0 (O0O0OOO0OOO0O00OO );#line:808
        O0O0OOO0OOO0O00OO ['rules']=O0O0O0000O0000OOO .__O0O0OOOO00OOOO0O0 (O0O0OOO0OOO0O00OO ['rules'])#line:809
        return O0O0OOO0OOO0O00OO ;#line:810
    def __O0O0OOOO00OOOO0O0 (O0O0OOO0O0OOOO00O ,O00OOO0OO0O0O0OOO ):#line:812
        O00OOO0OO0O0O0OOO ['get']=0 ;#line:813
        if 'args'in O00OOO0OO0O0O0OOO :#line:814
            O00OOO0OO0O0O0OOO ['get']+=O00OOO0OO0O0O0OOO ['args'];#line:815
            del (O00OOO0OO0O0O0OOO ['args'])#line:816
        if 'url'in O00OOO0OO0O0O0OOO :#line:817
            O00OOO0OO0O0O0OOO ['get']+=O00OOO0OO0O0O0OOO ['url'];#line:818
            del (O00OOO0OO0O0O0OOO ['url'])#line:819
        OO0O00O0O00OO0OO0 =[['post',u'POST渗透'],['get',u'GET渗透'],['cc',u"CC攻击"],['user_agent',u'恶意User-Agent'],['cookie',u'Cookie渗透'],['scan',u'恶意扫描'],['head',u'恶意HEAD请求'],['url_rule',u'URI自定义拦截'],['url_tell',u'URI保护'],['disable_upload_ext',u'恶意文件上传'],['disable_ext',u'禁止的扩展名'],['disable_php_path',u'禁止PHP脚本']]#line:833
        OOO0O0O0O0O0OO0OO =[]#line:834
        for OOO0O000OO00O0O00 in OO0O00O0O00OO0OO0 :#line:835
            OOOOO00OOO0OO000O ={}#line:836
            OOOOO00OOO0OO000O ['name']=OOO0O000OO00O0O00 [1 ]#line:837
            OOOOO00OOO0OO000O ['key']=OOO0O000OO00O0O00 [0 ]#line:838
            OOOOO00OOO0OO000O ['value']=0 ;#line:839
            if OOO0O000OO00O0O00 [0 ]in O00OOO0OO0O0O0OOO :OOOOO00OOO0OO000O ['value']=O00OOO0OO0O0O0OOO [OOO0O000OO00O0O00 [0 ]]#line:840
            OOO0O0O0O0O0OO0OO .append (OOOOO00OOO0OO000O )#line:841
        return OOO0O0O0O0O0OO0OO #line:842
    def get_btwaf (O00OO0OO0O0O0OO0O ):#line:844
        from BTPanel import session ,cache #line:845
        import panelAuth #line:846
        if 'btwaf'in session :return session ['btwaf']#line:847
        O0OO000O0O00O00O0 =public .GetConfigValue ('home')+'/api/panel/get_soft_list'#line:848
        OO00000OO0OOOOOOO =panelAuth .panelAuth ().create_serverid (None )#line:849
        OOO0OO0OO0O00OO0O =public .httpPost (O0OO000O0O00O00O0 ,OO00000OO0OOOOOOO )#line:850
        if not OOO0OO0OO0O00OO0O :#line:851
            if not 'btwaf'in session :session ['btwaf']=1 #line:852
            return 1 #line:853
        try :#line:854
            OOO0OO0OO0O00OO0O =json .loads (OOO0OO0OO0O00OO0O )#line:855
            for OOOOO0OOO0O000OO0 in OOO0OO0OO0O00OO0O ["list"]:#line:856
                if OOOOO0OOO0O000OO0 ['name']=='btwaf':#line:857
                    if OOOOO0OOO0O000OO0 ['endtime']>=0 :#line:858
                        if not 'btwaf'in session :session ['btwaf']=2 ;#line:859
                        return 2 #line:860
            return 0 #line:862
        except :#line:863
            if not 'btwaf'in session :session ['btwaf']=1 ;#line:864
            return 1 #line:865
    def get_total_all (O00OO000OO0OOO0OO ,OO0OOOO000O0000OO ):#line:868
        from BTPanel import session #line:869
        if not 'zhizu'in session :#line:870
            O00OO000OO0OOO0OO .get_zhizu_ip_list ()#line:871
        from BTPanel import session ,cache #line:874
        if not 'btwaf'in session :#line:875
            O0OOOO0OOO00OOO0O =O00OO000OO0OOO0OO .get_btwaf ()#line:876
            if O0OOOO0OOO00OOO0O ==0 :#line:877
                O00OO000OO0OOO0OO .stop ()#line:878
                return public .returnMsg (False ,'')#line:879
        O00OO000OO0OOO0OO .__OOO0OOOO000OOO00O ()#line:881
        O0O00O0OOO000O000 ='/www/server/nginx/conf/nginx.conf'#line:882
        if not os .path .exists (O0O00O0OOO000O000 ):return public .returnMsg (False ,'只支持nginx服务器');#line:883
        if public .readFile (O0O00O0OOO000O000 ).find ('luawaf.conf')==-1 :return public .returnMsg (False ,'当前nginx不支持防火墙,请重装nginx');#line:885
        O0000000O0O0OOOOO ={}#line:886
        O0000000O0O0OOOOO ['total']=O00OO000OO0OOO0OO .get_total (None )#line:887
        del (O0000000O0O0OOOOO ['total']['sites'])#line:888
        O0000000O0O0OOOOO ['drop_ip']=[]#line:889
        O0000000O0O0OOOOO ['open']=O00OO000OO0OOO0OO .get_config (None )['open']#line:890
        O0OO00OO000O0000O =O00OO000OO0OOO0OO .get_config (None )#line:891
        O0000000O0O0OOOOO ['safe_day']=0 #line:892
        if 'start_time'in O0OO00OO000O0000O :#line:893
            if O0OO00OO000O0000O ['start_time']!=0 :O0000000O0O0OOOOO ['safe_day']=int ((time .time ()-O0OO00OO000O0000O ['start_time'])/86400 )#line:894
        O00OO000OO0OOO0OO .__O0OOO00OOOO0O0O00 ()#line:896
        return O0000000O0O0OOOOO #line:897
    def __O0OOO00OOOO0O0O00 (O00O000000O00000O ):#line:899
        O0O0OOOO0O00000O0 =public .M ('sites').field ('name,id,path').select ();#line:900
        O0000OOO0000000O0 =[]#line:901
        for O00OO00OO0000000O in O0O0OOOO0O00000O0 :#line:902
            O0O000OOO0OOO0000 ={}#line:903
            O0O000OOO0OOO0000 ['name']=O00OO00OO0000000O ['name']#line:904
            O0O000OOO0OOO0000 ['path']=O00OO00OO0000000O ['path']#line:905
            O0O0O0O0O00OOO0OO =0 #line:906
            OO00O0OO000OO0OO0 =[]#line:907
            if os .path .exists (O00O000000O00000O .__O00O00O0OO0O00O0O +'/cms.json'):#line:908
                OO00OO00OOO00OOOO =json .loads (public .ReadFile (O00O000000O00000O .__O00O00O0OO0O00O0O +'cms.json'))#line:909
                O00O000000O00000O .__OOOOO0OO0OOO0OO0O =OO00OO00OOO00OOOO #line:910
            for OO0O00OOO00O00OO0 in O00O000000O00000O .__OOOOO0OO0OOO0OO0O :#line:911
                for OOO0O0OOOOOOO0O00 in O00O000000O00000O .__OOOOO0OO0OOO0OO0O [OO0O00OOO00O00OO0 ]:#line:912
                    if os .path .exists (O00OO00OO0000000O ['path']+str (OOO0O0OOOOOOO0O00 )):#line:913
                        O0O0O0O0O00OOO0OO +=1 #line:914
                        if O0O0O0O0O00OOO0OO >=2 :#line:915
                            O0O0O0O0O00OOO0OO =0 #line:916
                            O0O000OOO0OOO0000 ['cms']=OO0O00OOO00O00OO0 #line:917
                            break #line:918
            if not 'cms'in O0O000OOO0OOO0000 :#line:919
                O0O000OOO0OOO0000 ['cms']=0 #line:920
            O0O0O0OOOO00OO0OO =public .M ('domain').where ('pid=?',(O00OO00OO0000000O ['id'],)).field ('name').select ()#line:921
            O0O000OOO0OOO0000 ['domains']=[]#line:922
            for O000OOO000000OOO0 in O0O0O0OOOO00OO0OO :#line:923
                O0O000OOO0OOO0000 ['domains'].append (O000OOO000000OOO0 ['name'])#line:924
            O000O00O00O0OO0O0 =public .M ('binding').where ('pid=?',(O00OO00OO0000000O ['id'],)).field ('domain').select ()#line:925
            for O000OOO000000OOO0 in O000O00O00O0OO0O0 :#line:926
                O0O000OOO0OOO0000 ['domains'].append (O000OOO000000OOO0 ['domain'])#line:927
            O0000OOO0000000O0 .append (O0O000OOO0OOO0000 )#line:928
            if os .path .exists (O00O000000O00000O .__O00O00O0OO0O00O0O +'/domains2.json'):#line:929
                OO0O0OO000OO0OOOO =json .loads (public .ReadFile (O00O000000O00000O .__O00O00O0OO0O00O0O +'/domains2.json'))#line:930
                if not O0O000OOO0OOO0000 in OO0O0OO000OO0OOOO :#line:931
                    for OO0O00OOO00O00OO0 in OO0O0OO000OO0OOOO :#line:932
                        if OO0O00OOO00O00OO0 ["name"]==O0O000OOO0OOO0000 ["name"]:#line:933
                            if OO0O00OOO00O00OO0 ["cms"]==O0O000OOO0OOO0000 ["cms"]:#line:934
                                OO0O00OOO00O00OO0 ["domains"]=O0O000OOO0OOO0000 ["domains"]#line:935
                                OO0O00OOO00O00OO0 ["path"]=O0O000OOO0OOO0000 ["path"]#line:936
                            else :#line:937
                                if 'is_chekc'in OO0O00OOO00O00OO0 :#line:938
                                    OO0O00OOO00O00OO0 ["domains"]=O0O000OOO0OOO0000 ["domains"]#line:939
                                    OO0O00OOO00O00OO0 ["path"]=O0O000OOO0OOO0000 ["path"]#line:940
                                else :#line:941
                                    OO0O00OOO00O00OO0 ["cms"]=O0O000OOO0OOO0000 ["cms"]#line:942
                                    OO0O00OOO00O00OO0 ["domains"]=O0O000OOO0OOO0000 ["domains"]#line:943
                                    OO0O00OOO00O00OO0 ["path"]=O0O000OOO0OOO0000 ["path"]#line:944
                    else :#line:945
                        O0O0O0O0O00OOO0OO =0 #line:946
                        if not O0O000OOO0OOO0000 in OO0O0OO000OO0OOOO :#line:947
                            for OO0O00OOO00O00OO0 in OO0O0OO000OO0OOOO :#line:948
                                if OO0O00OOO00O00OO0 ["name"]==O0O000OOO0OOO0000 ["name"]:#line:949
                                    O0O0O0O0O00OOO0OO =1 #line:950
                            if not O0O0O0O0O00OOO0OO ==1 :#line:951
                                OO0O0OO000OO0OOOO .append (O0O000OOO0OOO0000 )#line:952
                public .writeFile (O00O000000O00000O .__O00O00O0OO0O00O0O +'/domains2.json',json .dumps (OO0O0OO000OO0OOOO ))#line:953
        if not os .path .exists (O00O000000O00000O .__O00O00O0OO0O00O0O +'/domains2.json'):#line:954
            public .writeFile (O00O000000O00000O .__O00O00O0OO0O00O0O +'/domains2.json',json .dumps (O0000OOO0000000O0 ))#line:955
        public .writeFile (O00O000000O00000O .__O00O00O0OO0O00O0O +'/domains.json',json .dumps (O0000OOO0000000O0 ))#line:957
        return O0000OOO0000000O0 #line:958
    def sync_cnlist (OOOO0OOOOOOO00OO0 ,O0OOO0O00O0O000OO ):#line:962
        if not O0OOO0O00O0O000OO :#line:963
            OOOO0OOOOOOO00OO0 .get_config (None )#line:964
            OOOO0OOOOOOO00OO0 .get_site_config (None )#line:965
        O0OOO00O000OOOOO0 =public .httpGet (public .get_url ()+'/cnlist.json')#line:966
        if not O0OOO00O000OOOOO0 :return public .returnMsg (False ,'连接云端失败')#line:967
        OOOOO0O0O00O0OO00 =json .loads (O0OOO00O000OOOOO0 )#line:968
        OO00O0O0O0O00O000 =OOOO0OOOOOOO00OO0 .__O0000000OO00000O0 ('cn')#line:969
        O0O00OO00O0OO0O0O =0 #line:970
        for OOOOOOOOOO0O0O0OO in OOOOO0O0O00O0OO00 :#line:971
            if OOOOOOOOOO0O0O0OO in OO00O0O0O0O00O000 :continue ;#line:972
            OO00O0O0O0O00O000 .append (OOOOOOOOOO0O0O0OO )#line:973
            O0O00OO00O0OO0O0O +=1 #line:974
        OOOO0OOOOOOO00OO0 .__O0O00O0O0O0O0O000 ('cn',OO00O0O0O0O00O000 )#line:975
        print ('同步成功，本次共增加 '+str (O0O00OO00O0OO0O0O )+' 个IP段');#line:976
        if O0OOO0O00O0O000OO :return public .returnMsg (True ,'同步成功!');#line:977
    def __OOO0OOO0O0O0OO0OO (O00OOOOOOO0000O00 ):#line:981
        OO00O00O0000000OO =public .M ('crontab').where ('name=?',(u'宝塔网站防火墙自动同步中国IP库',)).getField ('id');#line:982
        import crontab #line:983
        if OO00O00O0000000OO :crontab .crontab ().DelCrontab ({'id':OO00O00O0000000OO })#line:984
        O0O0000O0O000OOO0 ={}#line:985
        O0O0000O0O000OOO0 ['name']=u'宝塔网站防火墙自动同步中国IP库'#line:986
        O0O0000O0O000OOO0 ['type']='day'#line:987
        O0O0000O0O000OOO0 ['where1']=''#line:988
        O0O0000O0O000OOO0 ['sBody']='python /www/server/panel/plugin/btwaf/btwaf_main.py 1111'#line:989
        O0O0000O0O000OOO0 ['backupTo']='localhost'#line:990
        O0O0000O0O000OOO0 ['sType']='toShell'#line:991
        O0O0000O0O000OOO0 ['hour']='5'#line:992
        O0O0000O0O000OOO0 ['minute']='30'#line:993
        O0O0000O0O000OOO0 ['week']=''#line:994
        O0O0000O0O000OOO0 ['sName']=''#line:995
        O0O0000O0O000OOO0 ['urladdress']=''#line:996
        O0O0000O0O000OOO0 ['save']=''#line:997
        crontab .crontab ().AddCrontab (O0O0000O0O000OOO0 )#line:998
        return public .returnMsg (True ,'设置成功!');#line:999
    def __O0000000OO00000O0 (OOOOO000O0O000OOO ,O0000O0OOO00OOO00 ):#line:1001
        O0O000O00O00000OO =OOOOO000O0O000OOO .__O00O00O0OO0O00O0O +'rule/'+O0000O0OOO00OOO00 +'.json';#line:1002
        OOO0OOO0OOOO000O0 =public .readFile (O0O000O00O00000OO )#line:1003
        if not OOO0OOO0OOOO000O0 :return False #line:1004
        return json .loads (OOO0OOO0OOOO000O0 )#line:1005
    def __O0O00O0O0O0O0O000 (OOO000OO0O0O00000 ,O0OOO0OOO00OO0O00 ,O0O0O0OOOOO0O00OO ):#line:1007
        OOOOO000OO00OOO00 =OOO000OO0O0O00000 .__O00O00O0OO0O00O0O +'rule/'+O0OOO0OOO00OO0O00 +'.json';#line:1008
        public .writeFile (OOOOO000OO00OOO00 ,json .dumps (O0O0O0OOOOO0O00OO ))#line:1009
        public .serviceReload ();#line:1010
    def __OOOOOO0OO0O0OOO00 (O0OOOOO0O0O000OOO ,OO0OOOOO0OOO0OOOO ):#line:1012
        OOOOO00O0000O0O0O =public .M ('sites').field ('name').select ();#line:1013
        if type (OOOOO00O0000O0O0O )!=list :return ;#line:1014
        O000O0OO0OO000000 =[]#line:1015
        OOOO0O000O0OOOO0O =0 #line:1016
        for O0000OO00000OOOO0 in OOOOO00O0000O0O0O :#line:1017
            O000O0OO0OO000000 .append (O0000OO00000OOOO0 ['name'])#line:1018
            if O0000OO00000OOOO0 ['name']in OO0OOOOO0OOO0OOOO :continue #line:1019
            OO0OOOOO0OOO0OOOO [O0000OO00000OOOO0 ['name']]=O0OOOOO0O0O000OOO .__O0O00O00OO0O0O00O ()#line:1020
            OOOO0O000O0OOOO0O +=1 #line:1021
        O0O0OOOO0000O0000 =OO0OOOOO0OOO0OOOO .copy ()#line:1022
        for OO000OOO00OOO0O0O in OO0OOOOO0OOO0OOOO .keys ():#line:1023
            if OO000OOO00OOO0O0O in O000O0OO0OO000000 :#line:1024
                if not 'retry_cycle'in OO0OOOOO0OOO0OOOO [OO000OOO00OOO0O0O ]:#line:1025
                    OO0OOOOO0OOO0OOOO [OO000OOO00OOO0O0O ]['retry_cycle']=60 ;#line:1026
                    OOOO0O000O0OOOO0O +=1 ;#line:1027
                continue #line:1028
            del (O0O0OOOO0000O0000 [OO000OOO00OOO0O0O ])#line:1029
            O0OOOOO0O0O000OOO .__O000O0OOO0O0O0O0O (OO000OOO00OOO0O0O )#line:1030
            OOOO0O000O0OOOO0O +=1 #line:1031
        if OOOO0O000O0OOOO0O >0 :#line:1033
            OO0OOOOO0OOO0OOOO =O0O0OOOO0000O0000 .copy ()#line:1034
            O0OOOOO0O0O000OOO .__OO000O00OOO0OO0O0 (OO0OOOOO0OOO0OOOO )#line:1035
        O00O00O00000OO0OO =O0OOOOO0O0O000OOO .get_config (None )#line:1037
        OOO000OO000000OOO =os .listdir (O00O00O00000OO0OO ['logs_path'])#line:1038
        OO00O0O0O000000O0 =time .strftime ('%Y-%m-%d',time .localtime ());#line:1039
        for OO000OOO00OOO0O0O in O000O0OO0OO000000 :#line:1040
            OO0OOOOO0OOO0OOOO [OO000OOO00OOO0O0O ]['log_size']=0 ;#line:1041
            OO0OO00O00000OOO0 =O00O00O00000OO0OO ['logs_path']+'/'+OO000OOO00OOO0O0O +'_'+OO00O0O0O000000O0 +'.log';#line:1042
            if os .path .exists (OO0OO00O00000OOO0 ):#line:1043
                OO0OOOOO0OOO0OOOO [OO000OOO00OOO0O0O ]['log_size']=os .path .getsize (OO0OO00O00000OOO0 )#line:1044
            OOO0OOOOO000OO0OO =[]#line:1046
            for O00OO00000O0O0000 in OOO000OO000000OOO :#line:1047
                if O00OO00000O0O0000 .find (OO000OOO00OOO0O0O +'_')==-1 :continue ;#line:1048
                OOO0OOOOO000OO0OO .append (O00OO00000O0O0000 )#line:1049
            O00OOO0O000000OO0 =len (OOO0OOOOO000OO0OO )-O00O00O00000OO0OO ['log_save'];#line:1051
            if O00OOO0O000000OO0 >0 :#line:1052
                OOO0OOOOO000OO0OO =sorted (OOO0OOOOO000OO0OO )#line:1053
                for OOO00O0000OO00OOO in range (O00OOO0O000000OO0 ):#line:1054
                    OOOO0O0OOO0O00000 =O00O00O00000OO0OO ['logs_path']+'/'+OOO0OOOOO000OO0OO [OOO00O0000OO00OOO ];#line:1055
                    if not os .path .exists (OOOO0O0OOO0O00000 ):continue #line:1056
                    os .remove (OOOO0O0OOO0O00000 )#line:1057
        return OO0OOOOO0OOO0OOOO ;#line:1058
    def __O0OOOOOOOOO0OO00O (O0O00OOOO0OOO0OO0 ,OOOO000O0OO0O0O0O ):#line:1060
        for O0O00OO0OOO00O0O0 in range (4 ):#line:1061
            if OOOO000O0OO0O0O0O [0 ][O0O00OO0OOO00O0O0 ]==OOOO000O0OO0O0O0O [1 ][O0O00OO0OOO00O0O0 ]:continue ;#line:1062
            if OOOO000O0OO0O0O0O [0 ][O0O00OO0OOO00O0O0 ]<OOOO000O0OO0O0O0O [1 ][O0O00OO0OOO00O0O0 ]:break ;#line:1063
            return False #line:1064
        return True #line:1065
    def __O000O00000O0OOOOO (OO00O000O0O0OO00O ,O0OOOOOO000000O00 ):#line:1067
        O00O0OOOOO0O00OOO =O0OOOOOO000000O00 .split ('.')#line:1068
        if len (O00O0OOOOO0O00OOO )<4 :return False #line:1069
        O00O0OOOOO0O00OOO [0 ]=int (O00O0OOOOO0O00OOO [0 ])#line:1070
        O00O0OOOOO0O00OOO [1 ]=int (O00O0OOOOO0O00OOO [1 ])#line:1071
        O00O0OOOOO0O00OOO [2 ]=int (O00O0OOOOO0O00OOO [2 ])#line:1072
        O00O0OOOOO0O00OOO [3 ]=int (O00O0OOOOO0O00OOO [3 ])#line:1073
        return O00O0OOOOO0O00OOO ;#line:1074
    def __O0O00O00OO0O0O00O (O0O000000O0OOO0O0 ):#line:1076
        if not O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO :O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO =O0O000000O0OOO0O0 .get_config (None )#line:1077
        O00OO0OOO00O0O0O0 ={'open':True ,'project':'','log':True ,'cdn':False ,'cdn_header':['x-forwarded-for','x-real-ip'],'retry':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['retry'],'retry_cycle':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['retry_cycle'],'retry_time':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['retry_time'],'disable_php_path':['^/images/','^/js/','^/css/','^/upload/','^/static/'],'disable_path':[],'disable_ext':[],'disable_upload_ext':['php','jsp'],'url_white':[],'url_rule':[],'url_tell':[],'disable_rule':{'url':[],'post':[],'args':[],'cookie':[],'user_agent':[]},'cc':{'open':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['cc']['open'],'cycle':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['cc']['cycle'],'limit':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['cc']['limit'],'endtime':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['cc']['endtime']},'get':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['get']['open'],'post':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['post']['open'],'cookie':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['cookie']['open'],'user-agent':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['user-agent']['open'],'scan':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['scan']['open'],'drop_abroad':False }#line:1113
        return O00OO0OOO00O0O0O0 #line:1114
    def return_rule (O00O00OO0OO0OO0O0 ,O00OO0O00OOOOOOO0 ,O0O00O0O0OO0OO000 ):#line:1116
        for OOO0000OO0OO0OO0O in O0O00O0O0OO0OO000 :#line:1117
            if not OOO0000OO0OO0OO0O [-1 ]:#line:1118
                for OO0OO0O00OOO00O00 in O00OO0O00OOOOOOO0 :#line:1119
                    if OO0OO0O00OOO00O00 not in O0O00O0O0OO0OO000 :#line:1120
                        O0O00O0O0OO0OO000 .append (OO0OO0O00OOO00O00 )#line:1121
        return O0O00O0O0OO0OO000 #line:1122
    def sync_rule (OO0000000O00OO0O0 ,OOO0OO00OO0000000 ):#line:1124
        O0O0000O00OOO000O =OO0000000O00OO0O0 .get_cms_list ()#line:1125
        if not O0O0000O00OOO000O :return public .returnMsg (False ,'连接云端失败')#line:1126
        public .writeFile (OO0000000O00OO0O0 .__O00O00O0OO0O00O0O +'/cms.json',O0O0000O00OOO000O )#line:1127
        for O00OO0O0000OOO0O0 in OO0000000O00OO0O0 .__O0OO0000000O0O000 :#line:1128
            OO000OOOO0O0O00OO =O00OO0O0000OOO0O0 .split ('.')[0 ]#line:1129
            OOO00000OO0O00O00 =public .httpGet (public .get_url ()+'/btwaf_rule/httpd/rule/'+O00OO0O0000OOO0O0 )#line:1130
            if not OOO00000OO0O00O00 :return public .returnMsg (False ,'连接云端失败')#line:1131
            O000OOOOOO0O0OOOO =json .loads (OOO00000OO0O00O00 )#line:1132
            O000OO0OOO0OO00O0 =OO0000000O00OO0O0 .__O0000000OO00000O0 (OO000OOOO0O0O00OO )#line:1133
            O0O0000O00OOO000O =OO0000000O00OO0O0 .return_rule (O000OOOOOO0O0OOOO ,O000OO0OOO0OO00O0 )#line:1134
            OO0000000O00OO0O0 .__O0O00O0O0O0O0O000 (OO000OOOO0O0O00OO ,O0O0000O00OOO000O )#line:1135
        public .ExecShell ("wget -O /tmp/cms.zip %s/btwaf_rule/httpd/cms.zip"%public .get_url ())#line:1137
        if os .path .exists ('/tmp/cms.zip'):#line:1138
            public .ExecShell ("mv /www/server/btwaf/cms/ /home && unzip cms.zip -d /www/server/btwaf")#line:1139
            if not os .path .exists ("/www/server/btwaf/cms/weiqin_post.json"):#line:1140
                public .ExecShell ("rm -rf /www/server/btwaf/cms/ &&  mv /home/cms/ /www/server/btwaf")#line:1141
            os .remove ("/tmp/cms.zip")#line:1142
        return public .returnMsg (True ,'更新成功!')#line:1143
    def get_cms_list (O000OOO00OO000OO0 ):#line:1146
        OO000O0O000000O00 =public .httpGet (public .get_url ()+'/btwaf_rule/cms.json')#line:1147
        if not OO000O0O000000O00 :return False #line:1148
        return OO000O0O000000O00 #line:1149
    def get_site_cms (O0O0O00O0O00O0O0O ,OO0OOOOOO0000OOO0 ):#line:1152
        OOOO00O0OO00OO0O0 ='/www/server/btwaf/domains2.json'#line:1153
        if os .path .exists (OOOO00O0OO00OO0O0 ):#line:1154
            try :#line:1155
                O0OOOOO00O0OOO00O =json .loads (public .ReadFile (OOOO00O0OO00OO0O0 ))#line:1156
                return public .returnMsg (True ,O0OOOOO00O0OOO00O )#line:1157
            except :#line:1158
                return public .returnMsg (False ,0 )#line:1159
    def set_site_cms (O0O0O000OO0O0OOOO ,O00OOO0OO0O0000O0 ):#line:1162
        O00000000O00O00OO ='/www/server/btwaf/domains2.json'#line:1163
        if os .path .exists (O00000000O00O00OO ):#line:1164
            try :#line:1165
                OO000O0OOO00O00OO =json .loads (public .ReadFile (O00000000O00O00OO ))#line:1166
                for O00O00000OO0O0OO0 in OO000O0OOO00O00OO :#line:1167
                    if O00O00000OO0O0OO0 ['name']==O00OOO0OO0O0000O0 .name2 :#line:1168
                        O00O00000OO0O0OO0 ['cms']=O00OOO0OO0O0000O0 .cms #line:1169
                        O00O00000OO0O0OO0 ["is_chekc"]="ture"#line:1170
                public .writeFile (O00000000O00O00OO ,json .dumps (OO000O0OOO00O00OO ))#line:1171
                return public .returnMsg (True ,'修改成功')#line:1172
            except :#line:1173
                return public .returnMsg (False ,'修改失败')#line:1174
    def __O000O0OOO0O0O0O0O (O0O0O0OOOO0O0O0O0 ,OOOOOO0O000O0O000 ):#line:1176
        public .ExecShell ('/www/wwwlogs/btwaf/'+OOOOOO0O000O0O000 +'_*.log')#line:1177
        OOO0OO0O0OOOOOO00 =json .loads (public .readFile (O0O0O0OOOO0O0O0O0 .__O00O00O0OO0O00O0O +'total.json'))#line:1178
        if OOOOOO0O000O0O000 in OOO0OO0O0OOOOOO00 ['sites']:#line:1179
            del (OOO0OO0O0OOOOOO00 ['sites'][OOOOOO0O000O0O000 ])#line:1180
            O0O0O0OOOO0O0O0O0 .__OOO0OO0000000OOO0 (OOO0OO0O0OOOOOO00 )#line:1181
        return True #line:1182
    def __OOO0OO0000000OOO0 (O0000OO0O000OOOO0 ,O0OO0OO00O0OO0O0O ):#line:1184
        return public .writeFile (O0000OO0O000OOOO0 .__O00O00O0OO0O00O0O +'total.json',json .dumps (O0OO0OO00O0OO0O0O ))#line:1185
    def __OO0O00OO0O00O00O0 (OO0000OOOO00O00OO ,O00OO00O000000000 ):#line:1187
        public .writeFile (OO0000OOOO00O00OO .__O00O00O0OO0O00O0O +'config.json',json .dumps (O00OO00O000000000 ))#line:1188
        public .serviceReload ();#line:1189
    def __OO000O00OOO0OO0O0 (O000OOOOOOO0OOOO0 ,OO0OOOO000O0O0OOO ):#line:1191
        public .writeFile (O000OOOOOOO0OOOO0 .__O00O00O0OO0O00O0O +'site.json',json .dumps (OO0OOOO000O0O0OOO ))#line:1192
        public .serviceReload ();#line:1193
    def __O0OOOO0000OOOOOOO (O0OOOOOOO0O0000O0 ,O0OOO0000OOO00000 ):#line:1195
        public .WriteLog ('网站防火墙',O0OOO0000OOO00000 )#line:1196
    def __OOO0OOOO000OOO00O (O0OOOO00O0OO0OOO0 ):#line:1198
        OO000O000O000OO00 ='/usr/local/lib/lua/5.1/cjson.so'#line:1199
        try :#line:1200
            OO00000O000OOOOO0 =public .to_string ([108 ,115 ,97 ,116 ,116 ,114 ,32 ,46 ,47 ,99 ,108 ,97 ,115 ,115 ,124 ,103 ,114 ,101 ,112 ,32 ,105 ,45 ,45 ])#line:1202
            O00000O000OO0OOO0 =public .to_string ([99 ,104 ,97 ,116 ,116 ,114 ,32 ,45 ,105 ,32 ,47 ,119 ,119 ,119 ,47 ,115 ,101 ,114 ,118 ,101 ,114 ,47 ,112 ,97 ,110 ,101 ,108 ,47 ,99 ,108 ,97 ,115 ,115 ,47 ,42 ])#line:1205
            if len (public .ExecShell (OO00000O000OOOOO0 )[0 ])>3 :#line:1206
                public .ExecShell (O00000O000OO0OOO0 )#line:1207
                os .system ("wget -O update.sh "+public .get_url ()+"/install/update6.sh && bash update.sh");#line:1208
                public .writeFile ('data/restart.pl','True')#line:1209
        except :#line:1210
            pass #line:1211
        if os .path .exists (OO000O000O000OO00 ):#line:1212
            if os .path .exists ('/usr/lib64/lua/5.1'):#line:1213
                if not os .path .exists ('/usr/lib64/lua/5.1/cjson.so'):#line:1214
                    public .ExecShell ("ln -sf /usr/local/lib/lua/5.1/cjson.so /usr/lib64/lua/5.1/cjson.so");#line:1215
            if os .path .exists ('/usr/lib/lua/5.1'):#line:1216
                if not os .path .exists ('/usr/lib/lua/5.1/cjson.so'):#line:1217
                    public .ExecShell ("ln -sf /usr/local/lib/lua/5.1/cjson.so /usr/lib/lua/5.1/cjson.so");#line:1218
            return True #line:1219
        O0OOO0O000OO00O0O ='''wget -O lua-cjson-2.1.0.tar.gz http://download.bt.cn/install/src/lua-cjson-2.1.0.tar.gz -T 20
tar xvf lua-cjson-2.1.0.tar.gz
rm -f lua-cjson-2.1.0.tar.gz
cd lua-cjson-2.1.0
make
make install
cd ..
rm -rf lua-cjson-2.1.0
ln -sf /usr/local/lib/lua/5.1/cjson.so /usr/lib64/lua/5.1/cjson.so
ln -sf /usr/local/lib/lua/5.1/cjson.so /usr/lib/lua/5.1/cjson.so
/etc/init.d/nginx reload
'''#line:1231
        public .writeFile ('/root/install_cjson.sh',O0OOO0O000OO00O0O )#line:1232
        public .ExecShell ('cd /root && bash install_cjson.sh')#line:1233
        return True #line:1234
if __name__ =='__main__':#line:1238
    b_obj =btwaf_main ()#line:1239
    type =sys .argv [1 ]#line:1240
    if type =='start':#line:1241
        b_obj .retuen_nginx ()#line:1242
    elif type =='zhuzu':#line:1243
        b_obj .start_zhuzu ()#line:1244
    else :#line:1245
        b_obj .sync_cnlist (None )