#-*- coding: iso-8859-1 -*-
#---------------------------------------------------------------------
# PassBox v0.02
#---------------------------------------------------------------------
# Oleh      : cupucupu
# Email     : desktop.hobbie@gmail.com
#---------------------------------------------------------------------
#
# PassBox adalah sebuah program sederhana yang berjalan pada 
# ponsel-ponsel symbian seri 60. PassBox berfungsi sebagai
# password reminder yang akan menyimpan berbagai macam akun 
# yang kita miliki.
#
# Menggunakan:
#	- Python For S60 v1.45
#	- Module Pack v1.33
#
# CATATAN:
# passbox TIDAK PERNAH dicoba pada perangkat selain Nokia N-GAGE QD
#
# Lebih lanjut silahkan baca file README_PROGRAM.TXT
#---------------------------------------------------------------------


import os
import e32
import e32dbm
import base64
import md5
import appuifw
import time


users = ""
sl_db_nm = ""
logfail_attempt = []
logfail_data = []
hari = [u"Senin",u"Selasa",u"Rabu",u"Kamis",u"Jum'at",u"Sabtu",u"Minggu"]
root_dir = ""


# memeriksa lokasi instalasi program
def fu_cek_install():
    global root_dir
    # periksa dan buat variabel menuju direktori program.
    # variabel = root_dir
    if os.path.exists("C:\\System\\Apps\\passbox"):
        root_dir = "C:\\System\\Apps\\passbox"
        fu_cek_user()
    elif os.path.exists("E:\\System\\Apps\\passbox"):
        root_dir = "E:\\System\\Apps\\passbox"
        fu_cek_user()
    else:
        # Bila program tidak terinstall, misalnya dijankan dari script menggunakan interpreter
        # program akan keluar karena akan banyak menimbulkan masalah karena path
        root_error = "Kesalahan!\nLokasi instalasi program tidak ditemukan. Silahkan ulangi instalasi Anda..."
        appuifw.note(u"%s"%root_error,"error")
        appuifw.note(u"Menutup program...","info")
        fu_exit()


# memeriksa kepemilikan pengguna
def fu_cek_user():
    sop = open("%s\\conf\\sys.conf"%root_dir,"r")
    rsop = sop.read()
    sop.close()
    s64 = base64.encodestring("1")
    sm5 = md5.new(s64).hexdigest()
    if rsop == sm5:
        #appuifw.note(u"PassBox v0.02\nBy CupuCupu","info")
        appuifw.note(u"Selamat Datang di PassBox","info")
        fu_login()
    else:
        # penggunaan program untuk pertama kali, user harus mendaftar untuk mendapatkan akun login
        if appuifw.query(u"Belum ada akun terdaftar. Daftar sekarang ?","query") == True:
            readme_first()
        else:
            # program akan menutup dirinya bila user menolak untuk mendaftar
            appuifw.note(u"Anda tidak dapat menggunakan program ini...","info")
            fu_exit()
            
            
# fungsi untuk login
def fu_login():
    global login0, login1
    appuifw.app.title = u"PassBox Login"
    # saat program dijalankan dan telah ada user yang terdaftar
    # form login akan langsung ditampilkan
    login0 = appuifw.query(u"Nama Pengguna:","text")
    if login0 == None:
        fu_batal_login()
    else:
        login1 = appuifw.query(u"Kata Sandi:","code")
        if login1 == None:
            fu_batal_login()
        else:
            fu_cek_login()
            
            
def fu_batal_login():
    appuifw.app.title = u"Login Dibatalkan"
    appuifw.note(u"Login Dibatalkan...","info")
    fu_exit()
        
        
def fu_cek_login():
    global users
    akun = open("%s\\conf\\profile.conf"%root_dir,"r")
    baca_akun = akun.read()
    akun.close()
    data_user = baca_akun.split(":")
    if data_user[0] == login0:
        in_pwd_00 = base64.encodestring(login1)
        in_pwd_01 = md5.new(in_pwd_00).hexdigest()
        if data_user[1] == in_pwd_01:
            users = "%s"%login0
            vl = open("%s\\log\\status"%root_dir,"r")
            vsl = vl.read()
            vl.close()
            if str(vsl) == "1":
                # pemberitahuan bila ada seseorang yang mencoba login tapi gagal
                # pemberitahuan akan ditampilkan bila pelaku mencoba login sebanyak 5 kali
                appuifw.note(u"Anda memiliki catatan log yang mencurigakan.","info")
                if appuifw.query(u"Lihat catatan log sekarang ?","query") == True:
                    fu_last_log()
                else:
                    user_wellcome()
            else:
                user_wellcome()
        else:
            fu_login_gagal()
    else:
        fu_login_gagal()
        
        
