# shebang dihilangkan agar tidak error saat dijalankan dengan termux

#
# Nama         : PiroGames
# Versi        : 0.0.1-alpha
# Oleh         : cupucupu
# Kontak       : cupu.cupuh@yahoo.co.id
# Komentar     : Script permainan sederhana untuk latihan
#

# Hilangkan tanda komentar di dua baris berikut bila script
# dijalankan dengan Python For S60 (PYS60)
#import appuifw
#appuifw.app.title=u"Piro Games"

import random
nomor=""
peluang=""

print "\n*** SELAMAT DATANG ***"
print "\nHalo, ini adalah permainan tebak angka sederhana."
print "Untuk memenangkan permainan ini, kamu harus me"
print "nebak angka yang diacak antara 0-9 dengan benar."
print "\nDalam permainan, kamu hanya diberi kesempatan"
print "menebak sebanyak 3 (tiga) kali. Lebih dari itu, maka"
print "kamu dinyatakan kalah"
print "\nSelamat berjuang!"

def mulai():
    global nomor, peluang
    peluang=3
    nomor=random.randrange(0,9)
    print "\nTebak nilai antara 0-9 (Q = keluar)."
    bermain()

def bermain():
    global nomor, peluang
    kamu=raw_input("Nilai : ")
    try:
        kamu_lagi=int(kamu)
        if kamu_lagi==nomor:
            print "\n*** SELAMAT ***"
            print "Kamu berhasil menebak dengan benar!"
            print "\nKamu hebat. Ayo main lagi...!!!"
            mulai()
        else:
            peluang-=1
            if peluang==0:
                print "\nOops...! Kamu kalah!!!"
                print "Jawabanya adalah %s."%(nomor)
                print "\n!!! PERMAINAN BERAKHIR !!!\n"
                lagi=raw_input("Ulangi permainan (Y/N)? ")
                if lagi.lower()=="y":
                    mulai()
                else:
                    keluar()
            else:
                print "Kamu salah!"
                if kamu_lagi>nomor:
                    print "Nilai terlalu besar!"
                else:
                    print "Nilai terlalu kecil...!"
                print "Peluang kamu %sX lagi. Berjuanglah...!!!\n"%(peluang)
                bermain()
    except:
        if kamu.lower()=="q":
            keluar()
        else:
            print "\nOW,... OW,... OW,..."
            print "Kamu salah mengetik jawaban!"
            print "Masukan satu nilai antara 0-9 saja.\n"
            bermain()

def keluar():
    print "Sampai jumpa lagi :-)"

mulai()
