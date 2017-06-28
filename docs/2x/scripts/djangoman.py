#qpy:console
__doc__ = """
QPython django manage tool , you can use it to create project, syncdb and create suerpuser ....

@version: 0.9
@Author: River
"""

__webapptpl__ = "#"+"""qpy:webapp:Hello Django
#qpy://127.0.0.1:8000/

import os,sys
mf = os.path.dirname(__file__)+'/manage.py'

os.system(sys.executable+" "+mf+' runserver')
"""

import os,os.path,sys

os.chmod = lambda x,y: True

ROOT    = "/sdcard/qpython/projects"
PROJECT = None

def op(msg):
    print(msg)

def executearg(opt, arg):
    global PROJECT
    if arg=='ls':
        lsfiles()
    else:
        if opt=='choose_project':
            if arg=='ls':
                lsfiles()
            elif os.path.exists(ROOT+'/'+arg):
                PROJECT = arg
                os.chdir(ROOT+"/"+arg)
                op("Enter the django project %s\n" % arg)
            else:
                op("QPY> Django project not exist, do you want to create it ?")
                opt=raw_input("QPY> yes/no:")
                if opt=='yes':
                    createproject(arg)

        elif opt=='opt_project':
            if arg=='syncdb':
                syncdb()
            if arg=='createsuperuser':
                createsuperuser()
            if arg=='startapp':
                startapp()
            if arg=='runserver':
                runserver()

def lsfiles():
    op("[Files in %s]" % os.getcwd())
    os.system("ls")
    op("")
    opt=raw_input("")

def syncdb():
    os.system(sys.executable+" "+ROOT+'/'+PROJECT+'/manage.py'+' makemigrations')
    os.system(sys.executable+" "+ROOT+'/'+PROJECT+'/manage.py'+' migrate')

def createsuperuser():
    os.system(sys.executable+" "+ROOT+'/'+PROJECT+'/manage.py'+' createsuperuser')

def startapp():
    op("QPY> Input the app name ")
    opt=raw_input("QPY> ")

    os.system(sys.executable+" "+ROOT+'/'+PROJECT+'/manage.py'+' startapp '+opt)

def runserver():
    opt=raw_input("QPY> Input the <host:port> (default:127.0.0.1:8000) ")
    os.system(sys.executable+" "+ROOT+'/'+PROJECT+'/manage.py'+' runserver '+opt)



def createproject(arg):
    from django.core import management
    global PROJECT
    argv = [__file__, 'startproject', arg]
    management.execute_from_command_line(argv)

    PROJECT = arg
    with open(ROOT+'/'+PROJECT+"/main.py",'w') as d:
        d.write(__webapptpl__)
    op("Project %s created, you can develop this project with QEditor then manage this project through this tool.\n" % arg)

if __name__ == "__main__":
    try:
        import django

        os.chdir(ROOT)
        while(True):
            if PROJECT == None:
                op(__doc__)
                op("QPY> Input django project name: \n or enter \"ls\" to see all the qpython projects.\n ")
                opt = 'choose_project'
            else:
                opt = 'opt_project'
                op("QPY> Input your next command for %s:\n syncdb\n createsuperuser\n startapp\n runserver\n" % PROJECT)

            arg=raw_input("QPY> ").strip()
            if (arg==""):
                break

            executearg(opt, arg)
    except ImportError:

        op(__doc__)

        opt = raw_input("QPY> Django library not found, do you want to install it ?\n yes/no\n")
        if opt=='yes':
            os.system(sys.executable+" "+sys.prefix+"/bin/pip install django")
            op("You can restart this tool after django being installed")

