# tidak diberi shebang agar tidak menimbulkan error saat dijalankan dengan termux
#
# Nama file: imgr.py
# Versi rilis: 0.01-alpha
#
# Deskripsi:
#   imgr.py adalah script yang ditulis saat bos lama saya menyodorkan sdcard
#   sambil berkata, "kenapa foto ini gak bisa dibuka di handphone saya"?
#
#   * Saat itu sekitar tahun 2011, saat masih ramai-ramainya ponsel Blackberry *
#
#   Masalahnya adalah, gambar dalam sdcard berasal dari digital kamera dengan
#   resolusi yang besar sehingga tidak dapat di tangani oleh ponsel.
#
#   Solusinya, gambar harus di resize untuk mengurangi penggunaan sumber daya
#   ponsel. Dan script berikut ini saya gunakan untuk me-resize gambar secara
#   masal dengan memanfaatkan salah satu tools dari paket program ImageMagick.
#
# Perintah:
#   $ python2 imgr.py
#
# Jalankan dari direktori foto berada
#
# Oleh      : dhocnet
# Email     : dhocnet@gmail.com
# Website   : www.dhocnet.info
#

# memuat module os
import os

# membuat list dari isi direktori
x = os.listdir('.')

# membuat perulangan yang berfungsi sebagai
# pemroses file
for y in x:
    # memfilter tipe file dari ekstensinya
    yl = y.lower()
    if yl.endswith('.jpg') or yl.endswith('.png'):
        # menentukan nama file hasil resize
        #x_new="%s_new.png"%y[:-4]
        # verbose mode
        print "Resizing file: %s"%y,
        # fungsi untuk menjalankan perintah convert
        os.system('convert -resize 128 %s'%(y))
        print " ... done"
    else:
        # fungsi skip untuk file yang tidak ber-ekstensi jpg
        print "Skipping file: %s"%y
print "Resizing completed!!"
