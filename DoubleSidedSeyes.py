# file: DoubleSidedSeyes.py

from postscript.postscript import exitProcess
from postscript.postscript import hexcolor
from postscript.postscript import document

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
    leftmargin, lines = l+44+8*2, vn-2
    p.vgrid(leftmargin, leftmargin+(lines-1)*8, lines, tm, bm)
    # vertical margin
    p.rgbcolor(*hexcolor("f6bbcf"))
    # p.vline(l+36, tm, bm)
    p.vline(l+36-5, tm, bm) # shift left 5mm from the standard position
    # second vertical margin
    p.rgbcolor(*hexcolor("f6bbcf"))
    p.vline(l+36+8*2, tm, bm)
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
from postscript.postscript import sca

def page_border(m, w):
    lm, rm, tm, bm = 0, 0, 0.3, 0
    # define  block
    BLOCK = f'''
    % --- CURVE BREAK ---
    {sca(l+w+lm, t-w-tm)} moveto
    {sca(l+w+lm, b+w+bm)} lineto
    {sca(r-m, b+w+bm)} lineto
    {sca(r-m/2, b+w+bm, r-w-rm, b+m/2, r-w-rm, b+m)} curveto
    {sca(r-w-rm, t-m)} lineto
    {sca(r-w-rm, t-m/2, r-m/2, t-w-tm, r-m, t-w-tm)} curveto
    {sca(l+w+lm, t-w-tm)} lineto
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
    {sca(r, pos+h/2)} moveto
    {sca(r, pos, r-w, pos, r-w, pos-h/2)} curveto
    {sca(r-w, b)} lineto
    stroke
    '''
    # export text
    p.write(BLOCK)
    # done
    return

p = document("./tmp", Size = "A5", Type = "ps")

l, r, t, b, w = p.LEFT, p.RIGHT, p.TOP, p.BOTTOM, 0.299

n = 7

for page in range(n):

    if page: p.newpage()

    seyes(rm = 8, vn = 12)

    p.thickness(w)
    p.rgbcolor(*hexcolor("c8c8de"))

    page_border(6, w/3.0)

    h = (t-b)/n
    for i in range(1, n-page):
        rightIndent(h*(i-n/2), 8, 8)

    p.graycolor(0.5)
    for i, txt in zip(
            range(0, n-page),
            ["Dimanche", "Samedi",
             "Vendredi", "Jeudi",
             "Mercredi", "Mardi",
             "Lundi"]):
        
        x, y = r-3, h*(i-n/2)
        
        # display text
        p.vtext(x, y+6, txt)

        # create links
        p.pagelink(r-8, r, y+h*0.05, y+h*0.95, n-i)

    # p.rgbcolor(*hexcolor("c8c8de"))
    # p.thickness(w)
    # leftholes()

p.graycolor(1.0)

exitProcess("end-of-code.")
