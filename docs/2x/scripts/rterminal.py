#qpy:console

#--------Kivy Project Remote terminal Files
#main.py
main_py='''#coding=utf-8
#qpy:kivy

import os
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import WindowBase
from kivymd.theming import ThemeManager


def readsettings():
    pyhome=os.popen('echo $PYTHONHOME').read().strip()
    pyfile=os.path.join(pyhome,'bin/online.py')
    if os.path.exists(pyfile):
        with open(pyfile) as f:
            r=f.read()
        hostname=re.findall("env.hosts=\['(.*?)'\]",r)[0]
        password=re.findall("env.password='(.*?)'",r)[0]
        shellcommand=re.findall("run\('(.*?)'\)#shell",r)[0]
        runcommand=re.findall("run\('(.*?) \%s && rm -rf \%s'%\(dfile,dfile\)\)#run",r)[0]
    else:
        hostname='root@127.0.0.1:22'
        password='passwd'
        shellcommand='python'
        runcommand='python'
    return hostname,password,shellcommand,runcommand

def writesettings(hostname,password,shellcommand,runcommand):
    pyhome=os.popen('echo $PYTHONHOME').read().strip()
    pyfile=os.path.join(pyhome,'bin/online.py')
    with open('online.py') as f:
        r=f.read()
    old_hostname=re.findall("env.hosts=\['.*?'\]",r)[0]
    old_password=re.findall("env.password='.*?'",r)[0]
    old_shellcommand=re.findall("run\('.*?'\)#shell",r)[0]
    old_runcommand=re.findall("run\('.*? \%s && rm -rf \%s'%\(dfile,dfile\)\)#run",r)[0]
    r=r.replace(old_hostname,"env.hosts=['%s']"%hostname.strip())
    r=r.replace(old_password,"env.password='%s'"%password.strip())
    r=r.replace(old_shellcommand,"run('%s')#shell"%shellcommand.strip())
    r=r.replace(old_runcommand,"run('"+runcommand.strip()+" %s && rm -rf %s'%(dfile,dfile))#run")
    with open(pyfile,'w') as f:
        f.write(r)
    
def writesh(status):
    pyhome=os.popen('echo $PYTHONHOME').read().strip()
    pyfile1=os.path.join(pyhome,'bin/qpython.sh')
    pyfile2=os.path.join(pyhome,'bin/qpython-android5.sh')
    if status:
        with open('new_qpython.sh') as f:
            r1=f.read()
        with open('new_qpython-android5.sh') as f:
            r2=f.read()
    else:
        with open('qpython.sh') as f:
            r1=f.read()
        with open('qpython-android5.sh') as f:
            r2=f.read()
    with open(pyfile1,'w') as f:
        f.write(r1)
    with open(pyfile2,'w') as f:
        f.write(r2)

def readsh():
    pyhome=os.popen('echo $PYTHONHOME').read().strip()
    pyfile1=os.path.join(pyhome,'bin/qpython.sh')
    pyfile2=os.path.join(pyhome,'bin/qpython-android5.sh')
    with open(pyfile1) as f:r1=f.read()
    with open(pyfile2) as f:r2=f.read()
    if 'online.py' in r1 and 'online.py' in r2:
        return True
    else:
        return False

    
class MyLayout(BoxLayout):
    def write(self):
        status=self.ids.status.text
        dutton=self.ids.action.text
        if 'local' in status:
            hostname=self.ids.hostname.text
            password=self.ids.password.text
            shellcommand=self.ids.shellcommand.text
            runcommand=self.ids.runcommand.text
            writesettings(hostname,password,shellcommand,runcommand)
            writesh(True)
            self.ids.status.text='Status: remote running'
            self.ids.action.text='run local'
        else:
            writesh(False)
            self.ids.status.text='Status: local running'
            self.ids.action.text='run remote'


class MainApp(App):
    theme_cls=ThemeManager()
    def build(self):
        self.theme_cls.theme_style='Dark'
        return MyLayout()
    def on_start(self):
        status=readsh()
        hostname,password,shellcommand,runcommand=readsettings()
        self.root.ids.hostname.text=hostname
        self.root.ids.password.text=password
        self.root.ids.shellcommand.text=shellcommand
        self.root.ids.runcommand.text=runcommand
        if status:
            self.root.ids.status.text='Status: remote running'
            self.root.ids.action.text='run local'
        else:
            self.root.ids.status.text='Status: local running'
            self.root.ids.action.text='run remote'
        

if __name__=='__main__':
    MainApp().run()'''