def fu_login_gagal():
    global logfail_data
    appuifw.app.title = u"Login Error!"
    lft0 = time.time()
    lft1 = time.localtime(lft0)
    lft2 = "%s %s/%s/%s - %s:%s:%s\nStatus: Percobaan Login\nKeterangan:\n\tNama Pengguna: %s\n\tKata Sandi: %s\n"%(hari[lft1.tm_wday], lft1.tm_mday, lft1.tm_mon, lft1.tm_year, lft1.tm_hour, lft1.tm_min, lft1.tm_sec, login0, login1)
    logfail_data.append(u"%s"%lft2)
    logfails = len(logfail_data)
    if logfails < 5:
        appuifw.note(u"Kesalahan!\nNama Pengguna atau Kata Sandi Anda tidak cocok","error")
        appuifw.query(u"Periksa penggunaan huruf kapital dan non kapital...","query")
        fu_login()
    else:
        # Batas percobaan login adalah sebanyak 5 kali
        # bila sudah mencapai batas, program akan mencatat aktifitas tersebut
        # dan menutup dirinya
        appuifw.note(u"Anda sudah %s kali gagal melakukan login. Apakah Anda memiliki akun ?"%logfails,"error")
        wlg = open("%s\\log\\last.log"%root_dir,"w")
        logwrite = open("%s\\log\\report.log"%root_dir,"a")
        logfail_numb = len(logfail_data) - 1
        logloop = 0
        while logloop <= logfail_numb:
            logwrite.write(u"%s\n"%logfail_data[logloop])
            wlg.write(u"%s\n"%logfail_data[logloop])
            logloop += 1
        t00 = time.time()
        t01 = time.localtime(t00)
        app_close_status = "%s %s/%s/%s - %s:%s:%s\nAplikasi keluar\nStatus: percoba'an login sebanyak 5 kali\n"%(hari[t01.tm_wday], t01.tm_mday, t01.tm_mon, t01.tm_year, t01.tm_hour, t01.tm_min, t01.tm_sec)
        logwrite.write(u"%s\n"%app_close_status)
        wlg.write(u"%s\n"%app_close_status)
        logwrite.close()
        wlg.close()
        stt = open("%s\\log\\status"%root_dir,"w")
        stt.write(u"1")
        stt.close()
        fu_exit()
        

# menampilkan aktifitas terakhir yang mencurigakan saat user berhasil masuk/ login
def fu_last_log():
    appuifw.app.title = u"Log Terakhir"
    fopn = open("%s\\log\\last.log"%root_dir,"r")
    ropn = fopn.read()
    fopn.close()
    vllog = appuifw.Text()
    vllog.add(u"%s"%ropn)
    vllog.set_pos(0)
    appuifw.app.exit_key_handler = clear_text
    appuifw.app.menu = [(u"Tutup", clear_text)]
    appuifw.app.body = vllog
        
        
def user_wellcome():
    tin0 = time.time()
    tin1 = time.localtime()
    chkdate = tin1.tm_mday
    if str(chkdate) == "1":
        clrlog = open("%s\\log\\report.log"%root_dir,"w")
        clrlog.write(u"Catatan log telah dihapus!\n\n")
        clrlog.close()
    else:
        pass
    wllin = open("%s\\log\\report.log"%root_dir,"a")
    wllin.write(u"Login %s pada: \n%s %s/%s/%s - %s:%s:%s\n\n"%(users, hari[tin1.tm_wday], tin1.tm_mday, tin1.tm_mon, tin1.tm_year, tin1.tm_hour, tin1.tm_min, tin1.tm_sec))
    wllin.close()
    # llo = open("%s\\log\\last.log"%root_dir,"r")
    # rll = llo.read()
    # llo.close()
    appuifw.note(u"Halo %s :)"%users,"info")
    user_menu()


def readme_first():
    appuifw.app.title = u"Sebelum Memulai"
    appuifw.app.menu = [(u"Lanjutkan",readme_2), (u"Batalkan",notagree)]
    appuifw.app.exit_key_handler = notagree
    readme = appuifw.Text()
    readme.font = "title"
    readme.add(u"Sebelum Memulai\n\n")
    readme.font = "dense"
    readme.add(u"Sebelum Anda melanjutkan proses pendaftaran, Anda HARUS setuju dengan LISENSI dan PENOLAKAN yang digunakan oleh program ini.\n\nUntuk melanjutkan, tekan [Menu] dan pilih [Lanjutkan]. Dan untuk membatalkan, tekan [Menu] pilih [Batalkan] atau tekan [Exit].")
    readme.set_pos(0)
    appuifw.app.body = readme
    
    
