
# -*- coding: utf-8 -*-

# List all Fonts.

from pycocoa import FontError, fontfamilies, fontsof

__version__ = '18.05.08'

if __name__ == '__main__':

    import sys

    i = 0
    for fam in fontfamilies():
        print(' --- Family %r' % (fam,))
        for f in fontsof(fam):
            i += 1
            print('%4d %r' % (i, f))
            try:
                f = f.resize(f.size * 2)
            except FontError:
                continue
            if f:
                i += 1
                print('%4d+%r' % (i, f))

    sys.exit(0 if i > 1000 else 1)

# sample output, using Font.traitsup
_ = '''
% python -m test.test_Fonts
 --- Family 'Academy Engraved LET'
   1 Font(name='AcademyEngravedLetPlain', family='Academy Engraved LET', size=12, weight=5) at 0x105367f90
   2+Font(name='AcademyEngravedLetPlain', family='Academy Engraved LET', size=24, weight=5) at 0x105385250
 --- Family 'Al Bayan'
   3 Font(name='AlBayan', family='Al Bayan', size=12, weight=5) at 0x105385190
   4+Font(name='AlBayan', family='Al Bayan', size=24, weight=5) at 0x105385250
   5 Font(name='AlBayan-Bold', family='Al Bayan', size=12, traits='Bold', weight=9) at 0x105385110
   6+Font(name='AlBayan-Bold', family='Al Bayan', size=24, traits='Bold', weight=9) at 0x105385610
 --- Family 'Al Nile'
   7 Font(name='AlNile', family='Al Nile', size=12, weight=5) at 0x1053858d0
   8+Font(name='AlNile', family='Al Nile', size=24, weight=5) at 0x105385610
   9 Font(name='AlNile-Bold', family='Al Nile', size=12, traits='Bold', weight=9) at 0x105385710
  10+Font(name='AlNile-Bold', family='Al Nile', size=24, traits='Bold', weight=9) at 0x105385950
 --- Family 'Al Tarikh'
  11 Font(name='AlTarikh', family='Al Tarikh', size=12, weight=5) at 0x105385d10
  12+Font(name='AlTarikh', family='Al Tarikh', size=24, weight=5) at 0x105385950
 --- Family 'American Typewriter'
  13 Font(name='AmericanTypewriter', family='American Typewriter', size=12, weight=5) at 0x1053b8050
  14+Font(name='AmericanTypewriter', family='American Typewriter', size=24, weight=5) at 0x1053b8090
  15 Font(name='AmericanTypewriter-Light', family='American Typewriter', size=12, weight=3) at 0x105385d50
  16+Font(name='AmericanTypewriter-Light', family='American Typewriter', size=24, weight=3) at 0x1053b8090
  17 Font(name='AmericanTypewriter-Bold', family='American Typewriter', size=12, traits='Bold', weight=9) at 0x1053b8590
  18+Font(name='AmericanTypewriter-Bold', family='American Typewriter', size=24, traits='Bold', weight=9) at 0x1053b84d0
  19 Font(name='AmericanTypewriter-Bold', family='American Typewriter', size=12, traits='Bold', weight=9) at 0x1053b8790
  20+Font(name='AmericanTypewriter-Bold', family='American Typewriter', size=24, traits='Bold', weight=9) at 0x1053b8350
  21 Font(name='AmericanTypewriter', family='American Typewriter', size=12, weight=5) at 0x1053b81d0
  22+Font(name='AmericanTypewriter', family='American Typewriter', size=24, weight=5) at 0x1053b83d0
  23 Font(name='AmericanTypewriter', family='American Typewriter', size=12, weight=5) at 0x1053b89d0
  24+Font(name='AmericanTypewriter', family='American Typewriter', size=24, weight=5) at 0x1053b8910
  25 Font(name='AmericanTypewriter-Bold', family='American Typewriter', size=12, traits='Bold', weight=9) at 0x1053b8b10
  26+Font(name='AmericanTypewriter-Bold', family='American Typewriter', size=24, traits='Bold', weight=9) at 0x1053b8a10
 --- Family 'Andale Mono'
  27 Font(name='AndaleMono', family='Andale Mono', size=12, traits='MonoSpace', weight=5) at 0x1053b8bd0
  28+Font(name='AndaleMono', family='Andale Mono', size=24, traits='MonoSpace', weight=5) at 0x1053b8690
 --- Family 'Arial'
  29 Font(name='ArialMT', family='Arial', size=12, weight=5) at 0x1053b8f10
  30+Font(name='ArialMT', family='Arial', size=24, weight=5) at 0x1053b8690
  31 Font(name='Arial-ItalicMT', family='Arial', size=12, traits='Italic', weight=5) at 0x1053b8cd0
  32+Font(name='Arial-ItalicMT', family='Arial', size=24, traits='Italic', weight=5) at 0x1053b3190
  33 Font(name='Arial-BoldMT', family='Arial', size=12, traits='Bold', weight=9) at 0x1053b8c90
  34+Font(name='Arial-BoldMT', family='Arial', size=24, traits='Bold', weight=9) at 0x1053b3290
  35 Font(name='Arial-BoldItalicMT', family='Arial', size=12, traits='Bold Italic', weight=9) at 0x1053b3110
  36+Font(name='Arial-BoldItalicMT', family='Arial', size=24, traits='Bold Italic', weight=9) at 0x1053b3510
 --- Family 'Arial Black'
  37 Font(name='Arial-Black', family='Arial Black', size=12, traits='Bold', weight=11) at 0x1053b3710
  38+Font(name='Arial-Black', family='Arial Black', size=24, traits='Bold', weight=11) at 0x1053b3650
 --- Family 'Arial Hebrew'
  39 Font(name='ArialHebrew', family='Arial Hebrew', size=12, weight=5) at 0x1053b3990
  40+Font(name='ArialHebrew', family='Arial Hebrew', size=24, weight=5) at 0x1053b3750
  41 Font(name='ArialHebrew-Light', family='Arial Hebrew', size=12, weight=3) at 0x1053b3610
  42+Font(name='ArialHebrew-Light', family='Arial Hebrew', size=24, weight=3) at 0x1053b3a50
  43 Font(name='ArialHebrew-Bold', family='Arial Hebrew', size=12, traits='Bold', weight=9) at 0x1053b3650
  44+Font(name='ArialHebrew-Bold', family='Arial Hebrew', size=24, traits='Bold', weight=9) at 0x1053b3c90
 --- Family 'Arial Hebrew Scholar'
  45 Font(name='ArialHebrewScholar', family='Arial Hebrew Scholar', size=12, weight=5) at 0x1053b3e50
  46+Font(name='ArialHebrewScholar', family='Arial Hebrew Scholar', size=24, weight=5) at 0x1053b3f90
  47 Font(name='ArialHebrewScholar-Light', family='Arial Hebrew Scholar', size=12, weight=3) at 0x1053b3d10
  48+Font(name='ArialHebrewScholar-Light', family='Arial Hebrew Scholar', size=24, weight=3) at 0x1053d0150
  49 Font(name='ArialHebrewScholar-Bold', family='Arial Hebrew Scholar', size=12, traits='Bold', weight=9) at 0x1053b3f50
  50+Font(name='ArialHebrewScholar-Bold', family='Arial Hebrew Scholar', size=24, traits='Bold', weight=9) at 0x1053d0350
 --- Family 'Arial Narrow'
  51 Font(name='ArialNarrow', family='Arial Narrow', size=12, traits='Narrow', weight=5) at 0x1053d05d0
  52+Font(name='ArialNarrow', family='Arial Narrow', size=24, traits='Narrow', weight=5) at 0x1053d03d0
  53 Font(name='ArialNarrow-Italic', family='Arial Narrow', size=12, traits='Italic Narrow', weight=5) at 0x1053d0090
  54+Font(name='ArialNarrow-Italic', family='Arial Narrow', size=24, traits='Italic Narrow', weight=5) at 0x1053d0750
  55 Font(name='ArialNarrow-Bold', family='Arial Narrow', size=12, traits='Bold Narrow', weight=9) at 0x1053d0250
  56+Font(name='ArialNarrow-Bold', family='Arial Narrow', size=24, traits='Bold Narrow', weight=9) at 0x1053d0890
  57 Font(name='ArialNarrow-BoldItalic', family='Arial Narrow', size=12, traits='Bold Italic Narrow', weight=9) at 0x1053d09d0
  58+Font(name='ArialNarrow-BoldItalic', family='Arial Narrow', size=24, traits='Bold Italic Narrow', weight=9) at 0x1053d0750
 --- Family 'Arial Rounded MT Bold'
  59 Font(name='ArialRoundedMTBold', family='Arial Rounded MT Bold', size=12, traits='Bold', weight=5) at 0x1053d0b90
  60+Font(name='ArialRoundedMTBold', family='Arial Rounded MT Bold', size=24, traits='Bold', weight=5) at 0x1053d0b50
 --- Family 'Arial Unicode MS'
  61 Font(name='ArialUnicodeMS', family='Arial Unicode MS', size=12, weight=5) at 0x1053d0e90
  62+Font(name='ArialUnicodeMS', family='Arial Unicode MS', size=24, weight=5) at 0x1053d0c10
 --- Family 'Athelas'
  63 Font(name='Athelas-Regular', family='Athelas', size=12, weight=5) at 0x1053db050
  64+Font(name='Athelas-Regular', family='Athelas', size=24, weight=5) at 0x1053db1d0
  65 Font(name='Athelas-Italic', family='Athelas', size=12, traits='Italic', weight=5) at 0x1053d0ed0
  66+Font(name='Athelas-Italic', family='Athelas', size=24, traits='Italic', weight=5) at 0x1053db350
  67 Font(name='Athelas-Bold', family='Athelas', size=12, traits='Bold', weight=9) at 0x1053db150
  68+Font(name='Athelas-Bold', family='Athelas', size=24, traits='Bold', weight=9) at 0x1053db410
  69 Font(name='Athelas-BoldItalic', family='Athelas', size=12, traits='Bold Italic', weight=9) at 0x1053db110
  70+Font(name='Athelas-BoldItalic', family='Athelas', size=24, traits='Bold Italic', weight=9) at 0x1053db610
 --- Family 'Avenir'
  71 Font(name='Avenir-Book', family='Avenir', size=12, weight=5) at 0x1053db910
  72+Font(name='Avenir-Book', family='Avenir', size=24, weight=5) at 0x1053db610
  73 Font(name='Avenir-Book', family='Avenir', size=12, weight=5) at 0x1053db710
  74+Font(name='Avenir-Book', family='Avenir', size=24, weight=5) at 0x1053dbc50
  75 Font(name='Avenir-BookOblique', family='Avenir', size=12, traits='Italic', weight=5) at 0x1053dba50
  76+Font(name='Avenir-BookOblique', family='Avenir', size=24, traits='Italic', weight=5) at 0x1053dbd50
  77 Font(name='Avenir-BookOblique', family='Avenir', size=12, traits='Italic', weight=5) at 0x1053dbb50
  78+Font(name='Avenir-BookOblique', family='Avenir', size=24, traits='Italic', weight=5) at 0x1053dbfd0
  79 Font(name='Avenir-Light', family='Avenir', size=12, weight=3) at 0x1053dbc90
  80+Font(name='Avenir-Light', family='Avenir', size=24, weight=3) at 0x1053c80d0
  81 Font(name='Avenir-LightOblique', family='Avenir', size=12, traits='Italic', weight=3) at 0x1053dbf90
  82+Font(name='Avenir-LightOblique', family='Avenir', size=24, traits='Italic', weight=3) at 0x1053c8310
  83 Font(name='Avenir-Medium', family='Avenir', size=12, weight=6) at 0x1053c8090
  84+Font(name='Avenir-Medium', family='Avenir', size=24, weight=6) at 0x1053c84d0
  85 Font(name='Avenir-MediumOblique', family='Avenir', size=12, traits='Italic', weight=7) at 0x1053c86d0
  86+Font(name='Avenir-MediumOblique', family='Avenir', size=24, traits='Italic', weight=7) at 0x1053c8610
  87 Font(name='Avenir-Heavy', family='Avenir', size=12, traits='Bold', weight=10) at 0x1053c8310
  88+Font(name='Avenir-Heavy', family='Avenir', size=24, traits='Bold', weight=10) at 0x1053c8710
  89 Font(name='Avenir-HeavyOblique', family='Avenir', size=12, traits='Bold Italic', weight=10) at 0x1053c8790
  90+Font(name='Avenir-HeavyOblique', family='Avenir', size=24, traits='Bold Italic', weight=10) at 0x1053c8b90
  91 Font(name='Avenir-Black', family='Avenir', size=12, traits='Bold', weight=11) at 0x1053c8250
  92+Font(name='Avenir-Black', family='Avenir', size=24, traits='Bold', weight=11) at 0x1053c8d50
  93 Font(name='Avenir-BlackOblique', family='Avenir', size=12, traits='Bold Italic', weight=11) at 0x1053c8790
  94+Font(name='Avenir-BlackOblique', family='Avenir', size=24, traits='Bold Italic', weight=11) at 0x1053c8fd0
 --- Family 'Avenir Next'
  95 Font(name='AvenirNext-Regular', family='Avenir Next', size=12, weight=5) at 0x105b99190
  96+Font(name='AvenirNext-Regular', family='Avenir Next', size=24, weight=5) at 0x105b99350
  97 Font(name='AvenirNext-Italic', family='Avenir Next', size=12, traits='Italic', weight=5) at 0x105b99090
  98+Font(name='AvenirNext-Italic', family='Avenir Next', size=24, traits='Italic', weight=5) at 0x105b994d0
  99 Font(name='AvenirNext-UltraLight', family='Avenir Next', size=12, weight=2) at 0x105b99650
 100+Font(name='AvenirNext-UltraLight', family='Avenir Next', size=24, weight=2) at 0x105b99190
 101 Font(name='AvenirNext-UltraLightItalic', family='Avenir Next', size=12, traits='Italic', weight=2) at 0x105b99890
 102+Font(name='AvenirNext-UltraLightItalic', family='Avenir Next', size=24, traits='Italic', weight=2) at 0x105b99710
 103 Font(name='AvenirNext-Medium', family='Avenir Next', size=12, weight=6) at 0x105b99750
 104+Font(name='AvenirNext-Medium', family='Avenir Next', size=24, weight=6) at 0x105b99b50
 105 Font(name='AvenirNext-MediumItalic', family='Avenir Next', size=12, traits='Italic', weight=7) at 0x105b99a10
 106+Font(name='AvenirNext-MediumItalic', family='Avenir Next', size=24, traits='Italic', weight=7) at 0x105b99c50
 107 Font(name='AvenirNext-Bold', family='Avenir Next', size=12, traits='Bold', weight=9) at 0x105b99750
 108+Font(name='AvenirNext-Bold', family='Avenir Next', size=24, traits='Bold', weight=9) at 0x105b99490
 109 Font(name='AvenirNext-BoldItalic', family='Avenir Next', size=12, traits='Bold Italic', weight=9) at 0x105b99c90
 110+Font(name='AvenirNext-BoldItalic', family='Avenir Next', size=24, traits='Bold Italic', weight=9) at 0x105ba5110
 111 Font(name='AvenirNext-Bold', family='Avenir Next', size=12, traits='Bold', weight=9) at 0x105b99f10
 112+Font(name='AvenirNext-Bold', family='Avenir Next', size=24, traits='Bold', weight=9) at 0x105ba51d0
 113 Font(name='AvenirNext-BoldItalic', family='Avenir Next', size=12, traits='Bold Italic', weight=9) at 0x105ba54d0
 114+Font(name='AvenirNext-BoldItalic', family='Avenir Next', size=24, traits='Bold Italic', weight=9) at 0x105ba51d0
 115 Font(name='AvenirNext-Heavy', family='Avenir Next', size=12, traits='Bold', weight=10) at 0x105ba53d0
 116+Font(name='AvenirNext-Heavy', family='Avenir Next', size=24, traits='Bold', weight=10) at 0x105ba5390
 117 Font(name='AvenirNext-HeavyItalic', family='Avenir Next', size=12, traits='Bold Italic', weight=10) at 0x105ba56d0
 118+Font(name='AvenirNext-HeavyItalic', family='Avenir Next', size=24, traits='Bold Italic', weight=10) at 0x105ba54d0
 --- Family 'Avenir Next Condensed'
 119 Font(name='AvenirNextCondensed-Regular', family='Avenir Next Condensed', size=12, traits='Condensed', weight=5) at 0x105ba5b50
 120+Font(name='AvenirNextCondensed-Regular', family='Avenir Next Condensed', size=24, traits='Condensed', weight=5) at 0x105ba5a90
 121 Font(name='AvenirNextCondensed-Italic', family='Avenir Next Condensed', size=12, traits='Condensed Italic', weight=5) at 0x105ba5e10
 122+Font(name='AvenirNextCondensed-Italic', family='Avenir Next Condensed', size=24, traits='Condensed Italic', weight=5) at 0x105ba5c90
 123 Font(name='AvenirNextCondensed-UltraLight', family='Avenir Next Condensed', size=12, traits='Condensed', weight=2) at 0x105ba5c10
 124+Font(name='AvenirNextCondensed-UltraLight', family='Avenir Next Condensed', size=24, traits='Condensed', weight=2) at 0x105ba5dd0
 125 Font(name='AvenirNextCondensed-UltraLightItalic', family='Avenir Next Condensed', size=12, traits='Condensed Italic', weight=2) at 0x105ba5d90
 126+Font(name='AvenirNextCondensed-UltraLightItalic', family='Avenir Next Condensed', size=24, traits='Condensed Italic', weight=2) at 0x105ba5f90
 127 Font(name='AvenirNextCondensed-Medium', family='Avenir Next Condensed', size=12, traits='Condensed', weight=6) at 0x105ba5e50
 128+Font(name='AvenirNextCondensed-Medium', family='Avenir Next Condensed', size=24, traits='Condensed', weight=6) at 0x105bad1d0
 129 Font(name='AvenirNextCondensed-MediumItalic', family='Avenir Next Condensed', size=12, traits='Condensed Italic', weight=7) at 0x105ba5cd0
 130+Font(name='AvenirNextCondensed-MediumItalic', family='Avenir Next Condensed', size=24, traits='Condensed Italic', weight=7) at 0x105bad4d0
 131 Font(name='AvenirNextCondensed-Bold', family='Avenir Next Condensed', size=12, traits='Bold Condensed', weight=9) at 0x105bad190
 132+Font(name='AvenirNextCondensed-Bold', family='Avenir Next Condensed', size=24, traits='Bold Condensed', weight=9) at 0x105bad650
 133 Font(name='AvenirNextCondensed-BoldItalic', family='Avenir Next Condensed', size=12, traits='Bold Condensed Italic', weight=9) at 0x105bad590
 134+Font(name='AvenirNextCondensed-BoldItalic', family='Avenir Next Condensed', size=24, traits='Bold Condensed Italic', weight=9) at 0x105bad650
 135 Font(name='AvenirNextCondensed-Bold', family='Avenir Next Condensed', size=12, traits='Bold Condensed', weight=9) at 0x105badad0
 136+Font(name='AvenirNextCondensed-Bold', family='Avenir Next Condensed', size=24, traits='Bold Condensed', weight=9) at 0x105bada50
 137 Font(name='AvenirNextCondensed-BoldItalic', family='Avenir Next Condensed', size=12, traits='Bold Condensed Italic', weight=9) at 0x105bad6d0
 138+Font(name='AvenirNextCondensed-BoldItalic', family='Avenir Next Condensed', size=24, traits='Bold Condensed Italic', weight=9) at 0x105bad810
 139 Font(name='AvenirNextCondensed-Heavy', family='Avenir Next Condensed', size=12, traits='Bold Condensed', weight=10) at 0x105badd90
 140+Font(name='AvenirNextCondensed-Heavy', family='Avenir Next Condensed', size=24, traits='Bold Condensed', weight=10) at 0x105badc50
 141 Font(name='AvenirNextCondensed-HeavyItalic', family='Avenir Next Condensed', size=12, traits='Bold Condensed Italic', weight=10) at 0x105badcd0
 142+Font(name='AvenirNextCondensed-HeavyItalic', family='Avenir Next Condensed', size=24, traits='Bold Condensed Italic', weight=10) at 0x105badc50
 --- Family 'Ayuthaya'
 143 Font(name='Ayuthaya', family='Ayuthaya', size=12, weight=5) at 0x105bbb050
 144+Font(name='Ayuthaya', family='Ayuthaya', size=24, weight=5) at 0x105badc50
 --- Family 'Baghdad'
 145 Font(name='Baghdad', family='Baghdad', size=12, weight=5) at 0x105bbb050
 146+Font(name='Baghdad', family='Baghdad', size=24, weight=5) at 0x105bbb390
 --- Family 'Bangla MN'
 147 Font(name='BanglaMN', family='Bangla MN', size=12, weight=5) at 0x105bbb510
 148+Font(name='BanglaMN', family='Bangla MN', size=24, weight=5) at 0x105bbb390
 149 Font(name='BanglaMN-Bold', family='Bangla MN', size=12, traits='Bold', weight=9) at 0x105bbb050
 150+Font(name='BanglaMN-Bold', family='Bangla MN', size=24, traits='Bold', weight=9) at 0x105bbb850
 --- Family 'Bangla Sangam MN'
 151 Font(name='BanglaSangamMN', family='Bangla Sangam MN', size=12, weight=5) at 0x105bbb9d0
 152+Font(name='BanglaSangamMN', family='Bangla Sangam MN', size=24, weight=5) at 0x105bbbb90
 153 Font(name='BanglaSangamMN-Bold', family='Bangla Sangam MN', size=12, traits='Bold', weight=9) at 0x105bbb810
 154+Font(name='BanglaSangamMN-Bold', family='Bangla Sangam MN', size=24, traits='Bold', weight=9) at 0x105bbbd10
 --- Family 'Bank Gothic'
 155 Font(name='BankGothic-Light', family='Bank Gothic', size=12, weight=3) at 0x105bbbed0
 156+Font(name='BankGothic-Light', family='Bank Gothic', size=24, weight=3) at 0x105bbb9d0
 157 Font(name='BankGothic-Medium', family='Bank Gothic', size=12, weight=6) at 0x105bbbcd0
 158+Font(name='BankGothic-Medium', family='Bank Gothic', size=24, weight=6) at 0x105bc50d0
 --- Family 'Baskerville'
 159 Font(name='Baskerville', family='Baskerville', size=12, weight=5) at 0x105bc5110
 160+Font(name='Baskerville', family='Baskerville', size=24, weight=5) at 0x105bc5350
 161 Font(name='Baskerville-Italic', family='Baskerville', size=12, traits='Italic', weight=5) at 0x105bc51d0
 162+Font(name='Baskerville-Italic', family='Baskerville', size=24, traits='Italic', weight=5) at 0x105bc5510
 163 Font(name='Baskerville-Bold', family='Baskerville', size=12, traits='Bold', weight=9) at 0x105bc50d0
 164+Font(name='Baskerville-Bold', family='Baskerville', size=24, traits='Bold', weight=9) at 0x105bc56d0
 165 Font(name='Baskerville-BoldItalic', family='Baskerville', size=12, traits='Bold Italic', weight=9) at 0x105bc59d0
 166+Font(name='Baskerville-BoldItalic', family='Baskerville', size=24, traits='Bold Italic', weight=9) at 0x105bc5590
 167 Font(name='Baskerville-Bold', family='Baskerville', size=12, traits='Bold', weight=9) at 0x105bc5810
 168+Font(name='Baskerville-Bold', family='Baskerville', size=24, traits='Bold', weight=9) at 0x105bc5b10
 169 Font(name='Baskerville-BoldItalic', family='Baskerville', size=12, traits='Bold Italic', weight=9) at 0x105bc5c10
 170+Font(name='Baskerville-BoldItalic', family='Baskerville', size=24, traits='Bold Italic', weight=9) at 0x105bc5b10
 --- Family 'Beirut'
 171 Font(name='Beirut', family='Beirut', size=12, traits='Bold', weight=9) at 0x105bc5b50
 172+Font(name='Beirut', family='Beirut', size=24, traits='Bold', weight=9) at 0x105bc5c90
 --- Family 'Big Caslon'
 173 Font(name='BigCaslon-Medium', family='Big Caslon', size=12, weight=6) at 0x105bc5ad0
 174+Font(name='BigCaslon-Medium', family='Big Caslon', size=24, weight=6) at 0x105bc5ed0
 --- Family 'Blackmoor LET'
 175 Font(name='BlackmoorLetPlain', family='Blackmoor LET', size=12, traits='Bold', weight=11) at 0x108464150
 176+Font(name='BlackmoorLetPlain', family='Blackmoor LET', size=24, traits='Bold', weight=11) at 0x108464250
 --- Family 'BlairMdITC TT'
 177 Font(name='BlairMdITCTT-Medium', family='BlairMdITC TT', size=12, weight=6) at 0x108464490
 178+Font(name='BlairMdITCTT-Medium', family='BlairMdITC TT', size=24, weight=6) at 0x108464650
 --- Family 'Bodoni 72'
 179 Font(name='BodoniSvtyTwoITCTT-Book', family='Bodoni 72', size=12, weight=5) at 0x108464890
 180+Font(name='BodoniSvtyTwoITCTT-Book', family='Bodoni 72', size=24, weight=5) at 0x108464650
 181 Font(name='BodoniSvtyTwoITCTT-BookIta', family='Bodoni 72', size=12, traits='Italic', weight=5) at 0x108464a90
 182+Font(name='BodoniSvtyTwoITCTT-BookIta', family='Bodoni 72', size=24, traits='Italic', weight=5) at 0x108464ad0
 183 Font(name='BodoniSvtyTwoITCTT-Bold', family='Bodoni 72', size=12, traits='Bold', weight=9) at 0x108464c10
 184+Font(name='BodoniSvtyTwoITCTT-Bold', family='Bodoni 72', size=24, traits='Bold', weight=9) at 0x108464cd0
 --- Family 'Bodoni 72 Oldstyle'
 185 Font(name='BodoniSvtyTwoOSITCTT-Book', family='Bodoni 72 Oldstyle', size=12, weight=5) at 0x108464f50
 186+Font(name='BodoniSvtyTwoOSITCTT-Book', family='Bodoni 72 Oldstyle', size=24, weight=5) at 0x108464990
 187 Font(name='BodoniSvtyTwoOSITCTT-BookIt', family='Bodoni 72 Oldstyle', size=12, traits='Italic', weight=5) at 0x108464d90
 188+Font(name='BodoniSvtyTwoOSITCTT-BookIt', family='Bodoni 72 Oldstyle', size=24, traits='Italic', weight=5) at 0x10846c090
 189 Font(name='BodoniSvtyTwoOSITCTT-Bold', family='Bodoni 72 Oldstyle', size=12, traits='Bold', weight=9) at 0x108464fd0
 190+Font(name='BodoniSvtyTwoOSITCTT-Bold', family='Bodoni 72 Oldstyle', size=24, traits='Bold', weight=9) at 0x10846c290
 --- Family 'Bodoni 72 Smallcaps'
 191 Font(name='BodoniSvtyTwoSCITCTT-Book', family='Bodoni 72 Smallcaps', size=12, traits='SmallCaps', weight=5) at 0x10846c6d0
 192+Font(name='BodoniSvtyTwoSCITCTT-Book', family='Bodoni 72 Smallcaps', size=24, traits='SmallCaps', weight=5) at 0x10846c590
 --- Family 'Bodoni Ornaments'
 193 Font(name='BodoniOrnamentsITCTT', family='Bodoni Ornaments', size=12, weight=5) at 0x10846ca10
 194+Font(name='BodoniOrnamentsITCTT', family='Bodoni Ornaments', size=24, weight=5) at 0x10846cad0
 --- Family 'Bordeaux Roman Bold LET'
 195 Font(name='BordeauxRomanBoldLetPlain', family='Bordeaux Roman Bold LET', size=12, traits='Bold', weight=9) at 0x10846cdd0
 196+Font(name='BordeauxRomanBoldLetPlain', family='Bordeaux Roman Bold LET', size=24, traits='Bold', weight=9) at 0x10846cd10
 --- Family 'Bradley Hand'
 197 Font(name='BradleyHandITCTT-Bold', family='Bradley Hand', size=12, traits='Bold Expanded', weight=9) at 0x108484110
 198+Font(name='BradleyHandITCTT-Bold', family='Bradley Hand', size=24, traits='Bold Expanded', weight=9) at 0x10846cf10
 --- Family 'Brush Script MT'
 199 Font(name='BrushScriptMT', family='Brush Script MT', size=12, weight=5) at 0x1084842d0
 200+Font(name='BrushScriptMT', family='Brush Script MT', size=24, weight=5) at 0x10846ced0
 --- Family 'Capitals'
 201 Font(name='CapitalsRegular', family='Capitals', size=12, traits='Bold Condensed', weight=9) at 0x108484510
 202+Font(name='CapitalsRegular', family='Capitals', size=24, traits='Bold Condensed', weight=9) at 0x108484610
 --- Family 'Casual'
 203 Font(name='AppleCasual', family='Casual', size=12, weight=5) at 0x108484710
 204+Font(name='AppleCasual', family='Casual', size=24, weight=5) at 0x108484610
 --- Family 'Chalkboard'
 205 Font(name='Chalkboard', family='Chalkboard', size=12, weight=5) at 0x108484750
 206+Font(name='Chalkboard', family='Chalkboard', size=24, weight=5) at 0x108484610
 207 Font(name='Chalkboard-Bold', family='Chalkboard', size=12, traits='Bold', weight=9) at 0x1084848d0
 208+Font(name='Chalkboard-Bold', family='Chalkboard', size=24, traits='Bold', weight=9) at 0x108484bd0
 --- Family 'Chalkboard SE'
 209 Font(name='ChalkboardSE-Regular', family='Chalkboard SE', size=12, weight=5) at 0x108484e90
 210+Font(name='ChalkboardSE-Regular', family='Chalkboard SE', size=24, weight=5) at 0x108484d50
 211 Font(name='ChalkboardSE-Light', family='Chalkboard SE', size=12, weight=3) at 0x108484750
 212+Font(name='ChalkboardSE-Light', family='Chalkboard SE', size=24, weight=3) at 0x108484a10
 213 Font(name='ChalkboardSE-Bold', family='Chalkboard SE', size=12, traits='Bold', weight=9) at 0x108484e90
 214+Font(name='ChalkboardSE-Bold', family='Chalkboard SE', size=24, traits='Bold', weight=9) at 0x108490250
 --- Family 'Chalkduster'
 215 Font(name='Chalkduster', family='Chalkduster', size=12, weight=5) at 0x108490210
 216+Font(name='Chalkduster', family='Chalkduster', size=24, weight=5) at 0x1084904d0
 --- Family 'Charter'
 217 Font(name='Charter-Roman', family='Charter', size=12, weight=5) at 0x108490650
 218+Font(name='Charter-Roman', family='Charter', size=24, weight=5) at 0x108490810
 219 Font(name='Charter-Italic', family='Charter', size=12, traits='Italic', weight=5) at 0x108490590
 220+Font(name='Charter-Italic', family='Charter', size=24, traits='Italic', weight=5) at 0x108490990
 221 Font(name='Charter-Bold', family='Charter', size=12, traits='Bold', weight=9) at 0x1084904d0
 222+Font(name='Charter-Bold', family='Charter', size=24, traits='Bold', weight=9) at 0x108490a50
 223 Font(name='Charter-BoldItalic', family='Charter', size=12, traits='Bold Italic', weight=9) at 0x108490750
 224+Font(name='Charter-BoldItalic', family='Charter', size=24, traits='Bold Italic', weight=9) at 0x108490c50
 225 Font(name='Charter-Black', family='Charter', size=12, traits='Bold', weight=11) at 0x108490b90
 226+Font(name='Charter-Black', family='Charter', size=24, traits='Bold', weight=11) at 0x108490f10
 227 Font(name='Charter-BlackItalic', family='Charter', size=12, traits='Bold Italic', weight=11) at 0x108490750
 228+Font(name='Charter-BlackItalic', family='Charter', size=24, traits='Bold Italic', weight=11) at 0x10849c050
 --- Family 'Cochin'
 229 Font(name='Cochin', family='Cochin', size=12, weight=5) at 0x10849c190
 230+Font(name='Cochin', family='Cochin', size=24, weight=5) at 0x10849c050
 231 Font(name='Cochin-Italic', family='Cochin', size=12, traits='Italic', weight=5) at 0x10849c150
 232+Font(name='Cochin-Italic', family='Cochin', size=24, traits='Italic', weight=5) at 0x10849c590
 233 Font(name='Cochin-Bold', family='Cochin', size=12, traits='Bold', weight=9) at 0x10849c390
 234+Font(name='Cochin-Bold', family='Cochin', size=24, traits='Bold', weight=9) at 0x10849c650
 235 Font(name='Cochin-BoldItalic', family='Cochin', size=12, traits='Bold Italic', weight=9) at 0x10849c2d0
 236+Font(name='Cochin-BoldItalic', family='Cochin', size=24, traits='Bold Italic', weight=9) at 0x10849c850
 --- Family 'Comic Sans MS'
 237 Font(name='ComicSansMS', family='Comic Sans MS', size=12, traits='SansSerif', weight=5) at 0x10849cb10
 238+Font(name='ComicSansMS', family='Comic Sans MS', size=24, traits='SansSerif', weight=5) at 0x10849cbd0
 239 Font(name='ComicSansMS-Bold', family='Comic Sans MS', size=12, traits='Bold SansSerif', weight=9) at 0x10849c2d0
 240+Font(name='ComicSansMS-Bold', family='Comic Sans MS', size=24, traits='Bold SansSerif', weight=9) at 0x10849cd10
 --- Family 'Copperplate'
 241 Font(name='Copperplate', family='Copperplate', size=12, weight=5) at 0x10849cc90
 242+Font(name='Copperplate', family='Copperplate', size=24, weight=5) at 0x10849cf50
 243 Font(name='Copperplate-Light', family='Copperplate', size=12, weight=3) at 0x10849cbd0
 244+Font(name='Copperplate-Light', family='Copperplate', size=24, weight=3) at 0x1084a2050
 245 Font(name='Copperplate-Bold', family='Copperplate', size=12, traits='Bold', weight=9) at 0x10849ce90
 246+Font(name='Copperplate-Bold', family='Copperplate', size=24, traits='Bold', weight=9) at 0x1084a2310
 --- Family 'Corsiva Hebrew'
 247 Font(name='CorsivaHebrew', family='Corsiva Hebrew', size=12, weight=5) at 0x1084a2510
 248+Font(name='CorsivaHebrew', family='Corsiva Hebrew', size=24, weight=5) at 0x1084a2210
 249 Font(name='CorsivaHebrew-Bold', family='Corsiva Hebrew', size=12, traits='Bold', weight=9) at 0x1084a2390
 250+Font(name='CorsivaHebrew-Bold', family='Corsiva Hebrew', size=24, traits='Bold', weight=9) at 0x1084a26d0
 --- Family 'Courier'
 251 Font(name='Courier', family='Courier', size=12, traits='MonoSpace', weight=5) at 0x1084a2850
 252+Font(name='Courier', family='Courier', size=24, traits='MonoSpace', weight=5) at 0x1084a2810
 253 Font(name='Courier-Oblique', family='Courier', size=12, traits='Italic MonoSpace', weight=5) at 0x1084a2750
 254+Font(name='Courier-Oblique', family='Courier', size=24, traits='Italic MonoSpace', weight=5) at 0x1084a2ad0
 255 Font(name='Courier-Bold', family='Courier', size=12, traits='Bold MonoSpace', weight=9) at 0x1084a28d0
 256+Font(name='Courier-Bold', family='Courier', size=24, traits='Bold MonoSpace', weight=9) at 0x1084a2c50
 257 Font(name='Courier-BoldOblique', family='Courier', size=12, traits='Bold Italic MonoSpace', weight=9) at 0x1084a2750
 258+Font(name='Courier-BoldOblique', family='Courier', size=24, traits='Bold Italic MonoSpace', weight=9) at 0x1084a2c50
 --- Family 'Courier New'
 259 Font(name='CourierNewPSMT', family='Courier New', size=12, traits='MonoSpace', weight=5) at 0x1084a2f50
 260+Font(name='CourierNewPSMT', family='Courier New', size=24, traits='MonoSpace', weight=5) at 0x108db7090
 261 Font(name='CourierNewPS-ItalicMT', family='Courier New', size=12, traits='Italic MonoSpace', weight=5) at 0x1084a2e10
 262+Font(name='CourierNewPS-ItalicMT', family='Courier New', size=24, traits='Italic MonoSpace', weight=5) at 0x108db7310
 263 Font(name='CourierNewPS-BoldMT', family='Courier New', size=12, traits='Bold MonoSpace', weight=9) at 0x108db7190
 264+Font(name='CourierNewPS-BoldMT', family='Courier New', size=24, traits='Bold MonoSpace', weight=9) at 0x108db7150
 265 Font(name='CourierNewPS-BoldItalicMT', family='Courier New', size=12, traits='Bold Italic MonoSpace', weight=9) at 0x108db7610
 266+Font(name='CourierNewPS-BoldItalicMT', family='Courier New', size=24, traits='Bold Italic MonoSpace', weight=9) at 0x108db7150
 --- Family 'Cracked'
 267 Font(name='Cracked', family='Cracked', size=12, weight=5) at 0x108db75d0
 268+Font(name='Cracked', family='Cracked', size=24, weight=5) at 0x108db7150
 --- Family 'Damascus'
 269 Font(name='Damascus', family='Damascus', size=12, weight=5) at 0x108db7650
 270+Font(name='Damascus', family='Damascus', size=24, weight=5) at 0x108db7150
 271 Font(name='DamascusLight', family='Damascus', size=12, weight=3) at 0x108db75d0
 272+Font(name='DamascusLight', family='Damascus', size=24, weight=3) at 0x108db79d0
 273 Font(name='DamascusMedium', family='Damascus', size=12, weight=6) at 0x108db7a90
 274+Font(name='DamascusMedium', family='Damascus', size=24, weight=6) at 0x108db7c90
 275 Font(name='DamascusBold', family='Damascus', size=12, traits='Bold', weight=9) at 0x108db7150
 276+Font(name='DamascusBold', family='Damascus', size=24, traits='Bold', weight=9) at 0x108db7f10
 277 Font(name='DamascusBold', family='Damascus', size=12, traits='Bold', weight=9) at 0x108db79d0
 278+Font(name='DamascusBold', family='Damascus', size=24, traits='Bold', weight=9) at 0x108dc6250
 --- Family 'DecoType Naskh'
 279 Font(name='DecoTypeNaskh', family='DecoType Naskh', size=12, weight=5) at 0x108dc6390
 280+Font(name='DecoTypeNaskh', family='DecoType Naskh', size=24, weight=5) at 0x108dc6210
 --- Family 'Devanagari MT'
 281 Font(name='DevanagariMT', family='Devanagari MT', size=12, weight=5) at 0x108dc6590
 282+Font(name='DevanagariMT', family='Devanagari MT', size=24, weight=5) at 0x108dc63d0
 283 Font(name='DevanagariMT-Bold', family='Devanagari MT', size=12, traits='Bold', weight=9) at 0x108dc6390
 284+Font(name='DevanagariMT-Bold', family='Devanagari MT', size=24, traits='Bold', weight=9) at 0x108dc6750
 --- Family 'Devanagari Sangam MN'
 285 Font(name='DevanagariSangamMN', family='Devanagari Sangam MN', size=12, weight=5) at 0x108dc6a50
 286+Font(name='DevanagariSangamMN', family='Devanagari Sangam MN', size=24, weight=5) at 0x108dc6a10
 287 Font(name='DevanagariSangamMN-Bold', family='Devanagari Sangam MN', size=12, traits='Bold', weight=9) at 0x108dc6cd0
 288+Font(name='DevanagariSangamMN-Bold', family='Devanagari Sangam MN', size=24, traits='Bold', weight=9) at 0x108dc6950
 --- Family 'Didot'
 289 Font(name='Didot', family='Didot', size=12, weight=5) at 0x108dc6b10
 290+Font(name='Didot', family='Didot', size=24, weight=5) at 0x108dc6950
 291 Font(name='Didot-Italic', family='Didot', size=12, traits='Italic', weight=5) at 0x108dc6d10
 292+Font(name='Didot-Italic', family='Didot', size=24, traits='Italic', weight=5) at 0x108dcf090
 293 Font(name='Didot-Bold', family='Didot', size=12, traits='Bold', weight=9) at 0x108dc6e10
 294+Font(name='Didot-Bold', family='Didot', size=24, traits='Bold', weight=9) at 0x108dcf1d0
 --- Family 'DIN Alternate'
 295 Font(name='DINAlternate-Bold', family='DIN Alternate', size=12, traits='Bold', weight=9) at 0x108dcf490
 296+Font(name='DINAlternate-Bold', family='DIN Alternate', size=24, traits='Bold', weight=9) at 0x108dcf590
 --- Family 'DIN Condensed'
 297 Font(name='DINCondensed-Bold', family='DIN Condensed', size=12, traits='Bold Condensed', weight=9) at 0x108dcf8d0
 298+Font(name='DINCondensed-Bold', family='DIN Condensed', size=24, traits='Bold Condensed', weight=9) at 0x108dcf9d0
 --- Family 'Diwan Kufi'
 299 Font(name='DiwanKufi', family='Diwan Kufi', size=12, weight=5) at 0x108dcfad0
 300+Font(name='DiwanKufi', family='Diwan Kufi', size=24, weight=5) at 0x108dcf9d0
 --- Family 'Diwan Thuluth'
 301 Font(name='DiwanThuluth', family='Diwan Thuluth', size=12, weight=5) at 0x108dcfd90
 302+Font(name='DiwanThuluth', family='Diwan Thuluth', size=24, weight=5) at 0x108dcff50
 --- Family 'Euphemia UCAS'
 303 Font(name='EuphemiaUCAS', family='Euphemia UCAS', size=12, weight=5) at 0x108ddc090
 304+Font(name='EuphemiaUCAS', family='Euphemia UCAS', size=24, weight=5) at 0x108ddc050
 305 Font(name='EuphemiaUCAS-Italic', family='Euphemia UCAS', size=12, traits='Italic', weight=5) at 0x108dcff90
 306+Font(name='EuphemiaUCAS-Italic', family='Euphemia UCAS', size=24, traits='Italic', weight=5) at 0x108ddc2d0
 307 Font(name='EuphemiaUCAS-Bold', family='Euphemia UCAS', size=12, traits='Bold', weight=9) at 0x108ddc110
 308+Font(name='EuphemiaUCAS-Bold', family='Euphemia UCAS', size=24, traits='Bold', weight=9) at 0x108ddc490
 --- Family 'Farah'
 309 Font(name='Farah', family='Farah', size=12, weight=5) at 0x108ddc1d0
 310+Font(name='Farah', family='Farah', size=24, weight=5) at 0x108ddc490
 --- Family 'Farisi'
 311 Font(name='Farisi', family='Farisi', size=12, weight=5) at 0x108ddc1d0
 312+Font(name='Farisi', family='Farisi', size=24, weight=5) at 0x108ddc490
 --- Family 'Futura'
 313 Font(name='Futura-Medium', family='Futura', size=12, weight=6) at 0x108ddcb10
 314+Font(name='Futura-Medium', family='Futura', size=24, weight=6) at 0x108ddccd0
 315 Font(name='Futura-MediumItalic', family='Futura', size=12, traits='Italic', weight=7) at 0x108ddc1d0
 316+Font(name='Futura-MediumItalic', family='Futura', size=24, traits='Italic', weight=7) at 0x108ddce50
 317 Font(name='Futura-Bold', family='Futura', size=12, traits='Bold', weight=9) at 0x108ddc490
 318+Font(name='Futura-Bold', family='Futura', size=24, traits='Bold', weight=9) at 0x108ddce10
 319 Font(name='Futura-CondensedMedium', family='Futura', size=12, traits='Condensed', weight=7) at 0x108ddcc10
 320+Font(name='Futura-CondensedMedium', family='Futura', size=24, traits='Condensed', weight=7) at 0x108de6290
 321 Font(name='Futura-CondensedExtraBold', family='Futura', size=12, traits='Bold Condensed', weight=11) at 0x108de6590
 322+Font(name='Futura-CondensedExtraBold', family='Futura', size=24, traits='Bold Condensed', weight=11) at 0x108de65d0
 --- Family 'GB18030 Bitmap'
 323 Font(name='GB18030Bitmap', family='GB18030 Bitmap', size=12, traits='MonoSpace', weight=5) at 0x108de6610
 324+Font(name='GB18030Bitmap', family='GB18030 Bitmap', size=24, traits='MonoSpace', weight=5) at 0x108de6290
 --- Family 'Geeza Pro'
 325 Font(name='GeezaPro', family='Geeza Pro', size=12, weight=5) at 0x108de6950
 326+Font(name='GeezaPro', family='Geeza Pro', size=24, weight=5) at 0x108de6290
 327 Font(name='GeezaPro-Bold', family='Geeza Pro', size=12, traits='Bold', weight=9) at 0x108de67d0
 328+Font(name='GeezaPro-Bold', family='Geeza Pro', size=24, traits='Bold', weight=9) at 0x108de6c90
 --- Family 'Geneva'
 329 Font(name='Geneva', family='Geneva', size=12, weight=5) at 0x108de6c50
 330+Font(name='Geneva', family='Geneva', size=24, weight=5) at 0x108de6c90
 --- Family 'Georgia'
 331 Font(name='Georgia', family='Georgia', size=12, weight=5) at 0x10a180090
 332+Font(name='Georgia', family='Georgia', size=24, weight=5) at 0x10a1801d0
 333 Font(name='Georgia-Italic', family='Georgia', size=12, traits='Italic', weight=5) at 0x108de6c50
 334+Font(name='Georgia-Italic', family='Georgia', size=24, traits='Italic', weight=5) at 0x10a1803d0
 335 Font(name='Georgia-Bold', family='Georgia', size=12, traits='Bold', weight=9) at 0x10a1800d0
 336+Font(name='Georgia-Bold', family='Georgia', size=24, traits='Bold', weight=9) at 0x10a180490
 337 Font(name='Georgia-BoldItalic', family='Georgia', size=12, traits='Bold Italic', weight=9) at 0x10a180110
 338+Font(name='Georgia-BoldItalic', family='Georgia', size=24, traits='Bold Italic', weight=9) at 0x10a180690
 --- Family 'Gill Sans'
 339 Font(name='GillSans', family='Gill Sans', size=12, traits='SansSerif', weight=5) at 0x10a1808d0
 340+Font(name='GillSans', family='Gill Sans', size=24, traits='SansSerif', weight=5) at 0x10a180910
 341 Font(name='GillSans-Italic', family='Gill Sans', size=12, traits='Italic SansSerif', weight=5) at 0x10a180790
 342+Font(name='GillSans-Italic', family='Gill Sans', size=24, traits='Italic SansSerif', weight=5) at 0x10a180a90
 343 Font(name='GillSans', family='Gill Sans', size=12, traits='SansSerif', weight=5) at 0x10a180b90
 344+Font(name='GillSans', family='Gill Sans', size=24, traits='SansSerif', weight=5) at 0x10a180e90
 345 Font(name='GillSans-Italic', family='Gill Sans', size=12, traits='Italic SansSerif', weight=5) at 0x10a180f90
 346+Font(name='GillSans-Italic', family='Gill Sans', size=24, traits='Italic SansSerif', weight=5) at 0x10a180e90
 347 Font(name='GillSans-Bold', family='Gill Sans', size=12, traits='Bold SansSerif', weight=9) at 0x10a180ed0
 348+Font(name='GillSans-Bold', family='Gill Sans', size=24, traits='Bold SansSerif', weight=9) at 0x10a180e10
 349 Font(name='GillSans-BoldItalic', family='Gill Sans', size=12, traits='Bold Italic SansSerif', weight=9) at 0x10a180f90
 350+Font(name='GillSans-BoldItalic', family='Gill Sans', size=24, traits='Bold Italic SansSerif', weight=9) at 0x10a191410
 351 Font(name='GillSans-Bold', family='Gill Sans', size=12, traits='Bold SansSerif', weight=9) at 0x10a1911d0
 352+Font(name='GillSans-Bold', family='Gill Sans', size=24, traits='Bold SansSerif', weight=9) at 0x10a191410
 353 Font(name='GillSans-BoldItalic', family='Gill Sans', size=12, traits='Bold Italic SansSerif', weight=9) at 0x10a191450
 354+Font(name='GillSans-BoldItalic', family='Gill Sans', size=24, traits='Bold Italic SansSerif', weight=9) at 0x10a191590
 355 Font(name='GillSans-Bold', family='Gill Sans', size=12, traits='Bold SansSerif', weight=9) at 0x10a1911d0
 356+Font(name='GillSans-Bold', family='Gill Sans', size=24, traits='Bold SansSerif', weight=9) at 0x10a191590
 --- Family 'Gujarati MT'
 357 Font(name='GujaratiMT', family='Gujarati MT', size=12, weight=5) at 0x10a191810
 358+Font(name='GujaratiMT', family='Gujarati MT', size=24, weight=5) at 0x10a191610
 359 Font(name='GujaratiMT-Bold', family='Gujarati MT', size=12, traits='Bold', weight=9) at 0x10a1911d0
 360+Font(name='GujaratiMT-Bold', family='Gujarati MT', size=24, traits='Bold', weight=9) at 0x10a1919d0
 --- Family 'Gujarati Sangam MN'
 361 Font(name='GujaratiSangamMN', family='Gujarati Sangam MN', size=12, weight=5) at 0x10a191b50
 362+Font(name='GujaratiSangamMN', family='Gujarati Sangam MN', size=24, weight=5) at 0x10a191d10
 363 Font(name='GujaratiSangamMN-Bold', family='Gujarati Sangam MN', size=12, traits='Bold', weight=9) at 0x10a191c50
 364+Font(name='GujaratiSangamMN-Bold', family='Gujarati Sangam MN', size=24, traits='Bold', weight=9) at 0x10a191d90
 --- Family 'Gurmukhi MN'
 365 Font(name='GurmukhiMN', family='Gurmukhi MN', size=12, weight=5) at 0x10a18c050
 366+Font(name='GurmukhiMN', family='Gurmukhi MN', size=24, weight=5) at 0x10a1918d0
 367 Font(name='GurmukhiMN-Bold', family='Gurmukhi MN', size=12, traits='Bold', weight=9) at 0x10a191f50
 368+Font(name='GurmukhiMN-Bold', family='Gurmukhi MN', size=24, traits='Bold', weight=9) at 0x10a18c390
 --- Family 'Gurmukhi MT'
 369 Font(name='MonotypeGurmukhi', family='Gurmukhi MT', size=12, weight=5) at 0x10a18c590
 370+Font(name='MonotypeGurmukhi', family='Gurmukhi MT', size=24, weight=5) at 0x10a18c410
 --- Family 'Gurmukhi Sangam MN'
 371 Font(name='GurmukhiSangamMN', family='Gurmukhi Sangam MN', size=12, weight=5) at 0x10a18c710
 372+Font(name='GurmukhiSangamMN', family='Gurmukhi Sangam MN', size=24, weight=5) at 0x10a18c8d0
 373 Font(name='GurmukhiSangamMN-Bold', family='Gurmukhi Sangam MN', size=12, traits='Bold', weight=9) at 0x10a18c810
 374+Font(name='GurmukhiSangamMN-Bold', family='Gurmukhi Sangam MN', size=24, traits='Bold', weight=9) at 0x10a18c950
 --- Family 'Handwriting - Dakota'
 375 Font(name='Handwriting-Dakota', family='Handwriting - Dakota', size=12, weight=5) at 0x10a18ca50
 376+Font(name='Handwriting-Dakota', family='Handwriting - Dakota', size=24, weight=5) at 0x10a18ccd0
 --- Family 'Heiti SC'
 377 Font(name='STHeitiSC-Light', family='Heiti SC', size=12, weight=3) at 0x10a18ce50
 378+Font(name='STHeitiSC-Light', family='Heiti SC', size=24, weight=3) at 0x10a18cf90
 379 Font(name='STHeitiSC-Medium', family='Heiti SC', size=12, traits='Bold', weight=9) at 0x10a18ca50
 380+Font(name='STHeitiSC-Medium', family='Heiti SC', size=24, traits='Bold', weight=9) at 0x10a1ab190
 --- Family 'Heiti TC'
 381 Font(name='STHeitiTC-Light', family='Heiti TC', size=12, weight=3) at 0x10a1ab310
 382+Font(name='STHeitiTC-Light', family='Heiti TC', size=24, weight=3) at 0x10a1ab4d0
 383 Font(name='STHeitiTC-Medium', family='Heiti TC', size=12, traits='Bold', weight=9) at 0x10a1ab150
 384+Font(name='STHeitiTC-Medium', family='Heiti TC', size=24, traits='Bold', weight=9) at 0x10a1ab650
 --- Family 'Helvetica'
 385 Font(name='Helvetica', family='Helvetica', size=12, weight=5) at 0x10a1ab190
 386+Font(name='Helvetica', family='Helvetica', size=24, weight=5) at 0x10a1ab650
 387 Font(name='Helvetica-Oblique', family='Helvetica', size=12, traits='Italic', weight=5) at 0x10a1ab610
 388+Font(name='Helvetica-Oblique', family='Helvetica', size=24, traits='Italic', weight=5) at 0x10a1ab990
 389 Font(name='Helvetica-Light', family='Helvetica', size=12, weight=3) at 0x10a1ab7d0
 390+Font(name='Helvetica-Light', family='Helvetica', size=24, weight=3) at 0x10a1aba90
 391 Font(name='Helvetica-LightOblique', family='Helvetica', size=12, traits='Italic', weight=3) at 0x10a1abc50
 392+Font(name='Helvetica-LightOblique', family='Helvetica', size=24, traits='Italic', weight=3) at 0x10a1ab8d0
 393 Font(name='Helvetica-Bold', family='Helvetica', size=12, traits='Bold', weight=9) at 0x10a1ab990
 394+Font(name='Helvetica-Bold', family='Helvetica', size=24, traits='Bold', weight=9) at 0x10a1abc90
 395 Font(name='Helvetica-BoldOblique', family='Helvetica', size=12, traits='Bold Italic', weight=9) at 0x10a1abd90
 396+Font(name='Helvetica-BoldOblique', family='Helvetica', size=24, traits='Bold Italic', weight=9) at 0x10a1abbd0
 --- Family 'Helvetica Neue'
 397 Font(name='HelveticaNeue', family='Helvetica Neue', size=12, weight=5) at 0x10a1b4210
 398+Font(name='HelveticaNeue', family='Helvetica Neue', size=24, weight=5) at 0x10a1b4190
 399 Font(name='HelveticaNeue-Italic', family='Helvetica Neue', size=12, traits='Italic', weight=5) at 0x10a1b4350
 400+Font(name='HelveticaNeue-Italic', family='Helvetica Neue', size=24, traits='Italic', weight=5) at 0x10a1b4390
 401 Font(name='HelveticaNeue-UltraLight', family='Helvetica Neue', size=12, weight=2) at 0x10a1b45d0
 402+Font(name='HelveticaNeue-UltraLight', family='Helvetica Neue', size=24, weight=2) at 0x10a1b4610
 403 Font(name='HelveticaNeue-UltraLightItalic', family='Helvetica Neue', size=12, traits='Italic', weight=2) at 0x10a1b4490
 404+Font(name='HelveticaNeue-UltraLightItalic', family='Helvetica Neue', size=24, traits='Italic', weight=2) at 0x10a1b4650
 405 Font(name='HelveticaNeue-Thin', family='Helvetica Neue', size=12, weight=3) at 0x10a1b42d0
 406+Font(name='HelveticaNeue-Thin', family='Helvetica Neue', size=24, weight=3) at 0x10a1b4510
 407 Font(name='HelveticaNeue-LightItalic', family='Helvetica Neue', size=12, traits='Italic', weight=3) at 0x10a1b4b50
 408+Font(name='HelveticaNeue-LightItalic', family='Helvetica Neue', size=24, traits='Italic', weight=3) at 0x10a1b49d0
 409 Font(name='HelveticaNeue-Thin', family='Helvetica Neue', size=12, weight=3) at 0x10a1b42d0
 410+Font(name='HelveticaNeue-Thin', family='Helvetica Neue', size=24, weight=3) at 0x10a1b49d0
 411 Font(name='HelveticaNeue-LightItalic', family='Helvetica Neue', size=12, traits='Italic', weight=3) at 0x10a1b4e10
 412+Font(name='HelveticaNeue-LightItalic', family='Helvetica Neue', size=24, traits='Italic', weight=3) at 0x10a1b4c90
 413 Font(name='HelveticaNeue-Medium', family='Helvetica Neue', size=12, weight=6) at 0x10a1b4f10
 414+Font(name='HelveticaNeue-Medium', family='Helvetica Neue', size=24, weight=6) at 0x10a1b4cd0
 415 Font(name='HelveticaNeue-MediumItalic', family='Helvetica Neue', size=12, traits='Italic', weight=7) at 0x10a1b4ad0
 416+Font(name='HelveticaNeue-MediumItalic', family='Helvetica Neue', size=24, traits='Italic', weight=7) at 0x10dc9f050
 417 Font(name='HelveticaNeue-Bold', family='Helvetica Neue', size=12, traits='Bold', weight=9) at 0x10a1b4f10
 418+Font(name='HelveticaNeue-Bold', family='Helvetica Neue', size=24, traits='Bold', weight=9) at 0x10dc9f050
 419 Font(name='HelveticaNeue-BoldItalic', family='Helvetica Neue', size=12, traits='Bold Italic', weight=9) at 0x10dc9f390
 420+Font(name='HelveticaNeue-BoldItalic', family='Helvetica Neue', size=24, traits='Bold Italic', weight=9) at 0x10dc9f0d0
 421 Font(name='HelveticaNeue-Bold', family='Helvetica Neue', size=12, traits='Bold', weight=9) at 0x10dc9f1d0
 422+Font(name='HelveticaNeue-Bold', family='Helvetica Neue', size=24, traits='Bold', weight=9) at 0x10dc9f5d0
 423 Font(name='HelveticaNeue-CondensedBlack', family='Helvetica Neue', size=12, traits='Bold Condensed', weight=11) at 0x10dc9f390
 424+Font(name='HelveticaNeue-CondensedBlack', family='Helvetica Neue', size=24, traits='Bold Condensed', weight=11) at 0x10dc9f710
 --- Family 'Herculanum'
 425 Font(name='Herculanum', family='Herculanum', size=12, weight=5) at 0x10dc9f390
 426+Font(name='Herculanum', family='Herculanum', size=24, weight=5) at 0x10dc9f710
 --- Family 'Hiragino Kaku Gothic Pro'
 427 Font(name='HiraKakuPro-W3', family='Hiragino Kaku Gothic Pro', size=12, weight=4) at 0x10dc9fa10
 428+Font(name='HiraKakuPro-W3', family='Hiragino Kaku Gothic Pro', size=24, weight=4) at 0x10dc9fad0
 429 Font(name='HiraKakuPro-W6', family='Hiragino Kaku Gothic Pro', size=12, traits='Bold', weight=8) at 0x10dc9f890
 430+Font(name='HiraKakuPro-W6', family='Hiragino Kaku Gothic Pro', size=24, traits='Bold', weight=8) at 0x10dc9fc50
 --- Family 'Hiragino Kaku Gothic ProN'
 431 Font(name='HiraKakuProN-W3', family='Hiragino Kaku Gothic ProN', size=12, weight=4) at 0x10dc9fe50
 432+Font(name='HiraKakuProN-W3', family='Hiragino Kaku Gothic ProN', size=24, weight=4) at 0x10dc9ff90
 433 Font(name='HiraKakuProN-W6', family='Hiragino Kaku Gothic ProN', size=12, traits='Bold', weight=8) at 0x10dc9fa90
 434+Font(name='HiraKakuProN-W6', family='Hiragino Kaku Gothic ProN', size=24, traits='Bold', weight=8) at 0x10a1af190
 --- Family 'Hiragino Kaku Gothic Std'
 435 Font(name='HiraKakuStd-W8', family='Hiragino Kaku Gothic Std', size=12, traits='Bold', weight=10) at 0x10a1af410
 436+Font(name='HiraKakuStd-W8', family='Hiragino Kaku Gothic Std', size=24, traits='Bold', weight=10) at 0x10a1af250
 --- Family 'Hiragino Kaku Gothic StdN'
 437 Font(name='HiraKakuStdN-W8', family='Hiragino Kaku Gothic StdN', size=12, traits='Bold', weight=10) at 0x10a1af650
 438+Font(name='HiraKakuStdN-W8', family='Hiragino Kaku Gothic StdN', size=24, traits='Bold', weight=10) at 0x10a1af550
 --- Family 'Hiragino Maru Gothic Pro'
 439 Font(name='HiraMaruPro-W4', family='Hiragino Maru Gothic Pro', size=12, weight=5) at 0x10a1af9d0
 440+Font(name='HiraMaruPro-W4', family='Hiragino Maru Gothic Pro', size=24, weight=5) at 0x10a1af910
 --- Family 'Hiragino Maru Gothic ProN'
 441 Font(name='HiraMaruProN-W4', family='Hiragino Maru Gothic ProN', size=12, weight=5) at 0x10a1afb90
 442+Font(name='HiraMaruProN-W4', family='Hiragino Maru Gothic ProN', size=24, weight=5) at 0x10a1afc10
 --- Family 'Hiragino Mincho Pro'
 443 Font(name='HiraMinPro-W3', family='Hiragino Mincho Pro', size=12, weight=4) at 0x10a1afe10
 444+Font(name='HiraMinPro-W3', family='Hiragino Mincho Pro', size=24, weight=4) at 0x10a1afd90
 445 Font(name='HiraMinPro-W6', family='Hiragino Mincho Pro', size=12, traits='Bold', weight=8) at 0x10a1afb50
 446+Font(name='HiraMinPro-W6', family='Hiragino Mincho Pro', size=24, traits='Bold', weight=8) at 0x10a1aff90
 --- Family 'Hiragino Mincho ProN'
 447 Font(name='HiraMinProN-W3', family='Hiragino Mincho ProN', size=12, weight=4) at 0x10dcb2190
 448+Font(name='HiraMinProN-W3', family='Hiragino Mincho ProN', size=24, weight=4) at 0x10dcb2150
 449 Font(name='HiraMinProN-W6', family='Hiragino Mincho ProN', size=12, traits='Bold', weight=8) at 0x10dcb2050
 450+Font(name='HiraMinProN-W6', family='Hiragino Mincho ProN', size=24, traits='Bold', weight=8) at 0x10dcb2350
 --- Family 'Hiragino Sans'
 451 Font(name='HiraginoSans-W4', family='Hiragino Sans', size=12, traits='SansSerif', weight=5) at 0x10dcb2650
 452+Font(name='HiraginoSans-W4', family='Hiragino Sans', size=24, traits='SansSerif', weight=5) at 0x10dcb24d0
 453 Font(name='HiraginoSans-W4', family='Hiragino Sans', size=12, traits='SansSerif', weight=5) at 0x10dcb2390
 454+Font(name='HiraginoSans-W4', family='Hiragino Sans', size=24, traits='SansSerif', weight=5) at 0x10dcb2890
 455 Font(name='HiraginoSans-W4', family='Hiragino Sans', size=12, traits='SansSerif', weight=5) at 0x10dcb2590
 456+Font(name='HiraginoSans-W4', family='Hiragino Sans', size=24, traits='SansSerif', weight=5) at 0x10dcb2c50
 457 Font(name='HiraginoSans-W4', family='Hiragino Sans', size=12, traits='SansSerif', weight=5) at 0x10dcb2a10
 458+Font(name='HiraginoSans-W4', family='Hiragino Sans', size=24, traits='SansSerif', weight=5) at 0x10dcb2b90
 459 Font(name='HiraginoSans-W4', family='Hiragino Sans', size=12, traits='SansSerif', weight=5) at 0x10dcb2bd0
 460+Font(name='HiraginoSans-W4', family='Hiragino Sans', size=24, traits='SansSerif', weight=5) at 0x10dcb2f50
 461 Font(name='HiraginoSans-W7', family='Hiragino Sans', size=12, traits='Bold SansSerif', weight=9) at 0x10dcb2d90
 462+Font(name='HiraginoSans-W7', family='Hiragino Sans', size=24, traits='Bold SansSerif', weight=9) at 0x10dcbc150
 463 Font(name='HiraginoSans-W7', family='Hiragino Sans', size=12, traits='Bold SansSerif', weight=9) at 0x10dcb2e50
 464+Font(name='HiraginoSans-W7', family='Hiragino Sans', size=24, traits='Bold SansSerif', weight=9) at 0x10dcbc2d0
 465 Font(name='HiraginoSans-W7', family='Hiragino Sans', size=12, traits='Bold SansSerif', weight=9) at 0x10dcbc110
 466+Font(name='HiraginoSans-W7', family='Hiragino Sans', size=24, traits='Bold SansSerif', weight=9) at 0x10dcbc3d0
 467 Font(name='HiraginoSans-W7', family='Hiragino Sans', size=12, traits='Bold SansSerif', weight=9) at 0x10dcbc1d0
 468+Font(name='HiraginoSans-W7', family='Hiragino Sans', size=24, traits='Bold SansSerif', weight=9) at 0x10dcbc590
 469 Font(name='HiraginoSans-W7', family='Hiragino Sans', size=12, traits='Bold SansSerif', weight=9) at 0x10dcbc210
 470+Font(name='HiraginoSans-W7', family='Hiragino Sans', size=24, traits='Bold SansSerif', weight=9) at 0x10dcbc750
 --- Family 'Hiragino Sans GB'
 471 Font(name='HiraginoSansGB-W3', family='Hiragino Sans GB', size=12, traits='SansSerif', weight=4) at 0x10dcbc790
 472+Font(name='HiraginoSansGB-W3', family='Hiragino Sans GB', size=24, traits='SansSerif', weight=4) at 0x10dcbc990
 473 Font(name='HiraginoSansGB-W6', family='Hiragino Sans GB', size=12, traits='Bold SansSerif', weight=8) at 0x10dcbc410
 474+Font(name='HiraginoSansGB-W6', family='Hiragino Sans GB', size=24, traits='Bold SansSerif', weight=8) at 0x10dcbca10
 --- Family 'Hoefler Text'
 475 Font(name='HoeflerText-Regular', family='Hoefler Text', size=12, weight=5) at 0x10dcbccd0
 476+Font(name='HoeflerText-Regular', family='Hoefler Text', size=24, weight=5) at 0x10dcbc410
 477 Font(name='HoeflerText-Regular', family='Hoefler Text', size=12, weight=5) at 0x10dcbcc10
 478+Font(name='HoeflerText-Regular', family='Hoefler Text', size=24, weight=5) at 0x10dcbc410
 479 Font(name='HoeflerText-Italic', family='Hoefler Text', size=12, traits='Italic', weight=5) at 0x10dcbccd0
 480+Font(name='HoeflerText-Italic', family='Hoefler Text', size=24, traits='Italic', weight=5) at 0x10dcbcf10
 481 Font(name='HoeflerText-Black', family='Hoefler Text', size=12, traits='Bold', weight=9) at 0x10dcbcc10
 482+Font(name='HoeflerText-Black', family='Hoefler Text', size=24, traits='Bold', weight=9) at 0x10dcc8190
 483 Font(name='HoeflerText-BlackItalic', family='Hoefler Text', size=12, traits='Bold Italic', weight=9) at 0x10dcbce90
 484+Font(name='HoeflerText-BlackItalic', family='Hoefler Text', size=24, traits='Bold Italic', weight=9) at 0x10dcc8310
 --- Family 'Impact'
 485 Font(name='Impact', family='Impact', size=12, traits='Bold Condensed', weight=11) at 0x10dcc8550
 486+Font(name='Impact', family='Impact', size=24, traits='Bold Condensed', weight=11) at 0x10dcc8290
 --- Family 'InaiMathi'
 487 Font(name='InaiMathi', family='InaiMathi', size=12, weight=5) at 0x10dcc8390
 488+Font(name='InaiMathi', family='InaiMathi', size=24, weight=5) at 0x10dcc8290
 489 Font(name='InaiMathi-Bold', family='InaiMathi', size=12, traits='Bold', weight=9) at 0x10dcc8610
 490+Font(name='InaiMathi-Bold', family='InaiMathi', size=24, traits='Bold', weight=9) at 0x10dcc8a10
 --- Family 'Iowan Old Style'
 491 Font(name='IowanOldStyle-Roman', family='Iowan Old Style', size=12, weight=5) at 0x10dcc8b90
 492+Font(name='IowanOldStyle-Roman', family='Iowan Old Style', size=24, weight=5) at 0x10dcc8d50
 493 Font(name='IowanOldStyle-Roman', family='Iowan Old Style', size=12, weight=5) at 0x10dcc89d0
 494+Font(name='IowanOldStyle-Roman', family='Iowan Old Style', size=24, weight=5) at 0x10dcc8d50
 495 Font(name='IowanOldStyle-Italic', family='Iowan Old Style', size=12, traits='Italic', weight=5) at 0x10dcc8ed0
 496+Font(name='IowanOldStyle-Italic', family='Iowan Old Style', size=24, traits='Italic', weight=5) at 0x10dcd3050
 497 Font(name='IowanOldStyle-Bold', family='Iowan Old Style', size=12, traits='Bold', weight=9) at 0x10dcc89d0
 498+Font(name='IowanOldStyle-Bold', family='Iowan Old Style', size=24, traits='Bold', weight=9) at 0x10dcd3050
 499 Font(name='IowanOldStyle-BoldItalic', family='Iowan Old Style', size=12, traits='Bold Italic', weight=9) at 0x10dcd3290
 500+Font(name='IowanOldStyle-BoldItalic', family='Iowan Old Style', size=24, traits='Bold Italic', weight=9) at 0x10dcd30d0
 501 Font(name='IowanOldStyle-Black', family='Iowan Old Style', size=12, traits='Bold', weight=11) at 0x10dcd3190
 502+Font(name='IowanOldStyle-Black', family='Iowan Old Style', size=24, traits='Bold', weight=11) at 0x10dcd3350
 503 Font(name='IowanOldStyle-BlackItalic', family='Iowan Old Style', size=12, traits='Bold Italic', weight=11) at 0x10dcd3610
 504+Font(name='IowanOldStyle-BlackItalic', family='Iowan Old Style', size=24, traits='Bold Italic', weight=11) at 0x10dcd3290
 --- Family 'ITF Devanagari'
 505 Font(name='ITFDevanagari-Book', family='ITF Devanagari', size=12, weight=5) at 0x10dcd3910
 506+Font(name='ITFDevanagari-Book', family='ITF Devanagari', size=24, weight=5) at 0x10dcd3a50
 507 Font(name='ITFDevanagari-Light', family='ITF Devanagari', size=12, weight=3) at 0x10dcd3750
 508+Font(name='ITFDevanagari-Light', family='ITF Devanagari', size=24, weight=3) at 0x10dcd3ad0
 509 Font(name='ITFDevanagari-Medium', family='ITF Devanagari', size=12, weight=6) at 0x10dcd3c10
 510+Font(name='ITFDevanagari-Medium', family='ITF Devanagari', size=24, weight=6) at 0x10dcd3910
 511 Font(name='ITFDevanagari-Bold', family='ITF Devanagari', size=12, traits='Bold', weight=9) at 0x10dcd3750
 512+Font(name='ITFDevanagari-Bold', family='ITF Devanagari', size=24, traits='Bold', weight=9) at 0x10dcd3d90
 513 Font(name='ITFDevanagari-Bold', family='ITF Devanagari', size=12, traits='Bold', weight=9) at 0x10dcd3c10
 514+Font(name='ITFDevanagari-Bold', family='ITF Devanagari', size=24, traits='Bold', weight=9) at 0x10dcdd110
 --- Family 'ITF Devanagari Marathi'
 515 Font(name='ITFDevanagariMarathi-Book', family='ITF Devanagari Marathi', size=12, weight=5) at 0x10dcdd4d0
 516+Font(name='ITFDevanagariMarathi-Book', family='ITF Devanagari Marathi', size=24, weight=5) at 0x10dcdd110
 517 Font(name='ITFDevanagariMarathi-Light', family='ITF Devanagari Marathi', size=12, weight=3) at 0x10dcdd710
 518+Font(name='ITFDevanagariMarathi-Light', family='ITF Devanagari Marathi', size=24, weight=3) at 0x10dcdd110
 519 Font(name='ITFDevanagariMarathi-Medium', family='ITF Devanagari Marathi', size=12, weight=6) at 0x10dcdd890
 520+Font(name='ITFDevanagariMarathi-Medium', family='ITF Devanagari Marathi', size=24, weight=6) at 0x10dcdd110
 521 Font(name='ITFDevanagariMarathi-Bold', family='ITF Devanagari Marathi', size=12, traits='Bold', weight=9) at 0x10dcdd4d0
 522+Font(name='ITFDevanagariMarathi-Bold', family='ITF Devanagari Marathi', size=24, traits='Bold', weight=9) at 0x10dcdd810
 523 Font(name='ITFDevanagariMarathi-Bold', family='ITF Devanagari Marathi', size=12, traits='Bold', weight=9) at 0x10dcddb90
 524+Font(name='ITFDevanagariMarathi-Bold', family='ITF Devanagari Marathi', size=24, traits='Bold', weight=9) at 0x10dcdd890
 --- Family 'Jazz LET'
 525 Font(name='JazzLetPlain', family='Jazz LET', size=12, traits='Bold Expanded', weight=11) at 0x10dcddd90
 526+Font(name='JazzLetPlain', family='Jazz LET', size=24, traits='Bold Expanded', weight=11) at 0x10dcddb50
 --- Family 'Kailasa'
 527 Font(name='Kailasa', family='Kailasa', size=12, weight=5) at 0x10dcddf10
 528+Font(name='Kailasa', family='Kailasa', size=24, weight=5) at 0x10dcddb50
 529 Font(name='Kailasa-Bold', family='Kailasa', size=12, traits='Bold', weight=9) at 0x10dcdde10
 530+Font(name='Kailasa-Bold', family='Kailasa', size=24, traits='Bold', weight=9) at 0x117f95090
 --- Family 'Kannada MN'
 531 Font(name='KannadaMN', family='Kannada MN', size=12, weight=5) at 0x117f953d0
 532+Font(name='KannadaMN', family='Kannada MN', size=24, weight=5) at 0x117f95090
 533 Font(name='KannadaMN-Bold', family='Kannada MN', size=12, traits='Bold', weight=9) at 0x117f952d0
 534+Font(name='KannadaMN-Bold', family='Kannada MN', size=24, traits='Bold', weight=9) at 0x117f95710
 --- Family 'Kannada Sangam MN'
 535 Font(name='KannadaSangamMN', family='Kannada Sangam MN', size=12, weight=5) at 0x117f95890
 536+Font(name='KannadaSangamMN', family='Kannada Sangam MN', size=24, weight=5) at 0x117f95a50
 537 Font(name='KannadaSangamMN-Bold', family='Kannada Sangam MN', size=12, traits='Bold', weight=9) at 0x117f95990
 538+Font(name='KannadaSangamMN-Bold', family='Kannada Sangam MN', size=24, traits='Bold', weight=9) at 0x117f95ad0
 --- Family 'Kefa'
 539 Font(name='Kefa-Regular', family='Kefa', size=12, weight=5) at 0x117f95d90
 540+Font(name='Kefa-Regular', family='Kefa', size=24, weight=5) at 0x117f95ad0
 541 Font(name='Kefa-Bold', family='Kefa', size=12, traits='Bold', weight=9) at 0x117f95bd0
 542+Font(name='Kefa-Bold', family='Kefa', size=24, traits='Bold', weight=9) at 0x117fa30d0
 --- Family 'Khmer MN'
 543 Font(name='KhmerMN', family='Khmer MN', size=12, weight=5) at 0x117fa3250
 544+Font(name='KhmerMN', family='Khmer MN', size=24, weight=5) at 0x117fa30d0
 545 Font(name='KhmerMN-Bold', family='Khmer MN', size=12, traits='Bold', weight=9) at 0x117fa3150
 546+Font(name='KhmerMN-Bold', family='Khmer MN', size=24, traits='Bold', weight=9) at 0x117fa3350
 --- Family 'Khmer Sangam MN'
 547 Font(name='KhmerSangamMN', family='Khmer Sangam MN', size=12, weight=5) at 0x117fa3710
 548+Font(name='KhmerSangamMN', family='Khmer Sangam MN', size=24, weight=5) at 0x117fa38d0
 --- Family 'Kohinoor Bangla'
 549 Font(name='KohinoorBangla-Regular', family='Kohinoor Bangla', size=12, weight=5) at 0x117fa3b10
 550+Font(name='KohinoorBangla-Regular', family='Kohinoor Bangla', size=24, weight=5) at 0x117fa39d0
 551 Font(name='KohinoorBangla-Light', family='Kohinoor Bangla', size=12, weight=3) at 0x117fa38d0
 552+Font(name='KohinoorBangla-Light', family='Kohinoor Bangla', size=24, weight=3) at 0x117fa3d10
 553 Font(name='KohinoorBangla-Medium', family='Kohinoor Bangla', size=12, weight=6) at 0x117fa3c10
 554+Font(name='KohinoorBangla-Medium', family='Kohinoor Bangla', size=24, weight=6) at 0x117fa3e90
 555 Font(name='KohinoorBangla-Bold', family='Kohinoor Bangla', size=12, traits='Bold', weight=9) at 0x117fa38d0
 556+Font(name='KohinoorBangla-Bold', family='Kohinoor Bangla', size=24, traits='Bold', weight=9) at 0x117fa3f50
 557 Font(name='KohinoorBangla-Bold', family='Kohinoor Bangla', size=12, traits='Bold', weight=9) at 0x117fa3c50
 558+Font(name='KohinoorBangla-Bold', family='Kohinoor Bangla', size=24, traits='Bold', weight=9) at 0x117fa3d10
 --- Family 'Kohinoor Devanagari'
 559 Font(name='KohinoorDevanagari-Regular', family='Kohinoor Devanagari', size=12, weight=5) at 0x117fb0490
 560+Font(name='KohinoorDevanagari-Regular', family='Kohinoor Devanagari', size=24, weight=5) at 0x117fb0350
 561 Font(name='KohinoorDevanagari-Light', family='Kohinoor Devanagari', size=12, weight=3) at 0x117fb0550
 562+Font(name='KohinoorDevanagari-Light', family='Kohinoor Devanagari', size=24, weight=3) at 0x117fb0350
 563 Font(name='KohinoorDevanagari-Medium', family='Kohinoor Devanagari', size=12, weight=6) at 0x117fb0690
 564+Font(name='KohinoorDevanagari-Medium', family='Kohinoor Devanagari', size=24, weight=6) at 0x117fb0350
 565 Font(name='KohinoorDevanagari-Bold', family='Kohinoor Devanagari', size=12, traits='Bold', weight=9) at 0x117fb0990
 566+Font(name='KohinoorDevanagari-Bold', family='Kohinoor Devanagari', size=24, traits='Bold', weight=9) at 0x117fb0a10
 567 Font(name='KohinoorDevanagari-Bold', family='Kohinoor Devanagari', size=12, traits='Bold', weight=9) at 0x117fb0c90
 568+Font(name='KohinoorDevanagari-Bold', family='Kohinoor Devanagari', size=24, traits='Bold', weight=9) at 0x117fb0490
 --- Family 'Kohinoor Telugu'
 569 Font(name='KohinoorTelugu-Regular', family='Kohinoor Telugu', size=12, weight=5) at 0x117fb0e10
 570+Font(name='KohinoorTelugu-Regular', family='Kohinoor Telugu', size=24, weight=5) at 0x117fb0ed0
 571 Font(name='KohinoorTelugu-Light', family='Kohinoor Telugu', size=12, weight=3) at 0x117fb0f50
 572+Font(name='KohinoorTelugu-Light', family='Kohinoor Telugu', size=24, weight=3) at 0x117fb0ad0
 573 Font(name='KohinoorTelugu-Medium', family='Kohinoor Telugu', size=12, weight=6) at 0x117fb0e50
 574+Font(name='KohinoorTelugu-Medium', family='Kohinoor Telugu', size=24, weight=6) at 0x117fb0d90
 575 Font(name='KohinoorTelugu-Bold', family='Kohinoor Telugu', size=12, traits='Bold', weight=9) at 0x117fb0550
 576+Font(name='KohinoorTelugu-Bold', family='Kohinoor Telugu', size=24, traits='Bold', weight=9) at 0x117faf250
 577 Font(name='KohinoorTelugu-Bold', family='Kohinoor Telugu', size=12, traits='Bold', weight=9) at 0x117fb0f10
 578+Font(name='KohinoorTelugu-Bold', family='Kohinoor Telugu', size=24, traits='Bold', weight=9) at 0x117faf590
 --- Family 'Kokonor'
 579 Font(name='Kokonor', family='Kokonor', size=12, weight=5) at 0x117faf490
 580+Font(name='Kokonor', family='Kokonor', size=24, weight=5) at 0x117faf590
 --- Family 'Krungthep'
 581 Font(name='Krungthep', family='Krungthep', size=12, traits='Bold', weight=9) at 0x117faf490
 582+Font(name='Krungthep', family='Krungthep', size=24, traits='Bold', weight=9) at 0x117faf990
 --- Family 'KufiStandardGK'
 583 Font(name='KufiStandardGK', family='KufiStandardGK', size=12, weight=5) at 0x117faf8d0
 584+Font(name='KufiStandardGK', family='KufiStandardGK', size=24, weight=5) at 0x117fafbd0
 --- Family 'Lao MN'
 585 Font(name='LaoMN', family='Lao MN', size=12, weight=5) at 0x117fafd50
 586+Font(name='LaoMN', family='Lao MN', size=24, weight=5) at 0x117fafbd0
 587 Font(name='LaoMN-Bold', family='Lao MN', size=12, traits='Bold', weight=9) at 0x117fafc90
 588+Font(name='LaoMN-Bold', family='Lao MN', size=24, traits='Bold', weight=9) at 0x117fc40d0
 --- Family 'Lao Sangam MN'
 589 Font(name='LaoSangamMN', family='Lao Sangam MN', size=12, weight=5) at 0x117fc4250
 590+Font(name='LaoSangamMN', family='Lao Sangam MN', size=24, weight=5) at 0x117fc4410
 --- Family 'Lucida Grande'
 591 Font(name='LucidaGrande', family='Lucida Grande', size=12, weight=5) at 0x117fc4590
 592+Font(name='LucidaGrande', family='Lucida Grande', size=24, weight=5) at 0x117fc4150
 593 Font(name='LucidaGrande-Bold', family='Lucida Grande', size=12, traits='Bold', weight=9) at 0x117fc40d0
 594+Font(name='LucidaGrande-Bold', family='Lucida Grande', size=24, traits='Bold', weight=9) at 0x117fc4750
 --- Family 'Luminari'
 595 Font(name='Luminari-Regular', family='Luminari', size=12, weight=5) at 0x117fc48d0
 596+Font(name='Luminari-Regular', family='Luminari', size=24, weight=5) at 0x117fc4a90
 --- Family 'Malayalam MN'
 597 Font(name='MalayalamMN', family='Malayalam MN', size=12, weight=5) at 0x117fc4b90
 598+Font(name='MalayalamMN', family='Malayalam MN', size=24, weight=5) at 0x117fc4d50
 599 Font(name='MalayalamMN-Bold', family='Malayalam MN', size=12, traits='Bold', weight=9) at 0x117fc4ad0
 600+Font(name='MalayalamMN-Bold', family='Malayalam MN', size=24, traits='Bold', weight=9) at 0x117fc4ed0
 --- Family 'Malayalam Sangam MN'
 601 Font(name='MalayalamSangamMN', family='Malayalam Sangam MN', size=12, weight=5) at 0x1188d9050
 602+Font(name='MalayalamSangamMN', family='Malayalam Sangam MN', size=24, weight=5) at 0x1188d9250
 603 Font(name='MalayalamSangamMN-Bold', family='Malayalam Sangam MN', size=12, traits='Bold', weight=9) at 0x117fc4f90
 604+Font(name='MalayalamSangamMN-Bold', family='Malayalam Sangam MN', size=24, traits='Bold', weight=9) at 0x1188d9190
 --- Family 'Marion'
 605 Font(name='Marion-Regular', family='Marion', size=12, weight=5) at 0x1188d9590
 606+Font(name='Marion-Regular', family='Marion', size=24, weight=5) at 0x1188d96d0
 607 Font(name='Marion-Italic', family='Marion', size=12, traits='Italic', weight=5) at 0x1188d9350
 608+Font(name='Marion-Italic', family='Marion', size=24, traits='Italic', weight=5) at 0x1188d9890
 609 Font(name='Marion-Bold', family='Marion', size=12, traits='Bold', weight=9) at 0x1188d9190
 610+Font(name='Marion-Bold', family='Marion', size=24, traits='Bold', weight=9) at 0x1188d9950
 --- Family 'Marker Felt'
 611 Font(name='MarkerFelt-Thin', family='Marker Felt', size=12, weight=3) at 0x1188d9bd0
 612+Font(name='MarkerFelt-Thin', family='Marker Felt', size=24, weight=3) at 0x1188d9c10
 613 Font(name='MarkerFelt-Wide', family='Marker Felt', size=12, traits='Bold', weight=9) at 0x1188d9a90
 614+Font(name='MarkerFelt-Wide', family='Marker Felt', size=24, traits='Bold', weight=9) at 0x1188d9ed0
 --- Family 'Menlo'
 615 Font(name='Menlo-Regular', family='Menlo', size=12, traits='MonoSpace', weight=5) at 0x1188e4190
 616+Font(name='Menlo-Regular', family='Menlo', size=24, traits='MonoSpace', weight=5) at 0x1188e41d0
 617 Font(name='Menlo-Italic', family='Menlo', size=12, traits='Italic MonoSpace', weight=5) at 0x1188d9f90
 618+Font(name='Menlo-Italic', family='Menlo', size=24, traits='Italic MonoSpace', weight=5) at 0x1188e4450
 619 Font(name='Menlo-Bold', family='Menlo', size=12, traits='Bold MonoSpace', weight=9) at 0x1188e4290
 620+Font(name='Menlo-Bold', family='Menlo', size=24, traits='Bold MonoSpace', weight=9) at 0x1188e4610
 621 Font(name='Menlo-BoldItalic', family='Menlo', size=12, traits='Bold Italic MonoSpace', weight=9) at 0x1188e4410
 622+Font(name='Menlo-BoldItalic', family='Menlo', size=24, traits='Bold Italic MonoSpace', weight=9) at 0x1188e4610
 --- Family 'Microsoft Sans Serif'
 623 Font(name='MicrosoftSansSerif', family='Microsoft Sans Serif', size=12, traits='SansSerif', weight=5) at 0x1188e4990
 624+Font(name='MicrosoftSansSerif', family='Microsoft Sans Serif', size=24, traits='SansSerif', weight=5) at 0x1188e4ad0
 --- Family 'Mishafi'
 625 Font(name='DiwanMishafi', family='Mishafi', size=12, weight=5) at 0x1188e4b90
 626+Font(name='DiwanMishafi', family='Mishafi', size=24, weight=5) at 0x1188e4ad0
 --- Family 'Mishafi Gold'
 627 Font(name='DiwanMishafiGold', family='Mishafi Gold', size=12, weight=5) at 0x1188e4ed0
 628+Font(name='DiwanMishafiGold', family='Mishafi Gold', size=24, weight=5) at 0x1188e4fd0
 --- Family 'Mona Lisa Solid ITC TT'
 629 Font(name='MonaLisaSolidITCTT', family='Mona Lisa Solid ITC TT', size=12, traits='Bold Condensed', weight=9) at 0x1188f2390
 630+Font(name='MonaLisaSolidITCTT', family='Mona Lisa Solid ITC TT', size=24, traits='Bold Condensed', weight=9) at 0x1188f2410
 --- Family 'Monaco'
 631 Font(name='Monaco', family='Monaco', size=12, traits='MonoSpace', weight=5) at 0x1188f2450
 632+Font(name='Monaco', family='Monaco', size=24, traits='MonoSpace', weight=5) at 0x1188f2550
 --- Family 'Mshtakan'
 633 Font(name='Mshtakan', family='Mshtakan', size=12, weight=5) at 0x1188f2350
 634+Font(name='Mshtakan', family='Mshtakan', size=24, weight=5) at 0x1188f2550
 635 Font(name='MshtakanOblique', family='Mshtakan', size=12, traits='Italic', weight=5) at 0x1188f2710
 636+Font(name='MshtakanOblique', family='Mshtakan', size=24, traits='Italic', weight=5) at 0x1188f2b10
 637 Font(name='MshtakanBold', family='Mshtakan', size=12, traits='Bold', weight=9) at 0x1188f2910
 638+Font(name='MshtakanBold', family='Mshtakan', size=24, traits='Bold', weight=9) at 0x1188f2bd0
 639 Font(name='MshtakanBoldOblique', family='Mshtakan', size=12, traits='Bold Italic', weight=9) at 0x1188f2850
 640+Font(name='MshtakanBoldOblique', family='Mshtakan', size=24, traits='Bold Italic', weight=9) at 0x1188f2e90
 --- Family 'Muna'
 641 Font(name='Muna', family='Muna', size=12, weight=5) at 0x1188fe090
 642+Font(name='Muna', family='Muna', size=24, weight=5) at 0x1188fe190
 643 Font(name='MunaBold', family='Muna', size=12, traits='Bold', weight=9) at 0x1188f2dd0
 644+Font(name='MunaBold', family='Muna', size=24, traits='Bold', weight=9) at 0x1188fe0d0
 645 Font(name='MunaBlack', family='Muna', size=12, traits='Bold', weight=11) at 0x1188fe050
 646+Font(name='MunaBlack', family='Muna', size=24, traits='Bold', weight=11) at 0x1188fe450
 --- Family 'Myanmar MN'
 647 Font(name='MyanmarMN', family='Myanmar MN', size=12, weight=5) at 0x1188fe710
 648+Font(name='MyanmarMN', family='Myanmar MN', size=24, weight=5) at 0x1188fe450
 649 Font(name='MyanmarMN-Bold', family='Myanmar MN', size=12, traits='Bold', weight=9) at 0x1188fe610
 650+Font(name='MyanmarMN-Bold', family='Myanmar MN', size=24, traits='Bold', weight=9) at 0x1188fea50
 --- Family 'Myanmar Sangam MN'
 651 Font(name='MyanmarSangamMN', family='Myanmar Sangam MN', size=12, weight=5) at 0x1188febd0
 652+Font(name='MyanmarSangamMN', family='Myanmar Sangam MN', size=24, weight=5) at 0x1188fed90
 653 Font(name='MyanmarSangamMN-Bold', family='Myanmar Sangam MN', size=12, traits='Bold', weight=9) at 0x1188fecd0
 654+Font(name='MyanmarSangamMN-Bold', family='Myanmar Sangam MN', size=24, traits='Bold', weight=9) at 0x1188fee10
 --- Family 'Nadeem'
 655 Font(name='Nadeem', family='Nadeem', size=12, weight=5) at 0x1189080d0
 656+Font(name='Nadeem', family='Nadeem', size=24, weight=5) at 0x1188fee10
 --- Family 'New Peninim MT'
 657 Font(name='NewPeninimMT', family='New Peninim MT', size=12, weight=5) at 0x1189083d0
 658+Font(name='NewPeninimMT', family='New Peninim MT', size=24, weight=5) at 0x118908150
 659 Font(name='NewPeninimMT-Inclined', family='New Peninim MT', size=12, traits='Italic', weight=5) at 0x118908590
 660+Font(name='NewPeninimMT-Inclined', family='New Peninim MT', size=24, traits='Italic', weight=5) at 0x118908490
 661 Font(name='NewPeninimMT-Bold', family='New Peninim MT', size=12, traits='Bold', weight=9) at 0x118908350
 662+Font(name='NewPeninimMT-Bold', family='New Peninim MT', size=24, traits='Bold', weight=9) at 0x118908110
 663 Font(name='NewPeninimMT-BoldInclined', family='New Peninim MT', size=12, traits='Bold Italic', weight=9) at 0x118908950
 664+Font(name='NewPeninimMT-BoldInclined', family='New Peninim MT', size=24, traits='Bold Italic', weight=9) at 0x118908550
 --- Family 'Noteworthy'
 665 Font(name='Noteworthy-Light', family='Noteworthy', size=12, weight=3) at 0x118908ad0
 666+Font(name='Noteworthy-Light', family='Noteworthy', size=24, weight=3) at 0x118908c10
 667 Font(name='Noteworthy-Bold', family='Noteworthy', size=12, traits='Bold', weight=9) at 0x118908990
 668+Font(name='Noteworthy-Bold', family='Noteworthy', size=24, traits='Bold', weight=9) at 0x118908dd0
 --- Family 'Noto Nastaliq Urdu'
 669 Font(name='NotoNastaliqUrdu', family='Noto Nastaliq Urdu', size=12, weight=5) at 0x1189030d0
 670+Font(name='NotoNastaliqUrdu', family='Noto Nastaliq Urdu', size=24, weight=5) at 0x118903150
 --- Family 'Optima'
 671 Font(name='Optima-Regular', family='Optima', size=12, weight=5) at 0x118903250
 672+Font(name='Optima-Regular', family='Optima', size=24, weight=5) at 0x118903410
 673 Font(name='Optima-Italic', family='Optima', size=12, traits='Italic', weight=5) at 0x118903190
 674+Font(name='Optima-Italic', family='Optima', size=24, traits='Italic', weight=5) at 0x118903590
 675 Font(name='Optima-Bold', family='Optima', size=12, traits='Bold', weight=9) at 0x118903150
 676+Font(name='Optima-Bold', family='Optima', size=24, traits='Bold', weight=9) at 0x118903650
 677 Font(name='Optima-BoldItalic', family='Optima', size=12, traits='Bold Italic', weight=9) at 0x118903350
 678+Font(name='Optima-BoldItalic', family='Optima', size=24, traits='Bold Italic', weight=9) at 0x118903850
 679 Font(name='Optima-ExtraBlack', family='Optima', size=12, traits='Bold', weight=11) at 0x118903790
 680+Font(name='Optima-ExtraBlack', family='Optima', size=24, traits='Bold', weight=11) at 0x118903b50
 --- Family 'Oriya MN'
 681 Font(name='OriyaMN', family='Oriya MN', size=12, weight=5) at 0x118903cd0
 682+Font(name='OriyaMN', family='Oriya MN', size=24, weight=5) at 0x118903b50
 683 Font(name='OriyaMN-Bold', family='Oriya MN', size=12, traits='Bold', weight=9) at 0x118903b10
 684+Font(name='OriyaMN-Bold', family='Oriya MN', size=24, traits='Bold', weight=9) at 0x118903dd0
 --- Family 'Oriya Sangam MN'
 685 Font(name='OriyaSangamMN', family='Oriya Sangam MN', size=12, weight=5) at 0x1192d61d0
 686+Font(name='OriyaSangamMN', family='Oriya Sangam MN', size=24, weight=5) at 0x1192d6390
 687 Font(name='OriyaSangamMN-Bold', family='Oriya Sangam MN', size=12, traits='Bold', weight=9) at 0x1192d60d0
 688+Font(name='OriyaSangamMN-Bold', family='Oriya Sangam MN', size=24, traits='Bold', weight=9) at 0x1192d6510
 --- Family 'Osaka'
 689 Font(name='Osaka', family='Osaka', size=12, weight=5) at 0x1192d64d0
 690+Font(name='Osaka', family='Osaka', size=24, weight=5) at 0x1192d6510
 --- Family 'Palatino'
 691 Font(name='Palatino-Roman', family='Palatino', size=12, weight=5) at 0x1192d6910
 692+Font(name='Palatino-Roman', family='Palatino', size=24, weight=5) at 0x1192d6ad0
 693 Font(name='Palatino-Italic', family='Palatino', size=12, traits='Italic', weight=5) at 0x1192d64d0
 694+Font(name='Palatino-Italic', family='Palatino', size=24, traits='Italic', weight=5) at 0x1192d6c50
 695 Font(name='Palatino-Bold', family='Palatino', size=12, traits='Bold', weight=9) at 0x1192d6510
 696+Font(name='Palatino-Bold', family='Palatino', size=24, traits='Bold', weight=9) at 0x1192d6e50
 697 Font(name='Palatino-BoldItalic', family='Palatino', size=12, traits='Bold Italic', weight=9) at 0x1192d6a10
 698+Font(name='Palatino-BoldItalic', family='Palatino', size=24, traits='Bold Italic', weight=9) at 0x1192d6e10
 --- Family 'Papyrus'
 699 Font(name='Papyrus', family='Papyrus', size=12, weight=5) at 0x1192df0d0
 700+Font(name='Papyrus', family='Papyrus', size=24, weight=5) at 0x1192df290
 701 Font(name='Papyrus', family='Papyrus', size=12, weight=5) at 0x1192df090
 702+Font(name='Papyrus', family='Papyrus', size=24, weight=5) at 0x1192df410
 --- Family 'Party LET'
 703 Font(name='PartyLetPlain', family='Party LET', size=12, traits='Italic', weight=5) at 0x1192df550
 704+Font(name='PartyLetPlain', family='Party LET', size=24, traits='Italic', weight=5) at 0x1192df650
 --- Family 'Phosphate'
 705 Font(name='Phosphate-Inline', family='Phosphate', size=12, weight=5) at 0x1192df950
 706+Font(name='Phosphate-Inline', family='Phosphate', size=24, weight=5) at 0x1192dfa90
 707 Font(name='Phosphate-Inline', family='Phosphate', size=12, weight=5) at 0x1192df750
 708+Font(name='Phosphate-Inline', family='Phosphate', size=24, weight=5) at 0x1192dfc90
 --- Family 'PingFang HK'
 709 Font(name='PingFangHK-Regular', family='PingFang HK', size=12, weight=5) at 0x1192dfcd0
 710+Font(name='PingFangHK-Regular', family='PingFang HK', size=24, weight=5) at 0x1192dfe90
 711 Font(name='PingFangHK-Ultralight', family='PingFang HK', size=12, weight=2) at 0x1192dff90
 712+Font(name='PingFangHK-Ultralight', family='PingFang HK', size=24, weight=2) at 0x1192ed050
 713 Font(name='PingFangHK-Thin', family='PingFang HK', size=12, weight=3) at 0x1192dfcd0
 714+Font(name='PingFangHK-Thin', family='PingFang HK', size=24, weight=3) at 0x1192ed110
 715 Font(name='PingFangHK-Thin', family='PingFang HK', size=12, weight=3) at 0x1192dfc50
 716+Font(name='PingFangHK-Thin', family='PingFang HK', size=24, weight=3) at 0x1192ed110
 717 Font(name='PingFangHK-Medium', family='PingFang HK', size=12, weight=6) at 0x1192ed2d0
 718+Font(name='PingFangHK-Medium', family='PingFang HK', size=24, weight=6) at 0x1192ed250
 719 Font(name='PingFangHK-Semibold', family='PingFang HK', size=12, traits='Bold', weight=8) at 0x1192ed210
 720+Font(name='PingFangHK-Semibold', family='PingFang HK', size=24, traits='Bold', weight=8) at 0x1192ed650
 --- Family 'PingFang SC'
 721 Font(name='PingFangSC-Regular', family='PingFang SC', size=12, weight=5) at 0x1192ed7d0
 722+Font(name='PingFangSC-Regular', family='PingFang SC', size=24, weight=5) at 0x1192ed990
 723 Font(name='PingFangSC-Ultralight', family='PingFang SC', size=12, weight=2) at 0x1192ed8d0
 724+Font(name='PingFangSC-Ultralight', family='PingFang SC', size=24, weight=2) at 0x1192ed610
 725 Font(name='PingFangSC-Thin', family='PingFang SC', size=12, weight=3) at 0x1192ed7d0
 726+Font(name='PingFangSC-Thin', family='PingFang SC', size=24, weight=3) at 0x1192edc90
 727 Font(name='PingFangSC-Thin', family='PingFang SC', size=12, weight=3) at 0x1192edb50
 728+Font(name='PingFangSC-Thin', family='PingFang SC', size=24, weight=3) at 0x1192edc90
 729 Font(name='PingFangSC-Medium', family='PingFang SC', size=12, weight=6) at 0x1192ed7d0
 730+Font(name='PingFangSC-Medium', family='PingFang SC', size=24, weight=6) at 0x1192edcd0
 731 Font(name='PingFangSC-Semibold', family='PingFang SC', size=12, traits='Bold', weight=8) at 0x1192edb50
 732+Font(name='PingFangSC-Semibold', family='PingFang SC', size=24, traits='Bold', weight=8) at 0x1192f2150
 --- Family 'PingFang TC'
 733 Font(name='PingFangTC-Regular', family='PingFang TC', size=12, weight=5) at 0x1192f2290
 734+Font(name='PingFangTC-Regular', family='PingFang TC', size=24, weight=5) at 0x1192f2450
 735 Font(name='PingFangTC-Ultralight', family='PingFang TC', size=12, weight=2) at 0x1192f2390
 736+Font(name='PingFangTC-Ultralight', family='PingFang TC', size=24, weight=2) at 0x1192f20d0
 737 Font(name='PingFangTC-Thin', family='PingFang TC', size=12, weight=3) at 0x1192f2290
 738+Font(name='PingFangTC-Thin', family='PingFang TC', size=24, weight=3) at 0x1192f2750
 739 Font(name='PingFangTC-Thin', family='PingFang TC', size=12, weight=3) at 0x1192f2610
 740+Font(name='PingFangTC-Thin', family='PingFang TC', size=24, weight=3) at 0x1192f2750
 741 Font(name='PingFangTC-Medium', family='PingFang TC', size=12, weight=6) at 0x1192f2290
 742+Font(name='PingFangTC-Medium', family='PingFang TC', size=24, weight=6) at 0x1192f2790
 743 Font(name='PingFangTC-Semibold', family='PingFang TC', size=12, traits='Bold', weight=8) at 0x1192f2610
 744+Font(name='PingFangTC-Semibold', family='PingFang TC', size=24, traits='Bold', weight=8) at 0x1192f2b90
 --- Family 'Plantagenet Cherokee'
 745 Font(name='PlantagenetCherokee', family='Plantagenet Cherokee', size=12, weight=5) at 0x1192f2d50
 746+Font(name='PlantagenetCherokee', family='Plantagenet Cherokee', size=24, weight=5) at 0x1192f2d10
 --- Family 'PoemScriptW00-Regular'
 747 Font(name='PoemScriptW00-Regular', family='PoemScriptW00-Regular', size=12, weight=5) at 0x1192f8150
 748+Font(name='PoemScriptW00-Regular', family='PoemScriptW00-Regular', size=24, weight=5) at 0x1192f2d10
 --- Family 'PortagoITC TT'
 749 Font(name='PortagoITCTT', family='PortagoITC TT', size=12, traits='Bold Condensed', weight=11) at 0x1192f8090
 750+Font(name='PortagoITCTT', family='PortagoITC TT', size=24, traits='Bold Condensed', weight=11) at 0x1192f82d0
 --- Family 'Princetown LET'
 751 Font(name='PrincetownLET', family='Princetown LET', size=12, traits='Bold', weight=9) at 0x1192f8490
 752+Font(name='PrincetownLET', family='Princetown LET', size=24, traits='Bold', weight=9) at 0x1192f8590
 --- Family 'PT Mono'
 753 Font(name='PTMono-Regular', family='PT Mono', size=12, traits='MonoSpace', weight=5) at 0x1192f88d0
 754+Font(name='PTMono-Regular', family='PT Mono', size=24, traits='MonoSpace', weight=5) at 0x1192f8910
 755 Font(name='PTMono-Bold', family='PT Mono', size=12, traits='Bold MonoSpace', weight=9) at 0x1192f8690
 756+Font(name='PTMono-Bold', family='PT Mono', size=24, traits='Bold MonoSpace', weight=9) at 0x1192f8b90
 --- Family 'PT Sans'
 757 Font(name='PTSans-Regular', family='PT Sans', size=12, traits='SansSerif', weight=5) at 0x1192f8d10
 758+Font(name='PTSans-Regular', family='PT Sans', size=24, traits='SansSerif', weight=5) at 0x1192f8f10
 759 Font(name='PTSans-Italic', family='PT Sans', size=12, traits='Italic SansSerif', weight=5) at 0x1192f8bd0
 760+Font(name='PTSans-Italic', family='PT Sans', size=24, traits='Italic SansSerif', weight=5) at 0x11ea02090
 761 Font(name='PTSans-Bold', family='PT Sans', size=12, traits='Bold SansSerif', weight=9) at 0x1192f8fd0
 762+Font(name='PTSans-Bold', family='PT Sans', size=24, traits='Bold SansSerif', weight=9) at 0x11ea02190
 763 Font(name='PTSans-BoldItalic', family='PT Sans', size=12, traits='Bold Italic SansSerif', weight=9) at 0x11ea02050
 764+Font(name='PTSans-BoldItalic', family='PT Sans', size=24, traits='Bold Italic SansSerif', weight=9) at 0x11ea02190
 --- Family 'PT Sans Caption'
 765 Font(name='PTSans-Caption', family='PT Sans Caption', size=12, traits='SansSerif', weight=5) at 0x11ea02510
 766+Font(name='PTSans-Caption', family='PT Sans Caption', size=24, traits='SansSerif', weight=5) at 0x11ea02710
 767 Font(name='PTSans-CaptionBold', family='PT Sans Caption', size=12, traits='Bold SansSerif', weight=9) at 0x11ea02050
 768+Font(name='PTSans-CaptionBold', family='PT Sans Caption', size=24, traits='Bold SansSerif', weight=9) at 0x11ea02790
 --- Family 'PT Sans Narrow'
 769 Font(name='PTSans-Narrow', family='PT Sans Narrow', size=12, traits='Condensed Narrow SansSerif', weight=5) at 0x11ea02ad0
 770+Font(name='PTSans-Narrow', family='PT Sans Narrow', size=24, traits='Condensed Narrow SansSerif', weight=5) at 0x11ea02790
 771 Font(name='PTSans-NarrowBold', family='PT Sans Narrow', size=12, traits='Bold Condensed Narrow SansSerif', weight=9) at 0x11ea02710
 772+Font(name='PTSans-NarrowBold', family='PT Sans Narrow', size=24, traits='Bold Condensed Narrow SansSerif', weight=9) at 0x11ea02cd0
 --- Family 'PT Serif'
 773 Font(name='PTSerif-Regular', family='PT Serif', size=12, weight=5) at 0x11ea02ed0
 774+Font(name='PTSerif-Regular', family='PT Serif', size=24, weight=5) at 0x11ea02c90
 775 Font(name='PTSerif-Italic', family='PT Serif', size=12, traits='Italic', weight=5) at 0x11ea02e10
 776+Font(name='PTSerif-Italic', family='PT Serif', size=24, traits='Italic', weight=5) at 0x11ea0e210
 777 Font(name='PTSerif-Bold', family='PT Serif', size=12, traits='Bold', weight=9) at 0x11ea02cd0
 778+Font(name='PTSerif-Bold', family='PT Serif', size=24, traits='Bold', weight=9) at 0x11ea0e2d0
 779 Font(name='PTSerif-BoldItalic', family='PT Serif', size=12, traits='Bold Italic', weight=9) at 0x11ea0e0d0
 780+Font(name='PTSerif-BoldItalic', family='PT Serif', size=24, traits='Bold Italic', weight=9) at 0x11ea0e4d0
 --- Family 'PT Serif Caption'
 781 Font(name='PTSerif-Caption', family='PT Serif Caption', size=12, weight=5) at 0x11ea0e710
 782+Font(name='PTSerif-Caption', family='PT Serif Caption', size=24, weight=5) at 0x11ea0e8d0
 783 Font(name='PTSerif-CaptionItalic', family='PT Serif Caption', size=12, traits='Italic', weight=5) at 0x11ea0e810
 784+Font(name='PTSerif-CaptionItalic', family='PT Serif Caption', size=24, traits='Italic', weight=5) at 0x11ea0e950
 --- Family 'Raanana'
 785 Font(name='Raanana', family='Raanana', size=12, weight=5) at 0x11ea0e710
 786+Font(name='Raanana', family='Raanana', size=24, weight=5) at 0x11ea0e950
 787 Font(name='RaananaBold', family='Raanana', size=12, traits='Bold', weight=9) at 0x102937e10
 788+Font(name='RaananaBold', family='Raanana', size=24, traits='Bold', weight=9) at 0x105367690
 --- Family 'Rockwell'
 789 Font(name='Rockwell-Regular', family='Rockwell', size=12, weight=5) at 0x1053b8590
 790+Font(name='Rockwell-Regular', family='Rockwell', size=24, weight=5) at 0x1053b8cd0
 791 Font(name='Rockwell-Italic', family='Rockwell', size=12, traits='Italic', weight=5) at 0x105385710
 792+Font(name='Rockwell-Italic', family='Rockwell', size=24, traits='Italic', weight=5) at 0x1053dba50
 793 Font(name='Rockwell-Bold', family='Rockwell', size=12, traits='Bold', weight=9) at 0x1053b8b10
 794+Font(name='Rockwell-Bold', family='Rockwell', size=24, traits='Bold', weight=9) at 0x1053c8b90
 795 Font(name='Rockwell-BoldItalic', family='Rockwell', size=12, traits='Bold Italic', weight=9) at 0x1053dbf90
 796+Font(name='Rockwell-BoldItalic', family='Rockwell', size=24, traits='Bold Italic', weight=9) at 0x1053b3190
 --- Family 'Sana'
 797 Font(name='Sana', family='Sana', size=12, weight=5) at 0x105ba53d0
 798+Font(name='Sana', family='Sana', size=24, weight=5) at 0x105ba51d0
 --- Family 'Santa Fe LET'
 799 Font(name='SantaFeLetPlain', family='Santa Fe LET', size=12, traits='Bold Italic', weight=9) at 0x105b99090
 800+Font(name='SantaFeLetPlain', family='Santa Fe LET', size=24, traits='Bold Italic', weight=9) at 0x105b99f10
 --- Family 'Sathu'
 801 Font(name='Sathu', family='Sathu', size=12, weight=5) at 0x10846cdd0
 802+Font(name='Sathu', family='Sathu', size=24, weight=5) at 0x105b99f10
 --- Family 'Savoye LET'
 803 Font(name='SavoyeLetPlain', family='Savoye LET', size=12, traits='Italic', weight=5) at 0x105bc5590
 804+Font(name='SavoyeLetPlain', family='Savoye LET', size=24, traits='Italic', weight=5) at 0x105bc5b10
 --- Family 'SchoolHouse Cursive B'
 805 Font(name='SchoolHouseCursiveB', family='SchoolHouse Cursive B', size=12, traits='Italic', weight=5) at 0x108464a90
 806+Font(name='SchoolHouseCursiveB', family='SchoolHouse Cursive B', size=24, traits='Italic', weight=5) at 0x108db79d0
 --- Family 'SchoolHouse Printed A'
 807 Font(name='SchoolHousePrintedA', family='SchoolHouse Printed A', size=12, weight=5) at 0x1084a2390
 808+Font(name='SchoolHousePrintedA', family='SchoolHouse Printed A', size=24, weight=5) at 0x1084848d0
 --- Family 'Seravek'
 809 Font(name='Seravek', family='Seravek', size=12, weight=5) at 0x108490c50
 810+Font(name='Seravek', family='Seravek', size=24, weight=5) at 0x108dcf1d0
 811 Font(name='Seravek-Italic', family='Seravek', size=12, traits='Italic', weight=5) at 0x108490590
 812+Font(name='Seravek-Italic', family='Seravek', size=24, traits='Italic', weight=5) at 0x108dc6950
 813 Font(name='Seravek-ExtraLight', family='Seravek', size=12, weight=2) at 0x108dcf490
 814+Font(name='Seravek-ExtraLight', family='Seravek', size=24, weight=2) at 0x108ddc1d0
 815 Font(name='Seravek-ExtraLightItalic', family='Seravek', size=12, traits='Italic', weight=2) at 0x108dc6cd0
 816+Font(name='Seravek-ExtraLightItalic', family='Seravek', size=24, traits='Italic', weight=2) at 0x10a191610
 817 Font(name='Seravek-Light', family='Seravek', size=12, weight=3) at 0x108ddce50
 818+Font(name='Seravek-Light', family='Seravek', size=24, weight=3) at 0x108ddc110
 819 Font(name='Seravek-LightItalic', family='Seravek', size=12, traits='Italic', weight=3) at 0x10a191c50
 820+Font(name='Seravek-LightItalic', family='Seravek', size=24, traits='Italic', weight=3) at 0x10a1ab610
 821 Font(name='Seravek-Medium', family='Seravek', size=12, weight=6) at 0x10a191610
 822+Font(name='Seravek-Medium', family='Seravek', size=24, weight=6) at 0x10a1abc50
 823 Font(name='Seravek-MediumItalic', family='Seravek', size=12, traits='Italic', weight=7) at 0x10a1808d0
 824+Font(name='Seravek-MediumItalic', family='Seravek', size=24, traits='Italic', weight=7) at 0x10a1b4b50
 825 Font(name='Seravek-Bold', family='Seravek', size=12, traits='Bold', weight=9) at 0x10a180a90
 826+Font(name='Seravek-Bold', family='Seravek', size=24, traits='Bold', weight=9) at 0x10a1b4510
 827 Font(name='Seravek-BoldItalic', family='Seravek', size=12, traits='Bold Italic', weight=9) at 0x10a1b4610
 828+Font(name='Seravek-BoldItalic', family='Seravek', size=24, traits='Bold Italic', weight=9) at 0x10a1af650
 --- Family 'Shree Devanagari 714'
 829 Font(name='ShreeDev0714', family='Shree Devanagari 714', size=12, weight=5) at 0x10dcb2590
 830+Font(name='ShreeDev0714', family='Shree Devanagari 714', size=24, weight=5) at 0x10dcb2150
 831 Font(name='ShreeDev0714-Italic', family='Shree Devanagari 714', size=12, traits='Italic', weight=5) at 0x10a18cf90
 832+Font(name='ShreeDev0714-Italic', family='Shree Devanagari 714', size=24, traits='Italic', weight=5) at 0x10dcddb90
 833 Font(name='ShreeDev0714-Bold', family='Shree Devanagari 714', size=12, traits='Bold', weight=9) at 0x10dcb2bd0
 834+Font(name='ShreeDev0714-Bold', family='Shree Devanagari 714', size=24, traits='Bold', weight=9) at 0x10dcd30d0
 835 Font(name='ShreeDev0714-BoldItalic', family='Shree Devanagari 714', size=12, traits='Bold Italic', weight=9) at 0x10dcdd110
 836+Font(name='ShreeDev0714-BoldItalic', family='Shree Devanagari 714', size=24, traits='Bold Italic', weight=9) at 0x10dcd3d90
 --- Family 'SignPainter'
 837 Font(name='SignPainter-HouseScript', family='SignPainter', size=12, traits='Condensed', weight=5) at 0x117fa3150
 838+Font(name='SignPainter-HouseScript', family='SignPainter', size=24, traits='Condensed', weight=5) at 0x10dcc8610
 839 Font(name='SignPainter-HouseScriptSemibold', family='SignPainter', size=12, traits='Bold Condensed', weight=8) at 0x10dcc8d50
 840+Font(name='SignPainter-HouseScriptSemibold', family='SignPainter', size=24, traits='Bold Condensed', weight=8) at 0x10dcc8ed0
 --- Family 'Silom'
 841 Font(name='Silom', family='Silom', size=12, traits='Bold', weight=9) at 0x117fafbd0
 842+Font(name='Silom', family='Silom', size=24, traits='Bold', weight=9) at 0x1188e4990
 --- Family 'Sinhala MN'
 843 Font(name='SinhalaMN', family='Sinhala MN', size=12, weight=5) at 0x118908350
 844+Font(name='SinhalaMN', family='Sinhala MN', size=24, weight=5) at 0x1188e4990
 845 Font(name='SinhalaMN-Bold', family='Sinhala MN', size=12, traits='Bold', weight=9) at 0x117fc4150
 846+Font(name='SinhalaMN-Bold', family='Sinhala MN', size=24, traits='Bold', weight=9) at 0x1188d9350
 --- Family 'Sinhala Sangam MN'
 847 Font(name='SinhalaSangamMN', family='Sinhala Sangam MN', size=12, weight=5) at 0x1188fe050
 848+Font(name='SinhalaSangamMN', family='Sinhala Sangam MN', size=24, weight=5) at 0x1188fecd0
 849 Font(name='SinhalaSangamMN-Bold', family='Sinhala Sangam MN', size=12, traits='Bold', weight=9) at 0x1188f2410
 850+Font(name='SinhalaSangamMN-Bold', family='Sinhala Sangam MN', size=24, traits='Bold', weight=9) at 0x118903150
 --- Family 'Skia'
 851 Font(name='Skia-Regular', family='Skia', size=12, weight=5) at 0x1192f88d0
 852+Font(name='Skia-Regular', family='Skia', size=24, weight=5) at 0x1192f8590
 853 Font(name='Skia-Regular_Light', family='Skia', size=12, weight=3) at 0x1192df550
 854+Font(name='Skia-Regular_Light', family='Skia', size=24, weight=3) at 0x1192ed210
 855 Font(name='Skia-Regular_Bold', family='Skia', size=12, traits='Bold', weight=9) at 0x1192f8490
 856+Font(name='Skia-Regular_Bold', family='Skia', size=24, traits='Bold', weight=9) at 0x1192d6390
 857 Font(name='Skia-Regular_Black', family='Skia', size=12, traits='Bold', weight=11) at 0x1192d64d0
 858+Font(name='Skia-Regular_Black', family='Skia', size=24, traits='Bold', weight=11) at 0x11ea0ee90
 859 Font(name='Skia-Regular', family='Skia', size=12, weight=5) at 0x11ea0eb50
 860+Font(name='Skia-Regular', family='Skia', size=24, weight=5) at 0x11ea0ee90
 861 Font(name='Skia-Regular_Light', family='Skia', size=12, weight=3) at 0x11ea0e210
 862+Font(name='Skia-Regular_Light', family='Skia', size=24, weight=3) at 0x11ea0ee90
 863 Font(name='Skia-Regular_Black', family='Skia', size=12, traits='Bold', weight=11) at 0x11f781110
 864+Font(name='Skia-Regular_Black', family='Skia', size=24, traits='Bold', weight=11) at 0x11f781450
 865 Font(name='Skia-Regular', family='Skia', size=12, weight=5) at 0x11ea0ef50
 866+Font(name='Skia-Regular', family='Skia', size=24, weight=5) at 0x11f781490
 867 Font(name='Skia-Regular', family='Skia', size=12, weight=5) at 0x11f781190
 868+Font(name='Skia-Regular', family='Skia', size=24, weight=5) at 0x11f781710
 869 Font(name='Skia-Regular_Bold', family='Skia', size=12, traits='Bold', weight=9) at 0x11f7815d0
 870+Font(name='Skia-Regular_Bold', family='Skia', size=24, traits='Bold', weight=9) at 0x11f7818d0
 --- Family 'Snell Roundhand'
 871 Font(name='SnellRoundhand', family='Snell Roundhand', size=12, traits='Italic', weight=5) at 0x11f781a10
 872+Font(name='SnellRoundhand', family='Snell Roundhand', size=24, traits='Italic', weight=5) at 0x11f781b10
 873 Font(name='SnellRoundhand-Bold', family='Snell Roundhand', size=12, traits='Bold Italic', weight=9) at 0x11f781910
 874+Font(name='SnellRoundhand-Bold', family='Snell Roundhand', size=24, traits='Bold Italic', weight=9) at 0x11f781c90
 875 Font(name='SnellRoundhand-Black', family='Snell Roundhand', size=12, traits='Bold Italic', weight=11) at 0x11f781b10
 876+Font(name='SnellRoundhand-Black', family='Snell Roundhand', size=24, traits='Bold Italic', weight=11) at 0x11f781c50
 --- Family 'Songti SC'
 877 Font(name='STSongti-SC-Regular', family='Songti SC', size=12, weight=5) at 0x10538c0d0
 878+Font(name='STSongti-SC-Regular', family='Songti SC', size=24, weight=5) at 0x11f781c90
 879 Font(name='STSongti-SC-Light', family='Songti SC', size=12, weight=3) at 0x11f781ed0
 880+Font(name='STSongti-SC-Light', family='Songti SC', size=24, weight=3) at 0x10538c290
 881 Font(name='STSongti-SC-Bold', family='Songti SC', size=12, traits='Bold', weight=9) at 0x10538c210
 882+Font(name='STSongti-SC-Bold', family='Songti SC', size=24, traits='Bold', weight=9) at 0x10538c550
 883 Font(name='STSongti-SC-Black', family='Songti SC', size=12, traits='Bold', weight=11) at 0x10538c2d0
 884+Font(name='STSongti-SC-Black', family='Songti SC', size=24, traits='Bold', weight=11) at 0x10538c750
 --- Family 'Songti TC'
 885 Font(name='STSongti-TC-Regular', family='Songti TC', size=12, weight=5) at 0x10538c8d0
 886+Font(name='STSongti-TC-Regular', family='Songti TC', size=24, weight=5) at 0x10538ca90
 887 Font(name='STSongti-TC-Light', family='Songti TC', size=12, weight=3) at 0x10538c710
 888+Font(name='STSongti-TC-Light', family='Songti TC', size=24, weight=3) at 0x10538c9d0
 889 Font(name='STSongti-TC-Bold', family='Songti TC', size=12, traits='Bold', weight=9) at 0x10538c750
 890+Font(name='STSongti-TC-Bold', family='Songti TC', size=24, traits='Bold', weight=9) at 0x10538cd90
 --- Family 'STIXGeneral'
 891 Font(name='STIXGeneral-Regular', family='STIXGeneral', size=12, weight=5) at 0x10538ca90
 892+Font(name='STIXGeneral-Regular', family='STIXGeneral', size=24, weight=5) at 0x11f798110
 893 Font(name='STIXGeneral-Italic', family='STIXGeneral', size=12, traits='Italic', weight=5) at 0x10538cd50
 894+Font(name='STIXGeneral-Italic', family='STIXGeneral', size=24, traits='Italic', weight=5) at 0x11f798290
 895 Font(name='STIXGeneral-Bold', family='STIXGeneral', size=12, traits='Bold', weight=9) at 0x11f798090
 896+Font(name='STIXGeneral-Bold', family='STIXGeneral', size=24, traits='Bold', weight=9) at 0x11f798490
 897 Font(name='STIXGeneral-BoldItalic', family='STIXGeneral', size=12, traits='Bold Italic', weight=9) at 0x11f798550
 898+Font(name='STIXGeneral-BoldItalic', family='STIXGeneral', size=24, traits='Bold Italic', weight=9) at 0x11f798310
 --- Family 'STIXIntegralsD'
 899 Font(name='STIXIntegralsD-Regular', family='STIXIntegralsD', size=12, weight=5) at 0x11f798910
 900+Font(name='STIXIntegralsD-Regular', family='STIXIntegralsD', size=24, weight=5) at 0x11f7989d0
 901 Font(name='STIXIntegralsD-Bold', family='STIXIntegralsD', size=12, traits='Bold', weight=9) at 0x11f798610
 902+Font(name='STIXIntegralsD-Bold', family='STIXIntegralsD', size=24, traits='Bold', weight=9) at 0x11f798890
 --- Family 'STIXIntegralsSm'
 903 Font(name='STIXIntegralsSm-Regular', family='STIXIntegralsSm', size=12, weight=5) at 0x11f798d90
 904+Font(name='STIXIntegralsSm-Regular', family='STIXIntegralsSm', size=24, weight=5) at 0x11f798c50
 905 Font(name='STIXIntegralsSm-Bold', family='STIXIntegralsSm', size=12, traits='Bold', weight=9) at 0x11f798f90
 906+Font(name='STIXIntegralsSm-Bold', family='STIXIntegralsSm', size=24, traits='Bold', weight=9) at 0x11f798e90
 --- Family 'STIXIntegralsUp'
 907 Font(name='STIXIntegralsUp-Regular', family='STIXIntegralsUp', size=12, weight=5) at 0x11f7a52d0
 908+Font(name='STIXIntegralsUp-Regular', family='STIXIntegralsUp', size=24, weight=5) at 0x11f798f10
 909 Font(name='STIXIntegralsUp-Bold', family='STIXIntegralsUp', size=12, traits='Bold', weight=9) at 0x11f7a5390
 910+Font(name='STIXIntegralsUp-Bold', family='STIXIntegralsUp', size=24, traits='Bold', weight=9) at 0x11f7a5250
 --- Family 'STIXIntegralsUpD'
 911 Font(name='STIXIntegralsUpD-Regular', family='STIXIntegralsUpD', size=12, weight=5) at 0x11f7a5790
 912+Font(name='STIXIntegralsUpD-Regular', family='STIXIntegralsUpD', size=24, weight=5) at 0x11f7a5850
 913 Font(name='STIXIntegralsUpD-Bold', family='STIXIntegralsUpD', size=12, traits='Bold', weight=9) at 0x11f7a5250
 914+Font(name='STIXIntegralsUpD-Bold', family='STIXIntegralsUpD', size=24, traits='Bold', weight=9) at 0x11f7a5710
 --- Family 'STIXIntegralsUpSm'
 915 Font(name='STIXIntegralsUpSm-Regular', family='STIXIntegralsUpSm', size=12, weight=5) at 0x11f7a5c50
 916+Font(name='STIXIntegralsUpSm-Regular', family='STIXIntegralsUpSm', size=24, weight=5) at 0x11f7a5d10
 917 Font(name='STIXIntegralsUpSm-Bold', family='STIXIntegralsUpSm', size=12, traits='Bold', weight=9) at 0x11f7a5710
 918+Font(name='STIXIntegralsUpSm-Bold', family='STIXIntegralsUpSm', size=24, traits='Bold', weight=9) at 0x11f7a5bd0
 --- Family 'STIXNonUnicode'
 919 Font(name='STIXNonUnicode-Regular', family='STIXNonUnicode', size=12, weight=5) at 0x11f7b0150
 920+Font(name='STIXNonUnicode-Regular', family='STIXNonUnicode', size=24, weight=5) at 0x11f7a5e10
 921 Font(name='STIXNonUnicode-Italic', family='STIXNonUnicode', size=12, traits='Italic', weight=5) at 0x11f7a5e90
 922+Font(name='STIXNonUnicode-Italic', family='STIXNonUnicode', size=24, traits='Italic', weight=5) at 0x11f7b0050
 923 Font(name='STIXNonUnicode-Bold', family='STIXNonUnicode', size=12, traits='Bold', weight=9) at 0x11f7b0190
 924+Font(name='STIXNonUnicode-Bold', family='STIXNonUnicode', size=24, traits='Bold', weight=9) at 0x11f7b03d0
 925 Font(name='STIXNonUnicode-BoldItalic', family='STIXNonUnicode', size=12, traits='Bold Italic', weight=9) at 0x11f7b0550
 926+Font(name='STIXNonUnicode-BoldItalic', family='STIXNonUnicode', size=24, traits='Bold Italic', weight=9) at 0x11f7b0210
 --- Family 'STIXSizeFiveSym'
 927 Font(name='STIXSizeFiveSym-Regular', family='STIXSizeFiveSym', size=12, weight=5) at 0x11f7b0990
 928+Font(name='STIXSizeFiveSym-Regular', family='STIXSizeFiveSym', size=24, weight=5) at 0x11f7b0a50
 --- Family 'STIXSizeFourSym'
 929 Font(name='STIXSizeFourSym-Regular', family='STIXSizeFourSym', size=12, weight=5) at 0x11f7b0c50
 930+Font(name='STIXSizeFourSym-Regular', family='STIXSizeFourSym', size=24, weight=5) at 0x11f7b0d10
 931 Font(name='STIXSizeFourSym-Bold', family='STIXSizeFourSym', size=12, traits='Bold', weight=9) at 0x11f7b0a50
 932+Font(name='STIXSizeFourSym-Bold', family='STIXSizeFourSym', size=24, traits='Bold', weight=9) at 0x11f7b0bd0
 --- Family 'STIXSizeOneSym'
 933 Font(name='STIXSizeOneSym-Regular', family='STIXSizeOneSym', size=12, weight=5) at 0x1239cd150
 934+Font(name='STIXSizeOneSym-Regular', family='STIXSizeOneSym', size=24, weight=5) at 0x11f7b0990
 935 Font(name='STIXSizeOneSym-Bold', family='STIXSizeOneSym', size=12, traits='Bold', weight=9) at 0x11f7b0750
 936+Font(name='STIXSizeOneSym-Bold', family='STIXSizeOneSym', size=24, traits='Bold', weight=9) at 0x1239cd110
 --- Family 'STIXSizeThreeSym'
 937 Font(name='STIXSizeThreeSym-Regular', family='STIXSizeThreeSym', size=12, weight=5) at 0x1239cd5d0
 938+Font(name='STIXSizeThreeSym-Regular', family='STIXSizeThreeSym', size=24, weight=5) at 0x1239cd490
 939 Font(name='STIXSizeThreeSym-Bold', family='STIXSizeThreeSym', size=12, traits='Bold', weight=9) at 0x1239cd110
 940+Font(name='STIXSizeThreeSym-Bold', family='STIXSizeThreeSym', size=24, traits='Bold', weight=9) at 0x1239cd6d0
 --- Family 'STIXSizeTwoSym'
 941 Font(name='STIXSizeTwoSym-Regular', family='STIXSizeTwoSym', size=12, weight=5) at 0x1239cdad0
 942+Font(name='STIXSizeTwoSym-Regular', family='STIXSizeTwoSym', size=24, weight=5) at 0x1239cdb90
 943 Font(name='STIXSizeTwoSym-Bold', family='STIXSizeTwoSym', size=12, traits='Bold', weight=9) at 0x1239cd850
 944+Font(name='STIXSizeTwoSym-Bold', family='STIXSizeTwoSym', size=24, traits='Bold', weight=9) at 0x1239cda50
 --- Family 'STIXVariants'
 945 Font(name='STIXVariants-Regular', family='STIXVariants', size=12, weight=5) at 0x1239cdf50
 946+Font(name='STIXVariants-Regular', family='STIXVariants', size=24, weight=5) at 0x1239cdf90
 947 Font(name='STIXVariants-Bold', family='STIXVariants', size=12, traits='Bold', weight=9) at 0x1239cd610
 948+Font(name='STIXVariants-Bold', family='STIXVariants', size=24, traits='Bold', weight=9) at 0x1239cded0
 --- Family 'Stone Sans ITC TT'
 949 Font(name='StoneSansITCTT-Bold', family='Stone Sans ITC TT', size=12, traits='Bold SansSerif', weight=9) at 0x1239d7310
 950+Font(name='StoneSansITCTT-Bold', family='Stone Sans ITC TT', size=24, traits='Bold SansSerif', weight=9) at 0x1239d7350
 --- Family 'Stone Sans Sem ITC TT'
 951 Font(name='StoneSansITCTT-Semi', family='Stone Sans Sem ITC TT', size=12, traits='Bold Italic SansSerif', weight=8) at 0x1239d7790
 952+Font(name='StoneSansITCTT-Semi', family='Stone Sans Sem ITC TT', size=24, traits='Bold Italic SansSerif', weight=8) at 0x1239d7350
 953 Font(name='StoneSansITCTT-Semi', family='Stone Sans Sem ITC TT', size=12, traits='Bold Italic SansSerif', weight=8) at 0x1239d7590
 954+Font(name='StoneSansITCTT-Semi', family='Stone Sans Sem ITC TT', size=24, traits='Bold Italic SansSerif', weight=8) at 0x1239d7a10
 --- Family 'STSong'
 955 Font(name='STSong', family='STSong', size=12, weight=5) at 0x1239d79d0
 956+Font(name='STSong', family='STSong', size=24, weight=5) at 0x1239d7a10
 --- Family 'Sukhumvit Set'
 957 Font(name='SukhumvitSet-Text', family='Sukhumvit Set', size=12, weight=5) at 0x1239d7d90
 958+Font(name='SukhumvitSet-Text', family='Sukhumvit Set', size=24, weight=5) at 0x1239d7ed0
 959 Font(name='SukhumvitSet-Light', family='Sukhumvit Set', size=12, weight=3) at 0x1239d79d0
 960+Font(name='SukhumvitSet-Light', family='Sukhumvit Set', size=24, weight=3) at 0x1239d7e10
 961 Font(name='SukhumvitSet-Medium', family='Sukhumvit Set', size=12, weight=6) at 0x1239d7d90
 962+Font(name='SukhumvitSet-Medium', family='Sukhumvit Set', size=24, weight=6) at 0x11f79c050
 963 Font(name='SukhumvitSet-Bold', family='Sukhumvit Set', size=12, traits='Bold', weight=9) at 0x1239d7f10
 964+Font(name='SukhumvitSet-Bold', family='Sukhumvit Set', size=24, traits='Bold', weight=9) at 0x11f79c210
 965 Font(name='SukhumvitSet-Bold', family='Sukhumvit Set', size=12, traits='Bold', weight=9) at 0x11f79c110
 966+Font(name='SukhumvitSet-Bold', family='Sukhumvit Set', size=24, traits='Bold', weight=9) at 0x11f79c610
 967 Font(name='SukhumvitSet-Light', family='Sukhumvit Set', size=12, weight=3) at 0x11f79c490
 968+Font(name='SukhumvitSet-Light', family='Sukhumvit Set', size=24, weight=3) at 0x11f79c610
 --- Family 'Superclarendon'
 969 Font(name='Superclarendon-Regular', family='Superclarendon', size=12, weight=5) at 0x11f79c910
 970+Font(name='Superclarendon-Regular', family='Superclarendon', size=24, weight=5) at 0x11f79c7d0
 971 Font(name='Superclarendon-Italic', family='Superclarendon', size=12, traits='Italic', weight=5) at 0x11f79c610
 972+Font(name='Superclarendon-Italic', family='Superclarendon', size=24, traits='Italic', weight=5) at 0x11f79ca10
 973 Font(name='Superclarendon-Light', family='Superclarendon', size=12, weight=3) at 0x11f79cc50
 974+Font(name='Superclarendon-Light', family='Superclarendon', size=24, weight=3) at 0x11f79cd10
 975 Font(name='Superclarendon-LightItalic', family='Superclarendon', size=12, traits='Italic', weight=3) at 0x11f79cb10
 976+Font(name='Superclarendon-LightItalic', family='Superclarendon', size=24, traits='Italic', weight=3) at 0x11f79cdd0
 977 Font(name='Superclarendon-Bold', family='Superclarendon', size=12, traits='Bold', weight=9) at 0x11f79cc50
 978+Font(name='Superclarendon-Bold', family='Superclarendon', size=24, traits='Bold', weight=9) at 0x11f79ce90
 979 Font(name='Superclarendon-BoldItalic', family='Superclarendon', size=12, traits='Bold Italic', weight=9) at 0x11f79cbd0
 980+Font(name='Superclarendon-BoldItalic', family='Superclarendon', size=24, traits='Bold Italic', weight=9) at 0x1239e5110
 981 Font(name='Superclarendon-Black', family='Superclarendon', size=12, traits='Bold', weight=11) at 0x1239e52d0
 982+Font(name='Superclarendon-Black', family='Superclarendon', size=24, traits='Bold', weight=11) at 0x1239e51d0
 983 Font(name='Superclarendon-BlackItalic', family='Superclarendon', size=12, traits='Bold Italic', weight=11) at 0x1239e5590
 984+Font(name='Superclarendon-BlackItalic', family='Superclarendon', size=24, traits='Bold Italic', weight=11) at 0x1239e5650
 --- Family 'Symbol'
 985 Font(name='Symbol', family='Symbol', size=12, weight=5) at 0x1239e5710
 986+Font(name='Symbol', family='Symbol', size=24, weight=5) at 0x1239e5650
 --- Family 'Synchro LET'
 987 Font(name='SynchroLET', family='Synchro LET', size=12, traits='Bold', weight=9) at 0x1239e59d0
 988+Font(name='SynchroLET', family='Synchro LET', size=24, traits='Bold', weight=9) at 0x1239e5ad0
 --- Family 'Tahoma'
 989 Font(name='Tahoma', family='Tahoma', size=12, weight=5) at 0x1239e5a10
 990+Font(name='Tahoma', family='Tahoma', size=24, weight=5) at 0x1239e5ad0
 991 Font(name='Tahoma-Bold', family='Tahoma', size=12, traits='Bold', weight=9) at 0x1239e5b90
 992+Font(name='Tahoma-Bold', family='Tahoma', size=24, traits='Bold', weight=9) at 0x1239e5e50
 --- Family 'Tamil MN'
 993 Font(name='TamilMN', family='Tamil MN', size=12, weight=5) at 0x1239ee0d0
 994+Font(name='TamilMN', family='Tamil MN', size=24, weight=5) at 0x1239ee290
 995 Font(name='TamilMN-Bold', family='Tamil MN', size=12, traits='Bold', weight=9) at 0x1239e5f90
 996+Font(name='TamilMN-Bold', family='Tamil MN', size=24, traits='Bold', weight=9) at 0x1239ee1d0
 --- Family 'Tamil Sangam MN'
 997 Font(name='TamilSangamMN', family='Tamil Sangam MN', size=12, weight=5) at 0x1239ee590
 998+Font(name='TamilSangamMN', family='Tamil Sangam MN', size=24, weight=5) at 0x1239ee750
 999 Font(name='TamilSangamMN-Bold', family='Tamil Sangam MN', size=12, traits='Bold', weight=9) at 0x1239ee490
1000+Font(name='TamilSangamMN-Bold', family='Tamil Sangam MN', size=24, traits='Bold', weight=9) at 0x1239ee8d0
 --- Family 'Telugu MN'
1001 Font(name='TeluguMN', family='Telugu MN', size=12, weight=5) at 0x1239eea50
1002+Font(name='TeluguMN', family='Telugu MN', size=24, weight=5) at 0x1239ee8d0
1003 Font(name='TeluguMN-Bold', family='Telugu MN', size=12, traits='Bold', weight=9) at 0x1239ee890
1004+Font(name='TeluguMN-Bold', family='Telugu MN', size=24, traits='Bold', weight=9) at 0x1239eed90
 --- Family 'Telugu Sangam MN'
1005 Font(name='TeluguSangamMN', family='Telugu Sangam MN', size=12, weight=5) at 0x1239eef50
1006+Font(name='TeluguSangamMN', family='Telugu Sangam MN', size=24, weight=5) at 0x123a05110
1007 Font(name='TeluguSangamMN-Bold', family='Telugu Sangam MN', size=12, traits='Bold', weight=9) at 0x1239eed50
1008+Font(name='TeluguSangamMN-Bold', family='Telugu Sangam MN', size=24, traits='Bold', weight=9) at 0x123a05290
 --- Family 'Thonburi'
1009 Font(name='Thonburi', family='Thonburi', size=12, weight=5) at 0x123a05090
1010+Font(name='Thonburi', family='Thonburi', size=24, weight=5) at 0x123a05290
1011 Font(name='Thonburi-Light', family='Thonburi', size=12, weight=3) at 0x123a05250
1012+Font(name='Thonburi-Light', family='Thonburi', size=24, weight=3) at 0x123a05450
1013 Font(name='Thonburi-Bold', family='Thonburi', size=12, traits='Bold', weight=9) at 0x123a05510
1014+Font(name='Thonburi-Bold', family='Thonburi', size=24, traits='Bold', weight=9) at 0x123a05890
 --- Family 'Times'
1015 Font(name='Times-Roman', family='Times', size=12, weight=5) at 0x123a05a10
1016+Font(name='Times-Roman', family='Times', size=24, weight=5) at 0x123a05890
1017 Font(name='Times-Italic', family='Times', size=12, traits='Italic', weight=5) at 0x123a05850
1018+Font(name='Times-Italic', family='Times', size=24, traits='Italic', weight=5) at 0x123a05b10
1019 Font(name='Times-Bold', family='Times', size=12, traits='Bold', weight=9) at 0x123a05bd0
1020+Font(name='Times-Bold', family='Times', size=24, traits='Bold', weight=9) at 0x123a05e10
1021 Font(name='Times-BoldItalic', family='Times', size=12, traits='Bold Italic', weight=9) at 0x123a05d50
1022+Font(name='Times-BoldItalic', family='Times', size=24, traits='Bold Italic', weight=9) at 0x1243bd050
 --- Family 'Times New Roman'
1023 Font(name='TimesNewRomanPSMT', family='Times New Roman', size=12, weight=5) at 0x1243bd310
1024+Font(name='TimesNewRomanPSMT', family='Times New Roman', size=24, weight=5) at 0x1243bd090
1025 Font(name='TimesNewRomanPS-ItalicMT', family='Times New Roman', size=12, traits='Italic', weight=5) at 0x1243bd490
1026+Font(name='TimesNewRomanPS-ItalicMT', family='Times New Roman', size=24, traits='Italic', weight=5) at 0x1243bd4d0
1027 Font(name='TimesNewRomanPS-BoldMT', family='Times New Roman', size=12, traits='Bold', weight=9) at 0x1243bd6d0
1028+Font(name='TimesNewRomanPS-BoldMT', family='Times New Roman', size=24, traits='Bold', weight=9) at 0x1243bd150
1029 Font(name='TimesNewRomanPS-BoldItalicMT', family='Times New Roman', size=12, traits='Bold Italic', weight=9) at 0x1243bd250
1030+Font(name='TimesNewRomanPS-BoldItalicMT', family='Times New Roman', size=24, traits='Bold Italic', weight=9) at 0x1243bd890
 --- Family 'Trattatello'
1031 Font(name='Trattatello', family='Trattatello', size=12, weight=5) at 0x1243bd650
1032+Font(name='Trattatello', family='Trattatello', size=24, weight=5) at 0x1243bda50
 --- Family 'Trebuchet MS'
1033 Font(name='TrebuchetMS', family='Trebuchet MS', size=12, weight=5) at 0x1243bdc50
1034+Font(name='TrebuchetMS', family='Trebuchet MS', size=24, weight=5) at 0x1243bda90
1035 Font(name='TrebuchetMS-Italic', family='Trebuchet MS', size=12, traits='Italic', weight=5) at 0x1243bd890
1036+Font(name='TrebuchetMS-Italic', family='Trebuchet MS', size=24, traits='Italic', weight=5) at 0x1243bde10
1037 Font(name='TrebuchetMS-Bold', family='Trebuchet MS', size=12, traits='Bold', weight=9) at 0x1243bda50
1038+Font(name='TrebuchetMS-Bold', family='Trebuchet MS', size=24, traits='Bold', weight=9) at 0x1243bdd10
1039 Font(name='Trebuchet-BoldItalic', family='Trebuchet MS', size=12, traits='Bold Italic', weight=9) at 0x1243bde90
1040+Font(name='Trebuchet-BoldItalic', family='Trebuchet MS', size=24, traits='Bold Italic', weight=9) at 0x1243be190
 --- Family 'Type Embellishments One LET'
1041 Font(name='TypeEmbellishmentsOneLetPlain', family='Type Embellishments One LET', size=12, weight=5) at 0x1243be4d0
1042+Font(name='TypeEmbellishmentsOneLetPlain', family='Type Embellishments One LET', size=24, weight=5) at 0x1243be190
 --- Family 'Verdana'
1043 Font(name='Verdana', family='Verdana', size=12, weight=5) at 0x1243be0d0
1044+Font(name='Verdana', family='Verdana', size=24, weight=5) at 0x1243be190
1045 Font(name='Verdana-Italic', family='Verdana', size=12, traits='Italic', weight=5) at 0x1243be490
1046+Font(name='Verdana-Italic', family='Verdana', size=24, traits='Italic', weight=5) at 0x1243be910
1047 Font(name='Verdana-Bold', family='Verdana', size=12, traits='Bold', weight=9) at 0x1243be650
1048+Font(name='Verdana-Bold', family='Verdana', size=24, traits='Bold', weight=9) at 0x1243be9d0
1049 Font(name='Verdana-BoldItalic', family='Verdana', size=12, traits='Bold Italic', weight=9) at 0x1243be750
1050+Font(name='Verdana-BoldItalic', family='Verdana', size=24, traits='Bold Italic', weight=9) at 0x1243bebd0
 --- Family 'Waseem'
1051 Font(name='Waseem', family='Waseem', size=12, weight=5) at 0x1243beb10
1052+Font(name='Waseem', family='Waseem', size=24, weight=5) at 0x1243bebd0
1053 Font(name='WaseemLight', family='Waseem', size=12, weight=3) at 0x1243becd0
1054+Font(name='WaseemLight', family='Waseem', size=24, weight=3) at 0x1243d00d0
 --- Family 'Webdings'
1055 Font(name='Webdings', family='Webdings', size=12, weight=5) at 0x1243d0110
1056+Font(name='Webdings', family='Webdings', size=24, weight=5) at 0x1243d00d0
 --- Family 'Wingdings'
1057 Font(name='Wingdings-Regular', family='Wingdings', size=12, weight=5) at 0x1243d04d0
1058+Font(name='Wingdings-Regular', family='Wingdings', size=24, weight=5) at 0x1243d0690
 --- Family 'Wingdings 2'
1059 Font(name='Wingdings2', family='Wingdings 2', size=12, weight=5) at 0x1243d0810
1060+Font(name='Wingdings2', family='Wingdings 2', size=24, weight=5) at 0x1243d00d0
 --- Family 'Wingdings 3'
1061 Font(name='Wingdings3', family='Wingdings 3', size=12, weight=5) at 0x1243d0a10
1062+Font(name='Wingdings3', family='Wingdings 3', size=24, weight=5) at 0x1243d0690
 --- Family 'Zapf Dingbats'
1063 Font(name='ZapfDingbatsITC', family='Zapf Dingbats', size=12, weight=5) at 0x1243d0c10
1064+Font(name='ZapfDingbatsITC', family='Zapf Dingbats', size=24, weight=5) at 0x1243d00d0
 --- Family 'Zapfino'
1065 Font(name='Zapfino', family='Zapfino', size=12, weight=5) at 0x1243d0cd0
1066+Font(name='Zapfino', family='Zapfino', size=24, weight=5) at 0x1243d00d0
 --- Family 'Apple Braille'
1067 Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=12, traits='MonoSpace', weight=5) at 0x1243dd190
1068+Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=24, traits='MonoSpace', weight=5) at 0x1243dd150
1069 Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=12, traits='MonoSpace', weight=5) at 0x1243d0e90
1070+Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=24, traits='MonoSpace', weight=5) at 0x1243dd490
1071 Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=12, traits='MonoSpace', weight=5) at 0x1243dd6d0
1072+Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=24, traits='MonoSpace', weight=5) at 0x1243dd250
1073 Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=12, traits='MonoSpace', weight=5) at 0x1243dd890
1074+Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=24, traits='MonoSpace', weight=5) at 0x1243dd1d0
1075 Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=12, traits='MonoSpace', weight=5) at 0x1243dd9d0
1076+Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=24, traits='MonoSpace', weight=5) at 0x1243dd510
 --- Family 'Apple Chancery'
1077 Font(name='Apple-Chancery', family='Apple Chancery', size=12, weight=5) at 0x1243dda50
1078+Font(name='Apple-Chancery', family='Apple Chancery', size=24, weight=5) at 0x1243ddb10
 --- Family 'Apple Color Emoji'
1079 Font(name='AppleColorEmoji', family='Apple Color Emoji', size=12, traits='MonoSpace', weight=5) at 0x1243ddc10
1080+Font(name='AppleColorEmoji', family='Apple Color Emoji', size=24, traits='MonoSpace', weight=5) at 0x1243ddd10
 --- Family 'Apple SD Gothic Neo'
1081 Font(name='AppleSDGothicNeo-Regular', family='Apple SD Gothic Neo', size=12, weight=5) at 0x1243e4090
1082+Font(name='AppleSDGothicNeo-Regular', family='Apple SD Gothic Neo', size=24, weight=5) at 0x1243e4050
1083 Font(name='AppleSDGothicNeo-Thin', family='Apple SD Gothic Neo', size=12, weight=3) at 0x1243dddd0
1084+Font(name='AppleSDGothicNeo-Thin', family='Apple SD Gothic Neo', size=24, weight=3) at 0x1243e4050
1085 Font(name='AppleSDGothicNeo-Thin', family='Apple SD Gothic Neo', size=12, weight=3) at 0x1243e4590
1086+Font(name='AppleSDGothicNeo-Thin', family='Apple SD Gothic Neo', size=24, weight=3) at 0x1243e4390
1087 Font(name='AppleSDGothicNeo-Thin', family='Apple SD Gothic Neo', size=12, weight=3) at 0x1243dddd0
1088+Font(name='AppleSDGothicNeo-Thin', family='Apple SD Gothic Neo', size=24, weight=3) at 0x1243e4110
1089 Font(name='AppleSDGothicNeo-Medium', family='Apple SD Gothic Neo', size=12, weight=6) at 0x1243e4350
1090+Font(name='AppleSDGothicNeo-Medium', family='Apple SD Gothic Neo', size=24, weight=6) at 0x1243e4110
1091 Font(name='AppleSDGothicNeo-Bold', family='Apple SD Gothic Neo', size=12, traits='Bold', weight=9) at 0x1243e4810
1092+Font(name='AppleSDGothicNeo-Bold', family='Apple SD Gothic Neo', size=24, traits='Bold', weight=9) at 0x1243e4890
1093 Font(name='AppleSDGothicNeo-Bold', family='Apple SD Gothic Neo', size=12, traits='Bold', weight=9) at 0x1243e4b10
1094+Font(name='AppleSDGothicNeo-Bold', family='Apple SD Gothic Neo', size=24, traits='Bold', weight=9) at 0x1243e4590
1095 Font(name='AppleSDGothicNeo-ExtraBold', family='Apple SD Gothic Neo', size=12, traits='Bold', weight=10) at 0x1243e4b90
1096+Font(name='AppleSDGothicNeo-ExtraBold', family='Apple SD Gothic Neo', size=24, traits='Bold', weight=10) at 0x1243e4bd0
1097 Font(name='AppleSDGothicNeo-ExtraBold', family='Apple SD Gothic Neo', size=12, traits='Bold', weight=10) at 0x1243e4ed0
1098+Font(name='AppleSDGothicNeo-ExtraBold', family='Apple SD Gothic Neo', size=24, traits='Bold', weight=10) at 0x1243e49d0
 --- Family 'Apple Symbols'
1099 Font(name='AppleSymbols', family='Apple Symbols', size=12, weight=5) at 0x1243e4e90
1100+Font(name='AppleSymbols', family='Apple Symbols', size=24, weight=5) at 0x1243e4f90
 --- Family 'AppleGothic'
1101 Font(name='AppleGothic', family='AppleGothic', size=12, weight=5) at 0x1243ea090
1102+Font(name='AppleGothic', family='AppleGothic', size=24, weight=5) at 0x1243ea150
 --- Family 'AppleMyungjo'
1103 Font(name='AppleMyungjo', family='AppleMyungjo', size=12, weight=5) at 0x1243ea0d0
1104+Font(name='AppleMyungjo', family='AppleMyungjo', size=24, weight=5) at 0x1243ea310
'''
del _
