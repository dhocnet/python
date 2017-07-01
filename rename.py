# tidak diberi shebang agar tidak menimbulkan error saat dieksekusi dari berbagai platform.
# =========================================================================================
# jalankan dengan perintah:
#    $ python2 renamer.py
#
# dari direktori file atau direktori sticker disimpan.
#
# CATATAN:
#    renamer.py hanya dapat berpindah 1 level ke direktori sticker.
# =========================================================================================
# deskripsi:
#    renamer.py adalah script yang saya gunakan secara pribadi untuk menambah ekstensi .png
#    pada file sticker yang diambil dari aplikasi Line (/storage/emulated/0/Android/data/
#    jp.naver.line.android/stickers) dan BBM (/data/data/com.bbm/files/bbmcore/stickers).
# =========================================================================================
# Oleh: dhocnetwork
# website: www.dhocnet.info
# Email: desktop.hobbie@gmail.com
#

import os

ren_d=os.listdir('.')
ren_d_count=len(ren_d)
ren_d_loop=0

while ren_d_count > ren_d_loop:
    ren_chdir=0
    if os.path.isdir(ren_d[ren_d_loop]):
        os.chdir(ren_d[ren_d_loop])
        ren_chdir=1
        print 'Walking to '+ren_d[ren_d_loop]
    ren_f=os.listdir('.')
    ren_f_i=ren_f
    ren_f_count=len(ren_f)
    ren_f_loop=0
    while ren_f_count > ren_f_loop:
        ren_f_n=ren_f_i[ren_f_loop]
        if 'ani' in ren_f_n:
            os.rename(ren_f_n,'%s.gif'%ren_f_n)
            print "Moving %s to %s.gif"%(ren_f_n,ren_f_n)
        else:
            os.rename(ren_f_n,'%s.png'%ren_f_n)
            print "Moving %s to %s.png"%(ren_f_n,ren_f_n)
        ren_f_loop+=1
    if ren_chdir==1:
        os.chdir('..')
    ren_d_loop+=1

print 'Done!'
