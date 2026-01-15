[![CI](https://github.com/b-shields/chemscii/actions/workflows/ci.yml/badge.svg)](https://github.com/b-shields/chemscii/actions/workflows/ci.yml)

# chemscii

A Python package for rendering chemical structures as ASCII/Unicode art, optimized for display in LLM terminal interfaces and text-based environments.

Core Objectives:
- Parse common chemical structure formats (SMILES, SDF)
- Render 2D chemical structures as text-based visualizations
- Provide clean, readable output suitable for terminal display

## Installation

Install via pip.
```bash
pip install chemscii
```

Development installation.
```bash
conda env create -f environment.yml
conda activate chemscii
poetry install
pre-commit install
```

## Examples

### Pyridine (SMILES: c1ncccc1)
```
$ chemscii c1ncccc1 --columns 100
```
```
                                              "!3gVjJgVTr;
                                          ^rTqqJ*+.  -\13gFoi'
                                      ;cLmgf?|.          _)eFg5t>-
                                  '%zph3[\`        ,I)`      :%j6gy])`
                              _)eFh5a>_            +uqgwI/.      ;lnqgwI/
                          `\13gp7v'                   ={JSS#{=       +{JSq#{=
                      .|!fgmLc,                          ./Iwgmul;      ."?wgmul;
                   +}CSqTs^                                  `)[3g6z%:      `)[3gpz%'
               ^sTqSC}+                                          _>a5gFe)_      _>a5hFe)_
           ,cLmgf!|.                                                 'v7pg31\`      'vzpg3[\`
       `ijmg31\`                                                         ,cLmgf!".      ,cumg3?+
       rN3i_                                                                 ^sTqSJ*+       +}OY'
       {Rr                                                                       /}CgqT%      S&'
       {R{    .32.                                                                  .|[r      qO_
       {R{    .PP.                                                                            SO_
       {R{    .gg.                                                                            SO_
       {R{    .gg.                                                                            Sk_
       {R{    .gg.                                                                            Sk_
       {R{    .gg.                                                                            Sk_
       *R{    .Xg.                                                                            Sk_
       sDr    .Xg.                                                                            gk_
       )T|    .4V.                                                                            gk_
       |j"     t1                                                                             gY_
       |L"     !!                                                                             gY_
       |L"     ]!                                                                             gY_
       |L"     ]!                                                                             gY_
       |L"    .]!                                                                             gY-
       |L"    .]!                                                                             gY-
       |L"    .]!                                                                             gY-
       )u"    .[!                                                                             hY-
       /1=     *s                                                                             hY-
    `\/   _).                                                                       .|]x      hb-
    ,o?c` =o_                                                                    +*CSq#%      VO_
    ,t,)?;;e_                                                                ^rTqSC}+       =*&b_
    ,e, +Ile_`;.                                                         ,xLmgf!|.      ,xLmh2!/
    'I'  _s!-^*Ir\,                                                  'v7pg31\`      'v7pg21\`
               _/%}}c)'                                          _>a5gFe)_      _>a5gFe)_
                   '|c}}x"_                                  `\[3gpz%'      `)[3gpz%:
                       ,\lI*%/-                          ."?fgmLc,      ."?wgmul;
                          .;<rI{x)'                   +*JSqTs^       +*JSq#{=
                              `^{5h5a>_            |TqSC}/       ^rnqgC}/
                                  :%z6g3[)`        ^I|.      ,xjmgy!|.
                                      ;lumgwI/.          'voph21<-
                                          ={TqqT{=   _<t2g5e)_
                                             .|]5EqzwXhnc,
```

### Colchicine (by name)
```
$ chemscii colchicine --columns 100
```
```
                                                                           .__
                                                                          ;>;;i'
                                                                       `/=/)`-x;
                                                        15j}<,      .|v!oex;;;'
                                                        ,>IL2mpwel)eV&4j{\'
                                                             `=%[#hWUho+
                                                                  :&4.
                                                                   zp'
                                                                   +z<
                                                                   =*/'_,  '-
                                                                   xi+>"r+;c/
                                              ,vezl=.           ./ic_={+%:-)+
                                         -)}T6q3e1wmmw[>:    .)*?*\_  `..  ..
                                     _%o2qpn}|-    .+lz5SFLsthh!:
                                     F$ei,              _\?GHx
                                    >BL                    lW]
                                    68;                    .hk'
                                   iBz                      xWa
                                  .Sk'                       mA^`````````--
                       ^<>%{!aLJ2mgUX+                      '3H4gggXXXXXXd42+
                      }UmAK$$8AYGXf/wOL'                  .?ZS<}6FF55555pz/yOL'
