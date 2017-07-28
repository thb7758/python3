#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:Huppert
##此脚本支持单个ip复制，也支持多IP复制文件
try:
    import pexpect
except:
    import os
    print('Please enter the password installation module..\n')
    cmd = 'sudo apt -y install python3-pexpect'
    if os.system(cmd) == 0:
        print('Success install module...')
    else:
        print('Failt install module...')
        raise SystemExit
finally:
    import pexpect,os,getpass,traceback
def ssh_command (password, command):
    ssh_newkey = 'Are you sure you want to continue connecting'

    child = pexpect.spawn(command)
    i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '])

    if i == 0:
        print ('ERROR!')
        print ('SSH could not login. Here is what SSH said:')
        print (child.before, child.after)
        return None

    if i == 1:
        child.sendline ('yes')
        child.expect ('password: ')
        i = child.expect([pexpect.TIMEOUT, 'password: '])
        if i == 0:
            print ('ERROR!')
            print ('SSH could not login. Here is what SSH said:')
            print (child.before, child.after)
        return None
    child.sendline(password)
    return child

def single_download():
    host = input('Hostname: ')
    user = input('User: ')
    password = getpass.getpass()
    local_path = input('Local_file_path:')
    remote_path = input('Remote_file_path:')

    command = 'scp -r {}@{}:{} {}'.format(user, host, remote_path, local_path)
    child = ssh_command (password, command)
    child.expect(pexpect.EOF)
    print (child.before.decode())
    print("\33[32;1m{}\33[0m".format('File download is complete'))

def single_upload ():
    host = input('Hostname: ')
    user = input('User: ')
    password = getpass.getpass()
    local_path = input('Local_file_path:')
    remote_path = input('Remote_file_path:')

    command = 'scp -r {} {}@{}:{}'.format(local_path, user, host, remote_path)
    child = ssh_command (password, command)
    child.expect(pexpect.EOF)
    print (child.before.decode())
    print("\33[32;1m{}\33[0m".format('File upload is complete'))

def batch_upload():
    msg = '''
        1.Bulk copy files require all IP and username names are consistent,
        2.Please create a good ip_list.txt file and place it with the same path as the python script
        3.python3 -u file-copy.py
        '''
    print("\33[32;1m{}\33[0m".format(msg))
    with open('ip_list.txt','rb') as f:
        ip = [ ip.strip().decode() for ip in f ]
    host = ip
    print("Remote host IP list\n",host)
    user = 'liubin'
    password = 'inca'
    local_path = input('Local_file_path:')
    remote_path = input('Remote_file_path:')
    command = ['scp -r {} {}@{}:{}'.format(local_path, user, ip, remote_path) for ip in host]
    child = [ ssh_command (password, cmd) for cmd in command ]
    for a in child:
        a.expect(pexpect.EOF)
        print (a.before.decode())
        print("\33[32;1m{}\33[0m".format('File upload is complete'))

if __name__ == '__main__':
    while True:
        print ('\33[34;1m{}\33[0m'.format('''
        --------------scp software-----------------
            Single host download file       [ 1 ]:
            Single host upload file         [ 2 ]:
            Multiple hosts upload files     [ 3 ]:
            Exit SCP Please enter           [ q ]:
        -------------------------------------------
        '''))
        choice = input("please enter:")
        if choice == "1":
            try:
                single_download()
            except Exception as e:
                print(e)
                traceback.print_exc()
                os._exit(1)
        elif choice == "2":
            try:
                single_upload()
            except Exception as e:
                print(e)
                traceback.print_exc()
                os._exit(1)
        elif choice == "3":
            try:
                batch_upload()
            except Exception as e:
                print(e)
                traceback.print_exc()
                os._exit(1)
        elif choice == "q":
            print('\33[32;1m{}\33[0m'.format("Thanks for use, goodbye"))
            exit(0)

        else:
            print('\33[32;1m{}\33[0m'.format("Input errors, please re-enter"))