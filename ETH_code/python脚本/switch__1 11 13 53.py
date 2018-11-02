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
    print("配置文件保存在："+time_path)
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
        
    print("正在进行telnet连接交换机，请稍候-----------------------------")
    try :
        tel = telnetlib.Telnet(hostip,port,timeout=5)
    except:
        print("Telnet连接失败！")
        err_root = Tkinter.Tk()
        err_root.title(u"错误提示")
        err_root.geometry('500x500')
        label1 = Tkinter.Label(err_root,text = u"Telnet建立连接失败,请确认参数正"
                              u"确后检查网络配置是否正确!",wraplength = 300)
        label1.pack()
    time.sleep(3)
    th = tel.read_very_eager()
    
    #判断telnet连接时的不同情况
    if ('Password' in th) :  #telnet连接时需要telnet登录密码
        if (tel_flag) :
            tel.write(tel_password+enter)
            time.sleep(2)
            string1 = tel.read_very_eager()
            if ('#' in string1) :
                filename = date+' config.text'
                print("telnet连接成功！")
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
                #修改文档换行问题！两次修改文件格式！（这里的操作一定程度上取决于前面保存配置时候的操作）
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
                print("备份成功！")
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
                    #修改文档换行问题！两次修改文件格式！（这里的操作一定程度上取决于前面保存配置时候的操作）
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
                    print("备份成功！")
                    print("-------------------------------------------------\n")
                else:
                    #进入特权模式密码错误，弹出错误提示窗口！
                    print("特权密码错误！")
                    error_root1 = Tkinter.Tk()          
                    label = Tkinter.Label(error_root1,text = " The privilege password of the switch："+switchname+" is incorrect，please check!")
                    label.pack()
                    tel.close()
        else :
            print("提示：连接需要telnet登录密码")
            error_root2 = Tkinter.Tk()          
            label = Tkinter.Label(error_root2,text =  " The switch of "+switchname+" requires a Telnet login password,please check!")
            label.pack()
            tel.close()

    elif ('>' in th) :                 #telnet连接时不需要登录密码，进入交换机的普通用户模式
        print("telnet连接成功!")
        tel.write('enable'+enter)
        time.sleep(2)       #读取缓冲区前先让程序等待一定时间  
        string1 = tel.read_very_eager()
        if ('Password' in string1 ) :    #交换机设置了特权模式登录密码
            if (en_flag) :
                tel.write(en_password+enter) #进入特权模式
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
                    #修改文档换行问题！两次修改文件格式！（这里的操作一定程度上取决于前面保存配置时候的操作）
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
                    print("备份成功！")
                    print("-------------------------------------------------\n")
                else :
                    print("特权模式密码错误！")
                    error_root3 = Tkinter.Tk()          
                    label = Tkinter.Label(error_root3,text = " The privilege password of the switch："+switchname+" is incorrect，please check!")
                    label.pack()
                    tel.close()         #特权模式密码错误，退出连接！
            else :
                print("需要特权模式密码！")
                error_root4 = Tkinter.Tk()          
                label = Tkinter.Label(error_root4,text = " The switch of "+switchname+" requires a privileged mode password,please check!")
                label.pack()
                tel.close()             #没有输入特权模式密码，直接退出！
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
            #修改文档换行问题！两次修改文件格式！（这里的操作一定程度上取决于前面保存配置时候的操作）
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
            print("备份成功！")
            print("-------------------------------------------------\n")
                
    elif ('#' in th) :                #telnet连接时不需要登录密码，进入交换机的特权用户模式
        filename = date+' config.text'
        print("telnet连接成功！")
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
        #修改文档换行问题！两次修改文件格式！（这里的操作一定程度上取决于前面保存配置时候的操作）
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
        print("备份成功！")

    elif ('Username' in th) :#telnet连接时需要全局用户登录账号密码
        if (u_flag):
            tel.write(username+enter)
            tel.read_until('Password:')
            tel.write(u_password+enter)
            time.sleep(2)
            string = tel.read_very_eager()
            if ('Username' in string) :
                print("输入的用户账号密码错误！")
                tel.close()
            elif ('>' in string) :      #telnet连接成功并且进入交换机普通用户模式
                print("连接成功！")
                tel.write('enable'+enter)
                time.sleep(2)       #读取缓冲区前先让程序等待一定时间  
                string1 = tel.read_very_eager()
                if ('Password' in string1 ) :    #交换机设置了特权模式登录密码
                    if (en_flag) :
                        tel.write(en_password+enter) #进入特权模式
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
                            #修改文档换行问题！两次修改文件格式！（这里的操作一定程度上取决于前面保存配置时候的操作）
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
                            print("备份成功！")
                            print("-------------------------------------------------\n")
                        else :
                            print("特权模式密码错误！")
                            error_root5 = Tkinter.Tk()          
                            label = Tkinter.Label(error_root5,text = " The privilege password of the switch："+switchname+" is incorrect，please check!")
                            label.pack()
                            tel.close()         #特权模式密码错误，退出连接！
                    else :
                        print("需要特权模式密码！")
                        tel.close()
                elif ('#' in string1) :          #交换机没有设置特权模式登录密码
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
                    #修改文档换行问题！两次修改文件格式！（这里的操作一定程度上取决于前面保存配置时候的操作）
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
                    print("备份成功！")
                    print("-------------------------------------------------\n")
                else :                           #未知错误的简单处理
                    print("提示：发生错误！")
                    tel.close()
            elif ('#' in string) :      #telnet连接成功并且进入交换机特权用户模式
                print("连接成功！")
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
                #修改文档换行问题！两次修改文件格式！（这里的操作一定程度上取决于前面保存配置时候的操作）
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
                print("备份成功！")
                print("-------------------------------------------------\n")
            else :
                print("发生错误！")
                tel.close()
                
        else :
            print("提示：连接需要用户账号密码")
            error_root6 = Tkinter.Tk()          
            label = Tkinter.Label(error_root6,text = " The switch of " +switchname+"requires a login user name and password.")
            label.pack()
            tel.close()


