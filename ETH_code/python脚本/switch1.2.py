# -*- coding: cp936 -*-
'''
 * Copyright(C) 2005 Ruijie Network. All rights reserved.
 * switch.py          
 * Original Author:  zhuximin@ruijie.com.cn, 2018-1-12   
 *
 * 1.��������һ���ݽ���������,����Ӧ����
 * 2.��������һ�ָ�����������.
 *
 * Histroy
 *  v1.2     zhuximin@ruijie.com.cn     2018-1-17
 *           ѡ�񽻻��������ļ���ؽ����������ֱ��
 *           ��ȡ��ǰ���������ļ����µĲ����ļ�����
 *  v1.1     zhuximin@ruijie.com.cn     2018-1-16
 *           �޸����������ݹ��ܴ��ڵ�BUG
'''

import sys
import telnetlib
import time
import Tkinter
from Tkinter import *
import os
import json
import time
from ScrolledText import ScrolledText
import tkFileDialog

def enter_dir(date,tpath):
    time_path = tpath
    print("�����ļ������ڣ�"+time_path)
    flag1 = os.path.exists(time_path)             #�Ƿ���ڱ����ļ���

    if (flag1) :
        os.chdir(time_path)
        
    else :
        os.mkdir(time_path)
        os.chdir(time_path)

