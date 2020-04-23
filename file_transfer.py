import paramiko
import os

def send(ip_addr, usr, passwd, filename):
    ssh = paramiko.SSHClient()
    #ssh.load_system_host_keys()
    ssh.load_host_keys(os.path.expanduser(os.path.join(".ssh", "known_hosts.old")))
    server = ip_addr
    ssh.connect(server, username=usr, password=passwd)
    sftp = ssh.open_sftp()
    localpath = filename
    remotepath = 'data-signed.json'
    sftp.put(localpath, remotepath)
    sftp.close()
    ssh.close()
    
    
send('192.168.1.50', 'Idontknow', '1024@mr', '/home/pi/Current_Log/data-signed.json') // sending the json signed file