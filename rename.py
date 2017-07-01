import os

ren_d=os.listdir('.')
ren_d_count=len(ren_d)
ren_d_loop=0

while ren_d_count > ren_d_loop:
    print 'CD to '+ren_d[ren_d_loop]
    if os.path.isdir(ren_d[ren_d_loop]):
        os.chdir(ren_d[ren_d_loop])
        ren_f=os.listdir('.')
        ren_f_i=ren_f
        ren_f_count=len(ren_f)
        ren_f_loop=0
        while ren_f_count > ren_f_loop:
            ren_f_n=ren_f_i[ren_f_loop]
            if 'ani' in ren_f_n:
                os.rename(ren_f_n,'%s.gif'\
                %ren_f_n)
            else:
                os.rename(ren_f_n,'%s.png'\
                %ren_f_n)
            ren_f_loop+=1
        os.chdir('..')
    ren_d_loop+=1

print 'Done!'