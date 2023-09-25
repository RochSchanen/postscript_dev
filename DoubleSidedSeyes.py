# file: DoubleSidedSeyes.py

from localtools import exitProcess
from localtools import hexcolor
from localtools import psDoc

# create document
p = psDoc("./doublesidedseyes.ps", Format = "A5")

# get geometry
l, r, t, b = p.LEFT, p.RIGHT, p.TOP, p.BOTTOM

### SEYES RULES AND HOLES FOR AN A5 SIZE DOUBLE SIDED PAGE ###

def seyes():

    p.rgbcolor(*hexcolor("c8c8de"))
    p.thickness(0.199)

    # horizontal sub grid
    topmargin, lines = t-20, 22*4+2
    p.hgrid(topmargin, topmargin-(lines-1)*2, lines)
    p.thickness(0.398)

    # horizontal main grid
    topmargin, lines = t-20-3*2, 22
    p.hgrid(topmargin, topmargin-(lines-1)*8, lines)

    # vertical main grid
    leftmargin, lines = l+44, 13
    p.vgrid(leftmargin, leftmargin+(lines-1)*8, lines)

    # vertical margin
    p.rgbcolor(*hexcolor("f6bbcf"))
    p.vline(l+36)


def rightholes():
    p.graycolor(0.2)
    p.thickness(0.199)
    # right
    p.circle(r - 9.0, t - 55.75, 2.5)
    p.circle(r - 9.0, t -154.75, 2.5)
    
def leftholes():
    p.graycolor(0.2)
    p.thickness(0.199)
    # left
    p.circle(l + 9.0, t - 55.75, 2.5)
    p.circle(l + 9.0, t -154.75, 2.5)

def pagenumber():
    # display page number
    p.displaytext(r-5, t-6, f"{n}", 0.6)


seyes()
leftholes()
p.newpage()
seyes()
rightholes()

exitProcess("end-of-code.")
