#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# redpdf v0.2
# Script digunakan untuk membaca berkas PS/PDF melalui terminal
#
# Script ini menggunakan beberapa program eksternal yang sebelumnya
# harus sudah terinstall di sistem.
#
# Diantaranya adalah:
#   - pdftohtml
#   - ps2pdf
#   - enscript
#   - lynx
#
#
#
# Oleh	: cupucupu
# eMail	: desktop.hobbie@gmail.com
# Blog	: http://desktop-hobbie.blogspot.com
# Info	: http://pages.google.com/page/cuputoys/redpdf
#
# July 2011
#

import os
import sys
import gzip

# program banner ... :P
REDPDF_MSG = """
\xdb\xdb\xdb\xb2\xdf\xdf\xdf\xdf\xdf\xb2\xdb\xdb\xdb\xdb\xdb\xdb\xdb \
\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb  \xde\xdb\xdb\
\xdb\xdb\xb2\xdf\xdf\xdf\xdf\xdf\xb2\xdb\xdb\xdb\xdb\xdb\xb2\xdf\xdf\
\xdf\xdf\xb2\xb2\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xb2\xdf\xdf\xdf\xdf\
\xdf\xdf\xdf\xdf\xdb\n\xdb\xdb\xdb'      \xd4\xb2\xdb\xdb\xdb\xdb\xdb\
\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb  \xde\xdb\xdb\
\xdb\xdb'      \xd4\xb2\xdb\xdb\xdb\xdd      \xc4\xdf\xdb\xdb\xdb\xdb\
\xdb\xdb\xdd        \xb2\n\xdb\xdb\xdb   \xdc\xdc\xd6. )\xdb\xdb\xdb\xdb\
\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb  \xde\xdb\
\xdb\xdb\xdb   \xdc\xdc\xd6. \xd4\xdb\xdb\xdb\xdd j\xdc\xdc\xd6,  M\xdb\
\xdb\xdb\xdb\xdb\xdd \xaa\xdc\xdc\xdc\xdc. \xb2\n\xdb\xdb\xdb  \xf9\xdb\
\xdb\xdb\xb2  \xde\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\
\xdb\xdb\xdb\xdb\xdb  \xde\xdb\xdb\xdb\xdb  \xf9\xdb\xdb\xdb\xb2  \xde\xdb\
\xdb\xdd \xde\xdb\xdb\xdb\xdb\xdc  \xde\xdb\xdb\xdb\xdb\xdd \xde\xdb\xdb\
\xdb\xdb\xdb\xdb\xdb\n\xdb\xdb\xdb   \xdb\xdb\xdb\xdb  \xde\xdb\xdb\xdb\
\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xb2\xdf\xdf\xdb  \xde\xdb\xdb\
\xdb\xdb   \xdb\xdb\xdb\xdb  \xde\xdb\xdb\xdd \xde\xdb\xdb\xdb\xdb\xdb\xdd \
\xfb\xdb\xdb\xdb\xdb\xdd \xde\xdb\xdb\xdb\xdb \xde\xdb\n\xdb\xdb\xdb   \xdb\
\xdb\xdb\xdd  \xde\xdb\xdb\xdb\xdf` \xc4\xdf\xdb\xdb\xdb\xdb\xdb\xfd   -  \
\xde\xdb\xdb\xdb\xdb   \xdb\xdb\xdb\xdd  \xde\xdb\xdb\xdd \xde\xdb\xdb\xdb\
\xdb\xdb\xdb, \xdb\xdb\xdb\xdb\xdd \xde\xdb\xdb\xdb\xa5 \xde\xdb\n\xdb\xdb\
\xdb   \xdb\xdb\xdbF  \xb2\xdb\xdb\xfd     \xfb\xdb\xdb\xdb\xdd  \xd6\xdc   \
\xde\xdb\xdb\xdb\xdb   \xdb\xdb\xdbE  \xde\xdb\xdb\xdd \xde\xdb\xdb\xdb\xdb\
\xdb\xdbf \xb2\xdb\xdb\xdb\xdd       \xde\xdb\n\xdb\xdb\xdb   \xdf\xdf\xfd  j\
\xdb\xdb\xdd j\xdb\xdb\xb2p \xb2\xdb\xdb  j\xdb\xdb\xdd  \xde\xdb\xdb\xdb\xdb   \
\xdf\xdf\xbc  \xaa\xdb\xdb\xdb\xdd \xde\xdb\xdb\xdb\xdb\xdb\xdb\xdd \xde\xdb\
\xdb\xdb\xdd       \xde\xdb\n\xdb\xdb\xdb  \xbf   _\xdc\xdb\xdb\xdb[ \xbc\xdf\
\xdf\xdf\xbc \xde\xdb\xb2  \xb2\xdb\xdb\xdb  \xde\xdb\xdb\xdb\xdb       j\xb2\
\xdb\xdb\xdb\xdd \xde\xdb\xdb\xdb\xdb\xdb\xdb\xdd \xde\xdb\xdb\xdb\xdd  \xb2\
\xdb\xdb\xb2 \xde\xdb\n\xdb\xdb\xdb  \xde\xdd  \xdb\xdb\xdb\xdb\xdb`       \
\xde\xdb\xdd  \xdb\xdb\xdb\xdb  \xde\xdb\xdb\xdb\xdb  j\xdc\xdc\xdc\xb2\xdb\
\xdb\xdb\xdb\xdb\xdd \xd4\xb2\xdb\xdb\xdb\xdb\xb2\xf9 \xb2\xdb\xdb\xdb\xdd  \
\xb2\xdb\xdb\xdb\xdc\xb2\xdb\n\xdb\xdb\xdb  \xde\xdbr \xde\xdb\xdb\xdb\xdb  j\
\xdc\xdc\xdc\xdc\xdc\xb2\xdb\xdd  \xdb\xdb\xdb\xdb  \xde\xdb\xdb\xdb\xdb  \xde\
\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdd  \xb2\xdb\xdb\xdb\xdb\xdd  \xb2\
\xdb\xdb\xdb\xdd  \xb2\xdb\xdb\xdb\xdb\xdb\xdb\n\xdb\xdb\xdb  \xde\xdb\xb2  \
\xb2\xdb\xdb\xdb. \xde\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdd  \xdb\xdb\xdb\xb2  \xde\
\xdb\xdb\xdb\xdb  \xde\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdd  \xb2\xdb\xdb\
\xdb\xdb\xdd \xfa\xdb\xdb\xdb\xdb\xdd  \xb2\xdb\xdb\xdb\xdb\xdb\xdb\n\xdb\xdb\
\xdb  \xde\xdb\xdb\xe5 \xfb\xdb\xdb\xdb\xe5 \xde\xdb\xdb\xdb\xdb\xdb\xdb\xdb\
\xdd  \xb2\xdb\xdb\xdd  \xde\xdb\xdb\xdb\xdb  \xde\xdb\xdb\xdb\xdb\xdb\xdb\xdb\
\xdb\xdb\xdd  \xb2\xdb\xdb\xdb\xdbf j\xdb\xdb\xdb\xdb\xdd  \xb2\xdb\xdb\xdb\xdb\
\xdb\xdb\n\xdb\xdb\xdb  \xde\xdb\xdb\xb2  \xde\xdb\xdb\xdd  \xdf\xdb\xdb\xdb\xdb\
\xdb\xdb\xdb  \xfb\xdb\xdb\xfd  \xde\xdb\xdb\xdb\xdb  \xde\xdb\xdb\xdb\xdb\xdb\
\xdb\xdb\xdb\xdb\xdd  \xb2\xdb\xdb\xdb\xb2\xf9 \xb2\xdb\xdb\xdb\xdb\xdd  \xb2\xdb\
\xdb\xdb\xdb\xdb\xdb\n\xdb\xdb\xdb  \xde\xdb\xdb\xdb\xdd -\xb2\xdb\xdb/   \xc4\
\xb2\xdb\xdb\xdb\xdbp       \xde\xdb\xdb\xdb\xdb  \xde\xdb\xdb\xdb\xdb\xdb\xdb\
\xdb\xdb\xdb\xdd  \xdf\xdf\xdf\xdf` \xc9\xdb\xdb\xdb\xdb\xdb\xdd  \xb2\xdb\xdb\
\xdb\xdb\xdb\xdb\n\xdb\xdb\xdb. \xde\xdb\xdb\xdb\xdbr \xde\xdb\xdb\xb2p   \xde\
\xdb\xdb\xdb\xdb\xdbp   .  \xde\xdb\xdb\xdb\xdb. \xde\xdb\xdb\xdb\xdb\xdb\xdb\
\xdb\xdb\xdb\xdd      _\xdc\xdb\xdb\xdb\xdb\xdb\xdb\xdd  \xb2\xdb\xdb\xdb\xdb\
\xdb\xdb\n\xdb\xdb\xdb\xb2\xdc\xdb\xdb\xdb\xdb\xdb\xdb\xdc\xdb\xdb\xdb\xdb\xdb\
\xb2\xdc\xdc\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xb2\xdc\xdc\xb2\xb2\xdc\xdb\xdb\xdb\
\xdb\xdb\xb2\xdc\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xb2\xdc\xdc\xdc\xdc\
\xdc\xb2\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xdb\xb2\xdc\xdc\xb2\xdb\xdb\xdb\xdb\xdb\xdb"""
print '%sv0.2'%REDPDF_MSG

