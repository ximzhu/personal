# -*- coding: cp936 -*-
import telnetlib
import time
import Tkinter
import os
import json
import time
from ScrolledText import ScrolledText
import tkFileDialog

def enter_dir(date,tpath):
    time_path = tpath
    print("�����ļ������ڣ�"+time_path)
    flag1 = os.path.exists(time_path)
    if (flag1) :
        os.chdir(time_path)
    else :
        os.mkdir(time_path)
        os.chdir(time_path)

def backup_func(switchname,hostip,port,tel_password,username,
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
        
    print("���ڽ���telnet���ӽ����������Ժ�-----------------------------")
    try :
        tel = telnetlib.Telnet(hostip,port,timeout=5)
    except:
        print("Telnet����ʧ�ܣ�")
        err_root = Tkinter.Tk()
        err_root.title(u"������ʾ")
        err_root.geometry('500x500')
        label1 = Tkinter.Label(err_root,text = u"Telnet��������ʧ��,��ȷ�ϲ�����"
                              u"ȷ�������������Ƿ���ȷ!",wraplength = 300)
        label1.pack()
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
                    #������Ȩģʽ������󣬵���������ʾ���ڣ�
                    print("��Ȩ�������")
                    error_root1 = Tkinter.Tk()          
                    label = Tkinter.Label(error_root1,text = " The privilege password of the switch��"+switchname+" is incorrect��please check!")
                    label.pack()
                    tel.close()
        else :
            print("��ʾ��������Ҫtelnet��¼����")
            error_root2 = Tkinter.Tk()          
            label = Tkinter.Label(error_root2,text =  " The switch of "+switchname+" requires a Telnet login password,please check!")
            label.pack()
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
                    error_root3 = Tkinter.Tk()          
                    label = Tkinter.Label(error_root3,text = " The privilege password of the switch��"+switchname+" is incorrect��please check!")
                    label.pack()
                    tel.close()         #��Ȩģʽ��������˳����ӣ�
            else :
                print("��Ҫ��Ȩģʽ���룡")
                error_root4 = Tkinter.Tk()          
                label = Tkinter.Label(error_root4,text = " The switch of "+switchname+" requires a privileged mode password,please check!")
                label.pack()
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
                            error_root5 = Tkinter.Tk()          
                            label = Tkinter.Label(error_root5,text = " The privilege password of the switch��"+switchname+" is incorrect��please check!")
                            label.pack()
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
            error_root6 = Tkinter.Tk()          
            label = Tkinter.Label(error_root6,text = " The switch of " +switchname+"requires a login user name and password.")
            label.pack()
            tel.close()


#telnet���ӽ������ָ�����
def restore_func(r_hostip,r_port,r_telpassword,
            r_username,r_upassword,r_enpassword,r_filename):
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
                    error_root6 = Tkinter.Tk()          
                    label = Tkinter.Label(error_root6,text = " The privilege password of the switch is incorrect��please check!")
                    label.pack()
                    tel.close()
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
                error_root7 = Tkinter.Tk()          
                label = Tkinter.Label(error_root7,text = " The Telnet login password of the switch is incorrect��please check!")
                label.pack()
                tel.close()
                
        else :
            print("��ʾ��������Ҫtelnet��¼����")
            error_root8 = Tkinter.Tk()          
            label = Tkinter.Label(error_root8,text = " The switch requires a Telnet login password,please check!")
            label.pack()
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
                    error_root9 = Tkinter.Tk()          
                    label = Tkinter.Label(error_root9,text = " The privilege password of the switch is incorrect��please check!")
                    label.pack()
                    tel.close()
            else :
                print("��Ҫ��Ȩģʽ���룡")
                error_root10 = Tkinter.Tk()          
                label = Tkinter.Label(error_root10,text = " The switch requires a privilege password,please check!")
                label.pack()
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
            error_root10 = Tkinter.Tk()          
            label = Tkinter.Label(error_root10,text = " The privilege password of the switch is incorrect��please check!")
            label.pack()
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
                            error_root11 = Tkinter.Tk()          
                            label = Tkinter.Label(error_root11,text = " The privilege password of the switch is incorrect��please check!")
                            label.pack()
                            tel.close()
                    else :
                        print("��Ҫ��Ȩģʽ���룡")
                        error_root12 = Tkinter.Tk()          
                        label = Tkinter.Label(error_root12,text = " The switch requires a privilege password,please check!")
                        label.pack()
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
                     error_root13 = Tkinter.Tk()          
                     label = Tkinter.Label(error_root13,text = " The username and user's password of the switch is incorrect��please check!")
                     label.pack()
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
            error_root14 = Tkinter.Tk()          
            label = Tkinter.Label("The switch requires a login user name and password��please check!")
            label.pack()
            tel.close()
    
def hint_backup(event):
    root1 = Tkinter.Tk()
    root1.title(u"��������:")
    root1.geometry('500x500')
    #���������ò����ļ�·����ʾ��ǩ
    label1 = Tkinter.Label(root1,text = u"��ѡ�񽻻��������ò����ļ���",
                           wraplength = 300)
    label1.pack()
    #���������ò����ļ�·�������ı���
    entry1 = Tkinter.Entry(root1,width = 50)
    #���������ò����ļ�·������ȷ�ϰ�ť
    confirm1 = Tkinter.Button(root1,text = u"ѡ���ļ�")
    default_dir = r"C:\Users\85125\Desktop"  # ����Ĭ�ϴ�Ŀ¼
    def backup_1(event):
        fname1 = tkFileDialog.askopenfilename(title=u"ѡ���ļ�"
                                              ,initialdir=(os.path.expanduser
                                                           (default_dir)))
        print fname1                         # �����ļ�ȫ·��
        #print tkFileDialog.askdirectory()  # ����Ŀ¼·��

        #����ѡ������ļ���������ı����������ٲ����µĲ����ļ�·����
        entry1.delete(0,100)
        entry1.insert(0,fname1)
        #root2 = Tkinter.Tk()
        #root2.geometry('400x400')
    def backup_2(event):
        path = entry1.get()
        if (path == ''):
            tip1 =Tkinter.Label(root1,text = u"��ѡ����ȷ�Ľ����������ļ�",wraplength = 300) 
            tip1.pack()
            return 
        print path
        root2 = Tkinter.Tk()
        root2.title(u"ѡ�񽻻����������ļ�����Ŀ¼")
        root2.geometry('500x500')
        date = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))    #����ʱ��
        bpath = date +" config"              #����ı����ļ�Ĭ���ļ�����
        spath = "C:\\"+bpath     #�����������ļ���Ĭ�ϱ���·��
        label2 = Tkinter.Label(root2,text = u"�����������ò����ļ�·��Ϊ��"
                               ,wraplength = 300)
        label2.pack()
        label3 = Tkinter.Label(root2,text = path )
        label3.pack()
        label4 = Tkinter.Label(root2,text = u"�������������ļ�Ĭ�ϱ����ڣ�"
                               ,wraplength = 300)
        label4.pack()
        label5 = Tkinter.Label(root2,text = spath )
        label5.pack()
        entry2 = Tkinter.Entry(root2,width = 50)
        rechoose = Tkinter.Button(root2,text = u"��ѡ")
        next2 = Tkinter.Button(root2,text = u"��һ��")
        def backup_3(event):
            fname2 = tkFileDialog.asksaveasfilename(title=u"ѡ�񱸷ݱ���·��"
                                                  ,initialdir=(os.path.expanduser
                                                           (default_dir)),initialfile = bpath)
            entry2.delete(0,100) 
            entry2.insert(0,fname2)
            

        def backup_4(event):
            spath1 = entry2.get()        #�����������ļ��µı���·��
            print path
            print spath1


            root3 = Tkinter.Tk()
            root3.geometry('500x500')
            label6 = Tkinter.Label(root3,text = u"�������������ļ�����·��Ϊ��",wraplength = 300)
            label6.pack()
            if (spath1 == '') :
                spath1 = spath
            label7 = Tkinter.Label(root3,text = spath1)
            label7.pack()
            label8 = Tkinter.Label(root3,text = u"�ӽ��������ò����ļ��ж�ȡ���Ľ�����Ϊ��",wraplength = 300)
            label8.pack()
            #�����ò����ļ��ж������еĽ�������������ѡ��ȫѡ���������߹�ѡ���еĽ����������в���
            text1 = ScrolledText(root3,width = 30,height = 3) #���ݵ������ļ�����ʾ
            s_list = []                   #��Ž��������ֵ�����
            with open(path) as json_file:
                data = json.load(json_file)
                for i in range(len(data)) :
                    num = "switch" +str(i)
                    switch_name1 = data[num]['switchname']
                    switch_name = str(switch_name1)
                    s_list.append(switch_name)
                    j = i+1.0
                    text1.insert(j,switch_name+'\n')
                    text1.pack()
                    i = i + 1

            def backup_5(event):
                root1.destroy()
                root2.destroy()
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
                        if (s_list[i] == switchname) :
                            print switchname
                            print hostip
                            print port
                            print tel_password
                            print username
                            print u_password
                            print en_password
                            enter_dir(date,spath1)
                            backup_func(switchname,hostip,port,tel_password,username,
                                        u_password,en_password,date)
                            
                        i = i + 1
                    print("������ϣ�")
                    label = Tkinter.Label(root3,text = u"������ɣ�")
                    label.pack()
                
            confirm2 = Tkinter.Button(root3,text = u"ȷ��")
            confirm2.bind("<Button-1>",backup_5)
            confirm2.pack()
            
            
        rechoose.bind("<Button-1>",backup_3)
        next2.bind("<Button-1>",backup_4)
        entry2.pack()
        rechoose.pack()
        next2.pack()
        root2.mainloop()
        
    next1 = Tkinter.Button(root1,text = u"��һ��")

    def rechoose_dir(event):
        fname2 = tkFileDialog.asksaveasfilename(title=u"ѡ�񱣴��ļ���·��")
        print fname2                         # �����ļ�ȫ·��
        #print tkFileDialog.askdirectory()  # ����Ŀ¼·��
        spath = fname2

        #����ѡ������ļ���������ı����������ٲ����µĲ����ļ�·����
        entry2.delete(0,50)            
        entry2.insert(0,fname2)
        print spath
            
    confirm1.bind("<Button-1>",backup_1)
    next1.bind("<Button-1>",backup_2)
    entry1.pack()
    confirm1.pack()
    next1.pack()
    root1.mainloop()

