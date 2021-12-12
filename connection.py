import paramiko
import os
#
# Implimenataion of paramiko ssh libray
# https://www.paramiko.org/
# usernmame and passowrd is only good for SEED Project VM
#
#

# once you have the IP of the VM you are sending it to you will need to pass in the 
# the file path including the name and the name you want the file to have once its there
try_ip = '10.229.88.26'
port=22
username='seed'
password='dees'


def try_connection(ip):
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c = ssh.connect(ip,port,username,password)
    print ('connected', c)
    ssh.close()



def file_download(ip, remote_file_name, local_file_name):
    print('download called')
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    ssh.connect(ip,port,username,password)
    ftp_client=ssh.open_sftp()
    try :
        ftp_client.get(remote_file_name, local_file_name)
        return True
    except IOError:
        print('File missing or destroyed')
        os.remove(local_file_name)
        return False
    ftp_client.close()
    ssh.close()

def file_upload(ip, local_file_name, remote_file_name):
    #try_connection(ip)
    print('Upload file function called')
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ftp_client = ssh.connect(ip,port,username,password)
    ftp_client=ssh.open_sftp()
    ftp_client.put(local_file_name, remote_file_name)
    ftp_client.close()
    ssh.close()
    print("Success")


#os.chdir('fragments')
#file_upload(try_ip,'1','1')
#try_connection(try_ip)
#file_download(try_ip, str(0), "this_new.txt")