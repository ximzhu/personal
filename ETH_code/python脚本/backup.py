# -*- coding: cp936 -*-
#������Ҫ���ƣ�
#2.��ȡ�ļ�����ȡ������������ò���
#3.��������������
#4.����

import telnetlib
import time
import os
import json

def enter_dir(date,tpath):
    print tpath
    spath = os.path.dirname(tpath)
    print spath
    config_path = spath+"\switch-config"
    print("�����ļ������ڣ�"+config_path)
    flag = os.path.exists(config_path)
    if (flag) :
        os.chdir(config_path)
        time_path = date+" config"
        flag1 = os.path.exists(time_path)
        if (flag1) :
            os.chdir(time_path)
        else :
            os.mkdir(time_path)
            os.chdir(time_path)
    else :
        os.mkdir(config_path)
        os.chdir(config_path)
        time_path = date +" config"
        flag1 = os.path.exists(time_path)
        if (flag1) :
            os.chdir(time_path)
        else :
            os.mkdir(time_path)
            os.chdir(time_path)

#def res_enterconfigdir(r_switchname,res_filename,config_path):
    
    

#telnet���ӽ����������������ļ����߻ָ�����
def backup(switchname,hostip,port,tel_password,username,
           u_password,en_password,date):
    choice = '2'
    enter = '\n'
    u_flag = '1'
    tel_flag = '1'
    en_flag = '1'
    if (username == '') :
        u_flag = '0'
    if (tel_password == '') :
        tel_flag = '0'
    if (en_password == '') :
        en_flag = '0'
        
    print("����ʱ���ǣ�"+date)
    print("���ڽ���telnet���ӽ����������Ժ�-----------------------------")
    tel = telnetlib.Telnet(hostip,port,timeout=5)
    time.sleep(3)
    th = tel.read_very_eager()
    
    #�ж�telnet����ʱ�Ĳ�ͬ���
    if ('Password' in th) :  #telnet����ʱ��Ҫtelnet��¼����
        if (tel_flag) :
            tel.write(tel_password+enter)
            time.sleep(2)
            string1 = tel.read_very_eager()
            if ('#' in string1) :
                filename = date+' config.text'
                print("telnet���ӳɹ���")
                tel.write('run-system-shell'+enter)
                tel.read_until('~ # ')
                tel.write('cat data/config.text'+enter)
                f = open(filename,'ab')
                tel.read_until('\n')
                while (1) :
                    line = tel.read_until('\r')
                    if ('end' in line) :
                        f.write(line)
                        break
                    else :
                        f.write(line)
                f.close()
                tel.close()
                #�޸��ĵ��������⣡�����޸��ļ���ʽ��������Ĳ���һ���̶���ȡ����ǰ�汣������ʱ��Ĳ�����
                f1=open(filename,'r')
                content = f1.readlines()
                while('\n' in content):
                    content.remove('\n')
                f1.close()
                os.remove(filename)
                with open(filename,'ab')as fw:
                    for i in range(len(content)):
                        line = content[i]
                        fw.write(line)
                fw.close()
                f1=open(filename,'r')
                content = f1.readlines()
                while('\n' in content):
                    content.remove('\n')
                f1.close()
                os.remove(filename)
                with open(filename,'ab')as fw:
                    for i in range(len(content)):
                        line = content[i]
                        fw.write(line)
                fw.close()
                print("���ݳɹ���")
                print("-------------------------------------------------\n")
            elif ('>' in string1) :
                filename = date+' config.text'
                tel.write('enable'+enter)
                tel.read_until('Password:')
                tel.write(en_password+enter)
                time.sleep(2)
                string4 = tel.read_very_eager()
                if ('#' in string4) :
                    filename = date+' config.text'
                    tel.write('run-system-shell'+enter)
                    tel.read_until('~ # ')
                    tel.write('cat data/config.text'+enter)
                    f = open(filename,'ab')
                    tel.read_until('\n')
                    while (1) :
                        line = tel.read_until('\r')
                        if ('end' in line) :
                            f.write(line)
                            break
                        else :
                            f.write(line)
                    f.close()
                    tel.close()
                    #�޸��ĵ��������⣡�����޸��ļ���ʽ��������Ĳ���һ���̶���ȡ����ǰ�汣������ʱ��Ĳ�����
                    f1=open(filename,'r')
                    content = f1.readlines()
                    while('\n' in content):
                        content.remove('\n')
                    f1.close()
                    os.remove(filename)
                    with open(filename,'ab')as fw:
                        for i in range(len(content)):
                            line = content[i]
                            fw.write(line)
                    fw.close()
                    f1=open(filename,'r')
                    content = f1.readlines()
                    while('\n' in content):
                        content.remove('\n')
                    f1.close()
                    os.remove(filename)
                    with open(filename,'ab')as fw:
                        for i in range(len(content)):
                            line = content[i]
                            fw.write(line)
                    fw.close()
                    print("���ݳɹ���")
                    print("-------------------------------------------------\n")
                else:
                    print("��Ȩ�������")
                    tel.close()
        else :
            print("��ʾ��������Ҫtelnet��¼����")
            tel.close()

    elif ('>' in th) :                 #telnet����ʱ����Ҫ��¼���룬���뽻��������ͨ�û�ģʽ
        print("telnet���ӳɹ�!")
        tel.write('enable'+enter)
        time.sleep(2)       #��ȡ������ǰ���ó���ȴ�һ��ʱ��  
        string1 = tel.read_very_eager()
        if ('Password' in string1 ) :    #��������������Ȩģʽ��¼����
            if (en_flag) :
                tel.write(en_password+enter) #������Ȩģʽ
                time.sleep(2)
                string2 = tel.read_very_eager()
                if ('#' in string2 ) :
                    filename = date+' config.text'
                    tel.write('run-system-shell'+enter)
                    tel.read_until('~ # ')
                    tel.write('cat data/config.text'+enter)
                    f = open(filename,'ab')
                    tel.read_until('\n')
                    while (1) :
                        line = tel.read_until('\r')
                        if ('end' in line) :
                            f.write(line)
                            break
                        else :
                            f.write(line)
                    f.close()
                    tel.close()
                    #�޸��ĵ��������⣡�����޸��ļ���ʽ��������Ĳ���һ���̶���ȡ����ǰ�汣������ʱ��Ĳ�����
                    f1=open(filename,'r')
                    content = f1.readlines()
                    while('\n' in content):
                        content.remove('\n')
                    f1.close()
                    os.remove(filename)
                    with open(filename,'ab')as fw:
                        for i in range(len(content)):
                            line = content[i]
                            fw.write(line)
                    fw.close()
                    f1=open(filename,'r')
                    content = f1.readlines()
                    while('\n' in content):
                        content.remove('\n')
                    f1.close()
                    os.remove(filename)
                    with open(filename,'ab')as fw:
                        for i in range(len(content)):
                            line = content[i]
                            fw.write(line)
                    fw.close()
                    print("���ݳɹ���")
                    print("-------------------------------------------------\n")
                else :
                    print("��Ȩģʽ�������")
                    tel.close()         #��Ȩģʽ��������˳����ӣ�
            else :
                print("��Ҫ��Ȩģʽ���룡")
                tel.close()             #û��������Ȩģʽ���룬ֱ���˳���
        elif ('#' in string1) :
            filename = date+' config.text'
            tel.write('run-system-shell'+enter)
            tel.read_until('~ # ')
            tel.write('cat data/config.text'+enter)
            f = open(filename,'ab')
            tel.read_until('\n')
            while (1) :
                line = tel.read_until('\r')
                if ('end' in line) :
                    f.write(line)
                    break
                else :
                    f.write(line)
            f.close()
            tel.close()
            #�޸��ĵ��������⣡�����޸��ļ���ʽ��������Ĳ���һ���̶���ȡ����ǰ�汣������ʱ��Ĳ�����
            f1=open(filename,'r')
            content = f1.readlines()
            while('\n' in content):
                content.remove('\n')
            f1.close()
            os.remove(filename)
            with open(filename,'ab')as fw:
                for i in range(len(content)):
                    line = content[i]
                    fw.write(line)
            fw.close()
            f1=open(filename,'r')
            content = f1.readlines()
            while('\n' in content):
                content.remove('\n')
            f1.close()
            os.remove(filename)
            with open(filename,'ab')as fw:
                for i in range(len(content)):
                    line = content[i]
                    fw.write(line)
            fw.close()
            print("���ݳɹ���")
            print("-------------------------------------------------\n")
                
    elif ('#' in th) :                #telnet����ʱ����Ҫ��¼���룬���뽻��������Ȩ�û�ģʽ
        filename = date+' config.text'
        print("telnet���ӳɹ���")
        tel.write('run-system-shell'+enter)
        tel.read_until('~ # ')
        tel.write('cat data/config.text'+enter)
        f = open(filename,'ab')
        tel.read_until('\n')
        while (1) :
            line = tel.read_until('\r')
            if ('end' in line) :
                f.write(line)
                break
            else :
                f.write(line)
        f.close()
        tel.close()
        #�޸��ĵ��������⣡�����޸��ļ���ʽ��������Ĳ���һ���̶���ȡ����ǰ�汣������ʱ��Ĳ�����
        f1=open(filename,'r')
        content = f1.readlines()
        while('\n' in content):
            content.remove('\n')
        f1.close()
        os.remove(filename)
        with open(filename,'ab')as fw:
            for i in range(len(content)):
                line = content[i]
                fw.write(line)
        fw.close()
        f1=open(filename,'r')
        content = f1.readlines()
        while('\n' in content):
            content.remove('\n')
        f1.close()
        os.remove(filename)
        with open(filename,'ab')as fw:
            for i in range(len(content)):
                line = content[i]
                fw.write(line)
        fw.close()
        print("���ݳɹ���")

    elif ('Username' in th) :#telnet����ʱ��Ҫȫ���û���¼�˺�����
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
                tel.write('enable'+enter)
                time.sleep(2)       #��ȡ������ǰ���ó���ȴ�һ��ʱ��  
                string1 = tel.read_very_eager()
                if ('Password' in string1 ) :    #��������������Ȩģʽ��¼����
                    if (en_flag) :
                        tel.write(en_password+enter) #������Ȩģʽ
                        time.sleep(2)
                        string2 = tel.read_very_eager()
                        if ('#' in string2 ) :
                            filename = date+switchname+' config.text'
                            tel.write('run-system-shell'+enter)
                            tel.read_until('~ # ')
                            tel.write('cat data/config.text'+enter)
                            f = open(filename,'ab')
                            tel.read_until('\n')
                            while (1) :
                                line = tel.read_until('\r')
                                if ('end' in line) :
                                    f.write(line)
                                    break
                                else :
                                    f.write(line)
                            f.close()
                            tel.close()
                            #�޸��ĵ��������⣡�����޸��ļ���ʽ��������Ĳ���һ���̶���ȡ����ǰ�汣������ʱ��Ĳ�����
                            f1=open(filename,'r')
                            content = f1.readlines()
                            while('\n' in content):
                                content.remove('\n')
                            f1.close()
                            os.remove(filename)
                            with open(filename,'ab')as fw:
                                for i in range(len(content)):
                                    line = content[i]
                                    fw.write(line)
                            fw.close()
                            f1=open(filename,'r')
                            content = f1.readlines()
                            while('\n' in content):
                                content.remove('\n')
                            f1.close()
                            os.remove(filename)
                            with open(filename,'ab')as fw:
                                for i in range(len(content)):
                                    line = content[i]
                                    fw.write(line)
                            fw.close()
                            print("���ݳɹ���")
                            print("-------------------------------------------------\n")
                        else :
                            print("��Ȩģʽ�������")
                            tel.close()         #��Ȩģʽ��������˳����ӣ�
                    else :
                        print("��Ҫ��Ȩģʽ���룡")
                        tel.close()
                elif ('#' in string1) :          #������û��������Ȩģʽ��¼����
                    filename = date+' config.text'
                    tel.write('run-system-shell'+enter)
                    tel.read_until('~ # ')
                    tel.write('cat data/config.text'+enter)
                    f = open(filename,'ab')
                    tel.read_until('\n')
                    while (1) :
                        line = tel.read_until('\r')
                        if ('end' in line) :
                            f.write(line)
                            break
                        else :
                            f.write(line)
                    f.close()
                    tel.close()
                    #�޸��ĵ��������⣡�����޸��ļ���ʽ��������Ĳ���һ���̶���ȡ����ǰ�汣������ʱ��Ĳ�����
                    f1=open(filename,'r')
                    content = f1.readlines()
                    while('\n' in content):
                        content.remove('\n')
                    f1.close()
                    os.remove(filename)
                    with open(filename,'ab')as fw:
                        for i in range(len(content)):
                            line = content[i]
                            fw.write(line)
                    fw.close()
                    f1=open(filename,'r')
                    content = f1.readlines()
                    while('\n' in content):
                        content.remove('\n')
                    f1.close()
                    os.remove(filename)
                    with open(filename,'ab')as fw:
                        for i in range(len(content)):
                            line = content[i]
                            fw.write(line)
                    fw.close()
                    print("���ݳɹ���")
                    print("-------------------------------------------------\n")
                else :                           #δ֪����ļ򵥴���
                    print("��ʾ����������")
                    tel.close()
            elif ('#' in string) :      #telnet���ӳɹ����ҽ��뽻������Ȩ�û�ģʽ
                print("���ӳɹ���")
                filename = date+' config.text'
                tel.write('run-system-shell'+enter)
                tel.read_until('~ # ')
                tel.write('cat data/config.text'+enter)
                f = open(filename,'ab')
                tel.read_until('\n')
                while (1) :
                    line = tel.read_until('\r')
                    if ('end' in line) :
                        f.write(line)
                        break
                    else :
                        f.write(line)
                f.close()
                tel.close()
                #�޸��ĵ��������⣡�����޸��ļ���ʽ��������Ĳ���һ���̶���ȡ����ǰ�汣������ʱ��Ĳ�����
                f1=open(filename,'r')
                content = f1.readlines()
                while('\n' in content):
                    content.remove('\n')
                f1.close()
                os.remove(filename)
                with open(filename,'ab')as fw:
                    for i in range(len(content)):
                        line = content[i]
                        fw.write(line)
                fw.close()
                f1=open(filename,'r')
                content = f1.readlines()
                while('\n' in content):
                    content.remove('\n')
                f1.close()
                os.remove(filename)
                with open(filename,'ab')as fw:
                    for i in range(len(content)):
                        line = content[i]
                        fw.write(line)
                fw.close()
                print("���ݳɹ���")
                print("-------------------------------------------------\n")
            else :
                print("��������")
                tel.close()
                
        else :
            print("��ʾ��������Ҫ�û��˺�����")
            tel.close()