def backup_func(switchname,hostip,port,tel_password,username,
                u_password,en_password,date):
    
    enter = '\n'
    u_flag = 1
    tel_flag = 1
    en_flag = 1
    
    if (username == "") :
        u_flag = 0
        
    if (tel_password == "") :
        tel_flag = 0
        print tel_password
        print tel_flag
        
    if (en_password == "") :
        en_flag = 0
        
        
    print("���ڽ���telnet���ӽ����������Ժ�-----------------------------")
    
    try :
        tel = telnetlib.Telnet(hostip,port,timeout=5)
    except:
        print("Telnet����ʧ�ܣ�")
        err_root = Tkinter.Tk()
        err_root.title(u"������ʾ")
        err_root.geometry('500x500')
        label1 = Tkinter.Label(err_root,text = switchname+u"Telnet��������ʧ�ܣ����˳���\n\nȷ�ϲ�����"
                              u"ȷ�������������Ƿ���ȷ!",wraplength = 300)
        label1.pack(pady = 50)
    
    time.sleep(2)
    filename =switchname+'_config.text'
    th = tel.read_very_eager()
    #�ж�telnet����ʱ�Ĳ�ͬ���
    if ('Password' in th) :                       #telnet����ʱ��Ҫtelnet��¼����
        if (tel_flag) :
            tel.write(tel_password+enter)
            time.sleep(2)
            string1 = tel.read_very_eager()
            
            if ('#' in string1) :
                print("telnet���ӳɹ���")
                tel.write('run-system-shell'+enter)
                tel.read_until('~ # ')
                tel.write('cat data/config.text'+enter)
                f = open(filename,'wb')
                tel.read_until('\n')
                while (1) :
                    line = tel.read_until('\n')
                    line = line.strip('\r\r\n') +enter
                    print line
                    if (line == 'end\n') :
                        f.write(line)
                        break
                    else :
                        f.write(line)
                f.close()
                tel.close()
                print("���ݳɹ���")
                print("-------------------------------------------------\n")
                return 1
            
            elif ('>' in string1) :
                tel.write('enable'+enter)
                tel.read_until('Password:')
                tel.write(en_password+enter)
                time.sleep(2)
                string4 = tel.read_very_eager()
                
                if ('#' in string4) :
                    print('Telnet���ӳɹ���')
                    tel.write('run-system-shell'+enter)
                    tel.read_until('~ # ')
                    tel.write('cat data/config.text'+enter)
                    f = open(filename,'wb')
                    tel.read_until('\n')
                    while (1) :
                        line = tel.read_until('\n')
                        line = line.strip('\r\r\n') +enter
                        print line
                        if (line == 'end\n') :
                            f.write(line)
                            break
                        else :
                            f.write(line)
                    f.close()
                    tel.close()
                    print("���ݳɹ���")
                    print("-------------------------------------------------\n")
                    return 1
                else:
                    #������Ȩģʽ������󣬵���������ʾ���ڣ�
                    print("��Ȩ�������")
                    error_root1 = Tkinter.Tk()
                    error_root1.geometry('500x500')
                    label = Tkinter.Label(error_root1,text = switchname+u"��Ȩģʽ�������")
                    label.pack()
                    tel.close()
                    return 0
            else:
                print("Telnet��¼�������\n")
                error_ = Tkinter.Tk()
                error_.geometry('500x500')
                label = Tkinter.Label(error_,text = switchname+u"Telnet��¼�������")
                label.pack()
                tel.close()
                return 0
        else :
            print("��ʾ��������Ҫtelnet��¼����")
            error_root2 = Tkinter.Tk()
            error_root2.geometry('500x500')
            label = Tkinter.Label(error_root2,text =  switchname+u"������Ҫtelnet��¼���룡")
            label.pack()
            tel.close()
            return 0

    elif ('>' in th) :                            #telnet����ʱ����Ҫ��¼���룬���뽻��������ͨ�û�ģʽ
        print("telnet���ӳɹ�!")
        tel.write('enable'+enter)
        time.sleep(2)                             #��ȡ������ǰ���ó���ȴ�һ��ʱ��  
        string1 = tel.read_very_eager()
        if ('Password' in string1 ) :             #��������������Ȩģʽ��¼����
            if (en_flag) :
                tel.write(en_password+enter)      #������Ȩģʽ
                time.sleep(2)
                string2 = tel.read_very_eager()
                if ('#' in string2 ):
                    print("telnet���ӳɹ���")
                    tel.write('run-system-shell'+enter)
                    tel.read_until('~ # ')
                    tel.write('cat data/config.text'+enter)
                    f = open(filename,'wb')
                    tel.read_until('\n')
                    while (1) :
                        line = tel.read_until('\n')
                        line = line.strip('\r\r\n') +enter
                        print line
                        if (line == 'end\n') :
                            f.write(line)
                            break
                        else :
                            f.write(line)
                    f.close()
                    tel.close()
                    print("���ݳɹ���")
                    print("-------------------------------------------------\n")
                    return 1
                else :
                    print("��Ȩģʽ�������")
                    error_root3 = Tkinter.Tk()
                    error_root3.geometry('500x500')
                    label = Tkinter.Label(error_root3,text = switchname+u" ��Ȩģʽ�������")
                    label.pack()
                    tel.close()                   #��Ȩģʽ��������˳����ӣ�
                    return 0
            else :
                print("��Ҫ��Ȩģʽ���룡")
                error_root4 = Tkinter.Tk()
                error_root4.geometry('500x500')
                label = Tkinter.Label(error_root4,text = switchname+u" ��Ҫ��Ȩģʽ����!")
                label.pack()
                tel.close()                       #û��������Ȩģʽ���룬ֱ���˳���
                return 0
        elif ('#' in string1) :
            print("telnet���ӳɹ���")
            tel.write('run-system-shell'+enter)
            tel.read_until('~ # ')
            tel.write('cat data/config.text'+enter)
            f = open(filename,'wb')
            tel.read_until('\n')
            while (1) :
                line = tel.read_until('\n')
                line = line.strip('\r\r\n') +enter
                print line
                if (line == 'end\n') :
                    f.write(line)
                    break
                else :
                    f.write(line)
            f.close()
            tel.close()
            print("���ݳɹ���")
            print("-------------------------------------------------\n")
            return 1
                
    elif ('#' in th) :                            #telnet����ʱ����Ҫ��¼���룬���뽻��������Ȩ�û�ģʽ
        print("telnet���ӳɹ���")
        tel.write('run-system-shell'+enter)
        tel.read_until('~ # ')
        tel.write('cat data/config.text'+enter)
        f = open(filename,'wb')
        tel.read_until('\n')
        while (1) :
            line = tel.read_until('\n')
            line = line.strip('\r\r\n') +enter
            print line
            if (line == 'end\n') :
                f.write(line)
                break
            else :
                f.write(line)
        f.close()
        tel.close()
        print("���ݳɹ���")
        print("-------------------------------------------------\n")
        return 1

    elif ('Username' in th) :                     #telnet����ʱ��Ҫȫ���û���¼�˺�����
        if (u_flag):
            tel.write(username+enter)
            tel.read_until('Password:')
            tel.write(u_password+enter)
            time.sleep(2)
            string = tel.read_very_eager()
            if ('Username' in string) :
                print("������û��˺��������")
                tel.close()
            elif ('>' in string) :                #telnet���ӳɹ����ҽ��뽻������ͨ�û�ģʽ
                print("���ӳɹ���")
                tel.write('enable'+enter)
                time.sleep(2)                     #��ȡ������ǰ���ó���ȴ�һ��ʱ��  
                string1 = tel.read_very_eager()
                if ('Password' in string1 ) :     #��������������Ȩģʽ��¼����
                    if (en_flag) :
                        tel.write(en_password+enter) 
                        time.sleep(2)
                        string2 = tel.read_very_eager()
                        if ('#' in string2 ) :
                            print("telnet���ӳɹ���")
                            tel.write('run-system-shell'+enter)
                            tel.read_until('~ # ')
                            tel.write('cat data/config.text'+enter)
                            f = open(filename,'wb')
                            tel.read_until('\n')
                            while (1):
                                line = tel.read_until('\n')
                                line = line.strip('\r\r\n') +enter
                                print line
                                if (line == 'end\n') :
                                    f.write(line)
                                    break
                                else :
                                    f.write(line)
                            f.close()
                            tel.close()
                            print("���ݳɹ���")
                            print("-------------------------------------------------\n")
                            return 1
                        else :
                            print("��Ȩģʽ�������")
                            error_root5 = Tkinter.Tk()
                            error_root5.geometry('500x500')
                            label = Tkinter.Label(error_root5,text = switchname+u"��Ȩģʽ�������")
                            label.pack()
                            tel.close()           #��Ȩģʽ��������˳����ӣ�
                            return 0
                    else :
                        print("��Ҫ��Ȩģʽ���룡")
                        error_root5 = Tkinter.Tk()
                        error_root5.geometry('500x500')
                        label = Tkinter.Label(error_root5,text = switchname+u"��Ҫ��Ȩģʽ����!")
                        label.pack()
                        tel.close()
                        return 0
                elif ('#' in string1) :           #������û��������Ȩģʽ��¼����
                    print("telnet���ӳɹ���")
                    tel.write('run-system-shell'+enter)
                    tel.read_until('~ # ')
                    tel.write('cat data/config.text'+enter)
                    f = open(filename,'wb')
                    tel.read_until('\n')
                    while (1) :
                        line = tel.read_until('\n')
                        line = line.strip('\r\r\n') +enter
                        print line
                        if (line == 'end\n') :
                            f.write(line)
                            break
                        else :
                            f.write(line)
                    f.close()
                    tel.close()
                    print("���ݳɹ���")
                    print("-------------------------------------------------\n")
                    return 1
                else :                            #δ֪����ļ򵥴���
                    print("��ʾ����������")
                    tel.close()
                    return 0
            elif ('#' in string) :                #telnet���ӳɹ����ҽ��뽻������Ȩ�û�ģʽ
                print("telnet���ӳɹ���")
                tel.write('run-system-shell'+enter)
                tel.read_until('~ # ')
                tel.write('cat data/config.text'+enter)
                f = open(filename,'wb')
                tel.read_until('\n')
                while (1) :
                    line = tel.read_until('\n')
                    line = line.strip('\r\r\n') +enter
                    print line
                    if (line == 'end\n') :
                        f.write(line)
                        break
                    else :
                        f.write(line)
                f.close()
                tel.close()
                print("���ݳɹ���")
                print("-------------------------------------------------\n")
                return 1
            else :
                print("��������")
                error_root7 = Tkinter.Tk()
                error_root7.geometry('500x500')
                label = Tkinter.Label(error_root6,text = switchname+u"���ӷ�������!")
                label.pack()
                tel.close()
                return 0
                
        else :
            print("��ʾ��������Ҫ�û��˺�����")
            error_root6 = Tkinter.Tk()
            error_root6.geometry('500x500')
            label = Tkinter.Label(error_root6,text = switchname+u"������Ҫ�û��˺�����!")
            label.pack()
            tel.close()
            return 0

