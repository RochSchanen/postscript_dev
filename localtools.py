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
def _fix(*X):
    S = ""
    for x in X:
        s = f"{x:+08.3f}"
        S = f"{S} {s}" if S else s
    return S

# default units (pixels per mm)
_units = 72.0 / 25.4

# scaling and formating function
# an arbitrary list of arguments can be used
def _scl(*X):
    Y = []
    for x in X:
        Y.append(x*_units)
    return _fix(*Y)

### POSTSCRIPT DOCUMENT CLASS ###

class psDoc():

    # open file, write header, setup font, and fix the origin
    def __init__(self, Path = "./p.ps", Format = "A4"):
        # init page counter
        self.n = 1
        # setup document size:
        self.size = {
            "A4": (595, 842),   # A4 in pixels (72ppi)
            "A5": (420, 595),   # A5 in pixels (72ppi)
            # Remarkable 2 parameters are: 
            # size = 1404, 1872
            # units = 226.0 / 25.4
            # use A5 format instead and fit to height
            }[Format]
        # get file handle
        fh = open(Path, 'w')
        if fh is None:
            exitProcess(f"failed to open '{Path}'")
        # register file handle
        self.fh = fh
        # write file magic
        # fh.write(f"%!PS-Adobe-3.0 EPSF-3.0{EOL}") # --> .eps
        fh.write(f"%!PS-Adobe-3.0{EOL}") # --> .ps
        # create buffer
        self.text = ""
        # get geometry
        w, h = self.size
        # define header block
        BLOCK = f"""
        %%BoundingBox: 0 0 {w} {h}
        %%Creator:
        %%Title:
        %%CreationDate: {fulldatetime()}
        %%Pages: 001

        % set defaults font
        /Times-Roman 10 selectfont

        %%Page: 1 1

        % --- SET ORIGIN AT PAGE CENTER ---
        {w/2:.0f} {h/2:.0f} translate
        """
        # export block
        self.write(BLOCK)
        # setup user constants
        self.LEFT, self.RIGHT  = -w/2/_units, +w/2/_units 
        self.TOP,  self.BOTTOM = +h/2/_units, -h/2/_units 
        # done        
        return

    # add a new page to the document
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
        # done
        return

    ### CROSSHAIR ###

    # use the crosshair for scale calibration
    def displayCrosshair(self, size = 50.0):
        # setup
        l, r = -size/2.0, +size/2.0
        b, t = -size/2.0, +size/2.0
        # define  block
        BLOCK = f'''
        % --- CROSSHAIR ---
        {_scl(l, t, r, t, r, b)}
        {_scl(l, b)}
        moveto 3 {{lineto}} repeat closepath stroke
        gsave 0.3 setlinewidth [1 3 12 3] 0 setdash
        {_scl(l, 0.0)}
        {_scl(r, 0.0)}
        moveto lineto stroke
        {_scl(0.0, b)}
        {_scl(0.0, t)}
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
            {_scl(Value)} setlinewidth
            """)
        return

    # '0.0' is white up to '1.0' which is black
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

    def hline(self, Position = 0.0):
        # get geometry
        w, h = self.size
        # convert position to string
        p = _scl(Position)
        # define  block
        BLOCK = f'''
        % --- SINGLE HORIZONTAL LINE ---
        {+w/2.0} {p} {-w/2.0} {p}
        moveto lineto stroke
        '''
        # export text
        self.write(BLOCK)
        # done
        return

    def vline(self, Position = 0.0):
        # get geometry
        w, h = self.size
        # convert position to string
        p = _scl(Position)
        # define  block
        BLOCK = f'''
        % --- SINGLE VERTICAL LINE ---
        {p} {+h/2.0} {p} {-h/2.0}
        moveto lineto stroke
        '''
        # export text
        self.write(BLOCK)
        # done
        return

    ### MULTIPLE THROUGH LINES ###

    def hlines(self, *Positions):
        # get geometry
        w, h = self.size
        # convert position to string
        l, r = _fix(-w/2.0), _fix(+w/2.0)
        # define  block
        BLOCK = f'''
        % --- MULTIPLE HORIZONTAL LINES ---
        {_scl(*Positions)} {len(Positions)}
        {{{r} exch dup {l} exch moveto lineto stroke}} repeat
        '''
        # export text
        self.write(BLOCK)
        # done
        return

    def vlines(self, *Positions):
        # get geometry
        w, h = self.size
        # convert position to string
        t, b = _fix(+h/2.0), _fix(-h/2.0)
        # define  block
        BLOCK = f'''
        % --- MULTIPLE VERTICAL LINES ---
        {_scl(*Positions)} {len(Positions)}
        {{dup {b} exch {t} moveto lineto stroke}} repeat
        '''
        # export text
        self.write(BLOCK)
        # done
        return

    ### MULTIPLE EQUIDISTANT THROUGH LINES ###

    def hgrid(self, Start, Stop, nLines):
        # get geometry
        w, h = self.size                # width, height
        l, r = -w/2.0, +w/2.0           # left, right
        s, e = Start, Stop              # start, stop
        i = (Stop-Start)/(nLines-1)     # interval
        # define  block
        BLOCK = f'''
        % --- MULTIPLE EQUIDISTANT HORIZONTAL LINES ---
        {_scl(s-i)}
        {nLines} {{
        {_scl(i)} add  dup
        {_fix(r)} exch dup {_fix(l)} exch
        moveto lineto
        stroke}} repeat
        pop
        '''
        # export text
        self.write(BLOCK)
        # done
        return        

    def vgrid(self, Start, Stop, nLines):
        # get geometry
        w, h = self.size                # width, height
        t, b = +h/2.0, -h/2.0           # top, bottom
        s, e = Start, Stop              # start, stop
        i = (Stop-Start)/(nLines-1)     # interval
        # define  block
        BLOCK = f'''
        % --- MULTIPLE EQUIDISTANT VERTICAL LINES ---
        {_scl(s-i)}
        {nLines} {{
        {_scl(i)} add  dup
        dup  {_fix(b)} exch {_fix(t)}
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
        {_scl(x, y, r)} 0 360 arc stroke
        '''
        # export text
        self.write(BLOCK)
        # done
        return        

    def line(self, x1, y1, x2, y2):
        # define  block
        BLOCK = f'''
        % --- SINGLE LINE ---
        {_scl(x1, y1, x2, y2)} moveto lineto stroke
        '''
        # export text
        self.write(BLOCK)
        # done
        return                

    def rectangle(self, x1, y1, x2, y2):
        # define  block
        BLOCK = f'''
        % --- SINGLE RECTANGLE ---
        {_scl(x1, y1)} moveto
        {_scl(x2, y1)} lineto
        {_scl(x2, y2)} lineto
        {_scl(x1, y2)} lineto
        {_scl(x1, y1)} lineto
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
        {_scl(x1, y1)} moveto
        {_scl(x2, y1)} lineto
        {_scl(x2, y2)} lineto
        {_scl(x1, y2)} lineto
        {_scl(x1, y1)} lineto
        fill
        '''
        # export text
        self.write(BLOCK)
        # done
        return                

if __name__ == "__main__":

    p = psDoc()