def readme_2():
    global readme_3
    appuifw.app.title = u"KESEPAKATAN"
    readme_3 = []
    pop_menu = [u"Baca Penolakan",u"Saya Setuju",u"Saya Tidak Setuju"]
    selpm = appuifw.popup_menu(pop_menu,u"KESEPAKATAN")
    if selpm == 0:
        readme_3 = ["PENOLAKAN","disclaimer.txt"]
        readme_4()
    elif selpm == 1:
        if appuifw.query(u"Dengan memilih SETUJU, berarti Anda telah mengerti dan siap menaggung segala resiko.","query") == True:
            fu_register()
        else:
            readme_2()
    else:
        notagree()
        
        
def readme_4():
    appuifw.app.title = u"%s"%readme_3[0]
    appuifw.app.exit_key_handler = readme_2
    appuifw.app.menu = [(u"Kembali", readme_2)]
    readmefile = open("%s\\usr\\%s"%(root_dir, readme_3[1]), "r")
    readreadmefile = readmefile.read()
    readmefile.close()
    print_readme = appuifw.Text()
    print_readme.font = "title"
    print_readme.add(u"%s\n\n"%readme_3[0])
    print_readme.font = "dense"
    print_readme.add(u"%s\n\n"%readreadmefile)
    print_readme.set_pos(0)
    appuifw.app.body = print_readme
    
    
def notagree():
    appuifw.app.title = u"Tidak Setuju"
    appuifw.query(u"Karena Anda tidak setuju, segera buang PassBox dari perangkat Anda!","query")
    fu_exit()
        

# fungsi untuk register
def fu_register():
    global reg_name, reg_pass_more, users
    appuifw.app.title = u"Pendaftaran Akun Baru"
    reg_name = appuifw.query(u"Nama pengguna:","text")
    if reg_name != None:
        reg_pass = appuifw.query(u"Kata sandi:","code")
        if reg_pass != None:
            if len(reg_pass) < 8:
                # peringatan keamanan bila password lebih kecil dari 8 karakter
                # peringatan ditampilkan untuk alasan keamanan
                appuifw.note(u"PERINGATAN!\nKata Sandi Anda kurang dari 8 karakter","info")
                appuifw.note(u"Untuk alasan keamanan, gunakan lebih dari 8 karakter dengan kombinasi...","info")
                if appuifw.query(u"Tetap gunakan ?","query") == True:
                    reg_pass_more = appuifw.query(u"Kata sandi lagi:","code")
                    if reg_pass == reg_pass_more:
                        fu_proc_reguser()
                    else:
                        fu_reg_fail()
                else:
                    appuifw.note(u"Silahkan ulangi lagi...","info")
                    fu_register()
            else:
                reg_pass_more = appuifw.query(u"Kata sandi lagi:","code")
                if reg_pass == reg_pass_more:
                    fu_proc_reguser()
                else:
                    fu_reg_fail()
        else:
            fu_reg_batal()
    else:
        fu_reg_batal()
        
        
def fu_proc_reguser():
    if appuifw.query(u"Yakin dengan data yang Anda masukan sebelumnya ?","query") == True:
        appuifw.query(u"PERINGATAN!\nIngat baik-baik akun Anda karna tidak akan ditampilkan lagi.","query")
        proc_enc_pass_00 = base64.encodestring(reg_pass_more)
        proc_enc_pass_01 = md5.new(proc_enc_pass_00).hexdigest()
        proc_form_acc = "%s:%s"%(reg_name, proc_enc_pass_01)
        proc_cf = open("%s\\conf\\profile.conf"%root_dir,"w")
        proc_cf.write(proc_form_acc)
        proc_cf.close()
        ustt = base64.encodestring("1")
        sttusr = open("%s\\conf\\sys.conf"%root_dir,"w")
        sttusr.write(u"%s"%md5.new(ustt).hexdigest())
        sttusr.close()
        appuifw.note(u"Selamat!\nAkun Anda telah dibuat...","conf")
        # program akan tertutup untuk me-refresh data :^'
        appuifw.query(u"Aplikasi akan tertutup untuk memperbaharui basis data. Tekan OK untuk melanjutkan...","query")
        fu_exit()
    else:
        if appuifw.query(u"Apakah Anda ingin mengulangi proses Pendaftaran ?","query") == True:
            fu_register()
        else:
            fu_exit()
            
            
def fu_reg_fail():
    appuifw.note(u"KESALAHAN!\nPassword yang Anda masukan tidak sama. Silahkan ulangi lagi...","error")
    fu_register()
    
    