v-                   vKC.r{%<|^:_.   )gZ!.               %4P*               >gZ!.          -"+/+
4X{                 |8m`               {EV%            |Fbe-                  {Pd%/)s]%l*?*%) .r,
`!f}^              ;ZE'                 )J$SwwwwwwwwwwF&p)                     -eUK@@$y[!}r/|+/".
  `v]=-_`       `'/VZ/                 [$E@1))))))))))aHd&i                     "Km!l>=`.
    `>/,"<)vxl}2FFp&dmhx              r@YHe           .E&Um                     2$^
     c;`^x+/=,','` ^CU$82|           i8YK#             {HZHv                   \DT
     `;;;.           <pU$Ou^        _dOU5.             `4&Ug.                  5U=
                       r488f^^/<vr?tj5&A,               sWP#:            ^%eFp[W3
                        `uHgF53wTja!{vrhgc              .*T5qyav;   _<?CVO@@A4fnhS['               -
                        ,EP/`          .}z*^                ^%e3q6T}7$K8PFoc=.  `xa!{)` .    .')tJpF
                       .[F/              `%{:::_                `|*nF#})_          `|x/)=/|"r*{{tl/_
                       ce;                 _%:'<|                                     >\ .l+;-
                    ,/+x|                  -%:'<|                                     `/++^
          _/)ic\\)%<r' :l                  '}i:_
          xFfJj%\|/,/"=|=                 -][_
                      .                  _md;
                                         jUv
                                         ,;
```

### CHEMBL1000 (by ChEMBL ID)
```
$ chemscii CHEMBL1000 --columns 100
```
```
           _:'
          /\_;v
          ^<;+>
           lt['
           u4g=          ;^^,                                                                    ^^;
         _xYDDL)`      `^x.`c;`      `)]36Lx_       ,s#mC*+                     -\156t\-       ')>`_
 ,^_/=++r}a?|vuqgwI/<]}}>"==")}I]\/}Cgqnl<1jI{)\.;v*?u?\}CSqnl,             ./Iygmj*VHDk5]);{1?I<\=^
^)<)/ ;c'.      +{Jg6j\`      -<LmgJ{+      .;v>|c\,.     .|!pU]           `m8gs^   .+}fZ&ZA3*,   ..
 ';-/=+'           .              .           ;+\i_          /kt           -ZBY-        `,3@:
                                               vJ^           ;t>           -PB&:          y$;
                                               eNc          'r"^|          :kB4`       ->rmH;
                                               >Fhpoi'   `^)%>=xlv/_   .|!ygqShC}/  |]FkD$Vn_
                                                 _)oFh2j36?)+_ '^\sy6oTSqTr^  =*JSqyUDGf*+.
                                                     :xax,         _lDh+         .|!!".
                                                                    ;$f
                                                                    ,$w
                                                                  .|aH4v:
                                                               =*Cgquz&B&Se)_
                                                             /VbF*+   ;cnEK&ZL
                                                             )DDy         =)OV
                                                             )KWm           kg
                                                             iDHw        `))AV
                                                             +mG6[\`  /}yZD&go
                                                               :xLmgCCKDY5!|`
                                                                   ^{nt\`
```
