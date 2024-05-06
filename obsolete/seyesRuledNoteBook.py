# file: seyesRuledNoteBook.py

import postscript as ps
p = ps.document()


exit()

# from postscript import hexcolor
# from postscript import document

# create document
p = ps.document("./notebook.ps", Size = "A5")

# get geometry
l, r, t, b = p.LEFT, p.RIGHT, p.TOP, p.BOTTOM

##################
### FRONT PAGE ###
##################

Y = [50, 80, 110]

# decor
# p.rgbcolor(*hexcolor("e5e8e8"))
# m = 0; p.box(l+m, b+m, r-m, t-m)
p.rgbcolor(*hexcolor("ffffff"))
p.box(l+20, t-50+30, r-20, t-110-30)

# lines
# p.thickness(0.599)
p.thickness(0.398)
p.rgbcolor(*hexcolor("c8c8de"))
m = ((r-l)-90.0)/2.0 # margin
for i, y in enumerate(Y):
    p.line(l+m, t-y, r-m, t-y)

# punch left holes
p.graycolor(0.2)
p.thickness(0.199)
p.circle(l + 9.0, t - 55.75, 2.5)
p.circle(l + 9.0, t -154.75, 2.5)

###################
### SECOND PAGE ###
###################

p.newpage()
p.rgbcolor(*hexcolor("c8c8de"))
p.thickness(0.199)

# horizontal main grid
topmargin, lines = t-20-3*2, 22
p.hgrid(topmargin, topmargin-(lines-1)*8, lines)
for n in range(22):
    # create links
    p.pagelink(l+16-0.5, l+16+3.5, topmargin-n*8+6, topmargin-n*8, n+3)
    # diplay index
    p.displaytext(l+16, topmargin-n*8+2, f"{n+3}")

# punch right holes
p.graycolor(0.2)
p.thickness(0.199)
p.circle(r - 9.0, t - 55.75, 2.5)
p.circle(r - 9.0, t -154.75, 2.5)


### SEYES RULED PAGES ###

for n in range(3, 25):
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
    p.graycolor(0.2)
    p.thickness(0.199)
    if n % 2 == 0:
        # right
        p.circle(r - 9.0, t - 55.75, 2.5)
        p.circle(r - 9.0, t -154.75, 2.5)
    if n % 2 == 1:
        # left
        p.circle(l + 9.0, t - 55.75, 2.5)
        p.circle(l + 9.0, t -154.75, 2.5)
    
    # display page number
    p.displaytext(r-5, t-6, f"{n}", 0.6)
