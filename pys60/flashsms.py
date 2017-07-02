#
# nama      : smsflash.py
# rilis     : 0.0.1-alpha
# tanggal   : maret, 2010
#
# script ini berfungsi untuk menampilkan pesan sms secara langsung seperti popup
# pemberitahuan saat mekakses menu operator selular/ cek pulsa.


# pertama, import modul yang diperlukan 
import appuifw
import e32
import flashy

# buat tempat untuk menulis
def tulis():
    appuifw.app.title = u"Tulis Pesan"
    # menghandel tombol exit
    appuifw.app.exit_key_handler = keluar
    # buat menu
    appuifw.app.menu = [(u"Kirim", kirim_pesan), (u"Keluar", keluar)]
    tulisan = appuifw.Text(u"")
    appuifw.app.body = tulisan

# proses mengirim pesan
def kirim_pesan():
    appuifw.app.title = u"Mengirim Pesan"
    ambil_pesan = appuifw.app.body.get()
    # memprbaiki kalimat
    ambil_pesan = ambil_pesan.replace(u"u2029", u"\n")
    # menghitung jumlah karakter, max 160
    jml_chr = len(ambil_pesan)
    # bila jumlah karakter
    # lebih kecil atau sama dengan 160
    # perintah dibawah if akan dijalankan
    if jml_chr <= 160:
        # meminta nomor telepon
        nope = appuifw.query(u"Nomor Tujuan:", "text")
        if nope:
            appuifw.note(u"Mengirim pesan ...")
            flashy.send(u"%s"%nope, u"%s"%ambil_pesan)
            # kembali ke fungsi tulis
            tulis()
        # bila nomor tidak diisi, akan kembali ke fungsi tulis
        else:
            tulis()
    # bila karakter lebih dari 160
    else:
        appuifw.note(u"Error !\nPesan terlalu panjang. Max 160 karakter ...", "error")
        # kembali ke fungsi tulis
        tulis()

# fungsi keluar
def keluar():
    appuifw.note(u"Sampai jumpa, :)")
    jalan.signal()

jalan = e32.Ao_lock()
tulis()
jalan.wait()
