netsh interface ip set address "Ethernet 3" static 192.168.1.26 255.255.255.0 192.168.1.1
netsh interface ipv4 set dns "Ethernet 3" static 1.1.1.1
netsh interface ipv4 add dns "Ethernet 3" 8.8.8.8 index=2


pause