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
$ chemscii c1ncccc1
```
```
                    _\{t1xc11r|-
                _|l!!l|_ .|''|l!?x+`
            -"l!]r)_     `%?]r|''|r]?%+`
        `/c!]s)'            `+x?!r|':)s]?%=.
    ./x!]{\'                    `/c!!l"':\{]Iv^
   +y*\_                            -"l!!c/_;)!w_
   )F  iv                               _|rl  .h,
   )5  oo                                     `q,
   )5  aa                                     `q,
   )5  ee                                     `q,
   /[  !!                                     -q,
   ^r  >>                                     -q,
   ^s  )>                                     -q,
   ^s  )>                                     -q:
   ;r  ><                                     -q:
  /)_+```                               _|rl  .h,
  %\)s:`                            -"l!!c/_;)!f_
  +`-<')\";`                    -/c!!l"':\{]Iv^
        .'/\\",`            `/x!!l|':)s]?%=.
            .:/\rr|_     -%?]r|'')r]?x+`
                _|l!!l"- .|''|l!?x+`
                    '\*t1%l11r"-
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
