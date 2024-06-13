# file: OnePageSeyes.py
# author: Roch Schanen
# created: 2024 05 06
# content: example of generated document using the postscript package
# repository: https://github.com/RochSchanen/postscript_dev
# comment: extra functions using the library are examplified

############################## FUNCTIONS ##############################

def border(p, m, w):
    # w is the line width
    # m is the corner radius

    from pslib.postscript import sca

    # corrective values
    lm, rm, tm, bm = 0.0, 0.0, 0.3, 0.0

    l, r, t, b = p.LEFT, p.RIGHT, p.TOP, p.BOTTOM

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

def leftholes(p):
    # left
    p.circle(p.LEFT + 9.0, p.TOP - 55.75, 2.5)
    p.circle(p.LEFT + 9.0, p.TOP -154.75, 2.5)
    # done
    return

def rightIndent(p, v, w, h):

    from pslib.postscript import sca

    # get geometry
    r = p.RIGHT-0.2

    # define  block
    BLOCK = f'''
    % --- RIGHT INDENT ---
    {sca(r, v+h/2)} moveto
    {sca(r, v, r-w, v, r-w, v-h/2)} curveto
    {sca(r-w, v-h/2-6)} lineto
    stroke
    '''
    # export text
    p.write(BLOCK)
    # done
    return

############################## MAIN ##############################

from pslib.postscript import document
from pslib.postscript import hexcolor

p = document(Size = "A5")

# make border
p.rgbcolor(*hexcolor("c8c8de"))
# p.thickness(0.099)
p.thickness(0.199)
# border(p, 4, 0.099)
border(p, 4, 0.199)

# make indents
p.rgbcolor(*hexcolor("c8c8de"))
from numpy import linspace
V = linspace(p.BOTTOM+10, p.TOP-10, 25)
for v in V: rightIndent(p, v, 4, 6)

# make letters
p.graycolor(0.4)
from numpy import insert
V = insert(V,0, V[0]-7)
for i, v in enumerate(V):
    p.htext(p.RIGHT-3.5, v+2.5, chr(90-i))
    p.pagelink(p.RIGHT-3.8, p.RIGHT-0.5, v+1.7, v+5.7, 27-i)

# holes
p.rgbcolor(*hexcolor("c8c8de"))
p.thickness(0.199)
leftholes(p)

for pn in range(26):

    p.newpage()

    # make large seyes page
    p.seyespage(20, 20, 15, 22) # narrow margin

    # clear out a white band of 4mm on the right of the page
    p.graycolor(0)
    p.box(p.RIGHT-4, p.TOP, p.RIGHT, p.BOTTOM)

    # make border
    p.rgbcolor(*hexcolor("c8c8de"))
    # p.thickness(0.099)
    p.thickness(0.199)
    # border(p, 4, 0.099)
    border(p, 4, 0.199)

    # make indents
    p.rgbcolor(*hexcolor("c8c8de"))
    from numpy import linspace
    V = linspace(p.BOTTOM+10, p.TOP-10, 25)
    for v in V: rightIndent(p, v, 4, 6)

    # make letters
    p.graycolor(0.4)
    from numpy import insert
    V = insert(V,0, V[0]-7)
    for i, v in enumerate(V):
        p.htext(p.RIGHT-3.5, v+2.5, chr(90-i))
        p.pagelink(p.RIGHT-3.8, p.RIGHT-0.5, v+1.7, v+5.7, 27-i)

    # select page
    p.graycolor(1)
    p.htext(p.RIGHT-3.5, V[25-pn]+2.5, chr(90-(25-pn)))

    # holes
    p.rgbcolor(*hexcolor("c8c8de"))
    p.thickness(0.199)
    leftholes(p)

from sys import exit
# done
exit()
