Sun Jul  2 13:54:59 2017
# emacs-mode: -*- python-*-

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#                                PERINGATAN!
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
# limit.py:
#   seperti yang telah kami sampaikan dalam file readme.txt jika kami kehilangan
#   kode sumber asli limit.py. Sedangkan file limit.py yang sedang Anda akses sa
#   at ini adalah file kode hasil decompile dari file limit.pyc.
#
#   Kode ini hanya digunakan sebagai rujukan saja!
#

import os
import e32
import appuifw
import key_codes
import sys

sys.setdefaultencoding('utf-8')
LIMITKERNEL = e32.Ao_lock()

whoami = ''
HOME = ''
ROOT = ''
SIGN = ''
hostname = ''
PROMPTS = ''

def LimitHalt():
    LimitPrint.add(u"\nType `halt' to exit")
    LimitConsole()

def LimitReboot():
    LimitPrint.add(u"\nType `reboot' to reboot")
    LimitConsole()

def LimitHelp():
    LimitPrint.add(u"\nType `help' for help")
    LimitConsole()

def LimitAbout():
    LimitPrint.add(u"\nType `about' or `credit' for more information")
    LimitConsole()

def LimitConsole():
    global PROMPTS
    LimitPrint.font = 'dense'
    if os.path.exists(('%s\\var\\run\\cmd.run' % ROOT)):
        os.remove(('%s\\var\\run\\cmd.run' % ROOT))
    appuifw.app.title = (u'sh: %s@%s' % (whoami,hostname))
    LimitPrint.color = Gray
    WHERE = os.getcwd()
    if (WHERE[:-1] == ROOT):
        SIGN = '/'
    elif (os.getcwd()[:-1] == HOME):
        SIGN = '~'
    elif ((len(WHERE) > len(HOME)) and (WHERE[:(len(HOME) - len(WHERE))] == HOME)):
        SIGN = ('%s' % WHERE.replace((u'%s' % HOME), u'~')[:-1])
    else:
        SIGN = ('%s' % WHERE[20:-1])
    PROMPTS = ('%s@%s:%s# ' % (whoami,hostname,SIGN))
    PROMPTS = PROMPTS.replace(u'\\', u'/')
    LimitPrint.add((u'\n%s' % PROMPTS))
    if (LimitPrint.len() == (len(PROMPTS) + 1)):
        LimitPrint.delete(0, 1)
    appuifw.app.body = LimitPrint

def LimitEventEnter():
    LimitPrint.set_pos(LimitPrint.len())
    Much = ((((len(os.getcwd()) - 21) + len(whoami)) + len(hostname)) + 4)
    if ((PROMPTS != '') or (len(PROMPTS) > Much)):
        GetBody = appuifw.app.body.get().split(u'\u2029')
        LastPut = GetBody[-1]
        UserPrompt = LastPut[:len(PROMPTS)]
        UserPrompts = UserPrompt.replace(u' ', u'_')
        LastFill = ('%s%s' % (UserPrompts,LastPut[(len(PROMPTS) - 1):]))
        FillTer = LastFill.split(' ')
        if ((len(FillTer) > 1) and (FillTer[1] != '')):
            EXECCMD = ''
            if os.path.exists(('%s\\bin\\%s' % (ROOT,
             FillTer[1]))):
                EXECCMD = ('%s\\bin\\%s' % (ROOT,FillTer[1]))
                LimitPrint.add(u'\n')
                WriteCmd = open(('%s\\var\\run\\cmd.run' % ROOT), 'w')
                WriteLoop = 0
                while (WriteLoop <= (len(FillTer) - 1)):
                    WriteCmd.write((u'%s^' % str(FillTer[WriteLoop])))
                    WriteLoop += 1

                WriteCmd.close()
                execfile(EXECCMD, globals())
            elif (os.path.exists(('%s\\sbin\\%s' % (ROOT,
             FillTer[1]))) and (whoami == 'root')):
                EXECCMD = ('%s\\sbin\\%s' % (ROOT,FillTer[1]))
                LimitPrint.add(u'\n')
                WriteCmd = open(('%s\\var\\run\\cmd.run' % ROOT), 'w')
                WriteLoop = 0
                while (WriteLoop <= (len(FillTer) - 1)):
                    WriteCmd.write((u'%s^' % str(FillTer[WriteLoop])))
                    WriteLoop += 1

                WriteCmd.close()
                execfile(EXECCMD, globals())
            else:
                LimitPrint.add((u'\n-bash: %s: command not found' % FillTer[1]))
                LimitConsole()
        else:
            LimitConsole()
    else:
        LimitConsole()

if os.path.exists('C:\\System\\Apps\\limit'):
    ROOT = 'C:\\System\\Apps\\limit'
    os.chdir(('%s\\root' % ROOT))
else:
    ROOT = 'E:\\System\\Apps\\limit'
    os.chdir(('%s\\root' % ROOT))

HOME = ('%s\\root' % ROOT)
whoami = 'root'
hostname = 'limit'

Black = (0,0,0)
Gray = (85,85,85)
Red = (191,0,0)
Green = (0,140,0)
Yellow = (255,170,0)
Blue = (0,87,174)
White = (255,255,255)
Purple = (64,0,128)

LimitPrint = appuifw.Text()
LimitPrint.color = Gray
LimitPrint.font = 'dense'
appuifw.app.body = LimitPrint

LimitPrint.bind(key_codes.EKeySelect, LimitEventEnter)

appuifw.app.exit_key_handler = LimitHalt

LimitDefMenu = [(u'Reboot',LimitReboot),
                (u'Halt',LimitHalt),
                (u'Help',LimitHelp),
                (u'About',LimitAbout)]

appuifw.app.menu = LimitDefMenu
appuifw.app.title = u'Booting up...'
LimitPrint.color = Black
LimitPrint.add(u'Loading limit ')
LimitAnime = 0

while (LimitAnime < 17):
    LimitPrint.add(u'..')
    e32.ao_sleep(0.20000000000000001)
    LimitAnime += 1

LimitPrint.color = Green
LimitPrint.add(u' [OK]\n')
e32.ao_sleep(0.20000000000000001)
LimitPrint.color = Black
LimitPrint.add(u'BIOS data check successful\n\n')
e32.ao_sleep(2)

appuifw.app.body.clear()
LimitPrint.font = 'annotation'
LimitPrint.color = Red
LimitPrint.add(u'\t\t\tBoot Screen\n')
LimitPrint.font = 'title'
LimitPrint.color = Blue
LimitPrint.add(u'\n\nL.I.M.I.T\t0.01 beta')
LimitPrint.font = u'LatinPlain17'
LimitPrint.color = Purple
LimitPrint.add(u'\n\t   The Linux Miniature')
LimitPrint.font = 'dense'
LimitPrint.color = Black
LimitPrint.add(u'\n\n\nWellcome && enjoy to Limit v0.01')
LimitPrint.font = u'LatinPlain17'
LimitPrint.color = (177,177,177)
LimitPrint.add(u'\nPress enter to continue... ')
LIMITKERNEL.wait()

# local variables:
# tab-width: 4
+++ okay decompyling limit.pyc 
decompyled 1 files: 1 okay, 0 failed, 0 verify failed
Sun Jul  2 13:54:59 2017
