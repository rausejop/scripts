@echo off
chcp 1252
cls
whoami				> diagnostico.txt
ver				>> diagnostico.txt
ipconfig | findstr IPv4		>> diagnostico.txt
ipconfig | findstr subred	>> diagnostico.txt
ipconfig | findstr Puerta	>> diagnostico.txt
netstat -nr			>> diagnostico.txt
arp -a | findstr mico		>> diagnostico.txt
ipconfig /all			>> diagnostico.txt
ipconfig /displaydns		>> diagnostico.txt
netstat -e			>> diagnostico.txt
netstat -on			>> diagnostico.txt
netstat -an			>> diagnostico.txt
netstat -nr			>> diagnostico.txt