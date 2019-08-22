#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys, getopt, commands, os
def main(argv):
   server_name = raw_input("请输入域名:\r\n")
   sure = raw_input('输入域名'+server_name+'确定请输入 y:\r\n')
   if sure != 'y' and sure != 'Y':
        sys.exit(2)
   conf_path = '/usr/local/openresty/nginx/conf/nginx_vhosts.conf'
   conf_path_bk = conf_path+'.bk'
   command_1 = '/usr/local/openresty/nginx/sbin/nginx -t'
   command_2 = '/usr/local/openresty/nginx/sbin/nginx -s reload'
   wwwuser = 'www'
   webroot = '/data/web/'
   nginx_conf = '''

   server
   {{
     listen       {port};
     server_name  {servername};
     index index.html index.shtml index.php index.htm ;
     root  {home};
     include server.conf;
   }}
   '''.format(port='80', servername=server_name, access_log='/var/log/nginx/'+server_name+'.log',home='/data/web/'+server_name,proxy_port='9000')
   commands.getstatusoutput('rm -f '+conf_path_bk)
   commands.getstatusoutput('cp -a '+conf_path+' '+conf_path_bk)
   f = open(conf_path)
   content = f.read()
   f.close()
   if content.find(server_name) != -1:
       print "域名已经存在"
       sys.exit(2)
   handle = open(conf_path,'a')
   handle.write(nginx_conf)
   handle.close()
   isExists=os.path.exists(webroot+server_name)
   if not isExists:
       os.makedirs(webroot+server_name)
       commands.getstatusoutput('chown '+wwwuser+':'+wwwuser+' '+webroot+server_name)
   (status, output) = commands.getstatusoutput(command_1)
   if status == 0:
       commands.getstatusoutput(command_2)
       print "配置成功\r\n网站目录："+webroot+server_name
       sys.exit(0)
   else:
       print "配置错误"+output
       commands.getstatusoutput('rm -f '+conf_path)
       commands.getstatusoutput('mv '+conf_path_bk+' '+conf_path)
       sys.exit(2)
if __name__ == "__main__":
   main(sys.argv[1:])