#telnet连接交换机恢复配置
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
    date = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))    #设置时间

    print("现在时间是："+date)

    print("正在进行telnet连接交换机，请稍候-----------------------------")
    tel = telnetlib.Telnet(hostip,port,timeout=5)
    time.sleep(3)
    th = tel.read_very_eager()

    #判断telnet连接时的不同情况
    if ('Password' in th) :  #telnet连接时需要telnet登录密码
        if (tel_flag) :
            tel.write(tel_password+enter)
            time.sleep(2)
            string3 = tel.read_very_eager()
            if ('>' in string3) :
                print("连接成功！")
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
                    print("恢复配置成功！退出连接！")
                    tel.close()
                else :
                    print("特权模式密码错误！")
                    error_root6 = Tkinter.Tk()          
                    label = Tkinter.Label(error_root6,text = " The privilege password of the switch is incorrect，please check!")
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
                print("恢复配置成功！退出连接！")
                tel.close()
            else :
                print("telnet登录密码错误！")
                error_root7 = Tkinter.Tk()          
                label = Tkinter.Label(error_root7,text = " The Telnet login password of the switch is incorrect，please check!")
                label.pack()
                tel.close()
                
        else :
            print("提示：连接需要telnet登录密码")
            error_root8 = Tkinter.Tk()          
            label = Tkinter.Label(error_root8,text = " The switch requires a Telnet login password,please check!")
            label.pack()
            tel.close()
    elif ('>' in th) :                 #telnet连接时不需要登录密码，进入交换机的普通用户模式
        print("连接成功！")
        print("作为恢复文件的文件名为："+filename)
        tel.write('enable'+enter)
        time.sleep(2)       #读取缓冲区前先让程序等待一定时间  
        string1 = tel.read_very_eager()
        if ('Password' in string1 ) :    #交换机设置了特权模式登录密码
            if (en_flag) :
                tel.write(en_password+enter) #进入特权模式
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
                    print("恢复配置成功！退出连接！")
                    tel.close()
                else :
                    print("特权模式密码错误！")
                    error_root9 = Tkinter.Tk()          
                    label = Tkinter.Label(error_root9,text = " The privilege password of the switch is incorrect，please check!")
                    label.pack()
                    tel.close()
            else :
                print("需要特权模式密码！")
                error_root10 = Tkinter.Tk()          
                label = Tkinter.Label(error_root10,text = " The switch requires a privilege password,please check!")
                label.pack()
                tel.close()
        elif ('#' in string1) :          #交换机没有设置特权模式登录密码
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
            print("恢复配置成功！退出连接！")
            tel.close()
        else :  
            print("输入的用户账号密码错误！")
            error_root10 = Tkinter.Tk()          
            label = Tkinter.Label(error_root10,text = " The privilege password of the switch is incorrect，please check!")
            label.pack()
            tel.close()
    elif ('#' in th) :                #telnet连接时不需要登录密码，进入交换机的特权用户模式
        print("telnet连接成功!")
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
        print("恢复配置成功！退出连接！")
        tel.close()
    elif 'Username' in th :#telnet连接时需要全局用户登录账号密码
        if (u_flag):
            tel.write(username+enter)
            tel.read_until('Password:')
            tel.write(u_password+enter)
            time.sleep(2)
            string = tel.read_very_eager()
            if ('>' in string) :      #telnet连接成功并且进入交换机普通用户模式
                print("连接成功！")
                tel.write('enable'+enter)
                time.sleep(2)       #读取缓冲区前先让程序等待一定时间  
                string1 = tel.read_very_eager()
                if ('Password' in string1 ) :    #交换机设置了特权模式登录密码
                    if (en_flag) :
                        tel.write(en_password+enter) #进入特权模式
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
                            print("恢复配置成功！退出连接！")
                            tel.close()
                        else :
                            print("特权模式密码错误！")
                            error_root11 = Tkinter.Tk()          
                            label = Tkinter.Label(error_root11,text = " The privilege password of the switch is incorrect，please check!")
                            label.pack()
                            tel.close()
                    else :
                        print("需要特权模式密码！")
                        error_root12 = Tkinter.Tk()          
                        label = Tkinter.Label(error_root12,text = " The switch requires a privilege password,please check!")
                        label.pack()
                        tel.close()
                elif ('#' in string1) :          #交换机没有设置特权模式登录密码
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
                    print("恢复配置成功！退出连接！")
                    tel.close()
                else :  
                     print("输入的用户账号密码错误！")
                     error_root13 = Tkinter.Tk()          
                     label = Tkinter.Label(error_root13,text = " The username and user's password of the switch is incorrect，please check!")
                     label.pack()
                     tel.close()
            elif ('#' in string) :      #telnet连接成功并且进入交换机特权用户模式
                print("连接成功！")
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
                print("恢复配置成功！退出连接！")
                tel.close()
            else :
                print("发生错误！")
                tel.close()
                
        else :
            print("提示：连接需要用户账号密码")
            error_root14 = Tkinter.Tk()          
            label = Tkinter.Label("The switch requires a login user name and password，please check!")
            label.pack()
            tel.close()
    
