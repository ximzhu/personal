# -*- coding: cp936 -*-
#代码需要完善：
#2.读取文件来获取交换机相关配置参数
#3.批量操作交换机
#4.界面

import telnetlib
import time
import os
import json

def enter_dir(date,tpath):
    print tpath
    spath = os.path.dirname(tpath)
    print spath
    config_path = spath+"\switch-config"
    print("配置文件保存在："+config_path)
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
    
    

#telnet连接交换机并保存配置文件或者恢复配置
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
                    print("特权密码错误！")
                    tel.close()
        else :
            print("提示：连接需要telnet登录密码")
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
                    tel.close()         #特权模式密码错误，退出连接！
            else :
                print("需要特权模式密码！")
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
            tel.close()

#telnet连接交换机恢复配置
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
                tel.close()
                
        else :
            print("提示：连接需要telnet登录密码")
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
            else :
                print("需要特权模式密码！")
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
                    else :
                        print("需要特权模式密码！")
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
            tel.close()

if __name__ == '__main__':
    date = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))    #设置时间
  
    choice = raw_input("请选择1.配置交换机；2.备份交换机【1/2】：")
    if (choice == '1') :
        tpath = os.path.realpath("backup.py")
        spath = os.path.dirname(tpath)
        path = spath+"\switch-arguments.json" #交换机参数文件名
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
        print("批量备份完毕！")
                
    elif (choice == '2') :
        tpath = os.path.realpath("backup.py")
        spath = os.path.dirname(tpath)
        config_path1 = spath +"/switch-config"
        flag = os.path.exists(config_path1)
        if (flag) :
            files = os.listdir(config_path1)
            for f in files:
                print f
        res_filename = raw_input("请输入你想要恢复配置的文件名：")
        path1 = spath+"\switch-arguments.json" #交换机参数文件名
        with open(path1) as json_file:         #从.json配置文件中获取交换机配置参数
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
                        print("配置文件不存在！")
                else :
                    print("配置文件夹不存在！")

                
        #res_filename =raw_input("请输入你想要恢复配置的文件名：") 
        #restore(res_filename)
