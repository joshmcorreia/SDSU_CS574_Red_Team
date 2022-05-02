#!/usr/bin/python3

import re
import requests
import paramiko
import logging
import coloredlogs # pip3 install coloredlogs
import pwn # pip3 install pwntools
import pwnlib # pip3 install pwntools, need to import this so that we can check its exceptions

logger = None

def setup_logger():
    """
    Sets up the logger
    """
    logging.basicConfig(filename='xor_file_decryptor.log', level=logging.DEBUG)
    global logger
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='INFO', milliseconds=True) # the level specified here sets what level logs will be shown in the console
    return logger

def test_ssh(ip, username, password):
    """
    Tests for an SSH connection with the specified credentials
    """
    # TODO: If you set up SSH keys then this will give a false positive. Fix that
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys() # if we don't have ssh keys set up we still want to be able to connect
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # if we don't have ssh keys set up we still want to be able to connect
        ssh.connect(ip, username=username, password=password)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("whoami")
        output_as_string = ssh_stdout.read().decode()
        logger.error(f"---- VULNERABLE: The user forgot to change the password for the user '{username}'!")
    except paramiko.ssh_exception.AuthenticationException:
        logger.info(f"- NOT VULNERABLE: The user changed the password for the user '{username}'!")

def check_challenge_one(ip):
    """
    Tests that the user removed the backdoor virus which starts with ~/.bashrc.
    The netcat backdoor port decrements after each successful connection
    """
    for i in range(33123, 33083, -1):
        port = i
        try:
            conn = pwn.remote(ip, port)
            results = ""
            if conn:
                conn.send("ls /home/\n")
                results = conn.recv()
                conn.close()
            if "jackbauer" in results:
                logger.error("---- VULNERABLE: The user hasn't disabled the backdoor for challenge one")
                return True
        except:
            pass
    logger.info(f"- NOT VULNERABLE: The user disabled the backdoor for challenge one.")

def check_challenge_five(ip):
    """
    Test for command injection on port 2222
    @param ip: ip address of target
    """
    try:
        conn = pwn.remote(ip, 2222)
        prompt = conn.recv()
        conn.send("ls; ls /home/\n")
        results = conn.recv().decode()
        conn.close()
        if "jackbauer" in results:
            logger.error(f"---- VULNERABLE: The user has not finished challenge five and is vulnerable to command injection!")
        else:
            logger.info(f"- NOT VULNERABLE: The user patched command injection!")
        return
    except pwnlib.exception.PwnlibException:
        logger.critical(f"-- CHEATER: Port 2222 is not up!")
        return False
    

def main():
    logger = setup_logger()
    logging.getLogger("paramiko").setLevel(logging.CRITICAL) # turn off paramiko logging cause it's annoying
    logging.getLogger("pwnlib").setLevel(logging.CRITICAL) # turn off paramiko logging cause it's annoying
    ip = "192.168.229.130"
    logger.info(f"Checking {ip}....")
    test_ssh(ip=ip, username="jackbauer", password="devgru6")
    test_ssh(ip=ip, username="chloe", password="chloechloe")
    test_ssh(ip=ip, username="surnow", password="surnowsurnow")
    check_challenge_one(ip)
    check_challenge_five(ip)
    #TODO: Add --exploit mode that lets you upload ssh keys and fuck with them or something lol

if __name__ == "__main__":
    main()