#telnet���ӽ������ָ�����
def restore(r_hostip,r_port,r_telpassword,
            r_username,r_upassword,r_enpassword,r_filename):
    choice = '2'
    enter = '\n'
    hostip = r_hostip
    port = r_port
    username = r_username
    u_password = r_upassword
    tel_password = r_telpassword
    en_password = r_enpassword
    u_flag = '1'
    tel_flag = '1'
    en_flag = '1'
    if (username == '') :
        u_flag = '0'
    if (tel_password == '') :
        tel_flag = '0'
    if (en_password == '') :
        en_flag = '0'
    date = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))    #����ʱ��

    print("����ʱ���ǣ�"+date)

    print("���ڽ���telnet���ӽ����������Ժ�-----------------------------")
    tel = telnetlib.Telnet(hostip,port,timeout=5)
    time.sleep(3)
    th = tel.read_very_eager()

    #�ж�telnet����ʱ�Ĳ�ͬ���
    if ('Password' in th) :  #telnet����ʱ��Ҫtelnet��¼����
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
                        for line in open (r_filename) :
                            line = f.readline()
                            tel.write(line)
                        tel.write(enter+'EOF'+enter)
                    tel.read_until('~ # ')
                    tel.write('return'+enter)
                    tel.read_until('#')
                    tel.write('copy startup-config running-config'+enter)
                    tel.read_until('done')
                    print("�ָ����óɹ����˳����ӣ�")
                    tel.close()
                else :
                    print("��Ȩģʽ�������")
            elif ('#' in string3) :
                tel.write('run-system-shell'+enter)
                tel.read_until('~ # ')
                tel.write('cat > data/config.text <<EOF'+enter)
                tel.read_until('> ')
                with open (r_filename,"rb") as f:
                    for line in open (r_filename) :
                        line = f.readline()
                        tel.write(line)
                    tel.write(enter+'EOF'+enter)
                tel.read_until('~ # ')
                tel.write('return'+enter)
                tel.read_until('#')
                tel.write('copy startup-config running-config'+enter)
                tel.read_until('done')
                print("�ָ����óɹ����˳����ӣ�")
                tel.close()
            else :
                print("telnet��¼�������")
                tel.close()
                
        else :
            print("��ʾ��������Ҫtelnet��¼����")
            tel.close()
    elif ('>' in th) :                 #telnet����ʱ����Ҫ��¼���룬���뽻��������ͨ�û�ģʽ
        print("���ӳɹ���")
        print("��Ϊ�ָ��ļ����ļ���Ϊ��"+filename)
        tel.write('enable'+enter)
        time.sleep(2)       #��ȡ������ǰ���ó���ȴ�һ��ʱ��  
        string1 = tel.read_very_eager()
        if ('Password' in string1 ) :    #��������������Ȩģʽ��¼����
            if (en_flag) :
                tel.write(en_password+enter) #������Ȩģʽ
                time.sleep(2)
                string2 = tel.read_very_eager()
                if ('#' in string2) :
                    tel.write('run-system-shell'+enter)
                    tel.read_until('~ # ')
                    tel.write('cat > data/config.text <<EOF'+enter)
                    tel.read_until('> ')
                    with open (r_filename,"rb") as f:
                        for line in open (r_filename) :
                            line = f.readline()
                            tel.write(line)
                        tel.write(enter+'EOF'+enter)
                    tel.read_until('~ # ')
                    tel.write('return'+enter)
                    tel.read_until('#')
                    tel.write('copy startup-config running-config'+enter)
                    tel.read_until('done')
                    print("�ָ����óɹ����˳����ӣ�")
                    tel.close()
                else :
                    print("��Ȩģʽ�������")
            else :
                print("��Ҫ��Ȩģʽ���룡")
                tel.close()
        elif ('#' in string1) :          #������û��������Ȩģʽ��¼����
            tel.write('run-system-shell'+enter)
            tel.read_until('~ # ')
            tel.write('cat > data/config.text <<EOF'+enter)
            tel.read_until('> ')
            with open(r_filename,"rb") as f:
                for line in open(r_filename) :
                    line = f.readline()
                    tel.write(line)
                tel.write(enter+'EOF'+enter)
            tel.read_until('~ # ')
            tel.write('return'+enter)
            tel.read_until('#')
            tel.write('copy startup-config running-config'+enter)
            tel.read_until('done')
            print("�ָ����óɹ����˳����ӣ�")
            tel.close()
        else :  
            print("������û��˺��������")
            tel.close()
    elif ('#' in th) :                #telnet����ʱ����Ҫ��¼���룬���뽻��������Ȩ�û�ģʽ
        print("telnet���ӳɹ�!")
        tel.write('run-system-shell'+enter)
        tel.read_until('~ # ')
        tel.write('cat > data/config.text <<EOF'+enter)
        tel.read_until('> ')
        with open(r_filename,"rb") as f:
            for line in open(r_filename) :
                line = f.readline()
                tel.write(line)
            tel.write(enter+'EOF'+enter)
        tel.read_until('~ # ')
        tel.write('return'+enter)
        tel.read_until('#')
        tel.write('copy startup-config running-config'+enter)
        tel.read_until('done')
        print("�ָ����óɹ����˳����ӣ�")
        tel.close()
    elif 'Username' in th :#telnet����ʱ��Ҫȫ���û���¼�˺�����
        if (u_flag):
            tel.write(username+enter)
            tel.read_until('Password:')
            tel.write(u_password+enter)
            time.sleep(2)
            string = tel.read_very_eager()
            if ('>' in string) :      #telnet���ӳɹ����ҽ��뽻������ͨ�û�ģʽ
                print("���ӳɹ���")
                tel.write('enable'+enter)
                time.sleep(2)       #��ȡ������ǰ���ó���ȴ�һ��ʱ��  
                string1 = tel.read_very_eager()
                if ('Password' in string1 ) :    #��������������Ȩģʽ��¼����
                    if (en_flag) :
                        tel.write(en_password+enter) #������Ȩģʽ
                        time.sleep(2)
                        string2 = tel.read_very_eager()
                        if ('#' in string2) :
                            tel.write('run-system-shell'+enter)
                            tel.read_until('~ # ')
                            tel.write('cat > data/config.text <<EOF'+enter)
                            tel.read_until('> ')
                            with open (r_filename,"rb") as f:
                                for line in open (r_filename) :
                                    line = f.readline()
                                    tel.write(line)
                                tel.write('EOF'+enter)
                            tel.read_until('~ # ')
                            tel.write('return'+enter)
                            tel.read_until('#')
                            tel.write('copy startup-config running-config'+enter)
                            tel.read_until('done')
                            print("�ָ����óɹ����˳����ӣ�")
                            tel.close()
                        else :
                            print("��Ȩģʽ�������")
                    else :
                        print("��Ҫ��Ȩģʽ���룡")
                        tel.close()
                elif ('#' in string1) :          #������û��������Ȩģʽ��¼����
                    tel.write('run-system-shell'+enter)
                    tel.read_until('~ # ')
                    tel.write('cat > data/config.text <<EOF'+enter)
                    tel.read_until('> ')
                    with open (r_filename,"rb") as f:
                        for line in open (r_filename) :
                            line = f.readline()
                            tel.write(line)
                        tel.write('EOF'+enter)
                    tel.read_until('~ # ')
                    tel.write('return'+enter)
                    tel.read_until('#')
                    tel.write('copy startup-config running-config'+enter)
                    tel.read_until('done')
                    print("�ָ����óɹ����˳����ӣ�")
                    tel.close()
                else :  
                     print("������û��˺��������")
                     tel.close()
            elif ('#' in string) :      #telnet���ӳɹ����ҽ��뽻������Ȩ�û�ģʽ
                print("���ӳɹ���")
                tel.write('run-system-shell'+enter)
                tel.read_until('~ # ')
                tel.write('cat > data/config.text <<EOF'+enter)
                tel.read_until('> ')
                with open (r_filename,"rb") as f:
                    for line in open (r_filename) :
                        line = f.readline()
                        tel.write(line)
                    tel.write(enter+'EOF'+enter)
                tel.read_until('~ # ')
                tel.write('return'+enter)
                tel.read_until('#')
                tel.write('copy startup-config running-config'+enter)
                tel.read_until('done')
                print("�ָ����óɹ����˳����ӣ�")
                tel.close()
            else :
                print("��������")
                tel.close()
                
        else :
            print("��ʾ��������Ҫ�û��˺�����")
            tel.close()