#telnet���ӽ������ָ�����
def restore_func(r_switchname,r_hostip,r_port,r_telpassword,
            r_username,r_upassword,r_enpassword,r_filename):
    enter = '\n'
    hostip = r_hostip
    port = r_port
    username = r_username
    u_password = r_upassword
    tel_password = r_telpassword
    en_password = r_enpassword
    u_flag = 1
    tel_flag = 1
    en_flag = 1
    
    if (username == '') :
        u_flag = 0

    if (tel_password == '') :
        tel_flag = 0

    if (en_password == '') :
        en_flag = 0

    #����ʱ��    
    date = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))   

    print("����ʱ���ǣ�"+date)

    print("���ڽ���telnet���ӽ����������Ժ�-----------------------------")
    try :
        tel = telnetlib.Telnet(hostip,port,timeout=5)
    except:
        print("Telnet����ʧ�ܣ�")
        err_root = Tkinter.Tk()
        err_root.title(u"������ʾ")
        err_root.geometry('500x500')
        label1 = Tkinter.Label(err_root,text = r_switchname+u"Telnet��������ʧ�ܣ����˳���\n\nȷ�ϲ�����"
                              u"ȷ�������������Ƿ���ȷ!",wraplength = 300)
        label1.pack(pady = 50)
        
    time.sleep(2)
    th = tel.read_very_eager()

    #�ж�telnet����ʱ�Ĳ�ͬ���
    if ('Password' in th) :                       #telnet����ʱ��Ҫtelnet��¼����
        if (tel_flag) :
            tel.write(tel_password+enter)
            time.sleep(2)
            string3 = tel.read_very_eager()
            if ('>' in string3) :
                print("���ӳɹ���")
                tel.write('enable'+enter)
                tel.read_until('Password:')
                tel.write(en_password+enter)
                time.sleep(2)
                string4 = tel.read_very_eager()
                if ('#' in string4) :
                    tel.write('run-system-shell'+enter)
                    tel.read_until('~ # ')
                    tel.write('cat > data/config.text <<EOF'+enter)
                    tel.read_until('> ')
                    with open (r_filename,"rb") as f:
                        lines = f.readlines()
                        for line in lines :
                            tel.write(line)
                        tel.write('EOF'+enter)
                    tel.read_until('~ # ')
                    tel.write('return'+enter)
                    tel.read_until('#')
                    tel.write('exit'+enter)
                    #tel.write('copy startup-config running-config'+enter)
                    #tel.read_until('done')
                    print("�ָ����óɹ����˳����ӣ�")
                    tel.close()
                    return 1
                else :
                    print("��Ȩģʽ�������")
                    error_root6 = Tkinter.Tk()
                    error_root6.geometry('500x500')
                    label = Tkinter.Label(error_root6,text = r_switchname+u"��Ȩ�������")
                    label.pack()
                    tel.close()
                    return 0
            elif ('#' in string3) :
                tel.write('run-system-shell'+enter)
                tel.read_until('~ # ')
                tel.write('cat > data/config.text <<EOF'+enter)
                tel.read_until('> ')
                with open (r_filename,"rb") as f:
                    lines = f.readlines()
                    for line in lines :
                        tel.write(line)
                    tel.write('EOF'+enter)
                tel.read_until('~ # ')
                tel.write('return'+enter)
                tel.read_until('#')
                tel.write('exit'+enter)
                #tel.write('copy startup-config running-config'+enter)
                #tel.read_until('done')
                print("�ָ����óɹ����˳����ӣ�")
                tel.close()
                return 1
            else :
                print("telnet��¼�������")
                error_root7 = Tkinter.Tk()
                error_root7.geometry('500x500')
                label = Tkinter.Label(error_root7,text =r_switchname+ u" telnet��¼�������")
                label.pack()
                tel.close()
                return 0
                
        else :
            print("��ʾ��������Ҫtelnet��¼����")
            error_root8 = Tkinter.Tk()
            error_root8.geometry('500x500')
            label = Tkinter.Label(error_root8,text = r_switchname + u"������Ҫtelnet��¼���룡")
            label.pack()
            tel.close()
            return 0
    elif ('>' in th) :                            #telnet����ʱ����Ҫ��¼���룬���뽻��������ͨ�û�ģʽ
        print("���ӳɹ���")
        print("��Ϊ�ָ��ļ����ļ���Ϊ��"+filename)
        tel.write('enable'+enter)
        time.sleep(2)                             #��ȡ������ǰ���ó���ȴ�һ��ʱ��  
        string1 = tel.read_very_eager()
        if ('Password' in string1 ) :             #��������������Ȩģʽ��¼����
            if (en_flag) :
                tel.write(en_password+enter)      #������Ȩģʽ
                time.sleep(2)
                string2 = tel.read_very_eager()
                if ('#' in string2) :
                    tel.write('run-system-shell'+enter)
                    tel.read_until('~ # ')
                    tel.write('cat > data/config.text <<EOF'+enter)
                    tel.read_until('> ')
                    with open (r_filename,"rb") as f:
                        lines = f.readlines()
                        for line in lines :
                            tel.write(line)
                        tel.write('EOF'+enter)
                    tel.read_until('~ # ')
                    tel.write('return'+enter)
                    tel.read_until('#')
                    tel.write('exit'+enter)
                    #tel.write('copy startup-config running-config'+enter)
                    #tel.read_until('done')
                    print("�ָ����óɹ����˳����ӣ�")
                    tel.close()
                    return 1
                else :
                    print("��Ȩģʽ�������")
                    error_root9 = Tkinter.Tk()
                    error_root9.geometry('500x500')
                    label = Tkinter.Label(error_root9,text = r_switchname + u" ��Ȩģʽ�������")
                    label.pack()
                    tel.close()
                    return 0
            else :
                print("��Ҫ��Ȩģʽ���룡")
                error_root10 = Tkinter.Tk()
                error_root10.geometry('500x500')
                label = Tkinter.Label(error_root10,text = r_switchname +u"��Ҫ��Ȩģʽ���룡")
                label.pack()
                tel.close()
                return 0
        elif ('#' in string1) :                   #������û��������Ȩģʽ��¼����
            tel.write('run-system-shell'+enter)
            tel.read_until('~ # ')
            tel.write('cat > data/config.text <<EOF'+enter)
            tel.read_until('> ')
            with open(r_filename,"rb") as f:
                lines = f.readlines()
                for line in lines :
                    tel.write(line)
                tel.write('EOF'+enter)
            tel.read_until('~ # ')
            tel.write('return'+enter)
            tel.read_until('#')
            tel.write('exit'+enter)
            #tel.write('copy startup-config running-config'+enter)
            #tel.read_until('done')
            print("�ָ����óɹ����˳����ӣ�")
            tel.close()
            return 1
        else :  
            print("������û��˺��������")
            error_root10 = Tkinter.Tk()
            error_root10.geometry('500x500')
            label = Tkinter.Label(error_root10,text =r_switchname+ u"�û����˺��������!")
            label.pack()
            tel.close()
            return 0
    elif ('#' in th) :                            #telnet����ʱ����Ҫ��¼���룬���뽻��������Ȩ�û�ģʽ
        print("telnet���ӳɹ�!")
        tel.write('run-system-shell'+enter)
        tel.read_until('~ # ')
        tel.write('cat > data/config.text <<EOF'+enter)
        tel.read_until('> ')
        with open(r_filename,"rb") as f:
            lines = f.readlines()
            for line in lines :
                tel.write(line)
            tel.write('EOF'+enter)
        tel.read_until('~ # ')
        tel.write('return'+enter)
        tel.read_until('#')
        tel.write('exit'+enter)
        #tel.write('copy startup-config running-config'+enter)
        #tel.read_until('done')
        print("�ָ����óɹ����˳����ӣ�")
        tel.close()
        return 1
    elif 'Username' in th :                       #telnet����ʱ��Ҫȫ���û���¼�˺�����
        if (u_flag):
            tel.write(username+enter)
            tel.read_until('Password:')
            tel.write(u_password+enter)
            time.sleep(2)
            string = tel.read_very_eager()
            if ('>' in string) :                  #telnet���ӳɹ����ҽ��뽻������ͨ�û�ģʽ
                print("���ӳɹ���")
                tel.write('enable'+enter)
                time.sleep(2)                     #��ȡ������ǰ���ó���ȴ�һ��ʱ��  
                string1 = tel.read_very_eager()
                if ('Password' in string1 ) :     #��������������Ȩģʽ��¼����
                    if (en_flag) :
                        tel.write(en_password+enter) 
                        time.sleep(2)
                        string2 = tel.read_very_eager()
                        if ('#' in string2) :
                            tel.write('run-system-shell'+enter)
                            tel.read_until('~ # ')
                            tel.write('cat > data/config.text <<EOF'+enter)
                            tel.read_until('> ')
                            with open (r_filename,"rb") as f:
                                lines = f.readlines()
                                for line in lines :
                                    tel.write(line)
                                tel.write('EOF'+enter)
                            tel.read_until('~ # ')
                            tel.write('return'+enter)
                            tel.read_until('#')
                            tel.write('exit'+enter)
                            #tel.write('copy startup-config running-config'+enter)
                            #tel.read_until('done')
                            print("�ָ����óɹ����˳����ӣ�")
                            tel.close()
                            return 1
                        else :
                            print("��Ȩģʽ�������")
                            error_root11 = Tkinter.Tk()
                            error_root11.geometry('500x500')
                            label = Tkinter.Label(error_root11,text = r_switchname+ " ��Ȩģʽ�������")
                            label.pack()
                            tel.close()
                            return 0
                    else :
                        print("��Ҫ��Ȩģʽ���룡")
                        error_root12 = Tkinter.Tk()
                        error_root12.geometry('500x500')
                        label = Tkinter.Label(error_root12,text = r_switchname +u"��Ҫ��Ȩģʽ���룡")
                        label.pack()
                        tel.close()
                        return 0
                elif ('#' in string1) :           #������û��������Ȩģʽ��¼����
                    tel.write('run-system-shell'+enter)
                    tel.read_until('~ # ')
                    tel.write('cat > data/config.text <<EOF'+enter)
                    tel.read_until('> ')
                    with open (r_filename,"rb") as f:
                        lines = f.readlines()
                        for line in lines :
                            tel.write(line)
                        tel.write('EOF'+enter)
                    tel.read_until('~ # ')
                    tel.write('return'+enter)
                    tel.read_until('#')
                    tel.write('exit'+enter)
                    #tel.write('copy startup-config running-config'+enter)
                    #tel.read_until('done')
                    print("�ָ����óɹ����˳����ӣ�")
                    tel.close()
                    return 1
                else :  
                     print("������û��˺��������")
                     error_root13 = Tkinter.Tk()
                     error_root13.geometry('500x500')
                     label = Tkinter.Label(error_root13,text =r_switchname+ u"�û��˺�������� ")
                     label.pack()
                     tel.close()
                     return 0
            elif ('#' in string) :                #telnet���ӳɹ����ҽ��뽻������Ȩ�û�ģʽ
                print("���ӳɹ���")
                tel.write('run-system-shell'+enter)
                tel.read_until('~ # ')
                tel.write('cat > data/config.text <<EOF'+enter)
                tel.read_until('> ')
                with open (r_filename,"rb") as f:
                    lines = f.readlines()
                    for line in lines :
                        tel.write(line)
                    tel.write('EOF'+enter)
                tel.read_until('~ # ')
                tel.write('return'+enter)
                tel.read_until('#')
                tel.write('exit'+enter)
                #tel.write('copy startup-config running-config'+enter)
                #tel.read_until('done')
                print("�ָ����óɹ����˳����ӣ�")
                tel.close()
                return 1
            else :
                print("��������")
                tel.close()
                return 0
                
        else :
            print("��ʾ��������Ҫ�û��˺�����")
            error_root14 = Tkinter.Tk()
            error_root14.geometry('500x500')
            label = Tkinter.Label(r_switchname+u"������Ҫ�û��˺����룡")
            label.pack()
            tel.close()
            return 0
    
