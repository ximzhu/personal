# -*- coding: cp936 -*-

import telnetlib
import time

def Telnet(hostip,port,tpassword,tftphost,filename,filetype):
    enter = '\n'
    tel = telnetlib.Telnet(hostip,port)
    print("正在连接交换机请稍候-------------------------------")
    tel.read_until('Password:')
    tel.write(tpassword+enter)
    #tel.read_until('switch>')
    #tel.write('enable'+enter)        #进入特权模式并回车
    #tel.read_until('Password：')
    #tel.write(en_password+enter)   #输入特权模式密码
    #tel.read_until('#')
    if (tel.read_until('#')):
        print("telnet连接成功并且已经进入特权模式！")
        print("你希望程序接下来执行哪个动作？")
        print("1.备份交换机配置")
        print("2.恢复交换机配置")
        choice1 = raw_input('请选择执行动作相应的数字:')
        if (choice1 == '1'):
            print("你希望备份交换机的哪个配置文件？")
            print("1.running-conifg")
            print("2.startup-config")
            choice2 = raw_input("请选择你想要备份的交换机配置文件：")
            if (choice2 == '1'):
                print("开始备份交换机配置文件running-config")
                tel.write('copy running-config tftp://'+tftphost+'/'+filename+'running-config'+filetype+enter)
                #tel.read_until('Address of remote host []?')
                #print("正在输入tftp服务器端ip地址")
                #tel.write(tftp_hostip+enter)
                #tel.read_until('Destination filename []?')
                #print("正在输入备份的配置文件的文件名")
                #tel.write(filename+enter)
                #tel.read_until('Transmission finished,')
                tel.read_until('Copy success.')
                print("备份成功！请在tftp服务器上查看相关信息.")
            elif (choice2 == '2'):
                print("开始备份交换机配置文件startup-config")
                tel.write('copy startup-config tftp://'+tftphost+'/'+filename+'startup-config'+filetype+enter)
                tel.read_until('Copy success.')
                print("备份成功！请在tftp服务器上查看相关信息.")
            else:
                print("输入错误！")
        elif (choice1 == '2'):
            print("你希望使用哪个配置文件来恢复交换机配置？")
            filename1 = raw_input("请输入文件名：")
            print(filename1)
            tel.write('copy tftp://'+tftphost+'/'+filename1+filetype+' running-config'+enter)
            tel.read_until('[Y/N]:')
            tel.write('y'+enter)
            tel.read_until('Copy success.')
            print("恢复配置成功！")
            #print("你希望把这个配置保存到startup-config中去吗？")
        else:
            print("输入错误！")
        print("退出telnet连接")
        tel.write('exit'+enter)
    else:
        print("telnet连接交换机失败！")

hostip = '192.168.1.3'          #telnet交换机的ip
port = '23'                     #telnet端口号
tpassword = '123456'            #交换机telnet登录密码
tftphost = '192.168.1.10'       #tftp服务器ip地址
filetype = '.txt'               #配置文件的保存文件类型
date = time.strftime('%Y%m%d',time.localtime(time.time()))    #设置时间
filename = date+'-switch-'                           #保存的配置文件名前缀

print("为了保证后续动作都能够成功执行，请先确认以下内容：")
print("1.交换机开启了telnet功能并对其进行了适当的配置：")
print("  1.1交换机只设置了telnet登录密码而没有账号；")
print("  1.2telnet连接成功之后直接进入交换机的特权模式；")
print("2.交换机支持tftp传输文件的功能，并且注意交换机使用该功能时所需要命令的格式可能会因为不同交换机而有不同")
flag = raw_input("确认完毕？【Y/N】：")
if ((flag == 'Y') or (flag == 'y')):
    print('准备开始登录设备,当前时间'+date)
    #hostip = raw_input("请输入你想要连接的交换机的ip地址:")
    #port = raw_input("请输入你想要连接的交换机的端口:")
    #tpassword = raw_input("请输入你想要连接的交换机的telnet登录密码")
    #tftphost = raw_input("请输入你的tftp服务器ip地址")
    #filetype = raw_input("你想要保存的配置文件格式：")
    Telnet(hostip,port,tpassword,tftphost,filename,filetype)
else:
    flag1 = raw_input("是否选择退出程序【Y/N】：")
    if ((flag1 == 'Y' ) or (flag1 == 'y')):
        os._exit()
    elif ((flag1 == 'N') or (flag1 == 'n')):
        print("请继续确认！")
        