if __name__ == '__main__':
    date = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))    #����ʱ��
  
    choice = raw_input("��ѡ��1.���ý�������2.���ݽ�������1/2����")
    if (choice == '1') :
        tpath = os.path.realpath("backup.py")
        spath = os.path.dirname(tpath)
        path = spath+"\switch-arguments.json" #�����������ļ���
        with open(path) as json_file:
            data = json.load(json_file)
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
                i = i + 1
                print switchname
                print hostip
                print port
                print tel_password
                print username
                print u_password
                print en_password
                enter_dir(date,tpath)
                backup(switchname,hostip,port,tel_password,username,
                       u_password,en_password,date)
        json_file.close()
        print("����������ϣ�")
                
    elif (choice == '2') :
        tpath = os.path.realpath("backup.py")
        spath = os.path.dirname(tpath)
        config_path1 = spath +"/switch-config"
        flag = os.path.exists(config_path1)
        if (flag) :
            files = os.listdir(config_path1)
            for f in files:
                print f
        res_filename = raw_input("����������Ҫ�ָ����õ��ļ�����")
        path1 = spath+"\switch-arguments.json" #�����������ļ���
        with open(path1) as json_file:         #��.json�����ļ��л�ȡ���������ò���
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
                i = i + 1
                
                print r_switchname
                print r_hostip
                print r_port
                print r_telpassword
                print r_username
                print r_upassword
                print r_enpassword
                config_path2 = config_path1+"/"+res_filename
                if (os.path.exists(config_path2)) :
                    #config_path2 = config_path1+"/"+res_filename
                    os.chdir(config_path2)
                    files1 = os.listdir(config_path2)
                    for f2 in files1:
                        flag1 = 0
                        if (r_switchname in f2) :
                            r_filename = f2
                            restore(r_hostip,r_port,r_telpassword,r_username
                                    ,r_upassword,r_enpassword,r_filename)
                            print("----------------------------------------------\n")
                            flag = 1
                            break
                    if (not flag ) :
                        print("�����ļ������ڣ�")
                else :
                    print("�����ļ��в����ڣ�")

                
        #res_filename =raw_input("����������Ҫ�ָ����õ��ļ�����") 
        #restore(res_filename)
