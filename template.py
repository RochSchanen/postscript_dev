# file: template.py

""" the following  are the available and hiden classes, methods and variables

EOL # end-of-line
SPC # space character

_units = 72.0 / 25.4 # postscript default is 72ppi

fulldatetime():
exitProcess(em = None):
hexcolor(code): # "ffffff" returns (255,255,255)

fix(*X):
scl(*X):

AClass():
    PaperSize(self, Format):

psDoc():
    newpage(self, Origin = "tl"):
    write(self, Block):
    displayCrosshair(self, size = 50.0):
    thickness(self, Value):
    graycolor(self, Value):
    rgbcolor(self, r, g, b):
    hline(self, Position = 0.0):
    vline(self, Position = 0.0):
    hlines(self, *Positions):
    vlines(self, *Positions):
    hgrid(self, Start, Stop, nLines):
    vgrid(self, Start, Stop, nLines):
    circle(self, x, y, r):
    line(self, x1, y1, x2, y2):
    rectangle(self, x1, y1, x2, y2): # stroke
    box(self, x1, y1, x2, y2): # fill
    pagelink(self, l, r, t, b, page, debug = False):
    displaytext(self, l, b, txt, grayvalue = 1.0):

example: p.rgbcolor(*hexcolor("ffffff"))
"""

# from localtools import hexcolor
# from localtools import *

# class Doc(psDoc):

#     def writeblock(self, size = 50):
        
#         # setup
#         l, r = -size/2.0, +size/2.0

#         b, t = -size/2.0, +size/2.0
#         # define  block
#         BLOCK = f'''
        
#         /Courrier 20 selectfont

#         % --- CROSSHAIR ---
#         {scl(l, t, r, t, r, b)}
#         {scl(l, b)}
#         moveto 3 {{lineto}} repeat closepath stroke
#         gsave 0.3 setlinewidth [1 3 12 3] 0 setdash
#         {scl(l, 0.0)}
#         {scl(r, 0.0)}
#         moveto lineto stroke
#         {scl(0.0, b)}
#         {scl(0.0, t)}
#         moveto lineto stroke
#         grestore
#         '''
#         # export text
#         self.write(BLOCK)
#         # done
#         return

# create document
# d = Doc("./template.ps", Format = "A5")

# d.writeblock()
# d.displaytext(0, 0, "Hello World!")
# d.close()

#  from os import system as RunShellCmd

# RunShellCmd(' '.join([
#     f'"C:\\Program Files\\gs\\gs9.27\\bin\\gswin64.exe"', # ghostview
#     f'-sOutputFile=template.pdf', # destination file name
#     f'-dNOPAUSE', # option "no prompt" and "no pause between pages"
#     f'-dBATCH', # option "no interactive mode", exit after execute
#     f'-sPAPERSIZE=a5', # option papersize a0, a1, ...
#     f'-sDEVICE=pdfwrite', # option output file format: PDF
#     f'-dSAFER', # option filter ghostview file access for safety
#     f'template.ps', # source file name
#     ]))

# Program to display calendar of the given month and year

# importing calendar module
import calendar

# display the calendar
Y = calendar.calendar(2024)


sheet.read()
sheet.read("path")

x = sheet.col("name1")
y = sheet.col("name2")

x, y = sheet.Col("name1", "name2")

fg, ax = SelectFigure("figname")

Plot("figname", x, y, style = sheet.GetStyle("stylename"))

Plot("figname", x, y)
sheet.GetStyle("stylename")("figname")

s = sheet.GetStyle("stylename")
Plot("figname", x, y, style = s)
