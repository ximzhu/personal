# -*- coding: cp936 -*-

import telnetlib
import time

def Telnet(hostip,port,tpassword,tftphost,filename,filetype):
    enter = '\n'
    tel = telnetlib.Telnet(hostip,port)
    print("�������ӽ��������Ժ�-------------------------------")
    tel.read_until('Password:')
    tel.write(tpassword+enter)
    #tel.read_until('switch>')
    #tel.write('enable'+enter)        #������Ȩģʽ���س�
    #tel.read_until('Password��')
    #tel.write(en_password+enter)   #������Ȩģʽ����
    #tel.read_until('#')
    if (tel.read_until('#')):
        print("telnet���ӳɹ������Ѿ�������Ȩģʽ��")
        print("��ϣ�����������ִ���ĸ�������")
        print("1.���ݽ���������")
        print("2.�ָ�����������")
        choice1 = raw_input('��ѡ��ִ�ж�����Ӧ������:')
        if (choice1 == '1'):
            print("��ϣ�����ݽ��������ĸ������ļ���")
            print("1.running-conifg")
            print("2.startup-config")
            choice2 = raw_input("��ѡ������Ҫ���ݵĽ����������ļ���")
            if (choice2 == '1'):
                print("��ʼ���ݽ����������ļ�running-config")
                tel.write('copy running-config tftp://'+tftphost+'/'+filename+'running-config'+filetype+enter)
                #tel.read_until('Address of remote host []?')
                #print("��������tftp��������ip��ַ")
                #tel.write(tftp_hostip+enter)
                #tel.read_until('Destination filename []?')
                #print("�������뱸�ݵ������ļ����ļ���")
                #tel.write(filename+enter)
                #tel.read_until('Transmission finished,')
                tel.read_until('Copy success.')
                print("���ݳɹ�������tftp�������ϲ鿴�����Ϣ.")
            elif (choice2 == '2'):
                print("��ʼ���ݽ����������ļ�startup-config")
                tel.write('copy startup-config tftp://'+tftphost+'/'+filename+'startup-config'+filetype+enter)
                tel.read_until('Copy success.')
                print("���ݳɹ�������tftp�������ϲ鿴�����Ϣ.")
            else:
                print("�������")
        elif (choice1 == '2'):
            print("��ϣ��ʹ���ĸ������ļ����ָ����������ã�")
            filename1 = raw_input("�������ļ�����")
            print(filename1)
            tel.write('copy tftp://'+tftphost+'/'+filename1+filetype+' running-config'+enter)
            tel.read_until('[Y/N]:')
            tel.write('y'+enter)
            tel.read_until('Copy success.')
            print("�ָ����óɹ���")
            #print("��ϣ����������ñ��浽startup-config��ȥ��")
        else:
            print("�������")
        print("�˳�telnet����")
        tel.write('exit'+enter)
    else:
        print("telnet���ӽ�����ʧ�ܣ�")

hostip = '192.168.1.3'          #telnet��������ip
port = '23'                     #telnet�˿ں�
tpassword = '123456'            #������telnet��¼����
tftphost = '192.168.1.10'       #tftp������ip��ַ
filetype = '.txt'               #�����ļ��ı����ļ�����
date = time.strftime('%Y%m%d',time.localtime(time.time()))    #����ʱ��
filename = date+'-switch-'                           #����������ļ���ǰ׺

print("Ϊ�˱�֤�����������ܹ��ɹ�ִ�У�����ȷ���������ݣ�")
print("1.������������telnet���ܲ�����������ʵ������ã�")
print("  1.1������ֻ������telnet��¼�����û���˺ţ�")
print("  1.2telnet���ӳɹ�֮��ֱ�ӽ��뽻��������Ȩģʽ��")
print("2.������֧��tftp�����ļ��Ĺ��ܣ�����ע�⽻����ʹ�øù���ʱ����Ҫ����ĸ�ʽ���ܻ���Ϊ��ͬ���������в�ͬ")
flag = raw_input("ȷ����ϣ���Y/N����")
if ((flag == 'Y') or (flag == 'y')):
    print('׼����ʼ��¼�豸,��ǰʱ��'+date)
    #hostip = raw_input("����������Ҫ���ӵĽ�������ip��ַ:")
    #port = raw_input("����������Ҫ���ӵĽ������Ķ˿�:")
    #tpassword = raw_input("����������Ҫ���ӵĽ�������telnet��¼����")
    #tftphost = raw_input("���������tftp������ip��ַ")
    #filetype = raw_input("����Ҫ����������ļ���ʽ��")
    Telnet(hostip,port,tpassword,tftphost,filename,filetype)
else:
    flag1 = raw_input("�Ƿ�ѡ���˳�����Y/N����")
    if ((flag1 == 'Y' ) or (flag1 == 'y')):
        os._exit()
    elif ((flag1 == 'N') or (flag1 == 'n')):
        print("�����ȷ�ϣ�")
        
