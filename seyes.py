# file: seyes.py

from postscript.postscript import exitProcess
from postscript.postscript import hexcolor
from postscript.postscript import document
    
# def page_number(n):
#     # display page number
#     p.text(r-5, t-6, f"{n}")
#     # done
#     return

# # import tool 
# from postscript.postscript import sca

# def page_border(m, w):
#     lm, rm, tm, bm = 0, 0, 0.3, 0
#     # define  block
#     BLOCK = f'''
#     % --- CURVE BREAK ---
#     {sca(l+w+lm, t-w-tm)} moveto
#     {sca(l+w+lm, b+w+bm)} lineto
#     {sca(r-m, b+w+bm)} lineto
#     {sca(r-m/2, b+w+bm, r-w-rm, b+m/2, r-w-rm, b+m)} curveto
#     {sca(r-w-rm, t-m)} lineto
#     {sca(r-w-rm, t-m/2, r-m/2, t-w-tm, r-m, t-w-tm)} curveto
#     {sca(l+w+lm, t-w-tm)} lineto
#     closepath
#     stroke
#     '''
#     # export text
#     p.write(BLOCK)
#     # done
#     return

# def rightIndent(pos, w, h):
#     # define  block
#     BLOCK = f'''
#     % --- RIGHT INDENT ---
#     {sca(r, pos+h/2)} moveto
#     {sca(r, pos, r-w, pos, r-w, pos-h/2)} curveto
#     {sca(r-w, b)} lineto
#     stroke
#     '''
#     # export text
#     p.write(BLOCK)
#     # done
#     return


p = document("./tmp", Size = "A5", Type = "ps")


def leftholes(p):
    # left
    p.circle(p.LEFT + 9.0, p.TOP - 55.75, 2.5)
    p.circle(p.LEFT + 9.0, p.TOP -154.75, 2.5)
    # done
    return

def rightholes(p):
    # left
    p.circle(p.LEFT + 9.0, p.TOP - 55.75, 2.5)
    p.circle(p.LEFT + 9.0, p.TOP -154.75, 2.5)
    # done
    return

n = 2

for page in range(n):

    if page: p.newpage()

    p.seyespage(
        20, # 20mm left margin 
        20, # 20mm top margin
        15, # 13 vertical main lines
        22, # 22 horizontal main lines
        )

    # p.thickness(w)
    # p.rgbcolor(*hexcolor("c8c8de"))

    # page_border(6, w/3.0)

    # h = (t-b)/n
    # for i in range(1, n-page):
    #     rightIndent(h*(i-n/2), 8, 8)

    # p.graycolor(0.5)
    # for i, txt in zip(
    #         range(0, n-page),
    #         ["Dimanche", "Samedi",
    #          "Vendredi", "Jeudi",
    #          "Mercredi", "Mardi",
    #          "Lundi"]):
        
    #     x, y = r-3, h*(i-n/2)
        
    #     # display text
    #     p.vtext(x, y+6, txt)

    #     # create links
    #     p.pagelink(r-8, r, y+h*0.05, y+h*0.95, n-i)

    p.rgbcolor(*hexcolor("c8c8de"))
    p.thickness(0.199)
    leftholes(p)

# p.graycolor(1.0)

exitProcess("end-of-code.")
