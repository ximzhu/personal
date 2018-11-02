# -*- coding: cp936 -*-

import telnetlib
import time

def string_switch(x,y,z):
    with open(x, "r") as f:
        #readlines以列表的形式将文件读出
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
    print("请根据提示输入您想要操作的交换机的相关配置参数信息，并按下回车键结束：")
    while (1) :
        hostip = raw_input("交换机ip地址：")
        port = raw_input("交换机telnet端口：")
        fir = raw_input("请选择是否输入交换机全局登录用户账号密码【Y/N】：")
        if ((fir == 'Y') or (fir == 'y')):
            username = raw_input("请输入交换机登录用户账号：")
            u_password = raw_input("请输入交换机登录用户密码：")
            u_flag = 1
        elif ((fir == 'N') or (fir == 'n')) :
            u_flag = 0                    #用来检测是否输入了用户账号密码
        else :
            print("输入错误")
            return
        sec = raw_input("请选择是否输入交换机telnet登录密码【Y/N】：")
        if ((sec == 'Y') or (sec == 'y')) :
            tel_password = raw_input("交换机telnet登录密码：")
            tel_flag = 1
        elif ((sec == 'N') or (sec == 'n')) :
            tel_flag = 0                  #用来检测是否输入了telnet登录密码
        else :
            print("输入错误")
            return
        trd = raw_input("请选择是否输入交换机特权模式密码【Y/N】：")
        if ((trd == 'Y') or (trd == 'y')) :
            en_password = raw_input("交换机特权模式密码：")
            en_flag = 1
        elif ((trd == 'N') or (trd == 'n')) :
            en_flag = 0                  #是否输入了特权模式密码
        else :
            print("输入错误")
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
        flag = raw_input("请确认您以上信息并输入【Y】，否则您需要重新输入以上信息：")
        if ((flag == 'Y') or (flag == 'y')) :
            break

    print("正在进行telnet连接交换机，请稍候-----------------------------")
    tel = telnetlib.Telnet(hostip,port,timeout=5)
    time.sleep(3)
    th = tel.read_very_eager()

    #判断telnet连接时的不同情况
    if ('Password' in th) :  #telnet连接时需要telnet登录密码
        if (tel_flag) :
            tel.write(tel_password+enter)
            #后续动作补充
        else :
            print("提示：连接需要telnet登录密码")
            tel.close()
    elif ('>' in th) :                 #telnet连接时不需要登录密码，进入交换机的普通用户模式
        print("telnet连接成功!")
        #后续动作补充
    elif ('#' in th) :                #telnet连接时不需要登录密码，进入交换机的特权用户模式
        print("telnet连接成功！")
        #后续动作补充
    elif 'Username' in th :#telnet连接时需要全局用户登录账号密码
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
                date = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))    #设置时间
                filename = '2017-12-27 10-28-45 config.txt'
                print("现在时间是："+date)
                print("作为恢复文件的文件名为："+filename)
                tel.write('enable'+enter)
                time.sleep(2)       #读取缓冲区前先让程序等待一定时间  
                string1 = tel.read_very_eager()
                if ('Password' in string1 ) :    #交换机设置了特权模式登录密码
                    if (en_flag) :
                        tel.write(en_password+enter) #进入特权模式
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
                        print("需要特权模式密码！")
                        tel.close()
                elif ('#' in string1) :          #交换机没有设置特权模式登录密码
                    #进入特权模式
                    #待补充
                    print("补充")
                else :                           #未知错误的简单处理
                    print("提示：发生错误！")
                    tel.close()
            elif ('#' in string) :      #telnet连接成功并且进入交换机特权用户模式
                print("连接成功！")
                #补充
            else :
                print("发生错误！")
                tel.close()
                
        else :
            print("提示：连接需要用户账号密码")
            tel.close()
            
string1 = " --More--           "
restore()