# text file and executable
# from /usr/share/enscript/hl
TextFiles=['ada','asm','awk','bash','c','changelog','cpp','csh','delphi',
           'diff','diffs','diffu','elisp','enscript','f90','fortrant','haskell',
           'idl','inf','java','javascript','ksh','m4','mail','makefile','matlab',
           'nroff','objc','outline','pascal','passthrough','perl','pyrex','python',
           'rfc','scheme','sh','skill','sql','states','synopsys','tcl','tcsh','tex',
           'vba','verilog','vhdl','vrml','zsh']


def END_SCRIPT():
    print "\nReading done!\nBye,... :)"
    
def NotSupportedFileTypes(sources):
    print '\n%s: File type not supported!'%sources

def ReadXML(sources):
    os.system('enscript -B --highlight=wmlscript -c --style=emacs --language=html -t \'%s\' -o \'/tmp/%s.html\' \'%s\''%(os.path.basename(sources),os.path.basename(sources),sources))
    RunLynx('/tmp/%s.html'%os.path.basename(sources),True)
    
def ReadScripts(sources,hlg):
    os.system('enscript -B -c -t \'%s\' --highlight=%s --style=emacs --language=html -o \'/tmp/%s.html\' \'%s\''%(os.path.basename(sources),hlg,os.path.basename(sources),sources))
    RunLynx('/tmp/%s.html'%sources,True)