def fu_reg_batal():
    if appuifw.query(u"Proses pendaftaran belum lengkap. Batalkan ?","query") == True:
        fu_exit()
    else:
        appuifw.note(u"Silahkan ulangi lagi proses pendaftaran...","info")
        fu_register()
        
        
#**********************************************************
# Main menu setelah berhasil login
#**********************************************************
#     
# User menu
def user_menu():
    appuifw.app.title = u"%s@PassBox 0.2"%users
    # perbaikan dari sini
    if not os.path.exists("%s\\db"%root_dir):
        os.mkdir("%s\\db"%root_dir)
        if not os.path.exists("%s\\tmp"%root_dir):
            os.mkdir("%s\\tmp"%root_dir)
        else:
            pass
    else:
        pass
    # perbaikan selesai
    user_menu_choose = [u"Buat Berkas Baru", u"Buka Berkas Saya", u"Pengaturan", u"Bantuan", u"Keluar"]
    user_menu_select = appuifw.selection_list(user_menu_choose)
    if user_menu_select == 0:
        user_create_db()
    elif user_menu_select == 1:
        fu_clear_screen()
    elif user_menu_select == 2:
        user_settings()
    elif user_menu_select == 3:
        user_help()
    else:
        fu_quit()
        
    
# membuat data baru    
def user_create_db():
    global cr_db_nm
    appuifw.app.title = u"Buat Berkas Baru"
    cr_db_nm = appuifw.query(u"Nama Berkas:","text")
    if cr_db_nm != None:
        if os.path.exists("%s\\db\\%s.e32dbm"%(root_dir, cr_db_nm)):
            # Konfirmasi bila nama data telah digunakan
            # ganti data (replace) atau ganti nama (rename)
            appuifw.note(u"Nama %s telah digunakan"%cr_db_nm,"info")
            if appuifw.query(u"Ganti berkas lama dengan yang baru ?","query") == True:
                # membuat salinan (backup) file asli bila user membatalkan proses ditengah jalan
                e32.file_copy("%s\\tmp\\%s"%(root_dir,md5.new(cr_db_nm).hexdigest()),"%s\\db\\%s.e32dbm"%(root_dir,cr_db_nm))
                os.remove("%s\\db\\%s.e32dbm"%(root_dir, cr_db_nm))
                wrbakfl = open("%s\\tmp\\backup.bak"%root_dir,"w")
                wrbakfl.write(u"%s:%s"%(base64.encodestring(cr_db_nm),base64.encodestring(md5.new(cr_db_nm).hexdigest())))
                wrbakfl.close()
                usr_crdbtmp()
            else:
                appuifw.note(u"Silahkan pilih nama yang lain...","info")
                user_create_db()
        else:
            usr_crdbtmp()
    else:
        clear_text()
        
        
def usr_crdbtmp():
    appuifw.app.title = u"%s"%cr_db_nm
    # formulir isian untuk data baru
    cdbuname = appuifw.query(u"Nama pengguna:","text")
    if cdbuname != None:
        cdbupass = appuifw.query(u"Kata Sandi:","text")
        if cdbupass != None:
            cdbucomm = appuifw.query(u"Komentar (max 80 chr):","text")
            if cdbucomm != None:
                pass
            else:
                cdbucomm = "Tidak ada komentar untuk akun ini!"
            # menyimpan isi ke database
            dbfiledir = "%s\\db\\%s"%(root_dir, cr_db_nm)
            sdbf = e32dbm.open(dbfiledir,"cf")
            sdbf[u"Nama Pengguna:"] = u"%s"%base64.encodestring(cdbuname)
            sdbf[u"Kata Sandi:"] = u"%s"%base64.encodestring(cdbupass)
            sdbf[u"Komentar:"] = u"%s"%base64.encodestring(cdbucomm)
            sdbf.close()
            appuifw.note(u"Berkas disimpan dengan nama %s..."%cr_db_nm,"conf")
            chkdbtmp()
        else:
            canconfrm()
    else:
        canconfrm()
        

# memeriksa, apakah ada file sementara
def chkdbtmp():
    if os.path.exists("%s\\tmp\\backup.bak"%root_dir):
        remtmpfl()
    else:
        fu_clear_screen()
        

# menghapus file file sementara termasuk file salinan (backup) yang berada di direktri tmp\
def remtmpfl():
    ltmpfl = os.listdir("%s\\tmp"%root_dir)
    ftmpfl = len(ltmpfl) - 1
    lfl = 0
    while lfl <= ftmpfl:
        os.remove("%s\\tmp\\%s"%(root_dir,ltmpfl[lfl]))
        lfl += 1
    clear_text()
    

