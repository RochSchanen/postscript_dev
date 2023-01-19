# file: seyesRuledNoteBook.py

from localtools import exitProcess
from localtools import hexcolor
from localtools import psDoc

# create document
p = psDoc("./notebook.ps", Format = "A5")

# get geometry
l, r, t, b = p.LEFT, p.RIGHT, p.TOP, p.BOTTOM

### FRONT PAGE ###

Y = [50, 80, 110]

# decor
p.rgbcolor(*hexcolor("e5e8e8"))
m = 0; p.box(l+m, b+m, r-m, t-m)
p.rgbcolor(*hexcolor("ffffff"))
p.box(l+20, t-50+30, r-20, t-110-30)

# lines
# p.thickness(0.599)
p.thickness(0.398)
p.rgbcolor(*hexcolor("f6bbcf"))
m = ((r-l)-90.0)/2.0 # margin
for y in Y:
    p.line(l+m, t-y, r-m, t-y)

# punch holes
p.graycolor(0.3)
p.thickness(0.199)
p.circle(l + 9.0, t - 55.75, 2.5)
p.circle(l + 9.0, t -154.75, 2.5)

### SEYES RULED PAGES ###

for n in range(24):
    p.newpage()
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

    # punch holes
    p.graycolor(0.3)
    p.thickness(0.199)
    p.circle(l + 9.0, t - 55.75, 2.5)
    p.circle(l + 9.0, t -154.75, 2.5)

exitProcess("end-of-code.")
