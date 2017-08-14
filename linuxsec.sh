#!/bin/bash

#设置密码复杂度
if [ -z "`cat /etc/pam.d/system-auth | grep -v "^#" | grep "pam_cracklib.so"`" ];then
	sed -i '/password    required      pam_deny.so/a\password    required      pam_cracklib.so  try_first_pass minlen=8 ucredit=-1   lcredit=-1   ocredit=-1 dcredit=-1 retry=3 difok=5' /etc/pam.d/system-auth
fi


#设置连续登录失败暂锁机制
if [ -z "`cat /etc/pam.d/system-auth | grep -v "^#" | grep "pam_tally.so"`" ];then
	if [ -z "`cat /etc/pam.d/system-auth | grep -v "^#" | grep "pam_tally.so" | grep auth`" ];then
		sed -i '/auth	   include	system-auth/a\auth        required      pam_tally.so deny=5 unlock_time=600 even_deny_root root_unlock_time=600' /etc/pam.d/system-auth
	fi
	if [ -z "`cat /etc/pam.d/system-auth | grep -v "^#" | grep "pam_tally.so" | grep account`" ]; 
	then
		sed -i '/account    include      system-auth/a\account     required      pam_tally.so' /etc/pam.d/system-auth
	fi
fi

if [ -z "`cat /etc/pam.d/sshd | grep -v "^#" | grep "pam_tally.so"`" ];then
	if [ -z "`cat /etc/pam.d/sshd | grep -v "^#" | grep "pam_tally.so" | grep auth`" ];then
		sed -i '/auth        required      pam_deny.so/a\auth        required      pam_tally.so deny=5 unlock_time=600 even_deny_root root_unlock_time=600' /etc/pam.d/sshd
	fi
	if [ -z "`cat /etc/pam.d/sshd | grep -v "^#" | grep "pam_tally.so"` | grep account" ];then
		sed -i '/account     required      pam_unix.so/a\account required pam_tally.so' /etc/pam.d/sshd
	fi
fi


#检查密码重复使用次数
if [ -z "`cat /etc/pam.d/system-auth | grep password | grep remember`" ];then
	sed -i '/password    sufficient    pam_unix.so/s/$/& remember=5/' /etc/pam.d/system-auth
fi


#设置操作超时锁定
if [ -z "`cat /etc/profile | grep -v "^#" | grep TMOUT`" ];then
	echo -e "\nexport TMOUT=1800" >> /etc/profile
fi

#修改密码时效
sed -i '/PASS_WARN_AGE/s/7/10/' /etc/login.defs 
sed -i '/PASS_MIN_LEN/s/5/8/' /etc/login.defs
#sed -i '/PASS_MAX_DAYS/s/99999/90/' /etc/login.defs
sed -i '/PASS_MIN_DAYS/s/0/6/' /etc/login.defs

#修改默认访问权限
sed -i '/UMASK/s/077/027/' /etc/login.defs

#设置重要文件目录权限
chmod 644 /etc/passwd	
chmod 600 /etc/xinetd.conf 
chmod 600 /etc/inetd.conf	
chmod 644 /etc/group	
chmod 000 /etc/shadow	
chmod 644 /etc/services	
chmod 600 /etc/security
chmod 750 /etc/				#启动了nscd服务导致设置权限以后无法登陆
chmod 750 /etc/rc6.d	
chmod 750 /tmp	
chmod 750 /etc/rc0.d/	
chmod 750 /etc/rc1.d/	
chmod 750 /etc/rc2.d/	
chmod 750 /etc/rc4.d	
chmod 750 /etc/rc5.d/	
chmod 750 /etc/rc3.d	
chmod 750 /etc/rc.d/init.d/	
chmod 600 /etc/grub.conf
chmod 600 /boot/grub/grub.conf
chmod 600 /etc/lilo.conf


#检查用户umask设置
sed -i '/umask/s/002/077/' /etc/csh.cshrc
sed -i '/umask/s/002/077/' /etc/bashrc
sed -i '/umask/s/002/077/' /etc/profile
csh_login=`cat /etc/csh.login | grep -i "umask"`
if [ -z "$csh_login" ];then
	echo -e "/numask 077" >>/etc/csh.login
fi

#检查是否设置ssh登录前告警banner
sshbanner="/etc/ssh_banner"
if [ ! -f "$sshbanner" ];then
	touch /etc/ssh_banner
	chown bin:bin /etc/ssh_banner
	chmod 644 /etc/ssh_banner
	echo -e "Authorized only.All activity will be monitored and reported" > /etc/ssh_banner
	echo -e "Banner /etc/ssh_banner" >> /etc/ssh/sshd_config
	/etc/init.d/sshd restart
fi

#FTP安全设置
vsftpd_conf=`find /etc/ -maxdepth 2 -name vsftpd.conf`
if [ ! -z "$vsftpd_conf" ];then
	sed -i '/anonymous_enable/s/YES/NO/' $vsftpd_conf
fi

ftpuser=`find /etc/ -maxdepth 2 -name ftpusers`
if [ ! -z "$ftpuser" ] && [ -z "`cat $ftpuser | grep -v "^#" | grep root`"];then
	echo "root" >>$ftpuser
fi

sed -i '/^ftp/d' /etc/passwd

#检查重要文件属性设置
chattr +i /etc/passwd
chattr +i /etc/shadow
chattr +i /etc/group
chattr +i /etc/gshadow

#日志审计检查
if [ ! -f "/etc/rsyslog.conf" ] && [ ! -f "/etc/syslog.conf" ] && [ ! -f "/etc/syslog-ng/syslog-ng.conf" ];then
	echo "{tput setaf 1}syslog not installed!!!${tput sgr0}"
	exit
fi
	

if [ ! -f "/var/log/cron" ];then
	touch /var/log/cron
	chmod 775 /var/log/cron
fi

if [ ! -f "/var/adm/messages" ];then
	touch /var/adm/messages
	chmod 666 /var/adm/messages
fi

if [ -f "/etc/rsyslog.conf" ] ;then
	if [ -z "`cat /etc/rsyslog.conf | grep "^cron.*" | grep "/var/log/cron"`" ];then
		echo -e "cron.*        /var/log/cron" >> /etc/rsyslog.conf
	fi
	
	if [ -z "`cat /etc/rsyslog.conf | grep "/var/adm/messages"`" ];then
		echo -e "*.err;kern.debug;daemon.notice   /var/adm/messages" >>/etc/rsyslog.conf
	fi
	
	if [ -z "`grep "@[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}" /etc/rsyslog.conf`" ];then
		echo -e "*.* @192.168.0.1" >>/etc/rsyslog.conf
	fi
	
	/etc/init.d/rsyslog restart
fi

if [ -f "/etc/syslog.conf" ];then
	if [ -z "`cat /etc/rsyslog.conf | grep "^cron.*" | grep "/var/log/cron"`" ];then
		echo -e "cron.*        /var/log/cron" >> /etc/syslog.conf
	fi
	
	if [ -z "`cat /etc/rsyslog.conf | grep "/var/adm/messages"`" ];then
		echo -e "*.err;kern.debug;daemon.notice   /var/adm/messages" >>/etc/rsyslog.conf
	fi
	
	if [ -z "`grep "@[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}" /etc/syslog.conf`" ];then
		echo -e "*.* @192.168.0.1" >>/etc/syslog.conf
	fi
	
	/etc/init.d/syslog restart
fi

if [ -f "/etc/syslog-ng.conf" ];then
	if [ -z "`cat /etc/syslog-ng/syslog-ng.conf | grep "destination(cron)"`" ];then
		echo -e "filter f_cron { facility(cron); }; " >> /etc/syslog-ng/syslog-ng.conf
		echo -e "destination cron { file("/var/log/cron"); }; " >>/etc/syslog-ng/syslog-ng.conf
		echo -e "log { source(src); filter(f_cron); destination(cron); }; " >> /etc/syslog-ng/syslog-ng.conf
	fi
	
	if [ -z "`cat /etc/syslog-ng/syslog-ng.conf | grep "filter f_msgs"`" ];then
		echo -e "filter f_msgs { level(err) or facility(kern) and level(debug) \
				or facility(daemon) and level(notice); }; " >>/etc/syslog-ng/syslog-ng.conf
		echo -e "destination msgs { file("/var/adm/messages"); }; " >>/etc/syslog-ng/syslog-ng.conf
		echo -e "log { source(src); filter(f_msgs); destination(msgs); }; " >>/etc/syslog-ng/syslog-ng.conf
	fi
	
	if [ -z "`grep "@[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}" /etc/syslog-ng/syslog-ng.conf`" ];then
		echo -e "destination logserver { udp("192.168.0.1" port(514)); }; " >>/etc/syslog-ng/syslog-ng.conf
		echo -e "log { source(src); destination(logserver); }; ">>/etc/syslog-ng/syslog-ng.conf
	fi
	
	/etc/init.d/syslog restart
fi

#禁止wheel组以外的用户su为root
if [ -z "`cat /etc/pam.d/su | grep -v "^#" | grep pam_wheel.so`" ];then
	if [ -z "`cat /etc/pam.d/su | grep -v "^#" | grep pam_rootok.so`" ];then
		sed -i '2iauth            sufficient      pam_rootok.so' /etc/pam.d/su
		sed -i '/pam_rootok.so/a\auth            required        pam_wheel.so group=wheel' /etc/pam.d/su
	else
		sed -i '/pam_rootok.so/a\auth            required        pam_wheel.so group=wheel' /etc/pam.d/su
	fi
fi

#关闭不必要的服务和端口
chk_ntalk=`chkconfig --list | grep ntalk | grep on`
if [ ! -z "$chk_ntalk" ];then
	chkconfig --level 0123456 ntalk off
fi

chk_lpd=`chkconfig --list | grep lpd | grep on`
if [ ! -z "$chk_lpd" ];then
	chkconfig --level 0123456 lpd off
fi

chk_kshell=`chkconfig --list | grep kshell | grep on`
if [ ! -z "$chk_kshell" ];then
	chkconfig --level 0123456 kshell off
fi

chk_time=`chkconfig --list | grep time | grep on`
if [ ! -z "$chk_time" ];then
	chkconfig --level 0123456 time off
	chkconfig --level 0123456 time-udp off
fi

chk_sendmail=`chkconfig --list | grep sendmail | grep on`
if [ ! -z "$chk_sendmail" ];then
	chkconfig --level 0123456 sendmail off
fi

chk_klogin=`chkconfig --list | grep klogin | grep on`
if [ ! -z "$chk_klogin" ];then
	chkconfig --level 0123456 klogin off
fi

chk_printer=`chkconfig --list | grep printer | grep on`
if [ ! -z "$chk_printer" ];then
	chkconfig --level 0123456 printer off
fi

chk_nfslock=`chkconfig --list | grep nfslock | grep on`
if [ ! -z "$chk_nfslock" ];then
	chkconfig --level 0123456 nfslock off
fi

chk_echo=`chkconfig --list | grep echo | grep on`
if [ ! -z "$chk_echo" ];then
	chkconfig --level 0123456 echo off
fi

chk_discard=`chkconfig --list | grep discard | grep on`
if [ ! -z "$chk_discard" ];then
	chkconfig --level 0123456 discard off
fi

chk_chargen=`chkconfig --list | grep chargen | grep on`
if [ ! -z "$chk_chargen" ];then
	chkconfig --level 0123456 chargen off
fi

chk_bootps=`chkconfig --list | grep bootps | grep on`
if [ ! -z "$chk_bootps" ];then
	chkconfig --level 0123456 chk_bootps off
fi

chk_daytime=`chkconfig --list | grep daytime | grep on`
if [ ! -z "$chk_daytime" ];then
	chkconfig --level 0123456 daytime off
fi

chk_tftp=`chkconfig --list | grep tftp | grep on`
if [ ! -z "$chk_tftp" ];then
	chkconfig --level 0123456 tftp off
fi

chk_ypbind=`chkconfig --list | grep ypbind | grep on`
if [ ! -z "$chk_ypbind" ];then
	chkconfig --level 0123456 ypbind off
fi

chk_ident=`chkconfig --list | grep ident | grep on`
if [ ! -z "$chk_ident" ];then
	chkconfig --level 0123456 ident off
fi

#检查core dump 设置
chk_core=`grep core /etc/security/limits.conf | grep -v "^#"`
if [ -z "$chk_core" ];then
	echo "*               soft    core            0"  >> /etc/security/limits.conf
	echo "*               hard    core            0"  >> /etc/security/limits.conf
fi

#删除潜在危险文件
hosts_equiv=`find / -maxdepth 3 -name hosts.equiv 2>/dev/null`
if [ ! -z "$hosts_equiv" ];then
	mv "$hosts_equiv" "$hosts_equiv".bak
fi

_rhosts=`find / -maxdepth 3 -name .rhosts 2>/dev/null`
if [ ! -z "$_rhosts" ];then
	mv "$_rhosts" "$_rhosts".bak
fi

_netrc=`find / -maxdepth 3 -name .netrc 2>/dev/null`
if [ ! -z "$_netrc" ];then
	mv "$_netrc" "$_netrc".bak
fi

#检查系统内核参数配置,修改只当次生效，重启需重新设置
sysctl -w net.ipv4.conf.all.accept_source_route="0"
sysctl -w net.ipv4.conf.all.accept_redirects="0"
sysctl -w net.ipv4.icmp_echo_ignore_broadcasts="1"
sysctl -w net.ipv4.conf.all.send_redirects="0"
sysctl -w net.ipv4.ip_forward="0"

#检查拥有suid和sgid权限文件并修改文件权限为755
find /usr/bin/chage /usr/bin/gpasswd /usr/bin/wall /usr/bin/chfn /usr/bin/chsh /usr/bin/newgrp /usr/bin/write /usr/sbin/usernetctl /bin/mount /bin/umount /bin/ping /sbin/netreport -type f -perm /6000 | xargs chmod 755