from paramiko import SSHClient
from scp import SCPClient
import path
import os




def communication():
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect('10.100.6.60', username='michav',password = '123456')
    return(ssh)
def transfer(local_file_path, destination_path, ssh, file_directory_make = True ):

    #local_file_path :: r"C:\Users\micha.vardy\Desktop\scp_test_file_2.txt"
    #destination_path :: /Data/sharedprojects/Michav/pnera

    file_name,extension =  os.path.splitext(os.path.basename(local_file_path))
    #don't make unique directory for file
    if file_directory_make == False:
        with SCPClient(ssh.get_transport()) as scp:
            scp.put(local_file_path, destination_path)
    # if the unique directory for file in destination doesn't exist
    elif file_name not in [i.strip('\n') for i in ssh.exec_command(f'ls {destination_path}')[1].readlines()]:
        #make the directory
        ssh.exec_command(f'mkdir {destination_path}/{file_name}')
    #transfer the local file to the unique directory for file in destination
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(local_file_path, "".join([destination_path,'/',file_name,'/',file_name,extension]))  
def ls(directory,ssh):
    return([i.strip('\n') for i in ssh.exec_command(f'ls {directory}')[1].readlines()])
ssh = communication()
