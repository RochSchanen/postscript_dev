#!/usr/bin/python3
# content: local tools
# file: localtools.py
# date: 2023 01 17
# author: Roch Schanen
# repository: https://github.com/RochSchanen/postscript_dev
# packages: only built-in libraries
# comment: (default output to './p.ps')

EOL = "\x0A"    # end-of-line
SPC = "\x20"    # space character

def fulldatetime():
    from time import strftime 
    return strftime("%A, %d %b %Y at %H:%M:%S")

def exitProcess(em = None):
    from sys import exit
    if em is None: em = "done"
    print(em)
    print("exit process.")
    return exit()

### A-class paper sizes (millimeters)

class AClass():

    def __init__(self):
        # largest size
        d = {"A0" : (841, 1189)}
        # smaller sizes
        for i in range(10):
            W, H = d[f"A{i}"]
            d[f"A{i+1}"] = (round(H/2), W)
        # register dictionary
        self.sizes = d
        # done
        return

    def PaperSize(self, Format):
        return self.sizes[Format]

### COLOR CODE CONVERSION

def hexcolor(code):
    r = int(code[0:2], 16)
    g = int(code[2:4], 16)
    b = int(code[4:6], 16)
    return r/255, g/255, b/255

### NUMBER FORMATING AND SCALING ###

# fixed point formating function
# the finest resolution is 0.001 pixel
# an arbitrary list of arguments can be used
def fix(*X):
    S = ""
    for x in X:
        s = f"{x:+08.3f}"
        S = f"{S} {s}" if S else s
    return S

# default units (pixels per mm)
# the default postscript document resolution
# is 72 points per inches
_units = 72.0 / 25.4

# scaling and formating function
# an arbitrary list of arguments can be used
def scl(*X):
    Y = []
    for x in X:
        Y.append(x*_units)
    return fix(*Y)

### POSTSCRIPT DOCUMENT CLASS ###