#main.kv
main_kv='''#: import MDLabel kivymd.label.MDLabel
#: import MDTextField kivymd.textfields.MDTextField
#: import MDRaisedButton kivymd.button.MDRaisedButton

<MyLayout>:
    orientation:'vertical'
    padding:(36,36)
    MDLabel:
        id:status
        size_hint_y:None
        height:'48dp'
        color:(1,1,1,1)
    MDLabel:
        size_hint_y:None
        height:'3dp'
    MDTextField:
        id:hostname
        hint_text:'hostname(user@ip:port)'
        text:'root@127.0.0.1:22'
        size_hint:(1,0.3)
    Label:
        size_hint_y:None
        height:'3dp'
    MDTextField:
        id:password
        hint_text:'password'
        size_hint:(1,0.3)
    Label:
        size_hint_y:None
        height:'3dp'
    MDTextField:
        id:shellcommand
        hint_text:'shell command'
        text:'python'
        size_hint:(1,0.3)
    Label:
        size_hint_y:None
        height:'3dp'
    MDTextField:
        id:runcommand
        hint_text:'run program command'
        text:'python'
        size_hint:(1,0.3)
    Label:
        size_hint_y:None
        height:'3dp'
    MDRaisedButton:
        id:action
        size_hint:(1,0.3)
        on_release:root.write()
    MDLabel:'''

#online.py
online_py='''#coding=utf-8
import os
import sys
from fabric.api import env,run,put,output
pyhome=os.popen('echo $PYTHONHOME').read().strip()
os.chdir(pyhome)
env.hosts=['root@127.0.0.1:22']
env.password='12345678'
output['running']=False
output['status']=False
output['aborts']=False
env.output_prefix=False
def shell():
    run('python')#shell
def runfile(sfile):
    dfile=sfile.split('/')[-1]
    put(sfile,dfile)
    run('python %s && rm -rf %s'%(dfile,dfile))#run
if __name__ == '__main__':
    argv=[i for i in sys.argv if i]
    if len(argv) < 2:
        os.system('fab -f bin/online.py shell')
    else:
        os.system('fab -f bin/online.py runfile:%s'%argv[1])
'''

#qpython-android5.sh
qpy_droid_sh='''#!/system/bin/sh
DIR=${0%/*}
. $DIR/init.sh && $DIR/python-android5 "$@" && $DIR/end.sh

'''

#new_qpython-android5.sh
new_qpy_droid_sh='''#!/system/bin/sh
DIR=${0%/*}
. $DIR/init.sh && $DIR/python-android5 $DIR/online.py "$@" && $DIR/end.sh

'''

#qpython.sh
qpy_sh='''#!/system/bin/sh
DIR=${0%/*}
. $DIR/init.sh && $DIR/python "$@" && $DIR/end.sh

'''

#new_qpython.sh
new_qpy_sh='''#!/system/bin/sh
DIR=${0%/*}
. $DIR/init.sh && $DIR/python $DIR/online.py "$@" && $DIR/end.sh

'''

__doc__ = """
Remote terminal for QPython, the pythonic tool for remote execution and deployment
@version: 0.1
@Author: lr
"""
__title__ = "Remote terminal for QPython"

import os,sys,qpy

ROOT    = qpy.home

try:
    import androidhelper
    droid = androidhelper.Android()
except:
    pass

def writerterminalfiles():
    os.chdir(os.path.join(ROOT,'projects'))
    try:
        os.mkdir('rterminal')
        os.chdir('rterminal')
    except:
        os.chdir('rterminal')

    filedict = {'main.py':main_py, 'main.kv':main_kv, 'online.py':online_py, 'qpython-android5.sh':qpy_droid_sh, 'new_qpython-android5.sh':new_qpy_droid_sh, 'qpython.sh':qpy_sh, 'new_qpython.sh':new_qpy_sh}
    for i in filedict:
        with open(i,'w') as f:
            f.write(filedict[i])


def first_welcome():
    msg = __doc__+"\n\n"\
        +"To use rterminal, you need install fabric-qpython,kivymd-qpython first"
    droid.dialogCreateAlert(__title__, msg)
    droid.dialogSetPositiveButtonText('OK')
    droid.dialogSetNegativeButtonText('NO')
    droid.dialogShow()
    response = droid.dialogGetResponse().result
    if response['which'] == 'positive':
        #droid.dialogCreateSpinnerProgress(title, "Installing ...")
        os.system(sys.executable+" "+sys.prefix+"/bin/pip install fabric-qpython -i  http://qpypi.qpython.org/simple  --extra-index-url  https://pypi.python.org/simple/")
        os.system(sys.executable+" "+sys.prefix+"/bin/pip install kivymd-qpython -i  http://qpypi.qpython.org/simple  --extra-index-url  https://pypi.python.org/simple/")
        writerterminalfiles()
        #droid.dialogDismiss()

        message = 'Ok! run rterminal project and set ssh config'
        droid.dialogCreateAlert(__title__, message)
        droid.dialogSetPositiveButtonText('OK')
        droid.dialogShow()
        sys.exit()

    else:
        sys.exit()

def init_parameters():
    message = 'Ok! run rterminal project and set ssh config'
    droid.dialogCreateAlert(__title__, message)
    droid.dialogSetPositiveButtonText('OK')
    droid.dialogShow()
    sys.exit()


try:
    from fabric.api import env,run
    import kivymd
    os.chdir(os.path.join(ROOT,'projects/rterminal'))
except:
    first_welcome()
else:
    init_parameters()



def test():
    run('python -V')

def op(msg):
    print(msg)

def modcmd(arg):
  os.system(sys.executable+" "+sys.prefix+"/bin/"+arg)