def ReadPDF(sources,gzipped=False):
    if gzipped==True:
        print '\nDecompressing documents,... [%s]'%FILE_NAME
        RGZ=gzip.open(sources)
        GGZ=RGZ.read()
        RGZ.close()
        WTF=open('/tmp/%s'%os.path.basename(sources[:-3]),'wb')
        WTF.write(GGZ)
        WTF.close()
        os.system('pdftohtml -q -p -c -i -noframes -nodrm \'/tmp/%s\' \'/tmp/%s.html\''%(os.path.basename(sources[:-3]),os.path.basename(sources[:-3])))
        os.remove('/tmp/%s'%os.path.basename(sources[:-3]))
        RunLynx('/tmp/%s.html'%os.path.basename(sources[:-3]),True)
    else:
        os.system('pdftohtml -q -p -c -i -noframes -nodrm \'%s\' \'/tmp/%s.html\''%(sources,os.path.basename(sources)))
        RunLynx('/tmp/%s.html'%os.path.basename(sources),True)
        
def ReadPS(sources,gzipped=False):
    if gzipped==True:
        print '\nDecompressing documents,... [%s]'%FILE_NAME
        RGZ=gzip.open(sources)
        GGZ=RGZ.read()
        RGZ.close()
        WTF=open('/tmp/%s.ps'%os.path.basename(sources[:-3]),'wb')
        WTF.write(GGZ)
        WTF.close()
        os.system('ps2pdf \'/tmp/%s.ps\' \'/tmp/%s.pdf\''%(os.path.basename(sources[:-3]),os.path.basename(sources[:-3])))
        os.system('pdftohtml -q -p -c -i -noframes -nodrm \'/tmp/%s.pdf\' \'/tmp/%s.html\''%(os.path.basename(sources[:-3]),os.path.basename(sources[:-3])))
        os.remove('/tmp/%s.ps'%os.path.basename(sources[:-3]))
        os.remove('/tmp/%s.pdf'%os.path.basename(sources[:-3]))
        RunLynx('/tmp/%s.html'%os.path.basename(sources[:-3]),True)
    else:
        os.system('ps2pdf \'%s\' \'/tmp/%s.pdf\''%(sources,os.path.basename(sources)))
        os.system('pdftohtml -q -p -c -i -noframes -nodrm \'/tmp/%s.pdf\' \'/tmp/%s.html\''%(os.path.basename(sources),os.path.basename(sources)))
        os.remove('/tmp/%s.pdf'%os.path.basename(sources))
        RunLynx('/tmp/%s.html'%os.path.basename(sources),True)