# konfirmasi saat user membatalkan proses pembuatan data
def canconfrm():
    if appuifw.query(u"Batalkan pembuatan berkas baru ?","query") == True:
        if os.path.exists("%s\\tmp\\backup.bak"%root_dir):
            # bila user benar benar membatalkanya
            # file salinan (backup) akan dikembalikan (bila ada)
            cdelfl = open("%s\\tmp\\backup.bak"%root_dir,"r")
            cdelflc = cdelfl.read()
            cdelfl.close()
            cdelfls = cdelflc.split(":")
            cdelfname = "%s"%base64.dencodestring(cdelfls[0])
            cdelfhex = "%s"%base64.dencodestring(cdelfls[1])
            e32.file_copy("%s\\db\\%s.e32dbm"%(root_dir,cdelfname),"%s\\tmp\\%s"%(root_dir,cdelfhex))
            appuifw.note(u"Dibatalkan...","conf")
            remtmpfl()
        else:
            appuifw.note(u"Dibatalkan...","conf")
            clear_text()
    else:
        appuifw.note(u"Silahkan ulangi lagi ...","info")
        usr_crdbtmp()
    
    
# manager data
def user_open_db():
    global sl_db_nm
    t_file = os.listdir("%s\\db"%root_dir)
    n_file = len(t_file)
    if n_file == 0:
        confnew()
    else:
        appuifw.app.title = u"Berkas Anda: %s"%n_file
        l_num = n_file - 1
        l_file = 0
        f_list = []
        while l_file <= l_num:
            f_n = t_file[l_file]
            nadd = f_n[:-7]
            f_list.append(u"%s"%nadd)
            l_file += 1
        sl_db = appuifw.selection_list(f_list, 1)
        if sl_db != None:
            sl_db_nm = "%s"%f_list[sl_db]
            slc_act = appuifw.popup_menu([u"Buka Berkas",u"Perbaharui Berkas",u"Ubah Nama Berkas",u"Buat Berkas Baru",u"Hapus Berkas"], u"%s"%sl_db_nm)
            if slc_act == 0:
                user_read_db()
            elif slc_act == 1:
                user_update_db()
            elif slc_act == 2:
                user_rendb()
            elif slc_act == 3:
                user_create_db()
            elif slc_act == 4:
                user_deldb()
            else:
                fu_clear_screen()
        else:
            clear_text()
            
            
def confnew():
    appuifw.app.title = u"Tidak Ada Berkas"
    if appuifw.query(u"Anda belum memiliki berkas. Buat berkas baru ?","query") == True:
        user_create_db()
    else:
        user_menu()
        

# membuka/ membaca data
def user_read_db():
    appuifw.app.title = u"%s"%sl_db_nm
    shuname = ""
    shupass = ""
    shucomm = ""
    show_db = appuifw.Text()
    show_db.style = appuifw.STYLE_BOLD
    show_db.font = "title"
    show_db.add(u"%s"%sl_db_nm)
    show_db.color = (19,117,255)
    odbfile = "%s\\db\\%s.e32dbm"%(root_dir, sl_db_nm)
    rdb = e32dbm.open(odbfile, "r")
    for kdb, vdb in rdb.items():
        if kdb == "Nama Pengguna:":
            shuname = base64.decodestring(vdb)
        elif kdb == "Kata Sandi:":
            shupass = base64.decodestring(vdb)
        elif kdb == "Komentar:":
            shucomm = base64.decodestring(vdb)
    rdb.close()
    sdbui = 3
    sdbul = 0
    while sdbul <= sdbui:
        adddb1 = ""
        adddb2 = ""
        if sdbul == 1:
            adddb1 = "Nama Pengguna:"
            adddb2 = shuname
        elif sdbul == 2:
            adddb1 = "Kata Sandi:"
            adddb2 = shupass
        elif sdbul == 3:
            adddb1 = "Komentar:"
            adddb2 = shucomm
        show_db.font = "annotation"
        show_db.color = (0,111,111)
        show_db.add(u"%s\n"%adddb1)
        show_db.font = "dense"
        show_db.color = (0,0,0)
        show_db.add(u"%s\n\n"%adddb2)
        sdbul += 1
    show_db.set_pos(0)
    appuifw.app.exit_key_handler = fu_clear_screen
    appuifw.app.menu = [(u"Kembali", fu_clear_screen),(u"Perbaharui Berkas", user_update_db),(u"Buat Berkas Baru", user_create_db),(u"Ganti Nama Berkas", user_rendb), (u"Hapus Berkas", user_deldb)]
    appuifw.app.body = show_db
    
    
