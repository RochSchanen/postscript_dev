# file: seyesRuledNoteBook.py

from localtools import exitProcess
from localtools import hexcolor
from localtools import psDoc

p = psDoc("./notebook.ps", Format = "A5")

### FRONT PAGE ###

# lines
p.rgbcolor(*hexcolor("c8c8de"))
p.thickness(0.599)
m = ((p.RIGHT-p.LEFT)-90.0)/2.0
l, r, Y = p.LEFT+m, p.RIGHT-m, [50, 80, 110]
for y in Y: p.line(l, p.TOP-y, r, p.TOP-y)
# punch holes
p.graycolor(0.3)
p.thickness(0.199)
p.circle(p.LEFT + 9.0, p.TOP - 55.75, 2.5)
p.circle(p.LEFT + 9.0, p.TOP -154.75, 2.5)

### SEYES RULED PAGES ###

for n in range(25):
    p.newpage()
    p.rgbcolor(*hexcolor("c8c8de"))
    p.thickness(0.199)
    # horizontal sub grid
    topmargin, lines = p.TOP-20, 22*4+2
    p.hgrid(topmargin, topmargin-(lines-1)*2, lines)
    p.thickness(0.398)
    # horizontal main grid
    topmargin, lines = p.TOP-20-3*2, 22
    p.hgrid(topmargin, topmargin-(lines-1)*8, lines)
    # vertical main grid
    leftmargin, lines = p.LEFT+44, 13
    p.vgrid(leftmargin, leftmargin+(lines-1)*8, lines)
    # vertical margin
    p.rgbcolor(*hexcolor("f6bbcf"))
    p.vline(p.LEFT+36)
    # punch holes
    p.graycolor(0.3)
    p.thickness(0.199)
    p.circle(p.LEFT + 9.0, p.TOP - 55.75, 2.5)
    p.circle(p.LEFT + 9.0, p.TOP -154.75, 2.5)

exitProcess("end-of-code.")