def hint_restore(event):
    #�޸�·��Ϊ�������룡
    root1 = Tkinter.Tk()
    root1.title(u"�ָ�����:")
    root1.geometry('500x500')
    #���������ò����ļ�·����ʾ��ǩ
    label1 = Tkinter.Label(root1,text = u"��ѡ�񽻻��������ò����ļ�:",wraplength = 300)
    label1.pack()
    #���������ò����ļ�·�������ı���
    entry1 = Tkinter.Entry(root1,width = 50)
    #���������ò����ļ�·������ȷ�ϰ�ť
    choose1 = Tkinter.Button(root1,text = u"ѡ���ļ�")
    default_dir = r"C:\Users\85125\Desktop"  # ����Ĭ�ϴ�Ŀ¼
    def restore_1(event):

        fname1 = tkFileDialog.askopenfilename(title=u"ѡ���ļ�"
                                              ,initialdir=(os.path.expanduser
                                                           (default_dir)))
        print fname1                         # �����ļ�ȫ·��
        #print tkFileDialog.askdirectory()  # ����Ŀ¼·��

        #����ѡ������ļ���������ı����������ٲ����µĲ����ļ�·����
        entry1.delete(0,100)
        entry1.insert(0,fname1)
    def restore_2(event):
        path = entry1.get()
        if (path == ''):
            tip1 =Tkinter.Label(root1,text = u"��ѡ����ȷ�Ľ����������ļ�",wraplength = 300) 
            tip1.pack()
            return 
        print path
        root2 = Tkinter.Tk()
        root2.title(u"ѡ�񽻻����������ļ�����Ŀ¼")
        root2.geometry('500x500')
        label2 = Tkinter.Label(root2,text = u"�����������ò����ļ�·��Ϊ��"
                               ,wraplength = 300)
        label2.pack()
        label3 = Tkinter.Label(root2,text = path )
        label3.pack()
        
        #��������ʾ�����ļ��ж�ȡ���Ľ�������
        text1 = ScrolledText(root2,width = 30,height = 3) #���ݵ������ļ�����ʾ
        s_list = []                   #��Ž��������ֵ�����
        with open(path) as json_file:
            data = json.load(json_file)
            for i in range(len(data)) :
                num = "switch" +str(i)
                switch_name1 = data[num]['switchname']
                switch_name = str(switch_name1)
                s_list.append(switch_name)
                j = i+1.0
                text1.insert(j,switch_name+'\n')
                text1.pack()
                i = i + 1
        label4 = Tkinter.Label(root2,text = u"��ѡ��Ҫ�ָ����ݵĽ������������ļ�����Ŀ¼��"
                               ,wraplength = 300)
        label4.pack()
        entry2 = Tkinter.Entry(root2,width = 50)
        choose2 = Tkinter.Button(root2,text = u"ѡ���ļ���Ŀ¼")
        next2 = Tkinter.Button(root2,text = u"��һ��")
        def restore_3(event):

            #fname_2 = tkFileDialog.askopenfilename(title=u"ѡ���ļ���Ŀ¼"
                                              #,initialdir=(os.path.expanduser
                                                           #(default_dir)))
            #print fname_2                         # �����ļ�ȫ·��
            fname2 =tkFileDialog.askdirectory(title=u"ѡ���ļ���Ŀ¼"
                                              ,initialdir=(os.path.expanduser
                                                           (default_dir)))
            print fname2  # ����Ŀ¼·��

            #����ѡ������ļ���������ı����������ٲ����µĲ����ļ�·����
            entry2.delete(0,100)
            entry2.insert(0,fname2)

        def restore_4(event):
            root1.destroy()
            config_path2 = entry2.get()
            print config_path2
            with open(path) as json_file:         #��.json�����ļ��л�ȡ���������ò���
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
                                
                    os.chdir(config_path2)
                    files1 = os.listdir(config_path2)
                    for f2 in files1:
                        flag3 = 0
                        if (r_switchname in f2) :
                            r_filename = f2
                            restore_func(r_hostip,r_port,r_telpassword,r_username
                                         ,r_upassword,r_enpassword,r_filename)
                            print("------------------------------------------\n")
                            flag3 = 1
                            break
                    if (not flag3 ) :
                        print("�ý�������Ӧ���ݺõ������ļ������ڣ�")
                        break

            print("�ָ�����������ϣ�")
            json_file.close()
            label5 = Tkinter.Label(root2,text = "The restore switch configuration has been completed!",wraplength = 300)
            label5.pack()

        choose2.bind("<Button-1>",restore_3)
        next2.bind("<Button-1>",restore_4)
        entry2.pack()
        choose2.pack()
        next2.pack()
        
    
    choose1.bind("<Button-1>",restore_1)
    next1 = Tkinter.Button(root1,text = u"��һ��")
    next1.bind("<Button-1>",restore_2)
    entry1.pack()
    choose1.pack()
    next1.pack()
    root1.mainloop()
        
        

#�����洰������
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
