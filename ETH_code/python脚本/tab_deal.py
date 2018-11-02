import os
filename = 'x.text'
f=open(filename,'r')
string = f.readlines()
print string
while('\n' in string):
        string.remove('\n')
print string
f.close()
os.remove(filename)
with open(filename,'ab')as fw:
    for i in range(len(string)):
        line = string[i]
        fw.write(line)
    fw.close()