def hint_backup(event):
    root1 = Tkinter.Tk()
    root1.title(u"备份配置:")
    root1.geometry('500x500')
    #交换机配置参数文件路径显示标签
    label1 = Tkinter.Label(root1,text = u"请选择交换机的配置参数文件：",
                           wraplength = 300)
    label1.pack()
    #交换机配置参数文件路径输入文本框
    entry1 = Tkinter.Entry(root1,width = 50)
    #交换机配置参数文件路径输入确认按钮
    confirm1 = Tkinter.Button(root1,text = u"选择文件")
    default_dir = r"C:\Users\85125\Desktop"  # 设置默认打开目录
    def backup_1(event):
        fname1 = tkFileDialog.askopenfilename(title=u"选择文件"
                                              ,initialdir=(os.path.expanduser
                                                           (default_dir)))
        print fname1                         # 返回文件全路径
        #print tkFileDialog.askdirectory()  # 返回目录路径

        #重新选择参数文件，先清除文本框中内容再插入新的参数文件路径！
        entry1.delete(0,100)
        entry1.insert(0,fname1)
        #root2 = Tkinter.Tk()
        #root2.geometry('400x400')
    def backup_2(event):
        path = entry1.get()
        if (path == ''):
            tip1 =Tkinter.Label(root1,text = u"请选择正确的交换机参数文件",wraplength = 300) 
            tip1.pack()
            return 
        print path
        root2 = Tkinter.Tk()
        root2.title(u"选择交换机的配置文件备份目录")
        root2.geometry('500x500')
        date = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))    #设置时间
        bpath = date +" config"              #保存的备份文件默认文件夹名
        spath = "C:\\"+bpath     #交换机配置文件夹默认保存路径
        label2 = Tkinter.Label(root2,text = u"交换机的配置参数文件路径为："
                               ,wraplength = 300)
        label2.pack()
        label3 = Tkinter.Label(root2,text = path )
        label3.pack()
        label4 = Tkinter.Label(root2,text = u"交换机的配置文件默认保存在："
                               ,wraplength = 300)
        label4.pack()
        label5 = Tkinter.Label(root2,text = spath )
        label5.pack()
        entry2 = Tkinter.Entry(root2,width = 50)
        rechoose = Tkinter.Button(root2,text = u"重选")
        next2 = Tkinter.Button(root2,text = u"下一步")
        def backup_3(event):
            fname2 = tkFileDialog.asksaveasfilename(title=u"选择备份保存路径"
                                                  ,initialdir=(os.path.expanduser
                                                           (default_dir)),initialfile = bpath)
            entry2.delete(0,100) 
            entry2.insert(0,fname2)
            

        def backup_4(event):
            spath1 = entry2.get()        #交换机配置文件新的保存路径
            print path
            print spath1


            root3 = Tkinter.Tk()
            root3.geometry('500x500')
            label6 = Tkinter.Label(root3,text = u"交换机的配置文件备份路径为：",wraplength = 300)
            label6.pack()
            if (spath1 == '') :
                spath1 = spath
            label7 = Tkinter.Label(root3,text = spath1)
            label7.pack()
            label8 = Tkinter.Label(root3,text = u"从交换机配置参数文件中读取到的交换机为：",wraplength = 300)
            label8.pack()
            #从配置参数文件中读出所有的交换机名，可以选择全选交换机或者勾选其中的交换机来进行操作
            text1 = ScrolledText(root3,width = 30,height = 3) #备份的配置文件夹显示
            s_list = []                   #存放交换机名字的数组
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
                    print("备份完毕！")
                    label = Tkinter.Label(root3,text = u"备份完成！")
                    label.pack()
                
            confirm2 = Tkinter.Button(root3,text = u"确认")
            confirm2.bind("<Button-1>",backup_5)
            confirm2.pack()
            
            
        rechoose.bind("<Button-1>",backup_3)
        next2.bind("<Button-1>",backup_4)
        entry2.pack()
        rechoose.pack()
        next2.pack()
        root2.mainloop()
        
    next1 = Tkinter.Button(root1,text = u"下一步")

    def rechoose_dir(event):
        fname2 = tkFileDialog.asksaveasfilename(title=u"选择保存文件夹路径")
        print fname2                         # 返回文件全路径
        #print tkFileDialog.askdirectory()  # 返回目录路径
        spath = fname2

        #重新选择参数文件，先清除文本框中内容再插入新的参数文件路径！
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
    #修改路径为键盘输入！
    root1 = Tkinter.Tk()
    root1.title(u"恢复配置:")
    root1.geometry('500x500')
    #交换机配置参数文件路径显示标签
    label1 = Tkinter.Label(root1,text = u"请选择交换机的配置参数文件:",wraplength = 300)
    label1.pack()
    #交换机配置参数文件路径输入文本框
    entry1 = Tkinter.Entry(root1,width = 50)
    #交换机配置参数文件路径输入确认按钮
    choose1 = Tkinter.Button(root1,text = u"选择文件")
    default_dir = r"C:\Users\85125\Desktop"  # 设置默认打开目录
    def restore_1(event):

        fname1 = tkFileDialog.askopenfilename(title=u"选择文件"
                                              ,initialdir=(os.path.expanduser
                                                           (default_dir)))
        print fname1                         # 返回文件全路径
        #print tkFileDialog.askdirectory()  # 返回目录路径

        #重新选择参数文件，先清除文本框中内容再插入新的参数文件路径！
        entry1.delete(0,100)
        entry1.insert(0,fname1)
    def restore_2(event):
        path = entry1.get()
        if (path == ''):
            tip1 =Tkinter.Label(root1,text = u"请选择正确的交换机参数文件",wraplength = 300) 
            tip1.pack()
            return 
        print path
        root2 = Tkinter.Tk()
        root2.title(u"选择交换机的配置文件备份目录")
        root2.geometry('500x500')
        label2 = Tkinter.Label(root2,text = u"交换机的配置参数文件路径为："
                               ,wraplength = 300)
        label2.pack()
        label3 = Tkinter.Label(root2,text = path )
        label3.pack()
        
        #滚动框显示参数文件中读取到的交换机名
        text1 = ScrolledText(root2,width = 30,height = 3) #备份的配置文件夹显示
        s_list = []                   #存放交换机名字的数组
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
        label4 = Tkinter.Label(root2,text = u"请选择要恢复备份的交换机的配置文件保存目录："
                               ,wraplength = 300)
        label4.pack()
        entry2 = Tkinter.Entry(root2,width = 50)
        choose2 = Tkinter.Button(root2,text = u"选择文件夹目录")
        next2 = Tkinter.Button(root2,text = u"下一步")
        def restore_3(event):

            #fname_2 = tkFileDialog.askopenfilename(title=u"选择文件夹目录"
                                              #,initialdir=(os.path.expanduser
                                                           #(default_dir)))
            #print fname_2                         # 返回文件全路径
            fname2 =tkFileDialog.askdirectory(title=u"选择文件夹目录"
                                              ,initialdir=(os.path.expanduser
                                                           (default_dir)))
            print fname2  # 返回目录路径

            #重新选择参数文件，先清除文本框中内容再插入新的参数文件路径！
            entry2.delete(0,100)
            entry2.insert(0,fname2)

        def restore_4(event):
            root1.destroy()
            config_path2 = entry2.get()
            print config_path2
            with open(path) as json_file:         #从.json配置文件中获取交换机配置参数
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

                    #把获取到的交换机配置参数转换成字符串格式
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
                        print("该交换机对应备份好的配置文件不存在！")
                        break

            print("恢复备份配置完毕！")
            json_file.close()
            label5 = Tkinter.Label(root2,text = "The restore switch configuration has been completed!",wraplength = 300)
            label5.pack()

        choose2.bind("<Button-1>",restore_3)
        next2.bind("<Button-1>",restore_4)
        entry2.pack()
        choose2.pack()
        next2.pack()
        
    
    choose1.bind("<Button-1>",restore_1)
    next1 = Tkinter.Button(root1,text = u"下一步")
    next1.bind("<Button-1>",restore_2)
    entry1.pack()
    choose1.pack()
    next1.pack()
    root1.mainloop()
        
        

#主界面窗口设置
root = Tkinter.Tk()
root.title(u"交换机操作")
root.geometry('500x500')
frame1 = Tkinter.Frame(root)
button1 = Tkinter.Button(frame1,text = u"备份交换机配置",width = "25",height = "3")
button2 = Tkinter.Button(frame1,text = u"恢复交换机配置",width = "25",height = "3")
button1.bind("<Button-1>",hint_backup)
button2.bind("<Button-1>",hint_restore)
frame1.pack(expand = 1)
button1.pack()
button2.pack(pady = 70)
root.mainloop()
