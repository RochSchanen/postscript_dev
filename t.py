
    BLOCK += f'{width:.1f} setlinewidth\n'

    BLOCK += f'{dash} 0 setdash\n'

    BLOCK = f'''
    /arrow {{
    +000.000 +000.000 moveto
    {f(0,h)} 2 div rmoveto
    {f(-w)} 2 div {f(-h)} rlineto
    {f(w,0)} rlineto
    closepath fill
    }} def
    '''

    BLOCK = f'''
    0.85 0.95 1.0 setrgbcolor
    -292 +416 +292 +416 +292 -416 -292 -416
    moveto 3 {{lineto}} repeat closepath fill
    0.6 0.7 0.9 setrgbcolor
    '''

    BLOCK = f'''%!PS-Adobe-3.0 EPSF-3.0
    %%BoundingBox: 0 0 {_W} {_H}
    %%Creator: 
    %%Title:
    %%CreationDate:
    
    % new command
    /arrowto {{
    2 copy rlineto currentpoint stroke gsave
    translate atan -1 mul rotate arrow grestore
    }} def
    % set defaults font
    /Times-Roman 10 selectfont
    % set origin
    {_W/2:.0f} {_H/2:.0f} translate
    '''

    BLOCK = f'''
    % Axis
    gsave 0.3 setlinewidth [1 3 12 3] 0 setdash
    newpath
    {f(-_W/2-15, 0)} moveto
    +{_W/2-15:.0f} 0 lineto
    0 -{_H/2-15:.0f} moveto
    0 +{_H/2-15:.0f} lineto
    stroke
    grestore
    '''
    BLOCK = f'''
    % Circles: {name}
    newpath
    [] 0 setdash
    /circle {{ {r:.2f} 0 360 arc stroke }} def
    {DATA}
    {N} {{circle}} repeat
    '''

    BLOCK =f'''
    % Vectors
    newpath
    [] 0 setdash
    {DATA}
    {len(X)} {{moveto arrowto}} repeat
    '''

# Size     72 PPI       96 PPI      150 PPI        300 PPI
# 4A0   4768 x 6741  6357 x 8988  9933 x 14043  19866 x 28087
# 2A0   3370 x 4768  4494 x 6357  7022 x 9933   14043 x 19866
# A0    2384 x 3370  3179 x 4494  4967 x 7022    9933 x 14043
# A1    1684 x 2384  2245 x 3179  3508 x 4967    7016 x 9933
# A2    1191 x 1684  1587 x 2245  2480 x 3508    4960 x 7016
# A3     842 x 1191  1123 x 1587  1754 x 2480    3508 x 4960
# A4     595 x 842    794 x 1123  1240 x 1754    2480 x 3508
# A5     420 x 595    559 x 794    874 x 1240    1748 x 2480
# A6     298 x 420    397 x 559    620 x 874     1240 x 1748
# A7     210 x 298    280 x 397    437 x 620      874 x 1240
# A8     147 x 210    197 x 280    307 x 437      614 x 874
# A9     105 x 147    140 x 197    219 x 307      437 x 614
# A10     74 x 105     98 x 140    154 x 219      307 x 437
