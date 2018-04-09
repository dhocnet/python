#!/usr/bin/python2
#
# script untuk merubah extensi gambar
#
# Oleh  : Mongkee Lutfi
# Web   : https://www.dhocnet.work
# Blog  : https://blog.dhocnet.work
#
# Denpasar, 7 April 2018
#

import os

# variable ekstensi gambar yang didukung (rubah sesuai dengan kebutuhan)
ext_gambar = ["jpg","png","bmp","gif","webp","jpeg"]

# minta masukan ekstensi gambar dari user
print "Masukan ekstensi target!"
print "    Contoh: png, jpg, bmp, gif"
a_0 = raw_input("Pilihanmu: ")

# listing folder teratas (folder aktif)
a_1 = os.listdir(".")
a_2 = len(a_1)
a_3 = 0


while a_3 < a_2:
    if os.path.isdir(a_1[a_3]):
        os.chdir(a_1[a_3])
        b_1 = os.listdir(".")
        b_2 = len(b_1)
        b_3 = 0
        while b_3 < b_2:
            if os.path.isdir(b_1[b_3]):
                print "Kesalahan! Direktori terlalu banyak!"
                print "%s dilewati."%b_1[b_3]
            else:
                b_4 = b_1[b_3].split(".")
                if b_4[-1].lower() in ext_gambar:
                    if a_0 == b_4:
                        print "File %s berekstensi sama. Dilewati!"%b_1[b_3]
                    else:
                        print "Memproses file %s ..."%b_1[b_3]
                        b_5 = len(b_4[-1])
                        os.system("convert %s %s%s"%(b_1[b_3],b_1[b_3][:-b_5],a_0))
                        print "... Berhasil %s%s. OK!"%(b_1[b_3][:-b_5],a_0)
                else:
                    print "Kesalahan. Jenis file tidak didukung!"
                    print "%s dilewati."%b_1[b_3]
            b_3 += 1
        os.chdir("..")
    else:
        a_4 = a_1[a_3].split(".")
        if a_4[-1].lower() in ext_gambar:
            if a_0 == a_4:
                print "File %s berekstensi sama. Dilewati!"%a_1[a_3]
            else:
                print "Memproses file %s ..."%a_1[a_3]
                a_5 = len(a_4[-1])
                os.system("convert %s %s%s"%(a_1[a_3],a_1[a_3][:-a_5],a_0))
                print "... Berhasil %s%s. OK!"%(a_1[a_3][:-a_5],a_0)
        else:
            print "Kesalahan. Jenis file tidak didukung!"
            print "%s dilewati."%a_1[a_3]
    a_3 += 1

print "Pekerjaan selesai!"