# fungsi untuk mengupdate data
def user_update_db():
    appuifw.app.title = u"Memperbaharui %s"%sl_db_nm
    udbfile = "%s\\db\\%s.e32dbm"%(root_dir, sl_db_nm)
    updbop = e32dbm.open(udbfile, "r")
    tmpfl = open("%s\\tmp\\%s"%(root_dir,md5.new(sl_db_nm).hexdigest()), "w")
    for cdbk, cdbv in updbop.items():
        tmpfl.write(u"%s%s"%(cdbk,cdbv))
    updbop.close()
    tmpfl.close()
    user_chcdb()
    
    
def user_chcdb():
    tmpflop = open("%s\\tmp\\%s"%(root_dir,md5.new(sl_db_nm).hexdigest()), "r")
    tmpflrl = tmpflop.readlines()
    tmpflop.close()
    molddb = len(tmpflrl) - 1
    udbl = 0
    field_uc0 = ""
    field_uc1 = ""
    field_uc2 = ""
    while udbl <= molddb:
        if tmpflrl[udbl].startswith("Nama Pengguna"):
            olddbitems = tmpflrl[udbl].split(":")
            field_uc0 = base64.decodestring(olddbitems[1])
        elif tmpflrl[udbl].startswith("Kata Sandi"):
            olddbitems = tmpflrl[udbl].split(":")
            field_uc1 = base64.decodestring(olddbitems[1])
        elif tmpflrl[udbl].startswith("Komentar"):
            olddbitems = tmpflrl[udbl].split(":")
            field_uc2 = base64.decodestring(olddbitems[1])
        udbl +=1
    fieldup0 = appuifw.query(u"Nama Pengguna:","text",u"%s"%field_uc0)
    if fieldup0:
        fieldup1 = appuifw.query(u"Kata Sandi:","text",u"%s"%field_uc1)
        if fieldup1:
            fieldup2 = appuifw.query(u"Komentar (max 80 chr):","text",u"%s"%field_uc2)
            if fieldup2:
                pass
            else:
                fieldup2 = field_uc2
            fchdb0 = base64.encodestring(fieldup0)
            fchdb1 = base64.encodestring(fieldup1)
            fchdb2 = base64.encodestring(fieldup2)
            os.remove("%s\\db\\%s.e32dbm"%(root_dir,sl_db_nm))
            os.remove("%s\\tmp\\%s"%(root_dir,md5.new(sl_db_nm).hexdigest()))
            cdbfile = "%s\\db\\%s"%(root_dir, sl_db_nm)
            schdb = e32dbm.open(cdbfile, "cf")
            schdb[u"Nama Pengguna:"] = u"%s"%fchdb0
            schdb[u"Kata Sandi:"] = u"%s"%fchdb1
            schdb[u"Komentar:"] = u"%s"%fchdb2
            schdb.close()
            appuifw.note(u"Oke!\nBerkas berhasil diperbaharui...","conf")
            fu_clear_screen()
        else:
            user_cchdb()
    else:
        user_cchdb()
        
        
def user_cchdb():
    appuifw.note(u"Dibatalkan...","conf")
    fu_clear_screen()
    

# me-rename data
def user_rendb():
    nudbname = appuifw.query(U"Nama Baru:","text",u"%s"%sl_db_nm)
    if nudbname != None:
        if nudbname.lower() != sl_db_nm.lower():
            if os.path.exists(u"%s\\db\\%s.e32dbm"%(root_dir, nudbname)):
                if appuifw.query(u"Nama %s telah digunakan. Ganti berkas lama dengan yang baru ?"%nudbname,"query") == True:
                    os.remove("%s\\db\\%s.e32dbm"%(root_dir, nudbname))
                    os.rename("%s\\db\\%s.e32dbm"%(root_dir, sl_db_nm),"%s\\db\\%s.e32dbm"%(root_dir, nudbname))
                    appuifw.note(u"Berkas berhasil diganti...","conf")
                    fu_clear_screen()
                else:
                    appuifw.note(u"Silahkan pilih nama yang lain...","info")
                    user_rendb()
            else:
                os.rename("%s\\db\\%s.e32dbm"%(root_dir, sl_db_nm),"%s\\db\\%s.e32dbm"%(root_dir, nudbname))
                appuifw.note(u"Berkas berhasil dirubah namanya...","conf")
                fu_clear_screen()
        elif nudbname == sl_db_nm:
            appuifw.note(u"Nama berkas tidak diganti...","info")
            fu_clear_screen()
        else:
            fu_clear_screen()
    else:
        fu_clear_screen()
    

# menghapus data    
def user_deldb():
    appuifw.app.title = u"%s"%sl_db_nm
    if appuifw.query(u"Yakin Anda ingin menghapus %s ?"%sl_db_nm,"query") == True:
        os.remove("%s\\db\\%s.e32dbm"%(root_dir,sl_db_nm))
        appuifw.note(u"Berkas berhasil di hapus...","conf")
        fu_clear_screen()
    else:
        fu_clear_screen()
    
    
