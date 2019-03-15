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
import sys 
sys .path .append ('/www/server/panel/class');
import json ,os ,time ,public ,string 
os .chdir ('/www/server/panel')
if __name__ !='__main__':
    from panelAuth import panelAuth 
class btwaf_main :
    __O00O00O0OO0O00O0O ='/www/server/btwaf/'
    __O0OO0O0O000O0OOOO ={True :'开启',False :'关闭',0 :'停用',1 :'启用'}
    __O0OOOOOOO000OO0OO =None 
    __O0OO0000000O0O000 =["args.json","cookie.json","post.json","url_white.json","url.json","user_agent.json"]
    __OOOOO0OO0OOO0OO0O ={"EcShop":["/ecshop/api/cron.php","/appserver/public/js/main.js","/ecshop/js/index.js","/ecshop/data/config.php"],"weiqin":["/framework/table/users.table.php","/payment/alipay/return.php","/web/common/bootstrap.sys.inc.php"],"haiyang":["/data/admin/ping.php","/js/history.js","/templets/default/html/topicindex.html"],"canzhi":["/system/module/action/js/history.js","/system/framework/base/control.class.php","/www/data/css/default_clean_en.css"],"pingguo":["/static/js/jquery.pngFix.js","/static/css/admin_style.css","/template/default_pc/js/jquery-autocomplete.js"],"PHPCMS":["/phpsso_server/statics/css/system.css","/phpcms/languages/en/cnzz.lang.php","/api/reg_send_sms.php"],"wordpress":["/wp-content/languages/admin-network-zh_CN.mo","/wp-includes/js/admin-bar.js","/wp-admin/css/colors/ocean/colors.css"],"zhimeng":["/include/calendar/calendar-win2k-1.css","/include/js/jquery/ui.tabs.js","/inc/inc_stat.php","/images/js/ui.core.js"],"Discuz":["/static/js/admincp.js","/api/javascript/javascript.php","/api/trade/notify_invite.php"],"metlnfo":["/admin/content/article/save.php","/app/system/column","/config/metinfo.inc.php"]}
    def get_zhizu_list (O000OOO00O00O0O0O ):
        O0O0000O0000OO0O0 =public .httpGet ('http://www.bt.cn/api/panel/get_spider_type')
        if not O0O0000O0000OO0O0 :return False 
        public .WriteFile (O000OOO00O00O0O0O .__O00O00O0OO0O00O0O +'zhi.json',O0O0000O0000OO0O0 )
        return json .loads (O0O0000O0000OO0O0 )
    def get_zhizu_ip_list (OO0O0O0O0O0OOO000 ):
        from BTPanel import session 
        OOO00O000O00O0000 =OO0O0O0O0O0OOO000 .get_zhizu_list ()
        if 'types'in OOO00O000O00O0000 :
            if len (OOO00O000O00O0000 ['types'])>=1 :
                for O00OO0O0O00OO00OO in OOO00O000O00O0000 ['types']:
                    OO0O00O00000OO000 =public .httpGet ('http://www.bt.cn/api/panel/get_spider?spider=%s'%str (O00OO0O0O00OO00OO ['id']))
                    if not OO0O00O00000OO000 :continue 
                    try :
                        OO0OO0O00O0O0000O =json .dumps (OO0O00O00000OO000 )
                    except :
                        if not os .path .exists (OO0O0O0O0O0OOO000 .__O00O00O0OO0O00O0O +str (O00OO0O0O00OO00OO ['id'])+'.json'):
                            O0000OO000OOO0OOO =[]
                            public .WriteFile (OO0O0O0O0O0OOO000 .__O00O00O0OO0O00O0O +str (O00OO0O0O00OO00OO ['id'])+'.json',json .dumps (O0000OO000OOO0OOO ))
                        continue 
                    if os .path .exists (OO0O0O0O0O0OOO000 .__O00O00O0OO0O00O0O +str (O00OO0O0O00OO00OO ['id'])+'.json'):
                        O0OO0OO00OOO0000O =public .ReadFile (OO0O0O0O0O0OOO000 .__O00O00O0OO0O00O0O +str (O00OO0O0O00OO00OO ['id'])+'.json')
                        if O0OO0OO00OOO0000O :
                            O000OOOOO0O000OOO =list (set (json .loads (O0OO0OO00OOO0000O )).union (json .loads (OO0O00O00000OO000 )))
                            public .WriteFile (OO0O0O0O0O0OOO000 .__O00O00O0OO0O00O0O +str (O00OO0O0O00OO00OO ['id'])+'.json',json .dumps (O000OOOOO0O000OOO ))
                            O0O000OO00OOO0O0O =list (set (O0OO0OO00OOO0000O ).difference (set (OO0O00O00000OO000 )))
                            public .httpGet ('https://www.bt.cn/api/panel/add_spiders?address=%s'%json .dumps (O0O000OO00OOO0O0O ))
                        else :
                            public .WriteFile (OO0O0O0O0O0OOO000 .__O00O00O0OO0O00O0O +str (O00OO0O0O00OO00OO ['id'])+'.json',OO0O00O00000OO000 )
                    else :
                        public .WriteFile (OO0O0O0O0O0OOO000 .__O00O00O0OO0O00O0O +str (O00OO0O0O00OO00OO ['id'])+'.json',OO0O00O00000OO000 )
        if not 'zhizu'in session :session ['zhizu']=1 
        return True 
    def get_zhizu_list22 (OOOO0O0OOO0OO0OO0 ,OO0OOO0OO0O0O0000 ):
        O0O000OOO0O0OO0OO =OOOO0O0OOO0OO0OO0 .get_zhizu_list ()
        if 'types'in O0O000OOO0O0OO0OO :
            if len (O0O000OOO0O0OO0OO ['types'])>=1 :
                for O00OOOO000OO0O0OO in O0O000OOO0O0OO0OO ['types']:
                    OO00000OOOOOOO0O0 =public .httpGet ('http://www.bt.cn/api/panel/get_spider?spider=%s'%str (O00OOOO000OO0O0OO ['id']))
                    if not OO00000OOOOOOO0O0 :continue 
                    try :
                        OOOOOO0O000000OO0 =json .dumps (OO00000OOOOOOO0O0 )
                    except :
                        if not os .path .exists (OOOO0O0OOO0OO0OO0 .__O00O00O0OO0O00O0O +str (O00OOOO000OO0O0OO ['id'])+'.json'):
                            O0O0OOO00O00O00OO =[]
                            public .WriteFile (OOOO0O0OOO0OO0OO0 .__O00O00O0OO0O00O0O +str (O00OOOO000OO0O0OO ['id'])+'.json',json .dumps (O0O0OOO00O00O00OO ))
                        continue 
                    if os .path .exists (OOOO0O0OOO0OO0OO0 .__O00O00O0OO0O00O0O +str (O00OOOO000OO0O0OO ['id'])+'.json'):
                        OO0O0OO00OOO0O000 =public .ReadFile (OOOO0O0OOO0OO0OO0 .__O00O00O0OO0O00O0O +str (O00OOOO000OO0O0OO ['id'])+'.json')
                        if OO0O0OO00OOO0O000 :
                            O0OOOOO0000O0OOOO =list (set (json .loads (OO0O0OO00OOO0O000 )).union (json .loads (OO00000OOOOOOO0O0 )))
                            public .WriteFile (OOOO0O0OOO0OO0OO0 .__O00O00O0OO0O00O0O +str (O00OOOO000OO0O0OO ['id'])+'.json',json .dumps (O0OOOOO0000O0OOOO ))
                            OO00O00O00O0OO000 =list (set (OO0O0OO00OOO0O000 ).difference (set (OO00000OOOOOOO0O0 )))
                            public .httpGet ('https://www.bt.cn/api/panel/add_spiders?address=%s'%json .dumps (OO00O00O00O0OO000 ))
                        else :
                            public .WriteFile (OOOO0O0OOO0OO0OO0 .__O00O00O0OO0O00O0O +str (O00OOOO000OO0O0OO ['id'])+'.json',OO00000OOOOOOO0O0 )
                    else :
                        public .WriteFile (OOOO0O0OOO0OO0OO0 .__O00O00O0OO0O00O0O +str (O00OOOO000OO0O0OO ['id'])+'.json',OO00000OOOOOOO0O0 )
        return public .returnMsg (True ,'更新蜘蛛成功!')
    def start_zhuzu (OO0OOOO00000OO000 ):
        OOOO0OOOO0OO0OO0O =OO0OOOO00000OO000 .get_zhizu_list ()
        if 'types'in OOOO0OOOO0OO0OO0O :
            if len (OOOO0OOOO0OO0OO0O ['types'])>=1 :
                for OO0OO00O00OOOOOO0 in OOOO0OOOO0OO0OO0O ['types']:
                    O0O0OOO0000O0O00O =public .httpGet ('http://www.bt.cn/api/panel/get_spider?spider=%s'%str (OO0OO00O00OOOOOO0 ['id']))
                    if not O0O0OOO0000O0O00O :continue 
                    try :
                        O000OO00O0OO00O0O =json .dumps (O0O0OOO0000O0O00O )
                    except :
                        if not os .path .exists (OO0OOOO00000OO000 .__O00O00O0OO0O00O0O +str (OO0OO00O00OOOOOO0 ['id'])+'.json'):
                            OOO0OOO0O0000O0O0 =[]
                            public .WriteFile (OO0OOOO00000OO000 .__O00O00O0OO0O00O0O +str (OO0OO00O00OOOOOO0 ['id'])+'.json',json .dumps (OOO0OOO0O0000O0O0 ))
                        continue 
                    if os .path .exists (OO0OOOO00000OO000 .__O00O00O0OO0O00O0O +str (OO0OO00O00OOOOOO0 ['id'])+'.json'):
                        OO0O0OOO00000O0O0 =public .ReadFile (OO0OOOO00000OO000 .__O00O00O0OO0O00O0O +str (OO0OO00O00OOOOOO0 ['id'])+'.json')
                        if OO0O0OOO00000O0O0 :
                            OOO0O000OO00OO0OO =list (set (json .loads (OO0O0OOO00000O0O0 )).union (json .loads (O0O0OOO0000O0O00O )))
                            public .WriteFile (OO0OOOO00000OO000 .__O00O00O0OO0O00O0O +str (OO0OO00O00OOOOOO0 ['id'])+'.json',json .dumps (OOO0O000OO00OO0OO ))
                            OO000O0O00O000OOO =list (set (OO0O0OOO00000O0O0 ).difference (set (O0O0OOO0000O0O00O )))
                            public .httpGet ('https://www.bt.cn/api/panel/add_spiders?address=%s'%json .dumps (OO000O0O00O000OOO ))
                        else :
                            public .WriteFile (OO0OOOO00000OO000 .__O00O00O0OO0O00O0O +str (OO0OO00O00OOOOOO0 ['id'])+'.json',O0O0OOO0000O0O00O )
                    else :
                        public .WriteFile (OO0OOOO00000OO000 .__O00O00O0OO0O00O0O +str (OO0OO00O00OOOOOO0 ['id'])+'.json',O0O0OOO0000O0O00O )
        return True 
    def get_zhizu_ip (O0OO0O0OO000OO00O ,O00O0000O00O0O0O0 ):
        OOOOOO0O00O0O0OO0 =O0OO0O0OO000OO00O .get_zhizu_list ()
        if 'types'in OOOOOO0O00O0O0OO0 :
            if len (OOOOOO0O00O0O0OO0 ['types'])>=1 :
                for OO0OOOO0OOOOO00O0 in OOOOOO0O00O0O0OO0 ['types']:
                    O0OOO0O0OOO0000OO =public .httpGet ('http://www.bt.cn/api/panel/get_spider?spider=%s'%str (OO0OOOO0OOOOO00O0 ['id']))
                    if not O0OOO0O0OOO0000OO :continue 
                    try :
                        O0OOO0000O00OO00O =json .dumps (O0OOO0O0OOO0000OO )
                    except :
                        if not os .path .exists (O0OO0O0OO000OO00O .__O00O00O0OO0O00O0O +str (OO0OOOO0OOOOO00O0 ['id'])+'.json'):
                            OO000O000O00OOOOO =[]
                            public .WriteFile (O0OO0O0OO000OO00O .__O00O00O0OO0O00O0O +str (OO0OOOO0OOOOO00O0 ['id'])+'.json',json .dumps (OO000O000O00OOOOO ))
                        continue 
                    if os .path .exists (O0OO0O0OO000OO00O .__O00O00O0OO0O00O0O +str (OO0OOOO0OOOOO00O0 ['id'])+'.json'):
                        O0000O0O0000000O0 =public .ReadFile (O0OO0O0OO000OO00O .__O00O00O0OO0O00O0O +str (OO0OOOO0OOOOO00O0 ['id'])+'.json')
                        if O0000O0O0000000O0 :
                            O00OOO0O000OO0O0O =list (set (json .loads (O0000O0O0000000O0 )).union (json .loads (O0OOO0O0OOO0000OO )))
                            public .WriteFile (O0OO0O0OO000OO00O .__O00O00O0OO0O00O0O +str (OO0OOOO0OOOOO00O0 ['id'])+'.json',json .dumps (O00OOO0O000OO0O0O ))
                            OOOOO0OOOO0OOOOOO =list (set (O0000O0O0000000O0 ).difference (set (O0OOO0O0OOO0000OO )))
                            public .httpGet ('https://www.bt.cn/api/panel/add_spiders?address=%s'%json .dumps (OOOOO0OOOO0OOOOOO ))
                        else :
                            public .WriteFile (O0OO0O0OO000OO00O .__O00O00O0OO0O00O0O +str (OO0OOOO0OOOOO00O0 ['id'])+'.json',json .dumps (O0OOO0O0OOO0000OO ))
                    else :
                        public .WriteFile (O0OO0O0OO000OO00O .__O00O00O0OO0O00O0O +str (OO0OOOO0OOOOO00O0 ['id'])+'.json',json .dumps (O0OOO0O0OOO0000OO ))
        return public .returnMsg (True ,'更新蜘蛛成功!')
    def get_process_list (OOOO000O0OOO00000 ):
        import psutil 
        OOO0O0OOO000OOOOO =0 
        O00O0OOO0O00000O0 =int (public .ExecShell ('cat /proc/cpuinfo |grep "processor"|wc -l')[0 ])
        OO0O00O0O000OO00O =psutil .pids ();
        for O0000000OOO0OO0OO in OO0O00O0O000OO00O :
            O0OOO00O00O0OOO0O ={}
            try :
                OO0O0OOOOOOO0OO00 =psutil .Process (O0000000OOO0OO0OO );
            except :
                continue 
            if str (OO0O0OOOOOOO0OO00 .name ())=='php-fpm':
                OOO0O0OOO000OOOOO +=int (OO0O0OOOOOOO0OO00 .cpu_percent (0.1 ))
        public .ExecShell ("echo '%s' >/dev/shm/nginx.txt"%OOO0O0OOO000OOOOO /O00O0OOO0O00000O0 )
        return OOO0O0OOO000OOOOO /O00O0OOO0O00000O0 
    def Start_apache_cc (O0OO000OO0O0OO0O0 ,OO000000OO0000OOO ):
        OO000O0O0OO0OO000 =O0OO000OO0O0OO0O0 .auto_sync_apache ()
        return OO000O0O0OO0OO000 
    def Get_apap_cc (OO0O00O00O00O00OO ,O000O0O00000O00OO ):
        O00O00O0OO0O00O00 =public .M ('crontab').where ('name=?',(u'Nginx防火墙智能防御CC',)).getField ('id');
        if O00O00O0OO0O00O00 :return public .returnMsg (True ,'开启!');
        else :return public .returnMsg (False ,'关闭!');
    def Stop_apache_cc (OOO0O0OO0O000O00O ,O0OOO00000O0O00OO ):
        if os .path .exists ('/dev/shm/nginx.txt'):
            os .remove ('/dev/shm/nginx.txt')
        OOO000O0O0O0O0O00 =public .M ('crontab').where ('name=?',(u'Nginx防火墙智能防御CC',)).getField ('id');
        import crontab 
        if OOO000O0O0O0O0O00 :crontab .crontab ().DelCrontab ({'id':OOO000O0O0O0O0O00 })
        return public .returnMsg (True ,'设置成功!');
    def auto_sync_apache (OO0OO0O0OO0000OOO ):
        OO0OOO000O0OOO000 =public .M ('crontab').where ('name=?',(u'Nginx防火墙智能防御CC',)).getField ('id');
        import crontab 
        if OO0OOO000O0OOO000 :crontab .crontab ().DelCrontab ({'id':OO0OOO000O0OOO000 })
        OO0OOOO00OOO0OO0O ={}
        OO0OOOO00OOO0OO0O ['name']=u'Nginx防火墙智能防御CC'
        OO0OOOO00OOO0OO0O ['type']='minute-n'
        OO0OOOO00OOO0OO0O ['where1']='1'
        OO0OOOO00OOO0OO0O ['sBody']='python /www/server/panel/plugin/btwaf/btwaf_main.py start'
        OO0OOOO00OOO0OO0O ['backupTo']='localhost'
        OO0OOOO00OOO0OO0O ['sType']='toShell'
        OO0OOOO00OOO0OO0O ['hour']=''
        OO0OOOO00OOO0OO0O ['minute']=''
        OO0OOOO00OOO0OO0O ['week']=''
        OO0OOOO00OOO0OO0O ['sName']=''
        OO0OOOO00OOO0OO0O ['urladdress']=''
        OO0OOOO00OOO0OO0O ['save']=''
        crontab .crontab ().AddCrontab (OO0OOOO00OOO0OO0O )
        return public .returnMsg (True ,'设置成功!');
    def retuen_nginx (O0O000O0OOOO0O0O0 ):
        import psutil 
        O000O00O0OOOOOOO0 =0 
        OO0O0O00OOOOO0000 =int (public .ExecShell ('cat /proc/cpuinfo |grep "processor"|wc -l')[0 ])
        OO000O0OO0OO0O000 =psutil .pids ();
        for O0OO00OO00000O0OO in OO000O0OO0OO0O000 :
            O0O00OOO000O0OOOO ={}
            try :
                OOO00O0O0O0OO00O0 =psutil .Process (O0OO00OO00000O0OO );
            except :
                continue 
            if str (OOO00O0O0O0OO00O0 .name ())=='php-fpm':
                O000O00O0OOOOOOO0 +=int (OOO00O0O0O0OO00O0 .cpu_percent (0.1 ))
        public .ExecShell ("echo '%s' >/dev/shm/nginx.txt"%str (O000O00O0OOOOOOO0 /OO0O0O00OOOOO0000 ))
        return O000O00O0OOOOOOO0 /OO0O0O00OOOOO0000 
    def get_config (O0O0OOOO00OOO00OO ,O0OOO0OO0O0O00OO0 ):
        OO000O00OO000000O =json .loads (public .readFile (O0O0OOOO00OOO00OO .__O00O00O0OO0O00O0O +'config.json'))
        if not 'retry_cycle'in OO000O00OO000000O :
            OO000O00OO000000O ['retry_cycle']=60 ;
            O0O0OOOO00OOO00OO .__OO0O00OO0O00O00O0 (OO000O00OO000000O );
        if OO000O00OO000000O ['start_time']==0 :
            OO000O00OO000000O ['start_time']=time .time ();
            O0O0OOOO00OOO00OO .__OO0O00OO0O00O00O0 (OO000O00OO000000O );
        return OO000O00OO000000O 
    def get_site_config (OOO00OOO000OO00OO ,O0O000O00O0OO0OO0 ):
        O00O0O00OO0OOOO0O =public .readFile (OOO00OOO000OO00OO .__O00O00O0OO0O00O0O +'site.json');
        O000000OOO0O0O0O0 =OOO00OOO000OO00OO .__OOOOOO0OO0O0OOO00 (json .loads (O00O0O00OO0OOOO0O ))
        if O0O000O00O0OO0OO0 :
            OO000OO0O0OOOOO0O =OOO00OOO000OO00OO .get_total (None )['sites']
            OOO0O00O0OO0000O0 =[]
            for OOOOO0O0O0OOOO0OO in O000000OOO0O0O0O0 .keys ():
                if not OOOOO0O0O0OOOO0OO in OO000OO0O0OOOOO0O :OO000OO0O0OOOOO0O [OOOOO0O0O0OOOO0OO ]={}
                O000000OOO0O0O0O0 [OOOOO0O0O0OOOO0OO ]['total']=OOO00OOO000OO00OO .__O0O0OOOO00OOOO0O0 (OO000OO0O0OOOOO0O [OOOOO0O0O0OOOO0OO ])
                O0O0O000OOOOOO000 =O000000OOO0O0O0O0 [OOOOO0O0O0OOOO0OO ];
                O0O0O000OOOOOO000 ['siteName']=OOOOO0O0O0OOOO0OO ;
                OOO0O00O0OO0000O0 .append (O0O0O000OOOOOO000 );
            O000000OOO0O0O0O0 =sorted (OOO0O00O0OO0000O0 ,key =lambda O0OO0O0OO0OO000O0 :O0OO0O0OO0OO000O0 ['log_size'],reverse =True )
        return O000000OOO0O0O0O0 
    def get_site_config_byname (OOOO0OO0OOOO00O0O ,O0OO00O0OO00O0000 ):
        OO0OOOOO00OOOOO00 =OOOO0OO0OOOO00O0O .get_site_config (None );
        O0OO0O0OOOO0OO0O0 =OO0OOOOO00OOOOO00 [O0OO00O0OO00O0000 .siteName ]
        O0OO0O0OOOO0OO0O0 ['top']=OOOO0OO0OOOO00O0O .get_config (None )
        return O0OO0O0OOOO0OO0O0 
    def set_open (OO0000O0OOO0OO0OO ,OO00O00OOOO00OO00 ):
        from BTPanel import session ,cache 
        if not 'btwaf'in session :
            O00O0OOO0000OOOO0 =OO0000O0OOO0OO0OO .get_btwaf ()
            if O00O0OOO0000OOOO0 ==0 :
                OO0000O0OOO0OO0OO .stop ()
                return public .returnMsg (False ,'')
        OOO0OO000000O00OO =OO0000O0OOO0OO0OO .get_config (None )
        if OOO0OO000000O00OO ['open']:
            OOO0OO000000O00OO ['open']=False 
            OOO0OO000000O00OO ['start_time']=0 
        else :
            OOO0OO000000O00OO ['open']=True 
            OOO0OO000000O00OO ['start_time']=int (time .time ())
        OO0000O0OOO0OO0OO .__O0OOOO0000OOOOOOO (OO0000O0OOO0OO0OO .__O0OO0O0O000O0OOOO [OOO0OO000000O00OO ['open']]+'网站防火墙(WAF)');
        OO0000O0OOO0OO0OO .__OO0O00OO0O00O00O0 (OOO0OO000000O00OO )
        return public .returnMsg (True ,'设置成功!');
    def set_obj_open (O0000OO0OO0OO0OOO ,OOOOO0O0OOOO000OO ):
        O0O0O00O0OO0O00OO =O0000OO0OO0OO0OOO .get_config (None )
        if type (O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ])!=bool :
            if O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]['open']:
                O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]['open']=False 
            else :
                O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]['open']=True 
            O0000OO0OO0OO0OOO .__O0OOOO0000OOOOOOO (O0000OO0OO0OO0OOO .__O0OO0O0O000O0OOOO [O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]['open']]+'【'+OOOOO0O0OOOO000OO .obj +'】功能');
        else :
            if O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]:
                O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]=False 
            else :
                O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]=True 
            O0000OO0OO0OO0OOO .__O0OOOO0000OOOOOOO (O0000OO0OO0OO0OOO .__O0OO0O0O000O0OOOO [O0O0O00O0OO0O00OO [OOOOO0O0OOOO000OO .obj ]]+'【'+OOOOO0O0OOOO000OO .obj +'】功能');
        O0000OO0OO0OO0OOO .__OO0O00OO0O00O00O0 (O0O0O00O0OO0O00OO )
        return public .returnMsg (True ,'设置成功!');
    def set_site_obj_open (OO00OO0OOOO00O00O ,OOOOO0O0O000OOO00 ):
        OOOO00OOO0O0OOO00 =OO00OO0OOOO00O00O .get_site_config (None )
        if type (OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ])!=bool :
            if OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]['open']:
                OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]['open']=False 
            else :
                OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]['open']=True 
            OO00OO0OOOO00O00O .__O0OOOO0000OOOOOOO (OO00OO0OOOO00O00O .__O0OO0O0O000O0OOOO [OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]['open']]+'网站【'+OOOOO0O0O000OOO00 .siteName +'】【'+OOOOO0O0O000OOO00 .obj +'】功能');
        else :
            if OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]:
                OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]=False 
            else :
                OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]=True 
            OO00OO0OOOO00O00O .__O0OOOO0000OOOOOOO (OO00OO0OOOO00O00O .__O0OO0O0O000O0OOOO [OOOO00OOO0O0OOO00 [OOOOO0O0O000OOO00 .siteName ][OOOOO0O0O000OOO00 .obj ]]+'网站【'+OOOOO0O0O000OOO00 .siteName +'】【'+OOOOO0O0O000OOO00 .obj +'】功能');
        if OOOOO0O0O000OOO00 .obj =='drop_abroad':OO00OO0OOOO00O00O .__OOO0OOO0O0O0OO0OO ();
        OO00OO0OOOO00O00O .__OO000O00OOO0OO0O0 (OOOO00OOO0O0OOO00 )
        return public .returnMsg (True ,'设置成功!');
    def set_obj_status (O0000OO0OO000OOOO ,O0O00O0O0O0OOOOOO ):
        OOO0O000O00OO00OO =O0000OO0OO000OOOO .get_config (None )
        OOO0O000O00OO00OO [O0O00O0O0O0OOOOOO .obj ]['status']=int (O0O00O0O0O0OOOOOO .statusCode )
        O0000OO0OO000OOOO .__OO0O00OO0O00O00O0 (OOO0O000O00OO00OO )
        return public .returnMsg (True ,'设置成功!');
    def set_cc_conf (O0OOOO00OO000O000 ,O000OOOO00OOO0OO0 ):
        OO00000O000O000OO =O0OOOO00OO000O000 .get_config (None )
        OO00000O000O000OO ['cc']['cycle']=int (O000OOOO00OOO0OO0 .cycle )
        OO00000O000O000OO ['cc']['limit']=int (O000OOOO00OOO0OO0 .limit )
        OO00000O000O000OO ['cc']['endtime']=int (O000OOOO00OOO0OO0 .endtime )
        OO00000O000O000OO ['cc']['increase']=(O000OOOO00OOO0OO0 .increase =='1')|False 
        O0OOOO00OO000O000 .__OO0O00OO0O00O00O0 (OO00000O000O000OO )
        O0OOOO00OO000O000 .__O0OOOO0000OOOOOOO ('设置全局CC配置为：'+O000OOOO00OOO0OO0 .cycle +' 秒内累计请求超过 '+O000OOOO00OOO0OO0 .limit +' 次后,封锁 '+O000OOOO00OOO0OO0 .endtime +' 秒'+',增强:'+O000OOOO00OOO0OO0 .increase );
        return public .returnMsg (True ,'设置成功!');
    def set_site_cc_conf (OO000OOO00OOOO000 ,O0OO0000O0OO0OOO0 ):
        O00OOOOO0OOO0O0O0 =OO000OOO00OOOO000 .get_site_config (None )
        O00OOOOO0OOO0O0O0 [O0OO0000O0OO0OOO0 .siteName ]['cc']['cycle']=int (O0OO0000O0OO0OOO0 .cycle )
        O00OOOOO0OOO0O0O0 [O0OO0000O0OO0OOO0 .siteName ]['cc']['limit']=int (O0OO0000O0OO0OOO0 .limit )
        O00OOOOO0OOO0O0O0 [O0OO0000O0OO0OOO0 .siteName ]['cc']['endtime']=int (O0OO0000O0OO0OOO0 .endtime )
        O00OOOOO0OOO0O0O0 [O0OO0000O0OO0OOO0 .siteName ]['cc']['increase']=(O0OO0000O0OO0OOO0 .increase =='1')|False 
        OO000OOO00OOOO000 .__OO000O00OOO0OO0O0 (O00OOOOO0OOO0O0O0 )
        OO000OOO00OOOO000 .__O0OOOO0000OOOOOOO ('设置站点【'+O0OO0000O0OO0OOO0 .siteName +'】CC配置为：'+O0OO0000O0OO0OOO0 .cycle +' 秒内累计请求超过 '+O0OO0000O0OO0OOO0 .limit +' 次后,封锁 '+O0OO0000O0OO0OOO0 .endtime +' 秒'+',增强:'+O0OO0000O0OO0OOO0 .increase );
        return public .returnMsg (True ,'设置成功!');
    def add_cnip (OO00OOOOOO0O0OO00 ,OO0OO00O00OOO0000 ):
        O000OOO0000OO000O =[OO00OOOOOO0O0OO00 .__O000O00000O0OOOOO (OO0OO00O00OOO0000 .start_ip ),OO00OOOOOO0O0OO00 .__O000O00000O0OOOOO (OO0OO00O00OOO0000 .end_ip )]
        if not O000OOO0000OO000O [0 ]or not O000OOO0000OO000O [1 ]:return public .returnMsg (False ,'IP段格式不正确');
        if not OO00OOOOOO0O0OO00 .__O0OOOOOOOOO0OO00O (O000OOO0000OO000O ):return public .returnMsg (False ,'起始IP不能大于结束IP');
        OO000OOO00O000OOO =OO00OOOOOO0O0OO00 .__O0000000OO00000O0 ('cn')
        if O000OOO0000OO000O in OO000OOO00O000OOO :return public .returnMsg (False ,'指定IP段已存在!');
        OO000OOO00O000OOO .insert (0 ,O000OOO0000OO000O )
        OO00OOOOOO0O0OO00 .__O0O00O0O0O0O0O000 ('cn',OO000OOO00O000OOO )
        OO00OOOOOO0O0OO00 .__O0OOOO0000OOOOOOO ('添加IP段['+OO0OO00O00OOO0000 .start_ip +'-'+OO0OO00O00OOO0000 .end_ip +']到国内IP库');
        return public .returnMsg (True ,'添加成功!');
    def remove_cnip (O0OO0OO00OOOOOOO0 ,O0OO0O0O0OOOOOOO0 ):
        O0000000O00000OO0 =int (O0OO0O0O0OOOOOOO0 .index )
        OO0000OO0OO0O0000 =O0OO0OO00OOOOOOO0 .__O0000000OO00000O0 ('cn')
        OO0OOOO000O00O0O0 =OO0000OO0OO0O0000 [O0000000O00000OO0 ]
        del (OO0000OO0OO0O0000 [O0000000O00000OO0 ])
        O0OO0OO00OOOOOOO0 .__O0O00O0O0O0O0O000 ('cn',OO0000OO0OO0O0000 )
        O0OO0OO00OOOOOOO0 .__O0OOOO0000OOOOOOO ('从国内IP库删除['+'.'.join (map (str ,OO0OOOO000O00O0O0 [0 ]))+'-'+'.'.join (map (str ,OO0OOOO000O00O0O0 [1 ]))+']');
        return public .returnMsg (True ,'删除成功!');
    def add_ip_white (O0O00O0OOO000000O ,OOOOOO0O00O0OO0O0 ):
        OO00OOOOOOOO0O000 =[O0O00O0OOO000000O .__O000O00000O0OOOOO (OOOOOO0O00O0OO0O0 .start_ip ),O0O00O0OOO000000O .__O000O00000O0OOOOO (OOOOOO0O00O0OO0O0 .end_ip )]
        if not OO00OOOOOOOO0O000 [0 ]or not OO00OOOOOOOO0O000 [1 ]:return public .returnMsg (False ,'IP段格式不正确');
        if not O0O00O0OOO000000O .__O0OOOOOOOOO0OO00O (OO00OOOOOOOO0O000 ):return public .returnMsg (False ,'起始IP不能大于结束IP');
        O0O0OOO0OO000OOO0 =O0O00O0OOO000000O .__O0000000OO00000O0 ('ip_white')
        if OO00OOOOOOOO0O000 in O0O0OOO0OO000OOO0 :return public .returnMsg (False ,'指定IP段已存在!');
        O0O0OOO0OO000OOO0 .insert (0 ,OO00OOOOOOOO0O000 )
        O0O00O0OOO000000O .__O0O00O0O0O0O0O000 ('ip_white',O0O0OOO0OO000OOO0 )
        O0O00O0OOO000000O .__O0OOOO0000OOOOOOO ('添加IP段['+OOOOOO0O00O0OO0O0 .start_ip +'-'+OOOOOO0O00O0OO0O0 .end_ip +']到IP白名单');
        return public .returnMsg (True ,'添加成功!');
    def remove_ip_white (OOOOO00O0OO000OO0 ,O0O000000000OO0O0 ):
        OOOO0000O0O0OO0O0 =int (O0O000000000OO0O0 .index )
        OOOOO00OOO0000O00 =OOOOO00O0OO000OO0 .__O0000000OO00000O0 ('ip_white')
        OOOOO00O0O0OO0O0O =OOOOO00OOO0000O00 [OOOO0000O0O0OO0O0 ]
        del (OOOOO00OOO0000O00 [OOOO0000O0O0OO0O0 ])
        OOOOO00O0OO000OO0 .__O0O00O0O0O0O0O000 ('ip_white',OOOOO00OOO0000O00 )
        OOOOO00O0OO000OO0 .__O0OOOO0000OOOOOOO ('从IP白名单删除['+'.'.join (map (str ,OOOOO00O0O0OO0O0O [0 ]))+'-'+'.'.join (map (str ,OOOOO00O0O0OO0O0O [1 ]))+']');
        return public .returnMsg (True ,'删除成功!');
    def import_data (O00O0O000OOO0O0O0 ,OOOOO0OOOO0O0O00O ):
        O0O0OO0000OO0O0OO =OOOOO0OOOO0O0O00O .s_Name ;
        O00OOOO0O00OOO0O0 =json .loads (OOOOO0OOOO0O0O00O .pdata )
        if not O00OOOO0O00OOO0O0 :return public .returnMsg (False ,'数据格式不正确');
        OO000OOO0O0OO0000 =O00O0O000OOO0O0O0 .__O0000000OO00000O0 (O0O0OO0000OO0O0OO );
        for OO0O00O0OOOO000OO in O00OOOO0O00OOO0O0 :
            if OO0O00O0OOOO000OO in OO000OOO0O0OO0000 :continue ;
            OO000OOO0O0OO0000 .insert (0 ,OO0O00O0OOOO000OO )
        O00O0O000OOO0O0O0 .__O0O00O0O0O0O0O000 (O0O0OO0000OO0O0OO ,OO000OOO0O0OO0000 )
        return public .returnMsg (True ,'导入成功!')
    def output_data (OO0OO0OOOOOOOO0O0 ,O0000OO0OOOO0OOO0 ):
        O00OOOOO00O00OOOO =OO0OO0OOOOOOOO0O0 .__O0000000OO00000O0 (O0000OO0OOOO0OOO0 .s_Name )
        return O00OOOOO00O00OOOO ;
    def add_ip_black (OOO0O000O0OO0O0OO ,O0000O000OO0OOO00 ):
        OO0OOOOO0000000OO =[OOO0O000O0OO0O0OO .__O000O00000O0OOOOO (O0000O000OO0OOO00 .start_ip ),OOO0O000O0OO0O0OO .__O000O00000O0OOOOO (O0000O000OO0OOO00 .end_ip )]
        if not OO0OOOOO0000000OO [0 ]or not OO0OOOOO0000000OO [1 ]:return public .returnMsg (False ,'IP段格式不正确');
        if not OOO0O000O0OO0O0OO .__O0OOOOOOOOO0OO00O (OO0OOOOO0000000OO ):return public .returnMsg (False ,'起始IP不能大于结束IP');
        O0OO0O000000O000O =OOO0O000O0OO0O0OO .__O0000000OO00000O0 ('ip_black')
        if OO0OOOOO0000000OO in O0OO0O000000O000O :return public .returnMsg (False ,'指定IP段已存在!');
        O0OO0O000000O000O .insert (0 ,OO0OOOOO0000000OO )
        OOO0O000O0OO0O0OO .__O0O00O0O0O0O0O000 ('ip_black',O0OO0O000000O000O )
        OOO0O000O0OO0O0OO .__O0OOOO0000OOOOOOO ('添加IP段['+O0000O000OO0OOO00 .start_ip +'-'+O0000O000OO0OOO00 .end_ip +']到IP黑名单');
        return public .returnMsg (True ,'添加成功!');
    def remove_ip_black (O000OOOO00000O000 ,O0OOOO0OO00000O0O ):
        OOO000O00OOOOOO00 =int (O0OOOO0OO00000O0O .index )
        OOO0000O000O00O0O =O000OOOO00000O000 .__O0000000OO00000O0 ('ip_black')
        O0O000OO000000O0O =OOO0000O000O00O0O [OOO000O00OOOOOO00 ]
        del (OOO0000O000O00O0O [OOO000O00OOOOOO00 ])
        O000OOOO00000O000 .__O0O00O0O0O0O0O000 ('ip_black',OOO0000O000O00O0O )
        O000OOOO00000O000 .__O0OOOO0000OOOOOOO ('从IP黑名单删除['+'.'.join (map (str ,O0O000OO000000O0O [0 ]))+'-'+'.'.join (map (str ,O0O000OO000000O0O [1 ]))+']');
        return public .returnMsg (True ,'删除成功!');
    def add_url_white (O00O00OO0O0OO0O00 ,OOO0OO0O0O00OOOO0 ):
        O00000O0000O0O0OO =O00O00OO0O0OO0O00 .__O0000000OO00000O0 ('url_white')
        O00OO0OO000O00000 =OOO0OO0O0O00OOOO0 .url_rule .strip ()
        if OOO0OO0O0O00OOOO0 .url_rule in O00000O0000O0O0OO :return public .returnMsg (False ,'您添加的URL已存在')
        O00000O0000O0O0OO .insert (0 ,O00OO0OO000O00000 )
        O00O00OO0O0OO0O00 .__O0O00O0O0O0O0O000 ('url_white',O00000O0000O0O0OO )
        O00O00OO0O0OO0O00 .__O0OOOO0000OOOOOOO ('添加url规则['+O00OO0OO000O00000 +']到URL白名单');
        return public .returnMsg (True ,'添加成功!');
    def remove_url_white (O000O0O00OO0OOOOO ,O000OO00OO0O0O0OO ):
        OO0OO00000O000000 =O000O0O00OO0OOOOO .__O0000000OO00000O0 ('url_white')
        O000OOO0000OO00OO =int (O000OO00OO0O0O0OO .index )
        OO0OO0O0OO0O000O0 =OO0OO00000O000000 [O000OOO0000OO00OO ]
        del (OO0OO00000O000000 [O000OOO0000OO00OO ])
        O000O0O00OO0OOOOO .__O0O00O0O0O0O0O000 ('url_white',OO0OO00000O000000 )
        O000O0O00OO0OOOOO .__O0OOOO0000OOOOOOO ('从URL白名单删除URL规则['+OO0OO0O0OO0O000O0 +']');
        return public .returnMsg (True ,'删除成功!');
    def add_url_black (O0000O0OOOOO00O00 ,O0000O0000O00O0OO ):
        OOO00OO0OOO0OOO00 =O0000O0OOOOO00O00 .__O0000000OO00000O0 ('url_black')
        O00OO0OOO00O0OO00 =O0000O0000O00O0OO .url_rule .strip ()
        if O0000O0000O00O0OO .url_rule in OOO00OO0OOO0OOO00 :return public .returnMsg (False ,'您添加的URL已存在')
        OOO00OO0OOO0OOO00 .insert (0 ,O00OO0OOO00O0OO00 )
        O0000O0OOOOO00O00 .__O0O00O0O0O0O0O000 ('url_black',OOO00OO0OOO0OOO00 )
        O0000O0OOOOO00O00 .__O0OOOO0000OOOOOOO ('添加url规则['+O00OO0OOO00O0OO00 +']到URL黑名单');
        return public .returnMsg (True ,'添加成功!');
    def remove_url_black (O0O0O0000O00O00OO ,OO00O0O000OOO0O0O ):
        O0OOO0OOOO0OO00OO =O0O0O0000O00O00OO .__O0000000OO00000O0 ('url_black')
        OO000OO0OOO0OO0O0 =int (OO00O0O000OOO0O0O .index )
        OO000OOOO0O0O0OO0 =O0OOO0OOOO0OO00OO [OO000OO0OOO0OO0O0 ]
        del (O0OOO0OOOO0OO00OO [OO000OO0OOO0OO0O0 ])
        O0O0O0000O00O00OO .__O0O00O0O0O0O0O000 ('url_black',O0OOO0OOOO0OO00OO )
        O0O0O0000O00O00OO .__O0OOOO0000OOOOOOO ('从URL黑名单删除URL规则['+OO000OOOO0O0O0OO0 +']');
        return public .returnMsg (True ,'删除成功!');
    def save_scan_rule (O000OOO0OO00O0OO0 ,OOOO000OO00O0000O ):
        O000OO00O000O0O0O ={'header':OOOO000OO00O0000O .header ,'cookie':OOOO000OO00O0000O .cookie ,'args':OOOO000OO00O0000O .args }
        O000OOO0OO00O0OO0 .__O0O00O0O0O0O0O000 ('scan_black',O000OO00O000O0O0O )
        O000OOO0OO00O0OO0 .__O0OOOO0000OOOOOOO ('修改扫描器过滤规则');
        return public .returnMsg (True ,'设置成功')
    def set_retry (OOOO0OO0O0OOOO000 ,OO0O0O0O0OOO0OO00 ):
        O0OO00O00OO0O0O00 =OOOO0OO0O0OOOO000 .get_config (None )
        O0OO00O00OO0O0O00 ['retry']=int (OO0O0O0O0OOO0OO00 .retry )
        O0OO00O00OO0O0O00 ['retry_cycle']=int (OO0O0O0O0OOO0OO00 .retry_cycle )
        O0OO00O00OO0O0O00 ['retry_time']=int (OO0O0O0O0OOO0OO00 .retry_time )
        OOOO0OO0O0OOOO000 .__OO0O00OO0O00O00O0 (O0OO00O00OO0O0O00 )
        OOOO0OO0O0OOOO000 .__O0OOOO0000OOOOOOO ('设置非法请求容忍阈值: '+OO0O0O0O0OOO0OO00 .retry_cycle +' 秒内累计超过 '+OO0O0O0O0OOO0OO00 .retry +' 次, 封锁 '+OO0O0O0O0OOO0OO00 .retry_time +' 秒');
        return public .returnMsg (True ,'设置成功!');
    def set_site_retry (OOOOO000O00O0000O ,OOO000O0OOO00O0O0 ):
        O0O0OO00O00OOOOO0 =OOOOO000O00O0000O .get_site_config (None )
        O0O0OO00O00OOOOO0 [OOO000O0OOO00O0O0 .siteName ]['retry']=int (OOO000O0OOO00O0O0 .retry )
        O0O0OO00O00OOOOO0 [OOO000O0OOO00O0O0 .siteName ]['retry_cycle']=int (OOO000O0OOO00O0O0 .retry_cycle )
        O0O0OO00O00OOOOO0 [OOO000O0OOO00O0O0 .siteName ]['retry_time']=int (OOO000O0OOO00O0O0 .retry_time )
        OOOOO000O00O0000O .__OO000O00OOO0OO0O0 (O0O0OO00O00OOOOO0 )
        OOOOO000O00O0000O .__O0OOOO0000OOOOOOO ('设置网站【'+OOO000O0OOO00O0O0 .siteName +'】非法请求容忍阈值: '+OOO000O0OOO00O0O0 .retry_cycle +' 秒内累计超过 '+OOO000O0OOO00O0O0 .retry +' 次, 封锁 '+OOO000O0OOO00O0O0 .retry_time +' 秒');
        return public .returnMsg (True ,'设置成功!');
    def set_site_cdn_state (O00OOOO0OOO00O00O ,O00OO0O00OO0OO000 ):
        O0O000O000OO00OO0 =O00OOOO0OOO00O00O .get_site_config (None )
        if O0O000O000OO00OO0 [O00OO0O00OO0OO000 .siteName ]['cdn']:
            O0O000O000OO00OO0 [O00OO0O00OO0OO000 .siteName ]['cdn']=False 
        else :
            O0O000O000OO00OO0 [O00OO0O00OO0OO000 .siteName ]['cdn']=True 
        O00OOOO0OOO00O00O .__OO000O00OOO0OO0O0 (O0O000O000OO00OO0 )
        O00OOOO0OOO00O00O .__O0OOOO0000OOOOOOO (O00OOOO0OOO00O00O .__O0OO0O0O000O0OOOO [O0O000O000OO00OO0 [O00OO0O00OO0OO000 .siteName ]['cdn']]+'站点【'+O00OO0O00OO0OO000 .siteName +'】CDN模式');
        return public .returnMsg (True ,'设置成功!');
    def get_site_cdn_header (OOO0O0O00O00O0O00 ,OOO0000O0O0OO00OO ):
        OOOOOOOOO0O0OO00O =OOO0O0O00O00O0O00 .get_site_config (None )
        return OOOOOOOOO0O0OO00O [OOO0000O0O0OO00OO .siteName ]['cdn_header']
    def add_site_cdn_header (O0OOOOO00O0O00000 ,OOO00O00000000O0O ):
        OO00O0O00000000OO =O0OOOOO00O0O00000 .get_site_config (None )
        OOO00O00000000O0O .cdn_header =OOO00O00000000O0O .cdn_header .strip ().lower ();
        if OOO00O00000000O0O .cdn_header in OO00O0O00000000OO [OOO00O00000000O0O .siteName ]['cdn_header']:return public .returnMsg (False ,'您添加的请求头已存在!');
        OO00O0O00000000OO [OOO00O00000000O0O .siteName ]['cdn_header'].append (OOO00O00000000O0O .cdn_header )
        O0OOOOO00O0O00000 .__OO000O00OOO0OO0O0 (OO00O0O00000000OO )
        O0OOOOO00O0O00000 .__O0OOOO0000OOOOOOO ('添加站点【'+OOO00O00000000O0O .siteName +'】CDN-Header【'+OOO00O00000000O0O .cdn_header +'】');
        return public .returnMsg (True ,'添加成功!');
    def remove_site_cdn_header (O0000O0OOOO00OOO0 ,O00O0000O0000OO00 ):
        OO000000OOO0O00O0 =O0000O0OOOO00OOO0 .get_site_config (None )
        O00O0000O0000OO00 .cdn_header =O00O0000O0000OO00 .cdn_header .strip ().lower ();
        if not O00O0000O0000OO00 .cdn_header in OO000000OOO0O00O0 [O00O0000O0000OO00 .siteName ]['cdn_header']:return public .returnMsg (False ,'指定请求头不存在!');
        for O00OO0O00000O00OO in range (len (OO000000OOO0O00O0 [O00O0000O0000OO00 .siteName ]['cdn_header'])):
            if O00O0000O0000OO00 .cdn_header ==OO000000OOO0O00O0 [O00O0000O0000OO00 .siteName ]['cdn_header'][O00OO0O00000O00OO ]:
                O0000O0OOOO00OOO0 .__O0OOOO0000OOOOOOO ('删除站点【'+O00O0000O0000OO00 .siteName +'】CDN-Header【'+OO000000OOO0O00O0 [O00O0000O0000OO00 .siteName ]['cdn_header'][O00OO0O00000O00OO ]+'】');
                del (OO000000OOO0O00O0 [O00O0000O0000OO00 .siteName ]['cdn_header'][O00OO0O00000O00OO ])
                break ;
        O0000O0OOOO00OOO0 .__OO000O00OOO0OO0O0 (OO000000OOO0O00O0 )
        return public .returnMsg (True ,'删除成功!');
    def get_site_rule (OO00OO0OOO00O000O ,O000000OOO00OOO0O ):
        O0O0OO0OOO0000O00 =OO00OO0OOO00O000O .get_site_config (None )
        return O0O0OO0OOO0000O00 [O000000OOO00OOO0O .siteName ][O000000OOO00OOO0O .ruleName ]
    def add_site_rule (OO00OO00O0OO0OO00 ,OO0OO0OO000OOOOOO ):
        O0OO0OOO00O0000OO =OO00OO00O0OO0OO00 .get_site_config (None )
        if not OO0OO0OO000OOOOOO .ruleName in O0OO0OOO00O0000OO [OO0OO0OO000OOOOOO .siteName ]:return public .returnMsg (False ,'指定规则不存在!');
        OO0O0OOOO0OO0000O =type (O0OO0OOO00O0000OO [OO0OO0OO000OOOOOO .siteName ][OO0OO0OO000OOOOOO .ruleName ])
        if OO0O0OOOO0OO0000O ==bool :return public .returnMsg (False ,'指定规则不存在!');
        if OO0O0OOOO0OO0000O ==str :O0OO0OOO00O0000OO [OO0OO0OO000OOOOOO .siteName ][OO0OO0OO000OOOOOO .ruleName ]=OO0OO0OO000OOOOOO .ruleValue 
        if OO0O0OOOO0OO0000O ==list :
            if OO0OO0OO000OOOOOO .ruleName =='url_rule'or OO0OO0OO000OOOOOO .ruleName =='url_tell':
                for O0OOOO00000000OOO in O0OO0OOO00O0000OO [OO0OO0OO000OOOOOO .siteName ][OO0OO0OO000OOOOOO .ruleName ]:
                    if O0OOOO00000000OOO [0 ]==OO0OO0OO000OOOOOO .ruleUri :return public .returnMsg (False ,'指定URI已存在!');
                OOO0OO0O0O0OOO0O0 =[]
                OOO0OO0O0O0OOO0O0 .append (OO0OO0OO000OOOOOO .ruleUri )
                OOO0OO0O0O0OOO0O0 .append (OO0OO0OO000OOOOOO .ruleValue )
                if OO0OO0OO000OOOOOO .ruleName =='url_tell':
                    OO00OO00O0OO0OO00 .__O0OOOO0000OOOOOOO ('添加站点【'+OO0OO0OO000OOOOOO .siteName +'】URI【'+OO0OO0OO000OOOOOO .ruleUri +'】保护规则,参数【'+OO0OO0OO000OOOOOO .ruleValue +'】,参数值【'+OO0OO0OO000OOOOOO .rulePass +'】');
                    OOO0OO0O0O0OOO0O0 .append (OO0OO0OO000OOOOOO .rulePass )
                else :
                    OO00OO00O0OO0OO00 .__O0OOOO0000OOOOOOO ('添加站点【'+OO0OO0OO000OOOOOO .siteName +'】URI【'+OO0OO0OO000OOOOOO .ruleUri +'】过滤规则【'+OO0OO0OO000OOOOOO .ruleValue +'】');
                O0OO0OOO00O0000OO [OO0OO0OO000OOOOOO .siteName ][OO0OO0OO000OOOOOO .ruleName ].insert (0 ,OOO0OO0O0O0OOO0O0 )
            else :
                if OO0OO0OO000OOOOOO .ruleValue in O0OO0OOO00O0000OO [OO0OO0OO000OOOOOO .siteName ][OO0OO0OO000OOOOOO .ruleName ]:return public .returnMsg (False ,'指定规则已存在!');
                O0OO0OOO00O0000OO [OO0OO0OO000OOOOOO .siteName ][OO0OO0OO000OOOOOO .ruleName ].insert (0 ,OO0OO0OO000OOOOOO .ruleValue )
                OO00OO00O0OO0OO00 .__O0OOOO0000OOOOOOO ('添加站点【'+OO0OO0OO000OOOOOO .siteName +'】【'+OO0OO0OO000OOOOOO .ruleName +'】过滤规则【'+OO0OO0OO000OOOOOO .ruleValue +'】');
        OO00OO00O0OO0OO00 .__OO000O00OOO0OO0O0 (O0OO0OOO00O0000OO )
        return public .returnMsg (True ,'添加成功!');
    def remove_site_rule (OOOOOO0OO0O00O0O0 ,O0OOO0O0000000OO0 ):
        OOO0000OO0OO00OO0 =OOOOOO0OO0O00O0O0 .get_site_config (None )
        O0O0OO0OOO0OOOOO0 =int (O0OOO0O0000000OO0 .index )
        if not O0OOO0O0000000OO0 .ruleName in OOO0000OO0OO00OO0 [O0OOO0O0000000OO0 .siteName ]:return public .returnMsg (False ,'指定规则不存在!');
        O0O0O0O0OO0O00OOO =OOO0000OO0OO00OO0 [O0OOO0O0000000OO0 .siteName ][O0OOO0O0000000OO0 .ruleName ][O0O0OO0OOO0OOOOO0 ]
        del (OOO0000OO0OO00OO0 [O0OOO0O0000000OO0 .siteName ][O0OOO0O0000000OO0 .ruleName ][O0O0OO0OOO0OOOOO0 ])
        OOOOOO0OO0O00O0O0 .__OO000O00OOO0OO0O0 (OOO0000OO0OO00OO0 )
        OOOOOO0OO0O00O0O0 .__O0OOOO0000OOOOOOO ('删除站点【'+O0OOO0O0000000OO0 .siteName +'】【'+O0OOO0O0000000OO0 .ruleName +'】过滤规则【'+json .dumps (O0O0O0O0OO0O00OOO )+'】');
        return public .returnMsg (True ,'删除成功!');
    def get_rule (OOOOOO0OO0O00O0OO ,OO0000OOO00OO00O0 ):
        O00O000O00OOO0OOO =OOOOOO0OO0O00O0OO .__O0000000OO00000O0 (OO0000OOO00OO00O0 .ruleName )
        if not O00O000O00OOO0OOO :return [];
        return O00O000O00OOO0OOO 
    def add_rule (O0000O00OOO0O000O ,OOOO00OOOOOO0OOOO ):
        O00OO0OO00O000OO0 =O0000O00OOO0O000O .__O0000000OO00000O0 (OOOO00OOOOOO0OOOO .ruleName )
        O0O0OO0OO00OO0OOO =[1 ,OOOO00OOOOOO0OOOO .ruleValue .strip (),OOOO00OOOOOO0OOOO .ps ,1 ]
        for OO0OOOO000O00OO00 in O00OO0OO00O000OO0 :
            if OO0OOOO000O00OO00 [1 ]==O0O0OO0OO00OO0OOO [1 ]:return public .returnMsg (False ,'指定规则已存在，请勿重复添加');
        O00OO0OO00O000OO0 .append (O0O0OO0OO00OO0OOO )
        O0000O00OOO0O000O .__O0O00O0O0O0O0O000 (OOOO00OOOOOO0OOOO .ruleName ,O00OO0OO00O000OO0 )
        O0000O00OOO0O000O .__O0OOOO0000OOOOOOO ('添加全局规则【'+OOOO00OOOOOO0OOOO .ruleName +'】【'+OOOO00OOOOOO0OOOO .ps +'】');
        return public .returnMsg (True ,'添加成功!');
    def remove_rule (OOOO000O0O0O0O0O0 ,O0OOOOOOOOOO000O0 ):
        O00OO0O0000OO0O0O =OOOO000O0O0O0O0O0 .__O0000000OO00000O0 (O0OOOOOOOOOO000O0 .ruleName )
        OOO00OOO0000OOOO0 =int (O0OOOOOOOOOO000O0 .index )
        OOOOOOO0OO0O00OOO =O00OO0O0000OO0O0O [OOO00OOO0000OOOO0 ][2 ]
        del (O00OO0O0000OO0O0O [OOO00OOO0000OOOO0 ])
        OOOO000O0O0O0O0O0 .__O0O00O0O0O0O0O000 (O0OOOOOOOOOO000O0 .ruleName ,O00OO0O0000OO0O0O )
        OOOO000O0O0O0O0O0 .__O0OOOO0000OOOOOOO ('删除全局规则【'+O0OOOOOOOOOO000O0 .ruleName +'】【'+OOOOOOO0OO0O00OOO +'】');
        return public .returnMsg (True ,'删除成功!');
    def modify_rule (OOO00OOO0OOOOOO00 ,OOO0O0O0000000000 ):
        O0O000OO0000O0O00 =OOO00OOO0OOOOOO00 .__O0000000OO00000O0 (OOO0O0O0000000000 .ruleName )
        O000OO0000O0OO0OO =int (OOO0O0O0000000000 .index )
        O0O000OO0000O0O00 [O000OO0000O0OO0OO ][1 ]=OOO0O0O0000000000 .ruleBody 
        O0O000OO0000O0O00 [O000OO0000O0OO0OO ][2 ]=OOO0O0O0000000000 .rulePs 
        OOO00OOO0OOOOOO00 .__O0O00O0O0O0O0O000 (OOO0O0O0000000000 .ruleName ,O0O000OO0000O0O00 )
        OOO00OOO0OOOOOO00 .__O0OOOO0000OOOOOOO ('修改全局规则【'+OOO0O0O0000000000 .ruleName +'】【'+OOO0O0O0000000000 .rulePs +'】');
        return public .returnMsg (True ,'修改成功!');
    def set_rule_state (OO00O0O0OO000O000 ,O00O0000000O0000O ):
        O00OOO00OOO0OO000 =OO00O0O0OO000O000 .__O0000000OO00000O0 (O00O0000000O0000O .ruleName )
        O0O0000O00OO0000O =int (O00O0000000O0000O .index )
        if O00OOO00OOO0OO000 [O0O0000O00OO0000O ][0 ]==0 :
            O00OOO00OOO0OO000 [O0O0000O00OO0000O ][0 ]=1 ;
        else :
            O00OOO00OOO0OO000 [O0O0000O00OO0000O ][0 ]=0 ;
        OO00O0O0OO000O000 .__O0O00O0O0O0O0O000 (O00O0000000O0000O .ruleName ,O00OOO00OOO0OO000 )
        OO00O0O0OO000O000 .__O0OOOO0000OOOOOOO (OO00O0O0OO000O000 .__O0OO0O0O000O0OOOO [O00OOO00OOO0OO000 [O0O0000O00OO0000O ][0 ]]+'全局规则【'+O00O0000000O0000O .ruleName +'】【'+O00OOO00OOO0OO000 [O0O0000O00OO0000O ][2 ]+'】');
        return public .returnMsg (True ,'设置成功!');
    def get_site_disable_rule (OO0O00O000OOOO0O0 ,O00000O00000OOO00 ):
        OO0OOO0000OO0OO00 =OO0O00O000OOOO0O0 .__O0000000OO00000O0 (O00000O00000OOO00 .ruleName )
        OO0O000OOO0OOOO00 =OO0O00O000OOOO0O0 .get_site_config (None )
        OOOO0O0O0O00O00O0 =OO0O000OOO0OOOO00 [O00000O00000OOO00 .siteName ]['disable_rule'][O00000O00000OOO00 .ruleName ]
        for O00O000O000OO0OOO in range (len (OO0OOO0000OO0OO00 )):
            if OO0OOO0000OO0OO00 [O00O000O000OO0OOO ][0 ]==0 :OO0OOO0000OO0OO00 [O00O000O000OO0OOO ][0 ]=-1 ;
            if O00O000O000OO0OOO in OOOO0O0O0O00O00O0 :OO0OOO0000OO0OO00 [O00O000O000OO0OOO ][0 ]=0 ;
        return OO0OOO0000OO0OO00 ;
    def set_site_disable_rule (O00OOO0OO0O00O0OO ,O0OOOOO0OO00O0O0O ):
        O00O0O00000OOO0O0 =O00OOO0OO0O00O0OO .get_site_config (None )
        OO0O00O0OOO000OOO =int (O0OOOOO0OO00O0O0O .index )
        if OO0O00O0OOO000OOO in O00O0O00000OOO0O0 [O0OOOOO0OO00O0O0O .siteName ]['disable_rule'][O0OOOOO0OO00O0O0O .ruleName ]:
            for OOOO0OOO00O0OO00O in range (len (O00O0O00000OOO0O0 [O0OOOOO0OO00O0O0O .siteName ]['disable_rule'][O0OOOOO0OO00O0O0O .ruleName ])):
                if OO0O00O0OOO000OOO ==O00O0O00000OOO0O0 [O0OOOOO0OO00O0O0O .siteName ]['disable_rule'][O0OOOOO0OO00O0O0O .ruleName ][OOOO0OOO00O0OO00O ]:
                    del (O00O0O00000OOO0O0 [O0OOOOO0OO00O0O0O .siteName ]['disable_rule'][O0OOOOO0OO00O0O0O .ruleName ][OOOO0OOO00O0OO00O ])
                    break 
        else :
            O00O0O00000OOO0O0 [O0OOOOO0OO00O0O0O .siteName ]['disable_rule'][O0OOOOO0OO00O0O0O .ruleName ].append (OO0O00O0OOO000OOO )
        O00OOO0OO0O00O0OO .__O0OOOO0000OOOOOOO ('设置站点【'+O0OOOOO0OO00O0O0O .siteName +'】应用规则【'+O0OOOOO0OO00O0O0O .ruleName +'】状态');
        O00OOO0OO0O00O0OO .__OO000O00OOO0OO0O0 (O00O0O00000OOO0O0 )
        return public .returnMsg (True ,'设置成功!');
    def get_safe_logs (O00OO0OO000O00OO0 ,O00O00OO00O0OO000 ):
        try :
            import cgi 
            OO0O0OO0O0OO0OOOO =sys .version_info [0 ]
            if 'drop_ip'in O00O00OO00O0OO000 :
                OOOO00000O0OO0OOO ='/www/server/btwaf/drop_ip.log';
                OO00000OOO0O00O00 =14 ;
            else :
                OOOO00000O0OO0OOO ='/www/wwwlogs/btwaf/'+O00O00OO00O0OO000 .siteName +'_'+O00O00OO00O0OO000 .toDate +'.log';
                OO00000OOO0O00O00 =10 ;
            if not os .path .exists (OOOO00000O0OO0OOO ):return [];
            O00000O00OOO0O0O0 =1 ;
            if 'p'in O00O00OO00O0OO000 :
                O00000O00OOO0O0O0 =int (O00O00OO00O0OO000 .p );
            O0OOO000O0O00O0O0 =(O00000O00OOO0O0O0 -1 )*OO00000OOO0O00O00 ;
            O00O00OO00000OO0O =O0OOO000O0O00O0O0 +OO00000OOO0O00O00 ;
            OO0OO0O0OO0000OO0 =open (OOOO00000O0OO0OOO ,'rb')
            OO0000O0O0000O0OO =""
            try :
                OO0OO0O0OO0000OO0 .seek (-1 ,2 )
            except :
                return []
            if OO0OO0O0OO0000OO0 .read (1 )=="\n":OO0OO0O0OO0000OO0 .seek (-1 ,2 )
            OOO0OOOOOOOO0O00O =[]
            O0O0OO0O0O000OOO0 =True 
            O000OOOOO0O0OO000 =0 ;
            for OO000OO0000OO0000 in range (O00O00OO00000OO0O ):
                while True :
                    O0OOO00OO00OOOO0O =str .rfind (OO0000O0O0000O0OO ,"\n")
                    O0OO0OOOO00OO0O0O =OO0OO0O0OO0000OO0 .tell ()
                    if O0OOO00OO00OOOO0O !=-1 :
                        if O000OOOOO0O0OO000 >=O0OOO000O0O00O0O0 :
                            OOO0000OOOO0OO0O0 =OO0000O0O0000O0OO [O0OOO00OO00OOOO0O +1 :]
                            try :
                                OOO0OOOOOOOO0O00O .append (json .loads (cgi .escape (OOO0000OOOO0OO0O0 )))
                            except :
                                pass 
                        OO0000O0O0000O0OO =OO0000O0O0000O0OO [:O0OOO00OO00OOOO0O ]
                        O000OOOOO0O0OO000 +=1 ;
                        break ;
                    else :
                        if O0OO0OOOO00OO0O0O ==0 :
                            O0O0OO0O0O000OOO0 =False 
                            break 
                        O00O0OO00O0OO0OOO =min (4096 ,O0OO0OOOO00OO0O0O )
                        OO0OO0O0OO0000OO0 .seek (-O00O0OO00O0OO0OOO ,1 )
                        OO00O00O0OO0OO00O =OO0OO0O0OO0000OO0 .read (O00O0OO00O0OO0OOO )
                        if OO0O0OO0O0OO0OOOO ==3 :OO00O00O0OO0OO00O =OO00O00O0OO0OO00O .decode ('utf-8')
                        OO0000O0O0000O0OO =OO00O00O0OO0OO00O +OO0000O0O0000O0OO 
                        OO0OO0O0OO0000OO0 .seek (-O00O0OO00O0OO0OOO ,1 )
                        if O0OO0OOOO00OO0O0O -O00O0OO00O0OO0OOO ==0 :
                            OO0000O0O0000O0OO ="\n"+OO0000O0O0000O0OO 
                if not O0O0OO0O0O000OOO0 :break ;
            OO0OO0O0OO0000OO0 .close ()
            if 'drop_ip'in O00O00OO00O0OO000 :
                OO000000000OO0O0O =O00OO0OO000O00OO0 .get_waf_drop_ip (None )
                OO00000000O000O00 =time .time ()
                O0OO0000O00OO0OO0 =[]
                for OO000OO0000OO0000 in range (len (OOO0OOOOOOOO0O00O )):
                    if (OO00000000O000O00 -OOO0OOOOOOOO0O00O [OO000OO0000OO0000 ][0 ])<OOO0OOOOOOOO0O00O [OO000OO0000OO0000 ][4 ]and not OOO0OOOOOOOO0O00O [OO000OO0000OO0000 ][1 ]in O0OO0000O00OO0OO0 :
                        O0OO0000O00OO0OO0 .append (OOO0OOOOOOOO0O00O [OO000OO0000OO0000 ][1 ])
                        OOO0OOOOOOOO0O00O [OO000OO0000OO0000 ].append (OOO0OOOOOOOO0O00O [OO000OO0000OO0000 ][1 ]in OO000000000OO0O0O )
                    else :
                        OOO0OOOOOOOO0O00O [OO000OO0000OO0000 ].append (False )
        except :
            OOO0OOOOOOOO0O00O =[]
        return OOO0OOOOOOOO0O00O 
    def get_logs_list (O0OO0OO00OO00OOO0 ,O000OO00000O00O0O ):
        OO00O000O0OOOO0O0 ='/www/wwwlogs/btwaf/'
        O00OO0OO00000O000 =O000OO00000O00O0O .siteName +'_'
        O00O00OO0OOO00O00 =[]
        for OOOO00OOO0000O00O in os .listdir (OO00O000O0OOOO0O0 ):
            if OOOO00OOO0000O00O .find (O00OO0OO00000O000 )!=0 :continue ;
            O0O0O00O00O0OO0OO =OOOO00OOO0000O00O .replace (O00OO0OO00000O000 ,'').replace ('.log','')
            O00O00OO0OOO00O00 .append (O0O0O00O00O0OO0OO )
        return sorted (O00O00OO0OOO00O00 ,reverse =True );
    def stop (OO000OOO0000O00OO ):
        return;
    def get_waf_drop_ip (OO0O00O0O0O0O00O0 ,OO0OO0OOO0OOO0O0O ):
        try :
            return json .loads (public .httpGet ('http://127.0.0.1/get_btwaf_drop_ip'))
        except :
            return [];
    def remove_waf_drop_ip (O0OO00O0OOO00O00O ,O0000O00O0OO0OO00 ):
        try :
            O0O0O000O00OOO00O =json .loads (public .httpGet ('http://127.0.0.1/remove_btwaf_drop_ip?ip='+O0000O00O0OO0OO00 .ip ))
            O0OO00O0OOO00O00O .__O0OOOO0000OOOOOOO ('从防火墙解封IP【'+O0000O00O0OO0OO00 .ip +'】');
            return O0O0O000O00OOO00O 
        except :
            return public .returnMsg (False ,'获取数据失败');
    def clean_waf_drop_ip (OOOO0O00OO0OO00O0 ,OOOOOO0OO0000OOO0 ):
        try :
            return json .loads (public .httpGet ('http://127.0.0.1/clean_btwaf_drop_ip'))
            OOOO0O00OO0OO00O0 .__O0OOOO0000OOOOOOO ('从防火墙解封所有IP');
        except :
            return public .returnMsg (False ,'获取数据失败');
    def get_gl_logs (O0000O000O00O0OOO ,O00OOOOO0OOO00OO0 ):
        import page 
        page =page .Page ();
        OO0O0O000OOOO0O0O =public .M ('logs').where ('type=?',(u'网站防火墙',)).count ();
        OOOO000OOO0O00000 =12 ;
        OOO000OO0OOO0OOOO ={}
        OOO000OO0OOO0OOOO ['count']=OO0O0O000OOOO0O0O 
        OOO000OO0OOO0OOOO ['row']=OOOO000OOO0O00000 
        OOO000OO0OOO0OOOO ['p']=1 
        if hasattr (O00OOOOO0OOO00OO0 ,'p'):
            OOO000OO0OOO0OOOO ['p']=int (O00OOOOO0OOO00OO0 ['p'])
        OOO000OO0OOO0OOOO ['uri']=O00OOOOO0OOO00OO0 
        OOO000OO0OOO0OOOO ['return_js']=''
        if hasattr (O00OOOOO0OOO00OO0 ,'tojs'):
            OOO000OO0OOO0OOOO ['return_js']=O00OOOOO0OOO00OO0 .tojs 
        O0O000000OO0O0000 ={}
        O0O000000OO0O0000 ['page']=page .GetPage (OOO000OO0OOO0OOOO ,'1,2,3,4,5,8');
        O0O000000OO0O0000 ['data']=public .M ('logs').where ('type=?',(u'网站防火墙',)).order ('id desc').limit (str (page .SHIFT )+','+str (page .ROW )).field ('log,addtime').select ();
        return O0O000000OO0O0000 ;
    def get_total (O0O0O0000O0000OOO ,OO000O00O0OO00000 ):
        try :
            O0O0OOO0OOO0O00OO =json .loads (public .readFile (O0O0O0000O0000OOO .__O00O00O0OO0O00O0O +'total.json'))
        except :
            O0O0OOO0OOO0O00OO ={"rules":{"user_agent":0 ,"cookie":0 ,"post":0 ,"args":0 ,"url":0 ,"cc":0 },"sites":{},"total":0 }
            O0O0O0000O0000OOO .__OOO0OO0000000OOO0 (O0O0OOO0OOO0O00OO );
        if type (O0O0OOO0OOO0O00OO ['rules'])!=dict :
            O0O0OO000OOO0OO00 ={}
            for OO0O00O0000O0O0O0 in O0O0OOO0OOO0O00OO ['rules']:
                O0O0OO000OOO0OO00 [OO0O00O0000O0O0O0 ['key']]=OO0O00O0000O0O0O0 ['value'];
            O0O0OOO0OOO0O00OO ['rules']=O0O0OO000OOO0OO00 ;
            O0O0O0000O0000OOO .__OOO0OO0000000OOO0 (O0O0OOO0OOO0O00OO );
        O0O0OOO0OOO0O00OO ['rules']=O0O0O0000O0000OOO .__O0O0OOOO00OOOO0O0 (O0O0OOO0OOO0O00OO ['rules'])
        return O0O0OOO0OOO0O00OO ;
    def __O0O0OOOO00OOOO0O0 (O0O0OOO0O0OOOO00O ,O00OOO0OO0O0O0OOO ):
        O00OOO0OO0O0O0OOO ['get']=0 ;
        if 'args'in O00OOO0OO0O0O0OOO :
            O00OOO0OO0O0O0OOO ['get']+=O00OOO0OO0O0O0OOO ['args'];
            del (O00OOO0OO0O0O0OOO ['args'])
        if 'url'in O00OOO0OO0O0O0OOO :
            O00OOO0OO0O0O0OOO ['get']+=O00OOO0OO0O0O0OOO ['url'];
            del (O00OOO0OO0O0O0OOO ['url'])
        OO0O00O0O00OO0OO0 =[['post',u'POST渗透'],['get',u'GET渗透'],['cc',u"CC攻击"],['user_agent',u'恶意User-Agent'],['cookie',u'Cookie渗透'],['scan',u'恶意扫描'],['head',u'恶意HEAD请求'],['url_rule',u'URI自定义拦截'],['url_tell',u'URI保护'],['disable_upload_ext',u'恶意文件上传'],['disable_ext',u'禁止的扩展名'],['disable_php_path',u'禁止PHP脚本']]
        OOO0O0O0O0O0OO0OO =[]
        for OOO0O000OO00O0O00 in OO0O00O0O00OO0OO0 :
            OOOOO00OOO0OO000O ={}
            OOOOO00OOO0OO000O ['name']=OOO0O000OO00O0O00 [1 ]
            OOOOO00OOO0OO000O ['key']=OOO0O000OO00O0O00 [0 ]
            OOOOO00OOO0OO000O ['value']=0 ;
            if OOO0O000OO00O0O00 [0 ]in O00OOO0OO0O0O0OOO :OOOOO00OOO0OO000O ['value']=O00OOO0OO0O0O0OOO [OOO0O000OO00O0O00 [0 ]]
            OOO0O0O0O0O0OO0OO .append (OOOOO00OOO0OO000O )
        return OOO0O0O0O0O0OO0OO 
    def get_btwaf (O00OO0OO0O0O0OO0O ):
        from BTPanel import session ,cache 
        import panelAuth 
        if 'btwaf'in session :return session ['btwaf']
        O0OO000O0O00O00O0 =public .GetConfigValue ('home')+'/api/panel/get_soft_list'
        OO00000OO0OOOOOOO =panelAuth .panelAuth ().create_serverid (None )
        OOO0OO0OO0O00OO0O =public .httpPost (O0OO000O0O00O00O0 ,OO00000OO0OOOOOOO )
        if not OOO0OO0OO0O00OO0O :
            if not 'btwaf'in session :session ['btwaf']=1 
            return 1 
        try :
            OOO0OO0OO0O00OO0O =json .loads (OOO0OO0OO0O00OO0O )
            for OOOOO0OOO0O000OO0 in OOO0OO0OO0O00OO0O ["list"]:
                if OOOOO0OOO0O000OO0 ['name']=='btwaf':
                    if OOOOO0OOO0O000OO0 ['endtime']>=0 :
                        if not 'btwaf'in session :session ['btwaf']=2 ;
                        return 2 
            return  
        except :
            if not 'btwaf'in session :session ['btwaf']=1 ;
            return 1 
    def get_total_all (O00OO000OO0OOO0OO ,OO0OOOO000O0000OO ):
        from BTPanel import session 
        if not 'zhizu'in session :
            O00OO000OO0OOO0OO .get_zhizu_ip_list ()
        from BTPanel import session ,cache 
        if not 'btwaf'in session :
            O0OOOO0OOO00OOO0O =O00OO000OO0OOO0OO .get_btwaf ()
            if O0OOOO0OOO00OOO0O ==0 :
                O00OO000OO0OOO0OO .stop ()
                return public .returnMsg (False ,'恭喜你发现彩蛋了,出现这个提示说明破解失败~~')
        O00OO000OO0OOO0OO .__OOO0OOOO000OOO00O ()
        O0O00O0OOO000O000 ='/www/server/nginx/conf/nginx.conf'
        if not os .path .exists (O0O00O0OOO000O000 ):return public .returnMsg (False ,'只支持nginx服务器');
        if public .readFile (O0O00O0OOO000O000 ).find ('luawaf.conf')==-1 :return public .returnMsg (False ,'当前nginx不支持防火墙,请重装nginx');
        O0000000O0O0OOOOO ={}
        O0000000O0O0OOOOO ['total']=O00OO000OO0OOO0OO .get_total (None )
        del (O0000000O0O0OOOOO ['total']['sites'])
        O0000000O0O0OOOOO ['drop_ip']=[]
        O0000000O0O0OOOOO ['open']=O00OO000OO0OOO0OO .get_config (None )['open']
        O0OO00OO000O0000O =O00OO000OO0OOO0OO .get_config (None )
        O0000000O0O0OOOOO ['safe_day']=0 
        if 'start_time'in O0OO00OO000O0000O :
            if O0OO00OO000O0000O ['start_time']!=0 :O0000000O0O0OOOOO ['safe_day']=int ((time .time ()-O0OO00OO000O0000O ['start_time'])/86400 )
        O00OO000OO0OOO0OO .__O0OOO00OOOO0O0O00 ()
        return O0000000O0O0OOOOO 
    def __O0OOO00OOOO0O0O00 (O00O000000O00000O ):
        O0O0OOOO0O00000O0 =public .M ('sites').field ('name,id,path').select ();
        O0000OOO0000000O0 =[]
        for O00OO00OO0000000O in O0O0OOOO0O00000O0 :
            O0O000OOO0OOO0000 ={}
            O0O000OOO0OOO0000 ['name']=O00OO00OO0000000O ['name']
            O0O000OOO0OOO0000 ['path']=O00OO00OO0000000O ['path']
            O0O0O0O0O00OOO0OO =0 
            OO00O0OO000OO0OO0 =[]
            if os .path .exists (O00O000000O00000O .__O00O00O0OO0O00O0O +'/cms.json'):
                OO00OO00OOO00OOOO =json .loads (public .ReadFile (O00O000000O00000O .__O00O00O0OO0O00O0O +'cms.json'))
                O00O000000O00000O .__OOOOO0OO0OOO0OO0O =OO00OO00OOO00OOOO 
            for OO0O00OOO00O00OO0 in O00O000000O00000O .__OOOOO0OO0OOO0OO0O :
                for OOO0O0OOOOOOO0O00 in O00O000000O00000O .__OOOOO0OO0OOO0OO0O [OO0O00OOO00O00OO0 ]:
                    if os .path .exists (O00OO00OO0000000O ['path']+str (OOO0O0OOOOOOO0O00 )):
                        O0O0O0O0O00OOO0OO +=1 
                        if O0O0O0O0O00OOO0OO >=2 :
                            O0O0O0O0O00OOO0OO =0 
                            O0O000OOO0OOO0000 ['cms']=OO0O00OOO00O00OO0 
                            break 
            if not 'cms'in O0O000OOO0OOO0000 :
                O0O000OOO0OOO0000 ['cms']=0 
            O0O0O0OOOO00OO0OO =public .M ('domain').where ('pid=?',(O00OO00OO0000000O ['id'],)).field ('name').select ()
            O0O000OOO0OOO0000 ['domains']=[]
            for O000OOO000000OOO0 in O0O0O0OOOO00OO0OO :
                O0O000OOO0OOO0000 ['domains'].append (O000OOO000000OOO0 ['name'])
            O000O00O00O0OO0O0 =public .M ('binding').where ('pid=?',(O00OO00OO0000000O ['id'],)).field ('domain').select ()
            for O000OOO000000OOO0 in O000O00O00O0OO0O0 :
                O0O000OOO0OOO0000 ['domains'].append (O000OOO000000OOO0 ['domain'])
            O0000OOO0000000O0 .append (O0O000OOO0OOO0000 )
            if os .path .exists (O00O000000O00000O .__O00O00O0OO0O00O0O +'/domains2.json'):
                OO0O0OO000OO0OOOO =json .loads (public .ReadFile (O00O000000O00000O .__O00O00O0OO0O00O0O +'/domains2.json'))
                if not O0O000OOO0OOO0000 in OO0O0OO000OO0OOOO :
                    for OO0O00OOO00O00OO0 in OO0O0OO000OO0OOOO :
                        if OO0O00OOO00O00OO0 ["name"]==O0O000OOO0OOO0000 ["name"]:
                            if OO0O00OOO00O00OO0 ["cms"]==O0O000OOO0OOO0000 ["cms"]:
                                OO0O00OOO00O00OO0 ["domains"]=O0O000OOO0OOO0000 ["domains"]
                                OO0O00OOO00O00OO0 ["path"]=O0O000OOO0OOO0000 ["path"]
                            else :
                                if 'is_chekc'in OO0O00OOO00O00OO0 :
                                    OO0O00OOO00O00OO0 ["domains"]=O0O000OOO0OOO0000 ["domains"]
                                    OO0O00OOO00O00OO0 ["path"]=O0O000OOO0OOO0000 ["path"]
                                else :
                                    OO0O00OOO00O00OO0 ["cms"]=O0O000OOO0OOO0000 ["cms"]
                                    OO0O00OOO00O00OO0 ["domains"]=O0O000OOO0OOO0000 ["domains"]
                                    OO0O00OOO00O00OO0 ["path"]=O0O000OOO0OOO0000 ["path"]
                    else :
                        O0O0O0O0O00OOO0OO =0 
                        if not O0O000OOO0OOO0000 in OO0O0OO000OO0OOOO :
                            for OO0O00OOO00O00OO0 in OO0O0OO000OO0OOOO :
                                if OO0O00OOO00O00OO0 ["name"]==O0O000OOO0OOO0000 ["name"]:
                                    O0O0O0O0O00OOO0OO =1 
                            if not O0O0O0O0O00OOO0OO ==1 :
                                OO0O0OO000OO0OOOO .append (O0O000OOO0OOO0000 )
                public .writeFile (O00O000000O00000O .__O00O00O0OO0O00O0O +'/domains2.json',json .dumps (OO0O0OO000OO0OOOO ))
        if not os .path .exists (O00O000000O00000O .__O00O00O0OO0O00O0O +'/domains2.json'):
            public .writeFile (O00O000000O00000O .__O00O00O0OO0O00O0O +'/domains2.json',json .dumps (O0000OOO0000000O0 ))
        public .writeFile (O00O000000O00000O .__O00O00O0OO0O00O0O +'/domains.json',json .dumps (O0000OOO0000000O0 ))
        return O0000OOO0000000O0 
    def sync_cnlist (OOOO0OOOOOOO00OO0 ,O0OOO0O00O0O000OO ):
        if not O0OOO0O00O0O000OO :
            OOOO0OOOOOOO00OO0 .get_config (None )
            OOOO0OOOOOOO00OO0 .get_site_config (None )
        O0OOO00O000OOOOO0 =public .httpGet (public .get_url ()+'/cnlist.json')
        if not O0OOO00O000OOOOO0 :return public .returnMsg (False ,'连接云端失败')
        OOOOO0O0O00O0OO00 =json .loads (O0OOO00O000OOOOO0 )
        OO00O0O0O0O00O000 =OOOO0OOOOOOO00OO0 .__O0000000OO00000O0 ('cn')
        O0O00OO00O0OO0O0O =0 
        for OOOOOOOOOO0O0O0OO in OOOOO0O0O00O0OO00 :
            if OOOOOOOOOO0O0O0OO in OO00O0O0O0O00O000 :continue ;
            OO00O0O0O0O00O000 .append (OOOOOOOOOO0O0O0OO )
            O0O00OO00O0OO0O0O +=1 
        OOOO0OOOOOOO00OO0 .__O0O00O0O0O0O0O000 ('cn',OO00O0O0O0O00O000 )
        print ('同步成功，本次共增加 '+str (O0O00OO00O0OO0O0O )+' 个IP段');
        if O0OOO0O00O0O000OO :return public .returnMsg (True ,'同步成功!');
    def __OOO0OOO0O0O0OO0OO (O00OOOOOOO0000O00 ):
        OO00O00O0000000OO =public .M ('crontab').where ('name=?',(u'宝塔网站防火墙自动同步中国IP库',)).getField ('id');
        import crontab 
        if OO00O00O0000000OO :crontab .crontab ().DelCrontab ({'id':OO00O00O0000000OO })
        O0O0000O0O000OOO0 ={}
        O0O0000O0O000OOO0 ['name']=u'宝塔网站防火墙自动同步中国IP库'
        O0O0000O0O000OOO0 ['type']='day'
        O0O0000O0O000OOO0 ['where1']=''
        O0O0000O0O000OOO0 ['sBody']='python /www/server/panel/plugin/btwaf/btwaf_main.py 1111'
        O0O0000O0O000OOO0 ['backupTo']='localhost'
        O0O0000O0O000OOO0 ['sType']='toShell'
        O0O0000O0O000OOO0 ['hour']='5'
        O0O0000O0O000OOO0 ['minute']='30'
        O0O0000O0O000OOO0 ['week']=''
        O0O0000O0O000OOO0 ['sName']=''
        O0O0000O0O000OOO0 ['urladdress']=''
        O0O0000O0O000OOO0 ['save']=''
        crontab .crontab ().AddCrontab (O0O0000O0O000OOO0 )
        return public .returnMsg (True ,'设置成功!');
    def __O0000000OO00000O0 (OOOOO000O0O000OOO ,O0000O0OOO00OOO00 ):
        O0O000O00O00000OO =OOOOO000O0O000OOO .__O00O00O0OO0O00O0O +'rule/'+O0000O0OOO00OOO00 +'.json';
        OOO0OOO0OOOO000O0 =public .readFile (O0O000O00O00000OO )
        if not OOO0OOO0OOOO000O0 :return False 
        return json .loads (OOO0OOO0OOOO000O0 )
    def __O0O00O0O0O0O0O000 (OOO000OO0O0O00000 ,O0OOO0OOO00OO0O00 ,O0O0O0OOOOO0O00OO ):
        OOOOO000OO00OOO00 =OOO000OO0O0O00000 .__O00O00O0OO0O00O0O +'rule/'+O0OOO0OOO00OO0O00 +'.json';
        public .writeFile (OOOOO000OO00OOO00 ,json .dumps (O0O0O0OOOOO0O00OO ))
        public .serviceReload ();
    def __OOOOOO0OO0O0OOO00 (O0OOOOO0O0O000OOO ,OO0OOOOO0OOO0OOOO ):
        OOOOO00O0000O0O0O =public .M ('sites').field ('name').select ();
        if type (OOOOO00O0000O0O0O )!=list :return ;
        O000O0OO0OO000000 =[]
        OOOO0O000O0OOOO0O =0 
        for O0000OO00000OOOO0 in OOOOO00O0000O0O0O :
            O000O0OO0OO000000 .append (O0000OO00000OOOO0 ['name'])
            if O0000OO00000OOOO0 ['name']in OO0OOOOO0OOO0OOOO :continue 
            OO0OOOOO0OOO0OOOO [O0000OO00000OOOO0 ['name']]=O0OOOOO0O0O000OOO .__O0O00O00OO0O0O00O ()
            OOOO0O000O0OOOO0O +=1 
        O0O0OOOO0000O0000 =OO0OOOOO0OOO0OOOO .copy ()
        for OO000OOO00OOO0O0O in OO0OOOOO0OOO0OOOO .keys ():
            if OO000OOO00OOO0O0O in O000O0OO0OO000000 :
                if not 'retry_cycle'in OO0OOOOO0OOO0OOOO [OO000OOO00OOO0O0O ]:
                    OO0OOOOO0OOO0OOOO [OO000OOO00OOO0O0O ]['retry_cycle']=60 ;
                    OOOO0O000O0OOOO0O +=1 ;
                continue 
            del (O0O0OOOO0000O0000 [OO000OOO00OOO0O0O ])
            O0OOOOO0O0O000OOO .__O000O0OOO0O0O0O0O (OO000OOO00OOO0O0O )
            OOOO0O000O0OOOO0O +=1 
        if OOOO0O000O0OOOO0O >0 :
            OO0OOOOO0OOO0OOOO =O0O0OOOO0000O0000 .copy ()
            O0OOOOO0O0O000OOO .__OO000O00OOO0OO0O0 (OO0OOOOO0OOO0OOOO )
        O00O00O00000OO0OO =O0OOOOO0O0O000OOO .get_config (None )
        OOO000OO000000OOO =os .listdir (O00O00O00000OO0OO ['logs_path'])
        OO00O0O0O000000O0 =time .strftime ('%Y-%m-%d',time .localtime ());
        for OO000OOO00OOO0O0O in O000O0OO0OO000000 :
            OO0OOOOO0OOO0OOOO [OO000OOO00OOO0O0O ]['log_size']=0 ;
            OO0OO00O00000OOO0 =O00O00O00000OO0OO ['logs_path']+'/'+OO000OOO00OOO0O0O +'_'+OO00O0O0O000000O0 +'.log';
            if os .path .exists (OO0OO00O00000OOO0 ):
                OO0OOOOO0OOO0OOOO [OO000OOO00OOO0O0O ]['log_size']=os .path .getsize (OO0OO00O00000OOO0 )
            OOO0OOOOO000OO0OO =[]
            for O00OO00000O0O0000 in OOO000OO000000OOO :
                if O00OO00000O0O0000 .find (OO000OOO00OOO0O0O +'_')==-1 :continue ;
                OOO0OOOOO000OO0OO .append (O00OO00000O0O0000 )
            O00OOO0O000000OO0 =len (OOO0OOOOO000OO0OO )-O00O00O00000OO0OO ['log_save'];
            if O00OOO0O000000OO0 >0 :
                OOO0OOOOO000OO0OO =sorted (OOO0OOOOO000OO0OO )
                for OOO00O0000OO00OOO in range (O00OOO0O000000OO0 ):
                    OOOO0O0OOO0O00000 =O00O00O00000OO0OO ['logs_path']+'/'+OOO0OOOOO000OO0OO [OOO00O0000OO00OOO ];
                    if not os .path .exists (OOOO0O0OOO0O00000 ):continue 
                    os .remove (OOOO0O0OOO0O00000 )
        return OO0OOOOO0OOO0OOOO ;
    def __O0OOOOOOOOO0OO00O (O0O00OOOO0OOO0OO0 ,OOOO000O0OO0O0O0O ):
        for O0O00OO0OOO00O0O0 in range (4 ):
            if OOOO000O0OO0O0O0O [0 ][O0O00OO0OOO00O0O0 ]==OOOO000O0OO0O0O0O [1 ][O0O00OO0OOO00O0O0 ]:continue ;
            if OOOO000O0OO0O0O0O [0 ][O0O00OO0OOO00O0O0 ]<OOOO000O0OO0O0O0O [1 ][O0O00OO0OOO00O0O0 ]:break ;
            return False 
        return True 
    def __O000O00000O0OOOOO (OO00O000O0O0OO00O ,O0OOOOOO000000O00 ):
        O00O0OOOOO0O00OOO =O0OOOOOO000000O00 .split ('.')
        if len (O00O0OOOOO0O00OOO )<4 :return False 
        O00O0OOOOO0O00OOO [0 ]=int (O00O0OOOOO0O00OOO [0 ])
        O00O0OOOOO0O00OOO [1 ]=int (O00O0OOOOO0O00OOO [1 ])
        O00O0OOOOO0O00OOO [2 ]=int (O00O0OOOOO0O00OOO [2 ])
        O00O0OOOOO0O00OOO [3 ]=int (O00O0OOOOO0O00OOO [3 ])
        return O00O0OOOOO0O00OOO ;
    def __O0O00O00OO0O0O00O (O0O000000O0OOO0O0 ):
        if not O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO :O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO =O0O000000O0OOO0O0 .get_config (None )
        O00OO0OOO00O0O0O0 ={'open':True ,'project':'','log':True ,'cdn':False ,'cdn_header':['x-forwarded-for','x-real-ip'],'retry':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['retry'],'retry_cycle':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['retry_cycle'],'retry_time':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['retry_time'],'disable_php_path':['^/images/','^/js/','^/css/','^/upload/','^/static/'],'disable_path':[],'disable_ext':[],'disable_upload_ext':['php','jsp'],'url_white':[],'url_rule':[],'url_tell':[],'disable_rule':{'url':[],'post':[],'args':[],'cookie':[],'user_agent':[]},'cc':{'open':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['cc']['open'],'cycle':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['cc']['cycle'],'limit':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['cc']['limit'],'endtime':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['cc']['endtime']},'get':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['get']['open'],'post':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['post']['open'],'cookie':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['cookie']['open'],'user-agent':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['user-agent']['open'],'scan':O0O000000O0OOO0O0 .__O0OOOOOOO000OO0OO ['scan']['open'],'drop_abroad':False }
        return O00OO0OOO00O0O0O0 
    def return_rule (O00O00OO0OO0OO0O0 ,O00OO0O00OOOOOOO0 ,O0O00O0O0OO0OO000 ):
        for OOO0000OO0OO0OO0O in O0O00O0O0OO0OO000 :
            if not OOO0000OO0OO0OO0O [-1 ]:
                for OO0OO0O00OOO00O00 in O00OO0O00OOOOOOO0 :
                    if OO0OO0O00OOO00O00 not in O0O00O0O0OO0OO000 :
                        O0O00O0O0OO0OO000 .append (OO0OO0O00OOO00O00 )
        return O0O00O0O0OO0OO000 
    def sync_rule (OO0000000O00OO0O0 ,OOO0OO00OO0000000 ):
        O0O0000O00OOO000O =OO0000000O00OO0O0 .get_cms_list ()
        if not O0O0000O00OOO000O :return public .returnMsg (False ,'连接云端失败')
        public .writeFile (OO0000000O00OO0O0 .__O00O00O0OO0O00O0O +'/cms.json',O0O0000O00OOO000O )
        for O00OO0O0000OOO0O0 in OO0000000O00OO0O0 .__O0OO0000000O0O000 :
            OO000OOOO0O0O00OO =O00OO0O0000OOO0O0 .split ('.')[0 ]
            OOO00000OO0O00O00 =public .httpGet (public .get_url ()+'/btwaf_rule/httpd/rule/'+O00OO0O0000OOO0O0 )
            if not OOO00000OO0O00O00 :return public .returnMsg (False ,'连接云端失败')
            O000OOOOOO0O0OOOO =json .loads (OOO00000OO0O00O00 )
            O000OO0OOO0OO00O0 =OO0000000O00OO0O0 .__O0000000OO00000O0 (OO000OOOO0O0O00OO )
            O0O0000O00OOO000O =OO0000000O00OO0O0 .return_rule (O000OOOOOO0O0OOOO ,O000OO0OOO0OO00O0 )
            OO0000000O00OO0O0 .__O0O00O0O0O0O0O000 (OO000OOOO0O0O00OO ,O0O0000O00OOO000O )
        public .ExecShell ("wget -O /tmp/cms.zip %s/btwaf_rule/httpd/cms.zip"%public .get_url ())
        if os .path .exists ('/tmp/cms.zip'):
            public .ExecShell ("mv /www/server/btwaf/cms/ /home && unzip cms.zip -d /www/server/btwaf")
            if not os .path .exists ("/www/server/btwaf/cms/weiqin_post.json"):
                public .ExecShell ("rm -rf /www/server/btwaf/cms/ &&  mv /home/cms/ /www/server/btwaf")
            os .remove ("/tmp/cms.zip")
        return public .returnMsg (True ,'更新成功!')
    def get_cms_list (O000OOO00OO000OO0 ):
        OO000O0O000000O00 =public .httpGet (public .get_url ()+'/btwaf_rule/cms.json')
        if not OO000O0O000000O00 :return False 
        return OO000O0O000000O00 
    def get_site_cms (O0O0O00O0O00O0O0O ,OO0OOOOOO0000OOO0 ):
        OOOO00O0OO00OO0O0 ='/www/server/btwaf/domains2.json'
        if os .path .exists (OOOO00O0OO00OO0O0 ):
            try :
                O0OOOOO00O0OOO00O =json .loads (public .ReadFile (OOOO00O0OO00OO0O0 ))
                return public .returnMsg (True ,O0OOOOO00O0OOO00O )
            except :
                return public .returnMsg (False ,0 )
    def set_site_cms (O0O0O000OO0O0OOOO ,O00OOO0OO0O0000O0 ):
        O00000000O00O00OO ='/www/server/btwaf/domains2.json'
        if os .path .exists (O00000000O00O00OO ):
            try :
                OO000O0OOO00O00OO =json .loads (public .ReadFile (O00000000O00O00OO ))
                for O00O00000OO0O0OO0 in OO000O0OOO00O00OO :
                    if O00O00000OO0O0OO0 ['name']==O00OOO0OO0O0000O0 .name2 :
                        O00O00000OO0O0OO0 ['cms']=O00OOO0OO0O0000O0 .cms 
                        O00O00000OO0O0OO0 ["is_chekc"]="ture"
                public .writeFile (O00000000O00O00OO ,json .dumps (OO000O0OOO00O00OO ))
                return public .returnMsg (True ,'修改成功')
            except :
                return public .returnMsg (False ,'修改失败')
    def __O000O0OOO0O0O0O0O (O0O0O0OOOO0O0O0O0 ,OOOOOO0O000O0O000 ):
        public .ExecShell ('/www/wwwlogs/btwaf/'+OOOOOO0O000O0O000 +'_*.log')
        OOO0OO0O0OOOOOO00 =json .loads (public .readFile (O0O0O0OOOO0O0O0O0 .__O00O00O0OO0O00O0O +'total.json'))
        if OOOOOO0O000O0O000 in OOO0OO0O0OOOOOO00 ['sites']:
            del (OOO0OO0O0OOOOOO00 ['sites'][OOOOOO0O000O0O000 ])
            O0O0O0OOOO0O0O0O0 .__OOO0OO0000000OOO0 (OOO0OO0O0OOOOOO00 )
        return True 
    def __OOO0OO0000000OOO0 (O0000OO0O000OOOO0 ,O0OO0OO00O0OO0O0O ):
        return public .writeFile (O0000OO0O000OOOO0 .__O00O00O0OO0O00O0O +'total.json',json .dumps (O0OO0OO00O0OO0O0O ))
    def __OO0O00OO0O00O00O0 (OO0000OOOO00O00OO ,O00OO00O000000000 ):
        public .writeFile (OO0000OOOO00O00OO .__O00O00O0OO0O00O0O +'config.json',json .dumps (O00OO00O000000000 ))
        public .serviceReload ();
    def __OO000O00OOO0OO0O0 (O000OOOOOOO0OOOO0 ,OO0OOOO000O0O0OOO ):
        public .writeFile (O000OOOOOOO0OOOO0 .__O00O00O0OO0O00O0O +'site.json',json .dumps (OO0OOOO000O0O0OOO ))
        public .serviceReload ();
    def __O0OOOO0000OOOOOOO (O0OOOOOOO0O0000O0 ,O0OOO0000OOO00000 ):
        public .WriteLog ('网站防火墙',O0OOO0000OOO00000 )
    def __OOO0OOOO000OOO00O (O0OOOO00O0OO0OOO0 ):
        OO000O000O000OO00 ='/usr/local/lib/lua/5.1/cjson.so'
        try :
            OO00000O000OOOOO0 =public .to_string ([108 ,115 ,97 ,116 ,116 ,114 ,32 ,46 ,47 ,99 ,108 ,97 ,115 ,115 ,124 ,103 ,114 ,101 ,112 ,32 ,105 ,45 ,45 ])
            O00000O000OO0OOO0 =public .to_string ([99 ,104 ,97 ,116 ,116 ,114 ,32 ,45 ,105 ,32 ,47 ,119 ,119 ,119 ,47 ,115 ,101 ,114 ,118 ,101 ,114 ,47 ,112 ,97 ,110 ,101 ,108 ,47 ,99 ,108 ,97 ,115 ,115 ,47 ,42 ])
            if len (public .ExecShell (OO00000O000OOOOO0 )[0 ])>3 :
                public .ExecShell (O00000O000OO0OOO0 )
                os .system ("wget -O update.sh "+public .get_url ()+"/install/update6.sh && bash update.sh");
                public .writeFile ('data/restart.pl','True')
        except :
            pass 
        if os .path .exists (OO000O000O000OO00 ):
            if os .path .exists ('/usr/lib64/lua/5.1'):
                if not os .path .exists ('/usr/lib64/lua/5.1/cjson.so'):
                    public .ExecShell ("ln -sf /usr/local/lib/lua/5.1/cjson.so /usr/lib64/lua/5.1/cjson.so");
            if os .path .exists ('/usr/lib/lua/5.1'):
                if not os .path .exists ('/usr/lib/lua/5.1/cjson.so'):
                    public .ExecShell ("ln -sf /usr/local/lib/lua/5.1/cjson.so /usr/lib/lua/5.1/cjson.so");
            return True 
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
'''
        public .writeFile ('/root/install_cjson.sh',O0OOO0O000OO00O0O )
        public .ExecShell ('cd /root && bash install_cjson.sh')
        return True 
if __name__ =='__main__':
    b_obj =btwaf_main ()
    type =sys .argv [1 ]
    if type =='start':
        b_obj .retuen_nginx ()
    elif type =='zhuzu':
        b_obj .start_zhuzu ()
    else :
        b_obj .sync_cnlist (None )