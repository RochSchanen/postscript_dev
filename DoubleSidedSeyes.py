# file: DoubleSidedSeyes.py

from localtools import exitProcess
from localtools import hexcolor
from localtools import psDoc

### SEYES RULES AND HOLES FOR A SINGLE A5 SIZE PAGE ###
def seyes(lm = 0, rm = 0, tm = 0, bm = 0, vn = 13):
    p.rgbcolor(*hexcolor("c8c8de"))
    p.thickness(0.199)
    # horizontal sub grid
    topmargin, lines = t-20, 22*4+2
    p.hgrid(topmargin,  topmargin -(lines-1)*2, lines, lm, rm)
    p.thickness(0.398)
    # horizontal main grid
    topmargin, lines = t-20-3*2, 22
    p.hgrid(topmargin,  topmargin -(lines-1)*8, lines, lm, rm)
    # vertical main grid
    leftmargin, lines = l+44, vn
    p.vgrid(leftmargin, leftmargin+(lines-1)*8, lines, tm, bm)
    # vertical margin
    p.rgbcolor(*hexcolor("f6bbcf"))
    p.vline(l+36, tm, bm)
    # done
    return
    
def leftholes():
    # left
    p.circle(l + 9.0, t - 55.75, 2.5)
    p.circle(l + 9.0, t -154.75, 2.5)
    # done
    return

def page_number(n):
    # display page number
    p.text(r-5, t-6, f"{n}")
    # done
    return

# import tool 
from localtools import scl

def page_border(m, w):
    lm, rm, tm, bm = 0, 0, 0.3, 0
    # define  block
    BLOCK = f'''
    % --- CURVE BREAK ---
    {scl(l+w+lm, t-w-tm)} moveto
    {scl(l+w+lm, b+w+bm)} lineto
    {scl(r-m, b+w+bm)} lineto
    {scl(r-m/2, b+w+bm, r-w-rm, b+m/2, r-w-rm, b+m)} curveto
    {scl(r-w-rm, t-m)} lineto
    {scl(r-w-rm, t-m/2, r-m/2, t-w-tm, r-m, t-w-tm)} curveto
    {scl(l+w+lm, t-w-tm)} lineto
    closepath
    stroke
    '''
    # export text
    p.write(BLOCK)
    # done
    return

def rightIndent(pos, w, h):
    # define  block
    BLOCK = f'''
    % --- RIGHT INDENT ---
    {scl(r, pos+h/2)} moveto
    {scl(r, pos, r-w, pos, r-w, pos-h/2)} curveto
    {scl(r-w, b)} lineto
    stroke
    '''
    # export text
    p.write(BLOCK)
    # done
    return

p = psDoc("./doublesidedseyes.ps", Format = "A5")

l, r, t, b, w = p.LEFT, p.RIGHT, p.TOP, p.BOTTOM, 0.099

for page in range(7):

    if page: p.newpage()

    seyes(rm = 8, vn = 12)

    p.thickness(w)
    p.rgbcolor(*hexcolor("c8c8de"))

    page_border(6, w/3.0)

    for i in range(1, 7-page):
        rightIndent((t-b)/7*(i-7/2), 8, 8)

    for i, txt in zip(
            range(0, 7-page),
            ["Dimanche", "Samedi", "Vendredi", "Jeudi",
            "Mercredi", "Mardi", "Lundi"]):
        p.vtext(r-3, (t-b)/7*(i-7/2)+6, txt)

    p.thickness(w)
    leftholes()

p.graycolor(1.0)

exitProcess("end-of-code.")

