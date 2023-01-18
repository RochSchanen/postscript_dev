#!/usr/bin/python3
# content: local tools
# file: localtools.py
# date: 2023 01 17
# author: Roch Schanen
# repository: 
# package: only built-in library
# comment: (default output to './.output/p.ps')

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

class psDoc():

    def __init__(self, Path = "./.output/p.ps", Format = "A4"):
        # page number
        self.n = 1
        """the symbol @001 will be replaced by the page
        number value when closing the file """
        # default document size:
        self.size = {
            "A5": (420, 595),   # A5 in pixels (72ppi)
            "A4": (595, 842),   # A4 in pixels (72ppi)
            }[Format]
        # get file handle
        fh = open(Path, 'w')
        if fh is None:
            exitProcess(f"failed to open '{Path}'")
        # register file handle
        self.fh = fh
        # write file magic (EPSF-3.0 is encapsulated ps)
        # this is also used to test writing to the file
        # (early error generation)
        # fh.write(f"%!PS-Adobe-3.0 EPSF-3.0{EOL}")
        fh.write(f"%!PS-Adobe-3.0{EOL}")
        # create buffer
        self.text = ""
        # write header block:
        w, h = self.size
        # define default header block
        BLOCK = f"""
        %%BoundingBox: 0 0 {w} {h}
        %%Creator:
        %%Title:
        %%CreationDate: {fulldatetime()}
        %%Pages: 001

        %%Page: 1 1

        % --- SET ORIGIN AT PAGE CENTER ---
        {w/2:.0f} {h/2:.0f} translate
        """
        # export text
        self.write(BLOCK)
        # done        
        return

    def newpage(self):
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

    # write formatted text block to file/buffer
    def write(self, Block):
        for l in Block[len(EOL):].split(EOL):
            # self.fh.write(l.lstrip()+EOL)
            self.text += l.lstrip()+EOL
        return

    def __del__(self):
        # show last page
        self.write(f"{SPC}showpage")
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

    ### SINGLE THROUGH LINES ###

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
        % --- MULTIPLE HORIZONTAL LINES ---
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
        w, h = self.size
        # convert extrema
        l, r = _fix(-w/2.0), _fix(+w/2.0)
        # convert parameters
        s, e = _scl(Start), _scl(Stop)
        i = _scl((Stop-Start)/(nLines-1))
        # define  block
        BLOCK = f'''
        % --- MULTIPLE EQUIDISTANT HORIZONTAL LINES ---
        {s}
        {nLines} {{
        {i} add  dup
        {r} exch dup
        {l} exch
        moveto lineto
        stroke}} repeat
        pop
        '''
        # export text
        self.write(BLOCK)
        # done
        return        

    def thickness(self, Value):
        self.write(f"""
            % --- SET THICKNESS ---
            {Value:.3f} setlinewidth
            """)
        return

    def graycolor(self, Value):
        self.write(f"""
            % --- SET COLOR ---
            {Value:.2f} {Value:.2f} {Value:.2f} setrgbcolor
            """)
        return

    # the following is for scaling purposes
    def displayCrosshair(self, size = 100.0):
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

# # default document size (Remarkable 2) in pixels (226ppi):
# self.size = 1404, 1872
# _units = 226.0 / 25.4   # remarkable 2

# file: seyesRuledNoteBook.py

if __name__ == "__main__":

    # from localtools import exitProcess
    # from localtools import psDoc

    p = psDoc(Format = "A5")

    p.thickness(0.2)
    p.graycolor(0.6)

    p.hlines(2, 4, 6)
    p.vlines(2, 4, 6)

    p.thickness(0.5)
    p.graycolor(0.2)
    
    p.hlines(0, 8)
    p.vlines(0, 8)

    exitProcess("end-of-code.")

    p.newpage()
    p.displayCrosshair()
