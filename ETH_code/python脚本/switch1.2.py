# -*- coding: cp936 -*-
'''
 * Copyright(C) 2005 Ruijie Network. All rights reserved.
 * switch.py          
 * Original Author:  zhuximin@ruijie.com.cn, 2018-1-12   
 *
 * 1.可批量或单一备份交换机配置,并相应保存
 * 2.可批量或单一恢复交换机配置.
 *
 * Histroy
 *  v1.2     zhuximin@ruijie.com.cn     2018-1-17
 *           选择交换机参数文件相关界面中添加了直接
 *           读取当前程序所在文件夹下的参数文件功能
 *  v1.1     zhuximin@ruijie.com.cn     2018-1-16
 *           修复了批量备份功能存在的BUG
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
    print("配置文件保存在："+time_path)
    flag1 = os.path.exists(time_path)             #是否存在备份文件夹

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
        
        
    print("正在进行telnet连接交换机，请稍候-----------------------------")
    
    try :
        tel = telnetlib.Telnet(hostip,port,timeout=5)
    except:
        print("Telnet连接失败！")
        err_root = Tkinter.Tk()
        err_root.title(u"错误提示")
        err_root.geometry('500x500')
        label1 = Tkinter.Label(err_root,text = switchname+u"Telnet建立连接失败，请退出！\n\n确认参数正"
                              u"确或检查网络配置是否正确!",wraplength = 300)
        label1.pack(pady = 50)
    
    time.sleep(2)
    filename =switchname+'_config.text'
    th = tel.read_very_eager()
    #判断telnet连接时的不同情况
    if ('Password' in th) :                       #telnet连接时需要telnet登录密码
        if (tel_flag) :
            tel.write(tel_password+enter)
            time.sleep(2)
            string1 = tel.read_very_eager()
            
            if ('#' in string1) :
                print("telnet连接成功！")
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
                print("备份成功！")
                print("-------------------------------------------------\n")
                return 1
            
            elif ('>' in string1) :
                tel.write('enable'+enter)
                tel.read_until('Password:')
                tel.write(en_password+enter)
                time.sleep(2)
                string4 = tel.read_very_eager()
                
                if ('#' in string4) :
                    print('Telnet连接成功！')
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
                    print("备份成功！")
                    print("-------------------------------------------------\n")
                    return 1
                else:
                    #进入特权模式密码错误，弹出错误提示窗口！
                    print("特权密码错误！")
                    error_root1 = Tkinter.Tk()
                    error_root1.geometry('500x500')
                    label = Tkinter.Label(error_root1,text = switchname+u"特权模式密码错误！")
                    label.pack()
                    tel.close()
                    return 0
            else:
                print("Telnet登录密码错误！\n")
                error_ = Tkinter.Tk()
                error_.geometry('500x500')
                label = Tkinter.Label(error_,text = switchname+u"Telnet登录密码错误！")
                label.pack()
                tel.close()
                return 0
        else :
            print("提示：连接需要telnet登录密码")
            error_root2 = Tkinter.Tk()
            error_root2.geometry('500x500')
            label = Tkinter.Label(error_root2,text =  switchname+u"连接需要telnet登录密码！")
            label.pack()
            tel.close()
            return 0

    elif ('>' in th) :                            #telnet连接时不需要登录密码，进入交换机的普通用户模式
        print("telnet连接成功!")
        tel.write('enable'+enter)
        time.sleep(2)                             #读取缓冲区前先让程序等待一定时间  
        string1 = tel.read_very_eager()
        if ('Password' in string1 ) :             #交换机设置了特权模式登录密码
            if (en_flag) :
                tel.write(en_password+enter)      #进入特权模式
                time.sleep(2)
                string2 = tel.read_very_eager()
                if ('#' in string2 ):
                    print("telnet连接成功！")
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
                    print("备份成功！")
                    print("-------------------------------------------------\n")
                    return 1
                else :
                    print("特权模式密码错误！")
                    error_root3 = Tkinter.Tk()
                    error_root3.geometry('500x500')
                    label = Tkinter.Label(error_root3,text = switchname+u" 特权模式密码错误！")
                    label.pack()
                    tel.close()                   #特权模式密码错误，退出连接！
                    return 0
            else :
                print("需要特权模式密码！")
                error_root4 = Tkinter.Tk()
                error_root4.geometry('500x500')
                label = Tkinter.Label(error_root4,text = switchname+u" 需要特权模式密码!")
                label.pack()
                tel.close()                       #没有输入特权模式密码，直接退出！
                return 0
        elif ('#' in string1) :
            print("telnet连接成功！")
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
            print("备份成功！")
            print("-------------------------------------------------\n")
            return 1
                
    elif ('#' in th) :                            #telnet连接时不需要登录密码，进入交换机的特权用户模式
        print("telnet连接成功！")
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
        print("备份成功！")
        print("-------------------------------------------------\n")
        return 1

    elif ('Username' in th) :                     #telnet连接时需要全局用户登录账号密码
        if (u_flag):
            tel.write(username+enter)
            tel.read_until('Password:')
            tel.write(u_password+enter)
            time.sleep(2)
            string = tel.read_very_eager()
            if ('Username' in string) :
                print("输入的用户账号密码错误！")
                tel.close()
            elif ('>' in string) :                #telnet连接成功并且进入交换机普通用户模式
                print("连接成功！")
                tel.write('enable'+enter)
                time.sleep(2)                     #读取缓冲区前先让程序等待一定时间  
                string1 = tel.read_very_eager()
                if ('Password' in string1 ) :     #交换机设置了特权模式登录密码
                    if (en_flag) :
                        tel.write(en_password+enter) 
                        time.sleep(2)
                        string2 = tel.read_very_eager()
                        if ('#' in string2 ) :
                            print("telnet连接成功！")
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
                            print("备份成功！")
                            print("-------------------------------------------------\n")
                            return 1
                        else :
                            print("特权模式密码错误！")
                            error_root5 = Tkinter.Tk()
                            error_root5.geometry('500x500')
                            label = Tkinter.Label(error_root5,text = switchname+u"特权模式密码错误！")
                            label.pack()
                            tel.close()           #特权模式密码错误，退出连接！
                            return 0
                    else :
                        print("需要特权模式密码！")
                        error_root5 = Tkinter.Tk()
                        error_root5.geometry('500x500')
                        label = Tkinter.Label(error_root5,text = switchname+u"需要特权模式密码!")
                        label.pack()
                        tel.close()
                        return 0
                elif ('#' in string1) :           #交换机没有设置特权模式登录密码
                    print("telnet连接成功！")
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
                    print("备份成功！")
                    print("-------------------------------------------------\n")
                    return 1
                else :                            #未知错误的简单处理
                    print("提示：发生错误！")
                    tel.close()
                    return 0
            elif ('#' in string) :                #telnet连接成功并且进入交换机特权用户模式
                print("telnet连接成功！")
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
                print("备份成功！")
                print("-------------------------------------------------\n")
                return 1
            else :
                print("发生错误！")
                error_root7 = Tkinter.Tk()
                error_root7.geometry('500x500')
                label = Tkinter.Label(error_root6,text = switchname+u"连接发生错误!")
                label.pack()
                tel.close()
                return 0
                
        else :
            print("提示：连接需要用户账号密码")
            error_root6 = Tkinter.Tk()
            error_root6.geometry('500x500')
            label = Tkinter.Label(error_root6,text = switchname+u"连接需要用户账号密码!")
            label.pack()
            tel.close()
            return 0

#telnet连接交换机恢复配置
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

    #设置时间    
    date = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))   

    print("现在时间是："+date)

    print("正在进行telnet连接交换机，请稍候-----------------------------")
    try :
        tel = telnetlib.Telnet(hostip,port,timeout=5)
    except:
        print("Telnet连接失败！")
        err_root = Tkinter.Tk()
        err_root.title(u"错误提示")
        err_root.geometry('500x500')
        label1 = Tkinter.Label(err_root,text = r_switchname+u"Telnet建立连接失败，请退出！\n\n确认参数正"
                              u"确或检查网络配置是否正确!",wraplength = 300)
        label1.pack(pady = 50)
        
    time.sleep(2)
    th = tel.read_very_eager()

    #判断telnet连接时的不同情况
    if ('Password' in th) :                       #telnet连接时需要telnet登录密码
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
                    print("恢复配置成功！退出连接！")
                    tel.close()
                    return 1
                else :
                    print("特权模式密码错误！")
                    error_root6 = Tkinter.Tk()
                    error_root6.geometry('500x500')
                    label = Tkinter.Label(error_root6,text = r_switchname+u"特权密码错误！")
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
                print("恢复配置成功！退出连接！")
                tel.close()
                return 1
            else :
                print("telnet登录密码错误！")
                error_root7 = Tkinter.Tk()
                error_root7.geometry('500x500')
                label = Tkinter.Label(error_root7,text =r_switchname+ u" telnet登录密码错误！")
                label.pack()
                tel.close()
                return 0
                
        else :
            print("提示：连接需要telnet登录密码")
            error_root8 = Tkinter.Tk()
            error_root8.geometry('500x500')
            label = Tkinter.Label(error_root8,text = r_switchname + u"连接需要telnet登录密码！")
            label.pack()
            tel.close()
            return 0
    elif ('>' in th) :                            #telnet连接时不需要登录密码，进入交换机的普通用户模式
        print("连接成功！")
        print("作为恢复文件的文件名为："+filename)
        tel.write('enable'+enter)
        time.sleep(2)                             #读取缓冲区前先让程序等待一定时间  
        string1 = tel.read_very_eager()
        if ('Password' in string1 ) :             #交换机设置了特权模式登录密码
            if (en_flag) :
                tel.write(en_password+enter)      #进入特权模式
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
                    print("恢复配置成功！退出连接！")
                    tel.close()
                    return 1
                else :
                    print("特权模式密码错误！")
                    error_root9 = Tkinter.Tk()
                    error_root9.geometry('500x500')
                    label = Tkinter.Label(error_root9,text = r_switchname + u" 特权模式密码错误！")
                    label.pack()
                    tel.close()
                    return 0
            else :
                print("需要特权模式密码！")
                error_root10 = Tkinter.Tk()
                error_root10.geometry('500x500')
                label = Tkinter.Label(error_root10,text = r_switchname +u"需要特权模式密码！")
                label.pack()
                tel.close()
                return 0
        elif ('#' in string1) :                   #交换机没有设置特权模式登录密码
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
            print("恢复配置成功！退出连接！")
            tel.close()
            return 1
        else :  
            print("输入的用户账号密码错误！")
            error_root10 = Tkinter.Tk()
            error_root10.geometry('500x500')
            label = Tkinter.Label(error_root10,text =r_switchname+ u"用户的账号密码错误!")
            label.pack()
            tel.close()
            return 0
    elif ('#' in th) :                            #telnet连接时不需要登录密码，进入交换机的特权用户模式
        print("telnet连接成功!")
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
        print("恢复配置成功！退出连接！")
        tel.close()
        return 1
    elif 'Username' in th :                       #telnet连接时需要全局用户登录账号密码
        if (u_flag):
            tel.write(username+enter)
            tel.read_until('Password:')
            tel.write(u_password+enter)
            time.sleep(2)
            string = tel.read_very_eager()
            if ('>' in string) :                  #telnet连接成功并且进入交换机普通用户模式
                print("连接成功！")
                tel.write('enable'+enter)
                time.sleep(2)                     #读取缓冲区前先让程序等待一定时间  
                string1 = tel.read_very_eager()
                if ('Password' in string1 ) :     #交换机设置了特权模式登录密码
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
                            print("恢复配置成功！退出连接！")
                            tel.close()
                            return 1
                        else :
                            print("特权模式密码错误！")
                            error_root11 = Tkinter.Tk()
                            error_root11.geometry('500x500')
                            label = Tkinter.Label(error_root11,text = r_switchname+ " 特权模式密码错误！")
                            label.pack()
                            tel.close()
                            return 0
                    else :
                        print("需要特权模式密码！")
                        error_root12 = Tkinter.Tk()
                        error_root12.geometry('500x500')
                        label = Tkinter.Label(error_root12,text = r_switchname +u"需要特权模式密码！")
                        label.pack()
                        tel.close()
                        return 0
                elif ('#' in string1) :           #交换机没有设置特权模式登录密码
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
                    print("恢复配置成功！退出连接！")
                    tel.close()
                    return 1
                else :  
                     print("输入的用户账号密码错误！")
                     error_root13 = Tkinter.Tk()
                     error_root13.geometry('500x500')
                     label = Tkinter.Label(error_root13,text =r_switchname+ u"用户账号密码错误！ ")
                     label.pack()
                     tel.close()
                     return 0
            elif ('#' in string) :                #telnet连接成功并且进入交换机特权用户模式
                print("连接成功！")
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
                print("恢复配置成功！退出连接！")
                tel.close()
                return 1
            else :
                print("发生错误！")
                tel.close()
                return 0
                
        else :
            print("提示：连接需要用户账号密码")
            error_root14 = Tkinter.Tk()
            error_root14.geometry('500x500')
            label = Tkinter.Label(r_switchname+u"连接需要用户账号密码！")
            label.pack()
            tel.close()
            return 0
    
def hint_backup(event):
    root1 = Tkinter.Tk()
    root1.title(u"备份配置:")
    root1.geometry('500x500')

    #交换机配置参数文件路径显示标签
    label1 = Tkinter.Label(root1,text = u"请选择交换机的配置参数文件：(注意：交换机的配置参数文件必须为.json文件"
                           u",具体内容请参照程序文件夹下的样例json配置参数文件)",wraplength = 300,justify='left')
    label1.pack(pady = 40)

    #交换机配置参数文件路径输入文本框
    entry1 = Tkinter.Entry(root1,width = 50)

    #判断程序文件夹目录下是否存在存放读取参数文件的记录文本
    ScriptPath = os.path.split( os.path.realpath( sys.argv[0] ) )[0]            #获取当前脚本所在文件夹目录
    print ScriptPath
    f = 0

    for file in os.listdir(ScriptPath):
        if ('.json' in file):
            path = ScriptPath+'\\'+file
            f = 1
            print path
            addlbl = Tkinter.Label(root1,text = u"从当前脚本文件夹目录下读取到参数文件：")
            addlbl.pack()
            entry1.insert(0,path)
            break

    if (not f) :
        addlbl2 = Tkinter.Label(root1,text = u"从当前脚本文件夹目录下没有读取到参数文件,请点击下方查找按钮来选择文件")
        addlbl2.pack()
        confirm1 = Tkinter.Button(root1,text = u"查找",width = 10)

    else:
        #交换机配置参数文件路径输入确认按钮
        confirm1 = Tkinter.Button(root1,text = u"重选",width = 10)
        
    default_dir = r"C:\Users\85125\Desktop"       #设置默认打开目录

    def backup_1(event):
        #打开的参数文件默认文件名应该是.json文件
        fname1 = tkFileDialog.askopenfilename(title=u"选择交换机参数文件"
                                              ,initialdir=(os.path.expanduser
                                                           (default_dir)),)
        print fname1                              # 返回文件全路径

        #重新选择参数文件，先清除文本框中内容再插入新的参数文件路径！
        entry1.delete(0,100)
        entry1.insert(0,fname1)
        
    def backup_2(event):
        path = entry1.get()

        if (path == '' or not('.json' in path) ):
            tip1 =Tkinter.Label(root1,text = u"请选择正确的交换机参数文件",wraplength = 300) 
            tip1.pack()
            return

        root1.destroy()
        root2 = Tkinter.Tk()
        root2.title(u"选择交换机的配置文件备份目录")
        root2.geometry('500x500')
        date = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))    
        bpath = date +"_config"                   #保存的备份文件默认文件夹名
        spath = os.path.dirname(path)+"/"+bpath   #交换机配置文件夹默认保存路径
        label2 = Tkinter.Label(root2,text = u"交换机的配置参数文件路径为："
                               ,wraplength = 300)
        label2.pack(pady = 30)
        label3 = Tkinter.Label(root2,text = path )
        label3.pack()
        label4 = Tkinter.Label(root2,text = u"交换机的配置文件默认保存在：\n"
                               u"(注意：将在该文件夹下生成相应的交换机配置文件)"
                               ,wraplength = 300)
        label4.pack(pady = 30)
        label5 = Tkinter.Label(root2,text = spath )
        label5.pack()
        entry2 = Tkinter.Entry(root2,width = 62)
        rechoose = Tkinter.Button(root2,text = u"重选",width = 10)
        next2 = Tkinter.Button(root2,text = u"下一步",width = 10)

        def backup_3(event):
            fname2 = tkFileDialog.asksaveasfilename(title=u"选择备份保存路径：",
                                                    initialdir=(os.path.expanduser
                                                                (default_dir)),
                                                    initialfile = bpath)
            entry2.delete(0,100) 
            entry2.insert(0,fname2)
            
        def backup_4(event):
            spath1 = entry2.get()                 #交换机配置文件新的保存路径
            print path
            print spath1
            root2.destroy()
            root3 = Tkinter.Tk()
            root3.geometry('500x500')
            label6 = Tkinter.Label(root3,text = u"交换机的配置文件备份路径为：",wraplength = 300)
            label6.pack()

            if (spath1 == '') :
                spath1 = spath

            label7 = Tkinter.Label(root3,text = spath1)
            label7.pack()
            label8 = Tkinter.Label(root3,text = u"从交换机配置参数文件中读取到的交换机为：(可点击交换机名选择交换机是否被选中，蓝色状态为选中)",wraplength = 300)
            label8.pack()

            #Listbox复选来进行交换机勾选操作！
            frame3 =Tkinter.Frame(root3)
            frame3.pack()
            
            #Listbox来存放所有交换机名称
            lb1 = Listbox(frame3,width = 60,height = 5,selectmode = MULTIPLE)   
            sl1 = Scrollbar(frame3,command = lb1.yview)    
            lb1.configure(yscrollcommand = sl1.set)
            sl1.pack(side = RIGHT,fill = Y)

            #打开参数文件读取交换机,并把交换机名称插入Listbox
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
            all_button = Tkinter.Button(root3,text = u"全选",width = 10)
            all_button.bind("<Button-1>",all_select)
            all_button.pack()

            def backup_5(event):
                result1.insert(END,u"正在执行，请稍等...（不要重复点击！）\n")
                result1.update()                  #用函数先刷新一下界面提示进度！
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

                        if (lb1.get(i) == switchname) :                         #交换机名称匹配
                            bools = lb1.selection_includes(i)

                            if (bools) :                                        #交换机被勾选
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
                                res1 = switchname + u"备份成功！\n"

                                if (res_num):
                                    result1.insert(END,res1)
                                    confirm2.config(state="disable")

                                else:
                                    tip1 = u"配置文件备份失败！请检查参数文件或相关环境配置！"
                                    result1.insert(END,tip1)
                                    
                            
                        i = i + 1
                    
                    print("备份完毕！\n")
                    if (allselected == 0) :
                        nochoose = u"请至少选中一台交换机来进行操作！"
                        result1.insert(END,nochoose)
                json_file.close()
                
            confirm2 = Tkinter.Button(root3,text = u"确认",width = 10)
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
        
    next1 = Tkinter.Button(root1,text = u"下一步",width = 10)

    def rechoose_dir(event):
        fname2 = tkFileDialog.asksaveasfilename(title=u"选择配置文件保存路径")
        print fname2                         # 返回文件全路径
        spath = fname2

        #重新选择参数文件，先清除文本框中内容再插入新的参数文件路径！
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
    root1.title(u"恢复配置:")
    root1.geometry('500x500')

    #交换机配置参数文件路径显示标签
    label1 = Tkinter.Label(root1,text = u"请选择交换机的配置参数文件：\n(注意：交换机的配置参数文件必须为.json文件"
                           u",具体内容请参照程序文件夹下的样例json配置参数文件)",wraplength = 300)
    label1.pack()
    #交换机配置参数文件路径输入文本框
    entry1 = Tkinter.Entry(root1,width = 50)

    #判断程序文件夹目录下是否存在存放读取参数文件的记录文本
    ScriptPath = os.path.split( os.path.realpath( sys.argv[0] ) )[0]            #获取当前脚本所在文件夹目录
    print ScriptPath
    f = 0

    for file in os.listdir(ScriptPath):
        if ('.json' in file):
            path = ScriptPath+'\\'+file
            f = 1
            print path
            addlbl = Tkinter.Label(root1,text = u"从当前脚本文件夹目录下读取到参数文件：")
            addlbl.pack()
            entry1.insert(0,path)
            break

    if (not f) :
        addlbl2 = Tkinter.Label(root1,text = u"从当前脚本文件夹目录下没有读取到参数文件,请点击下方查找按钮来选择文件")
        addlbl2.pack()
        choose1 = Tkinter.Button(root1,text = u"查找",width = 10)

    else:
        #交换机配置参数文件路径输入确认按钮
        choose1 = Tkinter.Button(root1,text = u"重选",width = 10)
    
    default_dir = r"C:\Users\85125\Desktop"       #设置默认打开目录

    def restore_1(event):
        fname1 = tkFileDialog.askopenfilename(title=u"选择文件"
                                              ,initialdir=(os.path.expanduser
                                                           (default_dir)))
        print fname1                              #返回文件全路径

        #重新选择参数文件，先清除文本框中内容再插入新的参数文件路径！
        entry1.delete(0,100)
        entry1.insert(0,fname1)

    def restore_2(event):
        path = entry1.get()
        if (path == '' or not('.json' in path) ):
            tip1 =Tkinter.Label(root1,text = u"请选择正确的交换机参数文件",wraplength = 300) 
            tip1.pack()
            return 
        print path
        root1.destroy()
        root2 = Tkinter.Tk()
        root2.title(u"恢复配置：")
        root2.geometry('500x500')
        label2 = Tkinter.Label(root2,text = u"交换机的配置参数文件路径为："
                               ,wraplength = 300)
        label2.pack()
        label3 = Tkinter.Label(root2,text = path )
        label3.pack()
        lab = Tkinter.Label(root2,text = u"从交换机配置参数文件中读取到的交换机为：(可点击交换机名选择交换机是否被选中，蓝色状态为选中)",wraplength = 300)
        lab.pack()

        frame3 =Tkinter.Frame(root2)
        frame3.pack()
            
        #Listbox来存放所有交换机名称
        lb1 = Listbox(frame3,width = 60,height = 5,selectmode = MULTIPLE)   
        sl1 = Scrollbar(frame3,command = lb1.yview)
        #lb1['yscrollcommand'] = sl1.set
        lb1.configure(yscrollcommand = sl1.set)
        sl1.pack(side = RIGHT,fill = Y)

        #打开参数文件读取交换机,并把交换机名称插入Listbox
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
        all_button = Tkinter.Button(root2,text = u"全选",width = 10)
        all_button.bind("<Button-1>",all_select)
        all_button.pack()
        
        label4 = Tkinter.Label(root2,text = u"请选择要恢复备份的交换机相应配置文件的保存文件夹："
                               ,wraplength = 300)
        label4.pack(pady = 20)
        entry2 = Tkinter.Entry(root2,width = 62)
        choose2 = Tkinter.Button(root2,text = u"选择目录",width = 10)
        next2 = Tkinter.Button(root2,text = u"确认",width = 10)

        def restore_3(event):
            fname2 =tkFileDialog.askdirectory(title=u"选择文件夹"
                                              ,initialdir=(os.path.expanduser
                                                           (default_dir)))
            print fname2  # 返回目录路径

            #重新选择文件夹，先清除文本框中内容再插入新的文件夹路径！
            entry2.delete(0,100)
            entry2.insert(0,fname2)
            
        def restore_4(event):
            config_path2 = entry2.get()
            print config_path2
            exits = os.path.exists(config_path2)
            if (not exits):
                result1.insert(END,u"请选择正确的文件夹目录！\n")
                return
            result1.insert(END,u"正在执行，请稍等...\n")
            result1.update()                      
            result1.delete(1.0, END)

            with open(path) as json_file:         #从.json配置文件中获取交换机配置参数
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

                    #把获取到的交换机配置参数转换成字符串格式
                    r_switchname = str(switchname2)
                    r_hostip = str(hostip2)
                    r_port = str(port2)
                    r_telpassword = str(tel_password2)
                    r_username = str(username2)
                    r_upassword = str(u_password2)
                    r_enpassword = str(en_password2)
                
                    print lb1.get(i)
                    print lb1.selection_includes(i)
                    if (lb1.get(i) == r_switchname) :                           #交换机名称匹配
                        bools = lb1.selection_includes(i)
                        if (bools) :                                            #交换机被勾选
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
                                    res1 = r_switchname +u" 交换机恢复备份完成\n"
                                    tip3 = r_switchname +u" 交换机恢复备份失败！\n"
                                    if (res_num2):
                                        result1.insert(END,res1)
                                    else:
                                        result1.insert(END,tip3)
                                    print("------------------------------------------\n")
                                    flag3 = 1
                                    break

                            if (not flag3 ) :
                                print(r_switchname+":该交换机对应备份好的配置文件不存在！")
                                res2 = r_switchname+u":该交换机对应备份好的配置文件不存在！\n"
                                result1.insert(END,res2)
                                continue
                if (not alls) :
                    nochoose = u"请至少选中一台交换机来进行操作！"
                    result1.insert(END,nochoose)

            print("恢复备份配置完毕！")
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
    next1 = Tkinter.Button(root1,text = u"下一步",width = 10)
    next1.bind("<Button-1>",restore_2)
    entry1.pack()
    choose1.pack()
    next1.pack(pady = 30)
    root1.mainloop()

if __name__ == '__main__':                        #主界面窗口设置
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