# Pengaturan
def user_settings():
    appuifw.app.title = u"Pengaturan"
    selsetm = appuifw.popup_menu([u"Ganti Kata Sandi",u"Lihat Catatan Log",u"Hapus Catatan Log"],u"Pengaturan")
    if selsetm == 0:
        setuppwd()
    elif selsetm == 1:
        slog()
    elif selsetm == 2:
        clog()
    else:
        user_menu()
        
        
# mengganti password user
def setuppwd():
    appuifw.app.title = u"Ganti Kata Sandi"
    setuppwd0 = appuifw.query(u"Kata Sandi Lama:","code")
    if setuppwd0 != None:
        setuppwd0a = base64.encodestring(setuppwd0)
        setuppwd0b = md5.new(setuppwd0a).hexdigest()
        opac = open("%s\\conf\\profile.conf"%root_dir,"r")
        reac = opac.read()
        opac.close()
        flac = reac.split(":")
        if setuppwd0b == flac[1]:
            setnupwd0 = appuifw.query(u"Kata Sandi Baru:","code")
            if setnupwd0 != None:
                setnupwd1 = appuifw.query(u"Kata Sandi Lagi:","code")
                if setnupwd1 != None:
                    if setnupwd0 == setnupwd1:
                        if len(setnupwd1) < 8:
                            if appuifw.note(u"Kata Sandi terlalu pendek. Tetap gunakan ?","query") == True:
                                encnupwd0 = base64.encodestring(setnupwd1)
                                encnupwd1 = md5.new(encnupwd0).hexdigest()
                                wfl = open("%s\\conf\\profile.conf"%root_dir, "w")
                                flform = "%s:%s"%(users, encnupwd1)
                                wfl.write(u"%s"%flform)
                                wfl.close()
                                appuifw.note(u"Kata Sandi berhasil diperbaharui...","conf")
                                back2set()
                            else:
                                appuifw.note(u"Silahkan ulangi lagi...","info")
                                setuppwd()
                        else:
                            encnupwd0 = base64.encodestring(setnupwd1)
                            encnupwd1 = md5.new(encnupwd0).hexdigest()
                            wfl = open("%s\\conf\\profile.conf"%root_dir, "w")
                            flform = "%s:%s"%(users, encnupwd1)
                            wfl.write(u"%s"%flform)
                            wfl.close()
                            appuifw.note(u"Kata Sandi berhasil diperbaharui...","conf")
                            back2set()
                    else:
                        appuifw.note(u"Kata Sandi baru tidak sama. Silahkan ulangi lagi !","error")
                        setuppwd()
                else:
                    setuppwdcanc()
            else:
                setuppwdcanc()
        else:
            setuppwdconf()
    else:
        setuppwdcanc()
        
        
def setuppwdconf():
    if appuifw.note(u"Proses penggantian kata sandi gagal. Coba lagi ?","query") == True:
        setuppwd()
    else:
        appuifw.note(u"Dibatalkan!","conf")
        user_menu()
        
        
def setuppwdcanc():
    if appuifw.query(u"Batalkan penggantian kata sandi ?","query") == True:
        user_menu()
    else:
        appuifw.note(u"Silahkan ulangi lagi...","info")
        setuppwd()
        
        
# membaca file log
def slog():
    appuifw.app.title = u"Catatan Aplikasi"
    olog = open("%s\\log\\report.log"%root_dir,"r")
    rlog = olog.read()
    olog.close()
    vlog = appuifw.Text(u"%s"%rlog)
    appuifw.app.exit_key_handler = back2set
    appuifw.app.menu = [(u"Kembali",back2set)]
    appuifw.app.body = vlog
    
    
# menghapus log
def clog():
    appuifw.app.title = u"Menghapus Log"
    if appuifw.query(u"Hapus log ?", "query") == True:
        clogfile = open("%s\\log\\report.log"%root_dir,"w")
        clogfile.write(u"Log telah dihapus.\nTidak ada catatan log!\n\n")
        clogfile.close()
        appuifw.note(u"Log telah dihapus...","conf")
        back2set()
    else:
        back2set()
        
        
def back2set():
    try:
        appuifw.app.body.clear()
    except:
        pass
    user_settings()
        
        
