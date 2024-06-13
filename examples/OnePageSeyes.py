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

    from postscript.postscript import sca

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

############################## MAIN ##############################

from postscript.postscript import document
from postscript.postscript import hexcolor

p = document(Size = "A5")
p.seyespage(20, 20, 15, 22) # narrow margin

p.rgbcolor(*hexcolor("c8c8de"))

# homemade border
p.thickness(0.099)
border(p, 8, 0.099)

# holes
p.thickness(0.199)
leftholes(p)

from sys import exit
# done
exit()