def hint_backup(event):
    root1 = Tkinter.Tk()
    root1.title(u"��������:")
    root1.geometry('500x500')

    #���������ò����ļ�·����ʾ��ǩ
    label1 = Tkinter.Label(root1,text = u"��ѡ�񽻻��������ò����ļ���(ע�⣺�����������ò����ļ�����Ϊ.json�ļ�"
                           u",������������ճ����ļ����µ�����json���ò����ļ�)",wraplength = 300,justify='left')
    label1.pack(pady = 40)

    #���������ò����ļ�·�������ı���
    entry1 = Tkinter.Entry(root1,width = 50)

    #�жϳ����ļ���Ŀ¼���Ƿ���ڴ�Ŷ�ȡ�����ļ��ļ�¼�ı�
    ScriptPath = os.path.split( os.path.realpath( sys.argv[0] ) )[0]            #��ȡ��ǰ�ű������ļ���Ŀ¼
    print ScriptPath
    f = 0

    for file in os.listdir(ScriptPath):
        if ('.json' in file):
            path = ScriptPath+'\\'+file
            f = 1
            print path
            addlbl = Tkinter.Label(root1,text = u"�ӵ�ǰ�ű��ļ���Ŀ¼�¶�ȡ�������ļ���")
            addlbl.pack()
            entry1.insert(0,path)
            break

    if (not f) :
        addlbl2 = Tkinter.Label(root1,text = u"�ӵ�ǰ�ű��ļ���Ŀ¼��û�ж�ȡ�������ļ�,�����·����Ұ�ť��ѡ���ļ�")
        addlbl2.pack()
        confirm1 = Tkinter.Button(root1,text = u"����",width = 10)

    else:
        #���������ò����ļ�·������ȷ�ϰ�ť
        confirm1 = Tkinter.Button(root1,text = u"��ѡ",width = 10)
        
    default_dir = r"C:\Users\85125\Desktop"       #����Ĭ�ϴ�Ŀ¼

    def backup_1(event):
        #�򿪵Ĳ����ļ�Ĭ���ļ���Ӧ����.json�ļ�
        fname1 = tkFileDialog.askopenfilename(title=u"ѡ�񽻻��������ļ�"
                                              ,initialdir=(os.path.expanduser
                                                           (default_dir)),)
        print fname1                              # �����ļ�ȫ·��

        #����ѡ������ļ���������ı����������ٲ����µĲ����ļ�·����
        entry1.delete(0,100)
        entry1.insert(0,fname1)
        
    def backup_2(event):
        path = entry1.get()

        if (path == '' or not('.json' in path) ):
            tip1 =Tkinter.Label(root1,text = u"��ѡ����ȷ�Ľ����������ļ�",wraplength = 300) 
            tip1.pack()
            return

        root1.destroy()
        root2 = Tkinter.Tk()
        root2.title(u"ѡ�񽻻����������ļ�����Ŀ¼")
        root2.geometry('500x500')
        date = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))    
        bpath = date +"_config"                   #����ı����ļ�Ĭ���ļ�����
        spath = os.path.dirname(path)+"/"+bpath   #�����������ļ���Ĭ�ϱ���·��
        label2 = Tkinter.Label(root2,text = u"�����������ò����ļ�·��Ϊ��"
                               ,wraplength = 300)
        label2.pack(pady = 30)
        label3 = Tkinter.Label(root2,text = path )
        label3.pack()
        label4 = Tkinter.Label(root2,text = u"�������������ļ�Ĭ�ϱ����ڣ�\n"
                               u"(ע�⣺���ڸ��ļ�����������Ӧ�Ľ����������ļ�)"
                               ,wraplength = 300)
        label4.pack(pady = 30)
        label5 = Tkinter.Label(root2,text = spath )
        label5.pack()
        entry2 = Tkinter.Entry(root2,width = 62)
        rechoose = Tkinter.Button(root2,text = u"��ѡ",width = 10)
        next2 = Tkinter.Button(root2,text = u"��һ��",width = 10)

        def backup_3(event):
            fname2 = tkFileDialog.asksaveasfilename(title=u"ѡ�񱸷ݱ���·����",
                                                    initialdir=(os.path.expanduser
                                                                (default_dir)),
                                                    initialfile = bpath)
            entry2.delete(0,100) 
            entry2.insert(0,fname2)
            
        def backup_4(event):
            spath1 = entry2.get()                 #�����������ļ��µı���·��
            print path
            print spath1
            root2.destroy()
            root3 = Tkinter.Tk()
            root3.geometry('500x500')
            label6 = Tkinter.Label(root3,text = u"�������������ļ�����·��Ϊ��",wraplength = 300)
            label6.pack()

            if (spath1 == '') :
                spath1 = spath

            label7 = Tkinter.Label(root3,text = spath1)
            label7.pack()
            label8 = Tkinter.Label(root3,text = u"�ӽ��������ò����ļ��ж�ȡ���Ľ�����Ϊ��(�ɵ����������ѡ�񽻻����Ƿ�ѡ�У���ɫ״̬Ϊѡ��)",wraplength = 300)
            label8.pack()

            #Listbox��ѡ�����н�������ѡ������
            frame3 =Tkinter.Frame(root3)
            frame3.pack()
            
            #Listbox��������н���������
            lb1 = Listbox(frame3,width = 60,height = 5,selectmode = MULTIPLE)   
            sl1 = Scrollbar(frame3,command = lb1.yview)    
            lb1.configure(yscrollcommand = sl1.set)
            sl1.pack(side = RIGHT,fill = Y)

            #�򿪲����ļ���ȡ������,���ѽ��������Ʋ���Listbox
            with open(path) as json_file:
                data = json.load(json_file)
                for i in range(len(data)) :
                    num = "switch" +str(i)
                    switch_name1 = data[num]['switchname']
                    switch_name = str(switch_name1)
                    lb1.insert(END,switch_name)
                    lb1.selection_set(0,i)
                    i = i + 1
            json_file.close()
            lb1.pack(side = Tkinter.LEFT)

            def all_select(event):
                length = lb1.size()
                lb1.selection_set(0,length)
            all_button = Tkinter.Button(root3,text = u"ȫѡ",width = 10)
            all_button.bind("<Button-1>",all_select)
            all_button.pack()

            def backup_5(event):
                result1.insert(END,u"����ִ�У����Ե�...����Ҫ�ظ��������\n")
                result1.update()                  #�ú�����ˢ��һ�½�����ʾ���ȣ�
                result1.delete(1.0, END)
                
                with open(path) as json_file:
                    data = json.load(json_file)
                    res_num = 0
                    allselected = 0

                    for i in range(len(data)) :
                        number = "switch" +str(i)
                        switchname1 = data[number]['switchname']
                        hostip1 = data[number]['hostip']
                        port1 = data[number]['port']
                        tel_password1 = data[number]['tel_password']
                        username1 = data[number]['username']
                        u_password1 = data[number]['u_password']
                        en_password1 = data[number]['en_password']
                        switchname = str(switchname1)
                        hostip = str(hostip1)
                        port = str(port1)
                        tel_password = str(tel_password1)
                        username = str(username1)
                        u_password = str(u_password1)
                        en_password = str(en_password1)

                        if (lb1.get(i) == switchname) :                         #����������ƥ��
                            bools = lb1.selection_includes(i)

                            if (bools) :                                        #����������ѡ
                                allselected = 1                         
                                print switchname
                                print hostip
                                print port
                                print tel_password
                                print username
                                print u_password
                                print en_password
                                enter_dir(date,spath1)
                                res_num = backup_func(switchname,hostip,port,tel_password,username,
                                            u_password,en_password,date)
                                res1 = switchname + u"���ݳɹ���\n"

                                if (res_num):
                                    result1.insert(END,res1)
                                    confirm2.config(state="disable")

                                else:
                                    tip1 = u"�����ļ�����ʧ�ܣ���������ļ�����ػ������ã�"
                                    result1.insert(END,tip1)
                                    
                            
                        i = i + 1
                    
                    print("������ϣ�\n")
                    if (allselected == 0) :
                        nochoose = u"������ѡ��һ̨�����������в�����"
                        result1.insert(END,nochoose)
                json_file.close()
                
            confirm2 = Tkinter.Button(root3,text = u"ȷ��",width = 10)
            confirm2.bind("<Button-1>",backup_5)
            confirm2.pack(pady = 30)
            result1 = ScrolledText(root3,width = 60,height = 5)
            result1.pack()
            root3.mainloop()
            
            
        rechoose.bind("<Button-1>",backup_3)
        next2.bind("<Button-1>",backup_4)
        entry2.pack()
        rechoose.pack()
        next2.pack(pady = 30)
        root2.mainloop()
        
    next1 = Tkinter.Button(root1,text = u"��һ��",width = 10)

    def rechoose_dir(event):
        fname2 = tkFileDialog.asksaveasfilename(title=u"ѡ�������ļ�����·��")
        print fname2                         # �����ļ�ȫ·��
        spath = fname2

        #����ѡ������ļ���������ı����������ٲ����µĲ����ļ�·����
        entry2.delete(0,50)            
        entry2.insert(0,fname2)
        print spath
            
    confirm1.bind("<Button-1>",backup_1)
    next1.bind("<Button-1>",backup_2)
    entry1.pack()
    confirm1.pack()
    next1.pack(pady = 30)
    root1.mainloop()