# fungsi bantuan
def user_help():
    global sl_db_nm
    appuifw.app.title = u"Bantuan"
    helplist = [u"Buat Baru",u"Buka Berkas",u"Perbaharui Data",u"Mengganti Kata Sandi",u"Catatan Log",u"Tentang",u"Penolakan"]
    chelp = appuifw.selection_list(helplist)
    if chelp == 0:
        sl_db_nm = ["Membuat Berkas Baru","membuat_data_baru.txt"]
        rhelp()
    elif chelp == 1:
        sl_db_nm = ["Membuka Berkas","membuka_data.txt"]
        rhelp()
    elif chelp == 2:
        sl_db_nm = ["Memperbaharui Berkas","memperbaharui_data.txt"]
        rhelp()
    elif chelp == 3:
        sl_db_nm = ["Mengganti Kata Sandi","mengganti_password.txt"]
        rhelp()
    elif chelp == 4:
        sl_db_nm = ["Catatan Log","catatan_log.txt"]
        rhelp()
    elif chelp == 5:
        sl_db_nm = ["Tentang","about.txt"]
        rhelp()
    elif chelp == 6:
        sl_db_nm = ["Penolakan","disclaimer.txt"]
        rhelp()
    else:
        clear_text()
        
        
def rhelp():
    global fopenhelp
    appuifw.app.title = u"%s"%sl_db_nm[0]
    fopenhelp = ""
    if os.path.exists("%s\\usr\\%s"%(root_dir,sl_db_nm[1])):
        fopenhelp = "%s\\usr\\%s"%(root_dir,sl_db_nm[1])
        fopenhelpfile()
    elif os.path.exists("%s\\usr\\help\\%s"%(root_dir,sl_db_nm[1])):
        fopenhelp = "%s\\usr\\help\\%s"%(root_dir,sl_db_nm[1])
        fopenhelpfile()
    else:
        appuifw.note(u"KESALAHAN!\nBerkas bantuan tidak ditemukan...","error")
        appuifw.note(u"Periksa log untuk informasi lebih detail...","conf")
        hlperrlog()
        
        
def fopenhelpfile():
    hop = open("%s"%fopenhelp,"r")
    rhop = hop.read()
    hop.close()
    shelp = appuifw.Text()
    shelp.add(u"%s"%rhop)
    shelp.set_pos(0)
    appuifw.app.exit_key_handler = user_help
    appuifw.app.menu = [(u"Kembali", user_help)]
    appuifw.app.body = shelp
    
    
def hlperrlog():
    hlperr0 = time.time()
    hlperr1 = time.localtime(hlperr0)
    hlperrnote = "%s %s/%s/%s - %s:%s:%s\nKeterangan: Berkas bantuan %s tidak ditemukan. Lokasi seharusnya adalah [DRIVE]:\\System\\Apps\\passbox\\usr atau [DRIVE]:\\System\\Apps\\passbox\\usr\\help. Periksa lokasi tersebut, pastikan direktori dan file yang bersangkutan tidak dipindah dari lokasi yang seharusnya\n\n"%(hari[hlperr1.tm_wday], hlperr1.tm_mday, hlperr1.tm_mon, hlperr1.tm_year, hlperr1.tm_hour, hlperr1.tm_min, hlperr1.tm_sec, sl_db_nm[1])
    whlperr = open("%s\\log\\report.log"%root_dir,"a")
    whlperr.write(u"%s"%hlperrnote)
    whlperr.close()
    user_help()
    
    
    
def fu_clear_screen():
    try:
        appuifw.app.body.clear()
    except:
        pass
    user_open_db()
        
        
def clear_text():
    try:
        appuifw.app.body.clear()
    except:
        pass
    user_menu()
    
    
# fungsi keluar untuk user
def fu_quit():
    if appuifw.query(u"Keluar dari PassBox %s ?"%users,"query") == True:
        last_log()
    else:
        user_menu()
        
        
def last_log():
    ldt0 = time.time()
    ldt1 = time.localtime(ldt0)
    msg = "Logout %s pada:\n%s %s/%s/%s - %s:%s:%s\n"%(users, hari[ldt1.tm_wday], ldt1.tm_mday, ldt1.tm_mon, ldt1.tm_year, ldt1.tm_hour, ldt1.tm_min, ldt1.tm_sec)
    wlll = open("%s\\log\\last.log"%root_dir,"w")
    wall = open("%s\\log\\report.log"%root_dir,"a")
    stts = open("%s\\log\\status"%root_dir,"w")
    wlll.write(u"%s\n"%msg)
    wall.write(u"%s\n"%msg)
    stts.write(u"0")
    wlll.close()
    wall.close()
    stts.close()
    pb_run.signal()
    appuifw.app.set_exit()
        
        
def fu_exit():
    pb_run.signal()
    appuifw.app.set_exit()
    
    
pb_run = e32.Ao_lock()
fu_cek_install()
pb_run.wait()

#EOF