def RunLynx(sources,RemV=False):
    os.system('lynx \'%s\''%sources)
    if RemV==True:
        os.remove(sources)
    END_SCRIPT()

try:
    FILE_NAME = sys.argv[1] # mengambil input user dari shell ($ redpdf file.pdf <enter>)
    # hanya satu perintah/ opsi yang disediakan
    # dan hanya untuk melihat/ menampilkan versi program
    if FILE_NAME == "-v": # <- bila input yang ditangkap adalah '-v'
        print "\t\t-----------------------------------------------"
        print "\t\t\tRedPDF Version 0.2 (jul 2011)"
        print "\t\t  Using htmltopdf, ps2pdf enscript and lynx"
        print "\t\t-----------------------------------------------"
        print "\t\t   By: cupucupu <desktop.hobbie@gmail.com>"
        print "\t\t-----------------------------------------------"
    else: # bila input yang ditangkap selain '-v'
        # tampilkan sesuatu :D
        print "\nProcessing %s..."%FILE_NAME,
        os.system('file \'%s\' > /tmp/redpdf~'%FILE_NAME)
        ReadTypes=open('/tmp/redpdf~','r')
        GetType=ReadTypes.read().split(':')
        ReadTypes.close()
        os.remove('/tmp/redpdf~')
        FH=''
        if '.pdf",' in GetType[1].lower():
            ReadPDF(FILE_NAME,True)
        elif '.ps",' in GetType[1].lower():
            ReadPS(FILE_NAME,True)
        elif 'pdf document' in GetType[1].lower():
            ReadPDF(FILE_NAME,False)
        elif 'postscript document' in GetType[1].lower():
            ReadPS(FILE_NAME,False)
        elif 'xml' in GetType[1].lower():
            ReadXML(FILE_NAME)
        elif 'html' in GetType[1].lower():
            RunLynx(FILE_NAME,False)
        else:
            X=0
            Y=len(TextFiles)-1
            Z=False
            while X<=Y:
                if TextFiles[X] in GetType[1].lower():
                    Z=True
                    break
                X+=1
            if Z==True:
                ReadScripts(FILE_NAME,TextFiles[X])
            else:
                NotSupportedFileTypes(FILE_NAME)
except IndexError: # bila program dijalankan tanpa input ($ redpdf <enter>)
    print "\t\t-----------------------------------------------"
    print "\t\tBy\t: cupucupu <desktop.hobbie@gmail.com>"
    print "\t\t-----------------------------------------------"
    print "\t\t Usage: python redpdf.py <filename>"
    print "\t\t\t-v = print out the program version"
    print "\t\t-----------------------------------------------"
    
# EOF