class psDoc():

    # open file, write header, setup font, and fix the origin
    def __init__(self, Path = "./p.ps", Format = "A4", filetype = "ps"):
        # init page counter
        self.n = 1
        # setup document size
        w, h = None, None
        # try AClass document size:
        if Format in AClass().sizes.keys(): 
            w, h = AClass().PaperSize(Format)
        # try user size
        if "x" in Format.lower():
            w, h = (float(s) for s in Format.split("x"))
            print(w, h)
        # check parsing result
        if (w, h) == (None, None):
            exitProcess("Document format parsing failed")
        # convert into points, inches
        self.size = w*_units, h*_units
        # get file handle
        fh = open(Path, 'w')
        if fh is None:
            exitProcess(f"failed to open '{Path}'")
        # register file handle
        self.fh = fh
        # write file magic (two file types available)
        magic = {
            "eps": f"%!PS-Adobe-3.0 EPSF-3.0{EOL}",
            "ps" : f"%!PS-Adobe-3.0{EOL}",
        }
        fh.write(magic[filetype])
        # create buffer
        self.text = ""
        # get geometry
        w, h = self.size
        print(w, h)
        # define header block
        BLOCK = f"""
        %%BoundingBox: 0 0 {w:.0f} {h:.0f}
        %%Creator:
        %%Title:
        %%CreationDate: {fulldatetime()}
        %%Pages: 001

        % set defaults font
        % /Times-Roman 8 selectfont
        /Courier 12 selectfont

        %%Page: 1 1

        % --- SET ORIGIN AT PAGE CENTER ---
        {w/2:.0f} {h/2:.0f} translate
        """
        # export block
        self.write(BLOCK)
        # setup user constants
        self.LEFT, self.RIGHT  = -w/2.0/_units, +w/2.0/_units 
        self.TOP,  self.BOTTOM = +h/2.0/_units, -h/2.0/_units 
        # done        
        return

    # add a new page to the document (origin not yet implemented)
    def newpage(self, Origin = "tl"):
        # increment page number
        n = self.n + 1
        # get document size
        w, h = self.size
        # define newpage block
        BLOCK = f"""
        showpage

        %%Page: {n} {n}

        % --- SET ORIGIN AT PAGE CENTER ---
        {w/2:.0f} {h/2:.0f} translate
        """        
        # export text
        self.write(BLOCK)
        # update page counter
        self.n = n
        # done
        return        

    # write block to buffer
    def write(self, Block):
        for l in Block[len(EOL):].split(EOL):
            self.text += l.lstrip()+EOL
        return

    # adjust parameters, flush buffer, and close file
    def __del__(self):
        if self.fh:
            # show last page
            self.write(f"""
                showpage""")
            # update page number in header
            self.text = self.text.replace(
                f"%%Pages: 001",
                f"%%Pages: {self.n:03d}")
            # write buffer to file
            self.fh.write(self.text)
            # close file
            self.fh.close()
            # clear fh handle
            self.fh = None
        # done
        return

    def close(self):
        return self.__del__()

    ### CROSSHAIR ###

    # use the crosshair for scale calibration
    def displayCrosshair(self, size = 50.0):
        # setup
        l, r = -size/2.0, +size/2.0
        b, t = -size/2.0, +size/2.0
        # define  block
        BLOCK = f'''
        % --- CROSSHAIR ---
        {scl(l, t, r, t, r, b)}
        {scl(l, b)}
        moveto 3 {{lineto}} repeat closepath stroke
        gsave 0.3 setlinewidth [1 3 12 3] 0 setdash
        {scl(l, 0.0)}
        {scl(r, 0.0)}
        moveto lineto stroke
        {scl(0.0, b)}
        {scl(0.0, t)}
        moveto lineto stroke
        grestore
        '''
        # export text
        self.write(BLOCK)
        # done
        return

    ### STYLES ###

    def thickness(self, Value):
        self.write(f"""
            % --- SET THICKNESS ---
            {scl(Value)} setlinewidth
            """)
        return

    # A value of '0.0' is white.
    # A value of '1.0' is black.
    def graycolor(self, Value):
        self.write(f"""
            % --- SET GRAYSCALE ---
            {1.0-Value:.2f} dup dup setrgbcolor
            """)
        return

    def rgbcolor(self, r, g, b):
        self.write(f"""
            % --- SET COLOR ---
            {r:.2f} {g:.2f} {b:.2f} setrgbcolor
            """)
        return

    ### SINGLE THROUGH LINE ###

    def hline(self, Position = 0.0, lm = 0, rm = 0):
        # l, r margins are null by default
        # get geometry
        w, h = self.size
        # convert position to string
        p = scl(Position)
        # define  block
        BLOCK = f'''
        % --- SINGLE HORIZONTAL LINE ---
        {+w/2.0-rm*_units} {p} {-w/2.0+lm*_units} {p}
        moveto lineto stroke
        '''
        # export text
        self.write(BLOCK)
        # done
        return

    def vline(self, Position = 0.0, tm = 0, bm = 0):
        # t, b margins are null by default
        # get geometry
        w, h = self.size
        # convert position to string
        p = scl(Position)
        # define  block
        BLOCK = f'''
        % --- SINGLE VERTICAL LINE ---
        {p} {+h/2.0-tm*_units} {p} {-h/2.0+bm*_units}
        moveto lineto stroke
        '''
        # export text
        self.write(BLOCK)
        # done
        return

    ### MULTIPLE THROUGH LINES ###

    def hlines(self, *Positions, lm = 0, rm = 0):
        # get geometry
        w, h = self.size
        # convert position to string
        l = fix(-w/2.0+lm*_units)
        r = fix(+w/2.0-rm*_units)
        # define  block
        BLOCK = f'''
        % --- MULTIPLE HORIZONTAL LINES ---
        {scl(*Positions)} {len(Positions)}
        {{{r} exch dup {l} exch moveto lineto stroke}} repeat
        '''
        # export text
        self.write(BLOCK)
        # done
        return

    def vlines(self, *Positions, tm = 0, bm = 0):
        # get geometry
        w, h = self.size
        # convert position to string
        t = fix(+h/2.0-tm*_units)
        b = fix(-h/2.0+bm*_units)
        # define  block
        BLOCK = f'''
        % --- MULTIPLE VERTICAL LINES ---
        {scl(*Positions)} {len(Positions)}
        {{dup {b} exch {t} moveto lineto stroke}} repeat
        '''
        # export text
        self.write(BLOCK)
        # done
        return

    ### MULTIPLE EQUIDISTANT THROUGH LINES ###

    def hgrid(self, Start, Stop, nLines, lm = 0, rm = 0):
        # get geometry
        w, h = self.size                # width, height
        l = -w/2.0 + lm*_units          # left
        r = +w/2.0 - rm*_units          # right
        s, e = Start, Stop              # start, stop
        i = (Stop-Start)/(nLines-1)     # interval
        # define  block
        BLOCK = f'''
        % --- MULTIPLE EQUIDISTANT HORIZONTAL LINES ---
        {scl(s-i)}
        {nLines} {{
        {scl(i)} add  dup
        {fix(r)} exch dup {fix(l)} exch
        moveto lineto
        stroke}} repeat
        pop
        '''
        # export text
        self.write(BLOCK)
        # done
        return        

    def vgrid(self, Start, Stop, nLines, tm = 0, bm = 0):
        # get geometry
        w, h = self.size                # width, height
        t, b = +h/2.0-tm, -h/2.0+bm     # top, bottom
        s, e = Start, Stop              # start, stop
        i = (Stop-Start)/(nLines-1)     # interval
        # define  block
        BLOCK = f'''
        % --- MULTIPLE EQUIDISTANT VERTICAL LINES ---
        {scl(s-i)}
        {nLines} {{
        {scl(i)} add  dup
        dup  {fix(b)} exch {fix(t)}
        moveto lineto
        stroke}} repeat
        pop
        '''
        # export text
        self.write(BLOCK)
        # done
        return        

    ### SIMPLE GEOMETRICAL OBJECTS ###

    def circle(self, x, y, r):
        # define  block
        BLOCK = f'''
        % --- SINGLE CIRCLE ---
        {scl(x, y, r)} 0 360 arc stroke
        '''
        # export text
        self.write(BLOCK)
        # done
        return        

    def line(self, x1, y1, x2, y2):
        # define  block
        BLOCK = f'''
        % --- SINGLE LINE ---
        {scl(x1, y1, x2, y2)} moveto lineto stroke
        '''
        # export text
        self.write(BLOCK)
        # done
        return                

    def rectangle(self, x1, y1, x2, y2):
        # define  block
        BLOCK = f'''
        % --- SINGLE RECTANGLE ---
        {scl(x1, y1)} moveto
        {scl(x2, y1)} lineto
        {scl(x2, y2)} lineto
        {scl(x1, y2)} lineto
        {scl(x1, y1)} lineto
        stroke
        '''
        # export text
        self.write(BLOCK)
        # done
        return                

    def box(self, x1, y1, x2, y2):
        # define  block
        BLOCK = f'''
        % --- SINGLE BOX ---
        {scl(x1, y1)} moveto
        {scl(x2, y1)} lineto
        {scl(x2, y2)} lineto
        {scl(x1, y2)} lineto
        {scl(x1, y1)} lineto
        fill
        '''
        # export text
        self.write(BLOCK)
        # done
        return                

    def pagelink(self, l, r, t, b, page, showborder = False):
        # get geometry
        w, h = self.size
        # border style if debug
        border = f"/Border [0 0 1]" if showborder else f"% no border"
        # define  block
        BLOCK = f'''
        % --- PAGE LINK ---
        mark
        /Rect [{scl(l, b)} {scl(r, t)}]
        {border}
        /Page {page}
        /View [/XYZ 0 {h} null]
        /Subtype /Link /ANN pdfmark
        '''
        # export text
        self.write(BLOCK)
        # done
        return                

    def text(self, l, b, txt):
        # define  block
        BLOCK = f'''
        % --- TEXT ---
        {scl(l, b)} moveto
        ({txt}) show
        stroke % quick fix...
        '''
        # export text
        self.write(BLOCK)
        # done
        return                

    def vtext(self, l, b, txt):
        # define  block
        BLOCK = f'''
        % --- TEXT ---
        gsave
        {scl(l, b)} moveto
        90 rotate
        ({txt}) show
        % stroke % quick fix...
        grestore
        '''
        # export text
        self.write(BLOCK)
        # done
        return                

if __name__ == "__main__":

    p = psDoc()
