# -*- coding: cp936 -*-

import telnetlib
import time

def string_switch(x,y,z):
    with open(x, "r") as f:
        #readlines���б����ʽ���ļ�����
        lines = f.readlines()
 
    with open(x, "w") as f_w:
        for line in lines:
            if y in line:
                line = line.replace(y,z)
            elif ('end' in line):
                f_w.write(line)
                break
            f_w.write(line)
def restore():
    choice = '2'
    enter = '\n'
    print("�������ʾ��������Ҫ�����Ľ�������������ò�����Ϣ�������»س���������")
    while (1) :
        hostip = raw_input("������ip��ַ��")
        port = raw_input("������telnet�˿ڣ�")
        fir = raw_input("��ѡ���Ƿ����뽻����ȫ�ֵ�¼�û��˺����롾Y/N����")
        if ((fir == 'Y') or (fir == 'y')):
            username = raw_input("�����뽻������¼�û��˺ţ�")
            u_password = raw_input("�����뽻������¼�û����룺")
            u_flag = 1
        elif ((fir == 'N') or (fir == 'n')) :
            u_flag = 0                    #��������Ƿ��������û��˺�����
        else :
            print("�������")
            return
        sec = raw_input("��ѡ���Ƿ����뽻����telnet��¼���롾Y/N����")
        if ((sec == 'Y') or (sec == 'y')) :
            tel_password = raw_input("������telnet��¼���룺")
            tel_flag = 1
        elif ((sec == 'N') or (sec == 'n')) :
            tel_flag = 0                  #��������Ƿ�������telnet��¼����
        else :
            print("�������")
            return
        trd = raw_input("��ѡ���Ƿ����뽻������Ȩģʽ���롾Y/N����")
        if ((trd == 'Y') or (trd == 'y')) :
            en_password = raw_input("��������Ȩģʽ���룺")
            en_flag = 1
        elif ((trd == 'N') or (trd == 'n')) :
            en_flag = 0                  #�Ƿ���������Ȩģʽ����
        else :
            print("�������")
            return
        print(hostip)
        print(port)
        if (u_flag) :
            print(username)
            print(u_password)
        if (tel_flag) :
            print(tel_password)
        if (en_flag) :
            print(en_password)
        flag = raw_input("��ȷ����������Ϣ�����롾Y������������Ҫ��������������Ϣ��")
        if ((flag == 'Y') or (flag == 'y')) :
            break

    print("���ڽ���telnet���ӽ����������Ժ�-----------------------------")
    tel = telnetlib.Telnet(hostip,port,timeout=5)
    time.sleep(3)
    th = tel.read_very_eager()

    #�ж�telnet����ʱ�Ĳ�ͬ���
    if ('Password' in th) :  #telnet����ʱ��Ҫtelnet��¼����
        if (tel_flag) :
            tel.write(tel_password+enter)
            #������������
        else :
            print("��ʾ��������Ҫtelnet��¼����")
            tel.close()
    elif ('>' in th) :                 #telnet����ʱ����Ҫ��¼���룬���뽻��������ͨ�û�ģʽ
        print("telnet���ӳɹ�!")
        #������������
    elif ('#' in th) :                #telnet����ʱ����Ҫ��¼���룬���뽻��������Ȩ�û�ģʽ
        print("telnet���ӳɹ���")
        #������������
    elif 'Username' in th :#telnet����ʱ��Ҫȫ���û���¼�˺�����
        if (u_flag):
            tel.write(username+enter)
            tel.read_until('Password:')
            tel.write(u_password+enter)
            time.sleep(2)
            string = tel.read_very_eager()
            if ('Username' in string) :
                print("������û��˺��������")
                tel.close()
            elif ('>' in string) :      #telnet���ӳɹ����ҽ��뽻������ͨ�û�ģʽ
                print("���ӳɹ���")
                date = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))    #����ʱ��
                filename = '2017-12-27 10-28-45 config.txt'
                print("����ʱ���ǣ�"+date)
                print("��Ϊ�ָ��ļ����ļ���Ϊ��"+filename)
                tel.write('enable'+enter)
                time.sleep(2)       #��ȡ������ǰ���ó���ȴ�һ��ʱ��  
                string1 = tel.read_very_eager()
                if ('Password' in string1 ) :    #��������������Ȩģʽ��¼����
                    if (en_flag) :
                        tel.write(en_password+enter) #������Ȩģʽ
                        tel.read_until('#')
                        tel.write('run-system-shell'+enter)
                        tel.read_until('~ # ')
                        tel.write('cat > data/config.text <<EOF'+enter)
                        tel.read_until('> ')
                        with open (filename,"r") as f:
                            for line in open (filename) :
                                line = f.readline()
                                tel.write(line)
                        tel.write(enter+'EOF'+enter)
                        string10 = tel.read_until('~ # ')
                        print string10
                    else :
                        print("��Ҫ��Ȩģʽ���룡")
                        tel.close()
                elif ('#' in string1) :          #������û��������Ȩģʽ��¼����
                    #������Ȩģʽ
                    #������
                    print("����")
                else :                           #δ֪����ļ򵥴���
                    print("��ʾ����������")
                    tel.close()
            elif ('#' in string) :      #telnet���ӳɹ����ҽ��뽻������Ȩ�û�ģʽ
                print("���ӳɹ���")
                #����
            else :
                print("��������")
                tel.close()
                
        else :
            print("��ʾ��������Ҫ�û��˺�����")
            tel.close()
            
string1 = " --More--           "
restore()