def hint_restore(event):
    root1 = Tkinter.Tk()
    root1.title(u"�ָ�����:")
    root1.geometry('500x500')

    #���������ò����ļ�·����ʾ��ǩ
    label1 = Tkinter.Label(root1,text = u"��ѡ�񽻻��������ò����ļ���\n(ע�⣺�����������ò����ļ�����Ϊ.json�ļ�"
                           u",������������ճ����ļ����µ�����json���ò����ļ�)",wraplength = 300)
    label1.pack()
    #���������ò����ļ�·�������ı���
    entry1 = Tkinter.Entry(root1,width = 50)

    #�жϳ����ļ���Ŀ¼���Ƿ���ڴ�Ŷ�ȡ�����ļ��ļ�¼�ı�
    ScriptPath = os.path.split( os.path.realpath( sys.argv[0] ) )[0]            #��ȡ��ǰ�ű������ļ���Ŀ¼
    print ScriptPath
    f = 0

    for file in os.listdir(ScriptPath):
        if ('.json' in file):
            path = ScriptPath+'\\'+file
            f = 1
            print path
            addlbl = Tkinter.Label(root1,text = u"�ӵ�ǰ�ű��ļ���Ŀ¼�¶�ȡ�������ļ���")
            addlbl.pack()
            entry1.insert(0,path)
            break

    if (not f) :
        addlbl2 = Tkinter.Label(root1,text = u"�ӵ�ǰ�ű��ļ���Ŀ¼��û�ж�ȡ�������ļ�,�����·����Ұ�ť��ѡ���ļ�")
        addlbl2.pack()
        choose1 = Tkinter.Button(root1,text = u"����",width = 10)

    else:
        #���������ò����ļ�·������ȷ�ϰ�ť
        choose1 = Tkinter.Button(root1,text = u"��ѡ",width = 10)
    
    default_dir = r"C:\Users\85125\Desktop"       #����Ĭ�ϴ�Ŀ¼

    def restore_1(event):
        fname1 = tkFileDialog.askopenfilename(title=u"ѡ���ļ�"
                                              ,initialdir=(os.path.expanduser
                                                           (default_dir)))
        print fname1                              #�����ļ�ȫ·��

        #����ѡ������ļ���������ı����������ٲ����µĲ����ļ�·����
        entry1.delete(0,100)
        entry1.insert(0,fname1)

    def restore_2(event):
        path = entry1.get()
        if (path == '' or not('.json' in path) ):
            tip1 =Tkinter.Label(root1,text = u"��ѡ����ȷ�Ľ����������ļ�",wraplength = 300) 
            tip1.pack()
            return 
        print path
        root1.destroy()
        root2 = Tkinter.Tk()
        root2.title(u"�ָ����ã�")
        root2.geometry('500x500')
        label2 = Tkinter.Label(root2,text = u"�����������ò����ļ�·��Ϊ��"
                               ,wraplength = 300)
        label2.pack()
        label3 = Tkinter.Label(root2,text = path )
        label3.pack()
        lab = Tkinter.Label(root2,text = u"�ӽ��������ò����ļ��ж�ȡ���Ľ�����Ϊ��(�ɵ����������ѡ�񽻻����Ƿ�ѡ�У���ɫ״̬Ϊѡ��)",wraplength = 300)
        lab.pack()

        frame3 =Tkinter.Frame(root2)
        frame3.pack()
            
        #Listbox��������н���������
        lb1 = Listbox(frame3,width = 60,height = 5,selectmode = MULTIPLE)   
        sl1 = Scrollbar(frame3,command = lb1.yview)
        #lb1['yscrollcommand'] = sl1.set
        lb1.configure(yscrollcommand = sl1.set)
        sl1.pack(side = RIGHT,fill = Y)

        #�򿪲����ļ���ȡ������,���ѽ��������Ʋ���Listbox
        with open(path) as json_file:
            data = json.load(json_file)
            for i in range(len(data)) :
                num = "switch" +str(i)
                switch_name1 = data[num]['switchname']
                switch_name = str(switch_name1)
                lb1.insert(END,switch_name)
                lb1.selection_set(0,i)
                i = i + 1
        json_file.close()
        lb1.pack(side = Tkinter.LEFT)

        def all_select(event):
            length = lb1.size()
            lb1.selection_set(0,length)
        all_button = Tkinter.Button(root2,text = u"ȫѡ",width = 10)
        all_button.bind("<Button-1>",all_select)
        all_button.pack()
        
        label4 = Tkinter.Label(root2,text = u"��ѡ��Ҫ�ָ����ݵĽ�������Ӧ�����ļ��ı����ļ��У�"
                               ,wraplength = 300)
        label4.pack(pady = 20)
        entry2 = Tkinter.Entry(root2,width = 62)
        choose2 = Tkinter.Button(root2,text = u"ѡ��Ŀ¼",width = 10)
        next2 = Tkinter.Button(root2,text = u"ȷ��",width = 10)

        def restore_3(event):
            fname2 =tkFileDialog.askdirectory(title=u"ѡ���ļ���"
                                              ,initialdir=(os.path.expanduser
                                                           (default_dir)))
            print fname2  # ����Ŀ¼·��

            #����ѡ���ļ��У�������ı����������ٲ����µ��ļ���·����
            entry2.delete(0,100)
            entry2.insert(0,fname2)
            
        def restore_4(event):
            config_path2 = entry2.get()
            print config_path2
            exits = os.path.exists(config_path2)
            if (not exits):
                result1.insert(END,u"��ѡ����ȷ���ļ���Ŀ¼��\n")
                return
            result1.insert(END,u"����ִ�У����Ե�...\n")
            result1.update()                      
            result1.delete(1.0, END)

            with open(path) as json_file:         #��.json�����ļ��л�ȡ���������ò���
                alls = 0
                data = json.load(json_file)
                for i in range(len(data)) :
                    number = "switch" +str(i)
                    switchname2 = data[number]['switchname']
                    hostip2 = data[number]['hostip']
                    port2 = data[number]['port']
                    tel_password2 = data[number]['tel_password']
                    username2 = data[number]['username']
                    u_password2 = data[number]['u_password']
                    en_password2 = data[number]['en_password']

                    #�ѻ�ȡ���Ľ��������ò���ת�����ַ�����ʽ
                    r_switchname = str(switchname2)
                    r_hostip = str(hostip2)
                    r_port = str(port2)
                    r_telpassword = str(tel_password2)
                    r_username = str(username2)
                    r_upassword = str(u_password2)
                    r_enpassword = str(en_password2)
                
                    print lb1.get(i)
                    print lb1.selection_includes(i)
                    if (lb1.get(i) == r_switchname) :                           #����������ƥ��
                        bools = lb1.selection_includes(i)
                        if (bools) :                                            #����������ѡ
                            alls = 1
                            print r_switchname
                            print r_hostip
                            print r_port
                            print r_telpassword
                            print r_username
                            print r_upassword
                            print r_enpassword
                                
                            os.chdir(config_path2)
                            files1 = os.listdir(config_path2)
                            flag3 = 0
                            for f2 in files1:
                                if (r_switchname in f2) :
                                    r_filename = f2
                                    res_num2 = restore_func(r_switchname,r_hostip,r_port,r_telpassword,r_username
                                                ,r_upassword,r_enpassword,r_filename)
                                    res1 = r_switchname +u" �������ָ��������\n"
                                    tip3 = r_switchname +u" �������ָ�����ʧ�ܣ�\n"
                                    if (res_num2):
                                        result1.insert(END,res1)
                                    else:
                                        result1.insert(END,tip3)
                                    print("------------------------------------------\n")
                                    flag3 = 1
                                    break

                            if (not flag3 ) :
                                print(r_switchname+":�ý�������Ӧ���ݺõ������ļ������ڣ�")
                                res2 = r_switchname+u":�ý�������Ӧ���ݺõ������ļ������ڣ�\n"
                                result1.insert(END,res2)
                                continue
                if (not alls) :
                    nochoose = u"������ѡ��һ̨�����������в�����"
                    result1.insert(END,nochoose)

            print("�ָ�����������ϣ�")
            json_file.close()
            
        choose2.bind("<Button-1>",restore_3)
        next2.bind("<Button-1>",restore_4)
        entry2.pack()
        choose2.pack()
        next2.pack(pady = 30)
        result1 = ScrolledText(root2,width = 60,height = 5)
        result1.pack()
        root2.mainloop()
        
    choose1.bind("<Button-1>",restore_1)
    next1 = Tkinter.Button(root1,text = u"��һ��",width = 10)
    next1.bind("<Button-1>",restore_2)
    entry1.pack()
    choose1.pack()
    next1.pack(pady = 30)
    root1.mainloop()

if __name__ == '__main__':                        #�����洰������
    root = Tkinter.Tk()
    root.title(u"����������")
    root.geometry('500x500')
    frame1 = Tkinter.Frame(root)
    button1 = Tkinter.Button(frame1,text = u"���ݽ���������",width = "25",height = "3")
    button2 = Tkinter.Button(frame1,text = u"�ָ�����������",width = "25",height = "3")
    button1.bind("<Button-1>",hint_backup)
    button2.bind("<Button-1>",hint_restore)
    frame1.pack(expand = 1)
    button1.pack()
    button2.pack(pady = 70)
    
    root.mainloop()


