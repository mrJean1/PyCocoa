
# -*- coding: utf-8 -*-

# List all Fonts.

import run as __  # PYCHOK sys.path
from pycocoa import FontError, fontfamilies, fontsof

__version__ = '23.01.18'

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
   1 Font(name='AcademyEngravedLetPlain', family='Academy Engraved LET', size=12, weight=5) at 0x101f4f290
   2+Font(name='AcademyEngravedLetPlain', family='Academy Engraved LET', size=24, weight=5) at 0x101f4f6d0
 --- Family 'Al Bayan'
   3 Font(name='AlBayan', family='Al Bayan', size=12, weight=5) at 0x101f4f4d0
   4+Font(name='AlBayan', family='Al Bayan', size=24, weight=5) at 0x101f4f6d0
   5 Font(name='AlBayan-Bold', family='Al Bayan', size=12, traits='Bold', weight=9) at 0x101f4fa10
   6+Font(name='AlBayan-Bold', family='Al Bayan', size=24, traits='Bold', weight=9) at 0x101f4fb90
 --- Family 'Al Nile'
   7 Font(name='AlNile', family='Al Nile', size=12, weight=5) at 0x101f4f4d0
   8+Font(name='AlNile', family='Al Nile', size=24, weight=5) at 0x101f4fb90
   9 Font(name='AlNile-Bold', family='Al Nile', size=12, traits='Bold', weight=9) at 0x101f4ff10
  10+Font(name='AlNile-Bold', family='Al Nile', size=24, traits='Bold', weight=9) at 0x105a040d0
 --- Family 'Al Tarikh'
  11 Font(name='AlTarikh', family='Al Tarikh', size=12, weight=5) at 0x105a04250
  12+Font(name='AlTarikh', family='Al Tarikh', size=24, weight=5) at 0x105a040d0
 --- Family 'American Typewriter'
  13 Font(name='AmericanTypewriter', family='American Typewriter', size=12, weight=5) at 0x105a04410
  14+Font(name='AmericanTypewriter', family='American Typewriter', size=24, weight=5) at 0x105a046d0
  15 Font(name='AmericanTypewriter-Light', family='American Typewriter', size=12, weight=3) at 0x105a04510
  16+Font(name='AmericanTypewriter-Light', family='American Typewriter', size=24, weight=3) at 0x105a046d0
  17 Font(name='AmericanTypewriter-Semibold', family='American Typewriter', size=12, traits='Bold', weight=9) at 0x105a04910
  18+Font(name='AmericanTypewriter-Bold', family='American Typewriter', size=24, traits='Bold', weight=9) at 0x105a04b50
  19 Font(name='AmericanTypewriter-Bold', family='American Typewriter', size=12, traits='Bold', weight=9) at 0x105a049d0
  20+Font(name='AmericanTypewriter-Bold', family='American Typewriter', size=24, traits='Bold', weight=9) at 0x105a04910
  21 Font(name='AmericanTypewriter-Condensed', family='American Typewriter', size=12, traits='Condensed', weight=5) at 0x105a04ad0
  22+Font(name='AmericanTypewriter', family='American Typewriter', size=24, weight=5) at 0x105a04c10
  23 Font(name='AmericanTypewriter-CondensedLight', family='American Typewriter', size=12, traits='Condensed', weight=3) at 0x105a049d0
  24+Font(name='AmericanTypewriter-Light', family='American Typewriter', size=24, weight=3) at 0x105a04c50
  25 Font(name='AmericanTypewriter-CondensedBold', family='American Typewriter', size=12, traits='Bold Condensed', weight=9) at 0x105a04f50
  26+Font(name='AmericanTypewriter-Bold', family='American Typewriter', size=24, traits='Bold', weight=9) at 0x105a04f10
 --- Family 'Andale Mono'
  27 Font(name='AndaleMono', family='Andale Mono', size=12, traits='MonoSpace', weight=5) at 0x105a21150
  28+Font(name='AndaleMono', family='Andale Mono', size=24, traits='MonoSpace', weight=5) at 0x105a21210
 --- Family 'Arial'
  29 Font(name='ArialMT', family='Arial', size=12, weight=5) at 0x105a21310
  30+Font(name='ArialMT', family='Arial', size=24, weight=5) at 0x105a21210
  31 Font(name='Arial-ItalicMT', family='Arial', size=12, traits='Italic', weight=5) at 0x105a213d0
  32+Font(name='Arial-ItalicMT', family='Arial', size=24, traits='Italic', weight=5) at 0x105a21310
  33 Font(name='Arial-BoldMT', family='Arial', size=12, traits='Bold', weight=9) at 0x105a21750
  34+Font(name='Arial-BoldMT', family='Arial', size=24, traits='Bold', weight=9) at 0x105a21910
  35 Font(name='Arial-BoldItalicMT', family='Arial', size=12, traits='Bold Italic', weight=9) at 0x105a21850
  36+Font(name='Arial-BoldItalicMT', family='Arial', size=24, traits='Bold Italic', weight=9) at 0x105a21a10
 --- Family 'Arial Black'
  37 Font(name='Arial-Black', family='Arial Black', size=12, traits='Bold', weight=11) at 0x105a21750
  38+Font(name='Arial-Black', family='Arial Black', size=24, traits='Bold', weight=11) at 0x105a21d10
 --- Family 'Arial Hebrew'
  39 Font(name='ArialHebrew', family='Arial Hebrew', size=12, weight=5) at 0x105a21cd0
  40+Font(name='ArialHebrew', family='Arial Hebrew', size=24, weight=5) at 0x105a21ed0
  41 Font(name='ArialHebrew-Light', family='Arial Hebrew', size=12, weight=3) at 0x105a21f90
  42+Font(name='ArialHebrew-Light', family='Arial Hebrew', size=24, weight=3) at 0x105a21cd0
  43 Font(name='ArialHebrew-Bold', family='Arial Hebrew', size=12, traits='Bold', weight=9) at 0x105a2b150
  44+Font(name='ArialHebrew-Bold', family='Arial Hebrew', size=24, traits='Bold', weight=9) at 0x105a2b290
 --- Family 'Arial Hebrew Scholar'
  45 Font(name='ArialHebrewScholar', family='Arial Hebrew Scholar', size=12, weight=5) at 0x105a2b2d0
  46+Font(name='ArialHebrewScholar', family='Arial Hebrew Scholar', size=24, weight=5) at 0x105a2b490
  47 Font(name='ArialHebrewScholar-Light', family='Arial Hebrew Scholar', size=12, weight=3) at 0x105a2b290
  48+Font(name='ArialHebrewScholar-Light', family='Arial Hebrew Scholar', size=24, weight=3) at 0x105a2b490
  49 Font(name='ArialHebrewScholar-Bold', family='Arial Hebrew Scholar', size=12, traits='Bold', weight=9) at 0x105a2b4d0
  50+Font(name='ArialHebrewScholar-Bold', family='Arial Hebrew Scholar', size=24, traits='Bold', weight=9) at 0x105a2b710
 --- Family 'Arial Narrow'
  51 Font(name='ArialNarrow', family='Arial Narrow', size=12, traits='Narrow', weight=5) at 0x105a2b750
  52+Font(name='ArialNarrow', family='Arial Narrow', size=24, traits='Narrow', weight=5) at 0x105a2b890
  53 Font(name='ArialNarrow-Italic', family='Arial Narrow', size=12, traits='Italic Narrow', weight=5) at 0x105a2b950
  54+Font(name='ArialNarrow-Italic', family='Arial Narrow', size=24, traits='Italic Narrow', weight=5) at 0x105a2bd50
  55 Font(name='ArialNarrow-Bold', family='Arial Narrow', size=12, traits='Bold Narrow', weight=9) at 0x105a2b750
  56+Font(name='ArialNarrow-Bold', family='Arial Narrow', size=24, traits='Bold Narrow', weight=9) at 0x105a2be90
  57 Font(name='ArialNarrow-BoldItalic', family='Arial Narrow', size=12, traits='Bold Italic Narrow', weight=9) at 0x105a2b950
  58+Font(name='ArialNarrow-BoldItalic', family='Arial Narrow', size=24, traits='Bold Italic Narrow', weight=9) at 0x105a2bf50
 --- Family 'Arial Rounded MT Bold'
  59 Font(name='ArialRoundedMTBold', family='Arial Rounded MT Bold', size=12, traits='Bold', weight=5) at 0x105a2d050
  60+Font(name='ArialRoundedMTBold', family='Arial Rounded MT Bold', size=24, traits='Bold', weight=5) at 0x105a2d1d0
 --- Family 'Arial Unicode MS'
  61 Font(name='ArialUnicodeMS', family='Arial Unicode MS', size=12, weight=5) at 0x105a2d390
  62+Font(name='ArialUnicodeMS', family='Arial Unicode MS', size=24, weight=5) at 0x105a2d4d0
 --- Family 'Athelas'
  63 Font(name='Athelas-Regular', family='Athelas', size=12, weight=5) at 0x105a2d410
  64+Font(name='Athelas-Regular', family='Athelas', size=24, weight=5) at 0x105a2d650
  65 Font(name='Athelas-Italic', family='Athelas', size=12, traits='Italic', weight=5) at 0x105a2d7d0
  66+Font(name='Athelas-Italic', family='Athelas', size=24, traits='Italic', weight=5) at 0x105a2d410
  67 Font(name='Athelas-Bold', family='Athelas', size=12, traits='Bold', weight=9) at 0x105a2d850
  68+Font(name='Athelas-Bold', family='Athelas', size=24, traits='Bold', weight=9) at 0x105a2d910
  69 Font(name='Athelas-BoldItalic', family='Athelas', size=12, traits='Bold Italic', weight=9) at 0x105a2da50
  70+Font(name='Athelas-BoldItalic', family='Athelas', size=24, traits='Bold Italic', weight=9) at 0x105a2d7d0
 --- Family 'Avenir'
  71 Font(name='Avenir-Book', family='Avenir', size=12, weight=5) at 0x105a2d850
  72+Font(name='Avenir-Book', family='Avenir', size=24, weight=5) at 0x105a2df10
  73 Font(name='Avenir-Roman', family='Avenir', size=12, weight=5) at 0x105a2d7d0
  74+Font(name='Avenir-Book', family='Avenir', size=24, weight=5) at 0x105a2d850
  75 Font(name='Avenir-BookOblique', family='Avenir', size=12, traits='Italic', weight=5) at 0x105a26190
  76+Font(name='Avenir-BookOblique', family='Avenir', size=24, traits='Italic', weight=5) at 0x105a26310
  77 Font(name='Avenir-Oblique', family='Avenir', size=12, traits='Italic', weight=5) at 0x105a260d0
  78+Font(name='Avenir-BookOblique', family='Avenir', size=24, traits='Italic', weight=5) at 0x105a26510
  79 Font(name='Avenir-Light', family='Avenir', size=12, weight=3) at 0x105a26190
  80+Font(name='Avenir-Light', family='Avenir', size=24, weight=3) at 0x105a26510
  81 Font(name='Avenir-LightOblique', family='Avenir', size=12, traits='Italic', weight=3) at 0x105a26590
  82+Font(name='Avenir-LightOblique', family='Avenir', size=24, traits='Italic', weight=3) at 0x105a26190
  83 Font(name='Avenir-Medium', family='Avenir', size=12, weight=6) at 0x105a26450
  84+Font(name='Avenir-Medium', family='Avenir', size=24, weight=6) at 0x105a268d0
  85 Font(name='Avenir-MediumOblique', family='Avenir', size=12, traits='Italic', weight=7) at 0x105a26ad0
  86+Font(name='Avenir-MediumOblique', family='Avenir', size=24, traits='Italic', weight=7) at 0x105a26cd0
  87 Font(name='Avenir-Heavy', family='Avenir', size=12, traits='Bold', weight=10) at 0x105a26e50
  88+Font(name='Avenir-Heavy', family='Avenir', size=24, traits='Bold', weight=10) at 0x105a26d10
  89 Font(name='Avenir-HeavyOblique', family='Avenir', size=12, traits='Bold Italic', weight=10) at 0x106501050
  90+Font(name='Avenir-HeavyOblique', family='Avenir', size=24, traits='Bold Italic', weight=10) at 0x105a26e50
  91 Font(name='Avenir-Black', family='Avenir', size=12, traits='Bold', weight=11) at 0x106501090
  92+Font(name='Avenir-Black', family='Avenir', size=24, traits='Bold', weight=11) at 0x1065013d0
  93 Font(name='Avenir-BlackOblique', family='Avenir', size=12, traits='Bold Italic', weight=11) at 0x106501250
  94+Font(name='Avenir-BlackOblique', family='Avenir', size=24, traits='Bold Italic', weight=11) at 0x106501610
 --- Family 'Avenir Next'
  95 Font(name='AvenirNext-Regular', family='Avenir Next', size=12, weight=5) at 0x106501090
  96+Font(name='AvenirNext-Regular', family='Avenir Next', size=24, weight=5) at 0x1065017d0
  97 Font(name='AvenirNext-Italic', family='Avenir Next', size=12, traits='Italic', weight=5) at 0x106501790
  98+Font(name='AvenirNext-Italic', family='Avenir Next', size=24, traits='Italic', weight=5) at 0x106501090
  99 Font(name='AvenirNext-UltraLight', family='Avenir Next', size=12, weight=2) at 0x106501ad0
 100+Font(name='AvenirNext-UltraLight', family='Avenir Next', size=24, weight=2) at 0x106501790
 101 Font(name='AvenirNext-UltraLightItalic', family='Avenir Next', size=12, traits='Italic', weight=2) at 0x106501d50
 102+Font(name='AvenirNext-UltraLightItalic', family='Avenir Next', size=24, traits='Italic', weight=2) at 0x106501c90
 103 Font(name='AvenirNext-Medium', family='Avenir Next', size=12, weight=6) at 0x106501f50
 104+Font(name='AvenirNext-Medium', family='Avenir Next', size=24, weight=6) at 0x106501090
 105 Font(name='AvenirNext-MediumItalic', family='Avenir Next', size=12, traits='Italic', weight=7) at 0x106501e90
 106+Font(name='AvenirNext-MediumItalic', family='Avenir Next', size=24, traits='Italic', weight=7) at 0x106511050
 107 Font(name='AvenirNext-DemiBold', family='Avenir Next', size=12, traits='Bold', weight=9) at 0x106511390
 108+Font(name='AvenirNext-Bold', family='Avenir Next', size=24, traits='Bold', weight=9) at 0x106511050
 109 Font(name='AvenirNext-DemiBoldItalic', family='Avenir Next', size=12, traits='Bold Italic', weight=9) at 0x1065110d0
 110+Font(name='AvenirNext-BoldItalic', family='Avenir Next', size=24, traits='Bold Italic', weight=9) at 0x106511390
 111 Font(name='AvenirNext-Bold', family='Avenir Next', size=12, traits='Bold', weight=9) at 0x1065117d0
 112+Font(name='AvenirNext-Bold', family='Avenir Next', size=24, traits='Bold', weight=9) at 0x1065110d0
 113 Font(name='AvenirNext-BoldItalic', family='Avenir Next', size=12, traits='Bold Italic', weight=9) at 0x106511990
 114+Font(name='AvenirNext-BoldItalic', family='Avenir Next', size=24, traits='Bold Italic', weight=9) at 0x1065110d0
 115 Font(name='AvenirNext-Heavy', family='Avenir Next', size=12, traits='Bold', weight=10) at 0x106511890
 116+Font(name='AvenirNext-Heavy', family='Avenir Next', size=24, traits='Bold', weight=10) at 0x1065118d0
 117 Font(name='AvenirNext-HeavyItalic', family='Avenir Next', size=12, traits='Bold Italic', weight=10) at 0x106511910
 118+Font(name='AvenirNext-HeavyItalic', family='Avenir Next', size=24, traits='Bold Italic', weight=10) at 0x106511890
 --- Family 'Avenir Next Condensed'
 119 Font(name='AvenirNextCondensed-Regular', family='Avenir Next Condensed', size=12, traits='Condensed', weight=5) at 0x106511d10
 120+Font(name='AvenirNextCondensed-Regular', family='Avenir Next Condensed', size=24, traits='Condensed', weight=5) at 0x10651c190
 121 Font(name='AvenirNextCondensed-Italic', family='Avenir Next Condensed', size=12, traits='Condensed Italic', weight=5) at 0x10651c250
 122+Font(name='AvenirNextCondensed-Italic', family='Avenir Next Condensed', size=24, traits='Condensed Italic', weight=5) at 0x106511dd0
 123 Font(name='AvenirNextCondensed-UltraLight', family='Avenir Next Condensed', size=12, traits='Condensed', weight=2) at 0x10651c190
 124+Font(name='AvenirNextCondensed-UltraLight', family='Avenir Next Condensed', size=24, traits='Condensed', weight=2) at 0x10651c110
 125 Font(name='AvenirNextCondensed-UltraLightItalic', family='Avenir Next Condensed', size=12, traits='Condensed Italic', weight=2) at 0x10651c450
 126+Font(name='AvenirNextCondensed-UltraLightItalic', family='Avenir Next Condensed', size=24, traits='Condensed Italic', weight=2) at 0x10651c190
 127 Font(name='AvenirNextCondensed-Medium', family='Avenir Next Condensed', size=12, traits='Condensed', weight=6) at 0x10651c750
 128+Font(name='AvenirNextCondensed-Medium', family='Avenir Next Condensed', size=24, traits='Condensed', weight=6) at 0x10651c990
 129 Font(name='AvenirNextCondensed-MediumItalic', family='Avenir Next Condensed', size=12, traits='Condensed Italic', weight=7) at 0x10651ca50
 130+Font(name='AvenirNextCondensed-MediumItalic', family='Avenir Next Condensed', size=24, traits='Condensed Italic', weight=7) at 0x10651c950
 131 Font(name='AvenirNextCondensed-DemiBold', family='Avenir Next Condensed', size=12, traits='Bold Condensed', weight=9) at 0x10651c790
 132+Font(name='AvenirNextCondensed-Bold', family='Avenir Next Condensed', size=24, traits='Bold Condensed', weight=9) at 0x10651cbd0
 133 Font(name='AvenirNextCondensed-DemiBoldItalic', family='Avenir Next Condensed', size=12, traits='Bold Condensed Italic', weight=9) at 0x10651c950
 134+Font(name='AvenirNextCondensed-BoldItalic', family='Avenir Next Condensed', size=24, traits='Bold Condensed Italic', weight=9) at 0x10651cbd0
 135 Font(name='AvenirNextCondensed-Bold', family='Avenir Next Condensed', size=12, traits='Bold Condensed', weight=9) at 0x10651ce10
 136+Font(name='AvenirNextCondensed-Bold', family='Avenir Next Condensed', size=24, traits='Bold Condensed', weight=9) at 0x10651cf50
 137 Font(name='AvenirNextCondensed-BoldItalic', family='Avenir Next Condensed', size=12, traits='Bold Condensed Italic', weight=9) at 0x1065271d0
 138+Font(name='AvenirNextCondensed-BoldItalic', family='Avenir Next Condensed', size=24, traits='Bold Condensed Italic', weight=9) at 0x10651cbd0
 139 Font(name='AvenirNextCondensed-Heavy', family='Avenir Next Condensed', size=12, traits='Bold Condensed', weight=10) at 0x10651ce10
 140+Font(name='AvenirNextCondensed-Heavy', family='Avenir Next Condensed', size=24, traits='Bold Condensed', weight=10) at 0x10651cd90
 141 Font(name='AvenirNextCondensed-HeavyItalic', family='Avenir Next Condensed', size=12, traits='Bold Condensed Italic', weight=10) at 0x1065273d0
 142+Font(name='AvenirNextCondensed-HeavyItalic', family='Avenir Next Condensed', size=24, traits='Bold Condensed Italic', weight=10) at 0x10651cd90
 --- Family 'Ayuthaya'
 143 Font(name='Ayuthaya', family='Ayuthaya', size=12, weight=5) at 0x1065272d0
 144+Font(name='Ayuthaya', family='Ayuthaya', size=24, weight=5) at 0x106527590
 --- Family 'Baghdad'
 145 Font(name='Baghdad', family='Baghdad', size=12, weight=5) at 0x106527750
 146+Font(name='Baghdad', family='Baghdad', size=24, weight=5) at 0x106527590
 --- Family 'Bangla MN'
 147 Font(name='BanglaMN', family='Bangla MN', size=12, weight=5) at 0x1065279d0
 148+Font(name='BanglaMN', family='Bangla MN', size=24, weight=5) at 0x106527590
 149 Font(name='BanglaMN-Bold', family='Bangla MN', size=12, traits='Bold', weight=9) at 0x106527cd0
 150+Font(name='BanglaMN-Bold', family='Bangla MN', size=24, traits='Bold', weight=9) at 0x1065279d0
 --- Family 'Bangla Sangam MN'
 151 Font(name='BanglaSangamMN', family='Bangla Sangam MN', size=12, weight=5) at 0x106527e10
 152+Font(name='BanglaSangamMN', family='Bangla Sangam MN', size=24, weight=5) at 0x105a3e090
 153 Font(name='BanglaSangamMN-Bold', family='Bangla Sangam MN', size=12, traits='Bold', weight=9) at 0x105a3e0d0
 154+Font(name='BanglaSangamMN-Bold', family='Bangla Sangam MN', size=24, traits='Bold', weight=9) at 0x105a3e090
 --- Family 'Bank Gothic'
 155 Font(name='BankGothic-Light', family='Bank Gothic', size=12, weight=3) at 0x105a3e310
 156+Font(name='BankGothic-Light', family='Bank Gothic', size=24, weight=3) at 0x105a3e510
 157 Font(name='BankGothic-Medium', family='Bank Gothic', size=12, weight=6) at 0x105a3e4d0
 158+Font(name='BankGothic-Medium', family='Bank Gothic', size=24, weight=6) at 0x105a3e610
 --- Family 'Baskerville'
 159 Font(name='Baskerville', family='Baskerville', size=12, weight=5) at 0x105a3e310
 160+Font(name='Baskerville', family='Baskerville', size=24, weight=5) at 0x105a3e990
 161 Font(name='Baskerville-Italic', family='Baskerville', size=12, traits='Italic', weight=5) at 0x105a3e950
 162+Font(name='Baskerville-Italic', family='Baskerville', size=24, traits='Italic', weight=5) at 0x105a3e310
 163 Font(name='Baskerville-SemiBold', family='Baskerville', size=12, traits='Bold', weight=9) at 0x105a3eb10
 164+Font(name='Baskerville-Bold', family='Baskerville', size=24, traits='Bold', weight=9) at 0x105a3e950
 165 Font(name='Baskerville-SemiBoldItalic', family='Baskerville', size=12, traits='Bold Italic', weight=9) at 0x105a3ecd0
 166+Font(name='Baskerville-BoldItalic', family='Baskerville', size=24, traits='Bold Italic', weight=9) at 0x105a3eb10
 167 Font(name='Baskerville-Bold', family='Baskerville', size=12, traits='Bold', weight=9) at 0x105a3edd0
 168+Font(name='Baskerville-Bold', family='Baskerville', size=24, traits='Bold', weight=9) at 0x105a3ecd0
 169 Font(name='Baskerville-BoldItalic', family='Baskerville', size=12, traits='Bold Italic', weight=9) at 0x108972110
 170+Font(name='Baskerville-BoldItalic', family='Baskerville', size=24, traits='Bold Italic', weight=9) at 0x105a3ecd0
 --- Family 'Beirut'
 171 Font(name='Beirut', family='Beirut', size=12, traits='Bold', weight=9) at 0x108972210
 172+Font(name='Beirut', family='Beirut', size=24, traits='Bold', weight=9) at 0x108972150
 --- Family 'Big Caslon'
 173 Font(name='BigCaslon-Medium', family='Big Caslon', size=12, weight=6) at 0x1089723d0
 174+Font(name='BigCaslon-Medium', family='Big Caslon', size=24, weight=6) at 0x108972610
 --- Family 'Blackmoor LET'
 175 Font(name='BlackmoorLetPlain', family='Blackmoor LET', size=12, traits='Bold', weight=11) at 0x108972690
 176+Font(name='BlackmoorLetPlain', family='Blackmoor LET', size=24, traits='Bold', weight=11) at 0x108972750
 --- Family 'BlairMdITC TT'
 177 Font(name='BlairMdITCTT-Medium', family='BlairMdITC TT', size=12, weight=6) at 0x1089729d0
 178+Font(name='BlairMdITCTT-Medium', family='BlairMdITC TT', size=24, weight=6) at 0x108972ad0
 --- Family 'Bodoni 72'
 179 Font(name='BodoniSvtyTwoITCTT-Book', family='Bodoni 72', size=12, weight=5) at 0x108972bd0
 180+Font(name='BodoniSvtyTwoITCTT-Book', family='Bodoni 72', size=24, weight=5) at 0x108972ad0
 181 Font(name='BodoniSvtyTwoITCTT-BookIta', family='Bodoni 72', size=12, traits='Italic', weight=5) at 0x108972ed0
 182+Font(name='BodoniSvtyTwoITCTT-BookIta', family='Bodoni 72', size=24, traits='Italic', weight=5) at 0x108972bd0
 183 Font(name='BodoniSvtyTwoITCTT-Bold', family='Bodoni 72', size=12, traits='Bold', weight=9) at 0x108981150
 184+Font(name='BodoniSvtyTwoITCTT-Bold', family='Bodoni 72', size=24, traits='Bold', weight=9) at 0x108972ed0
 --- Family 'Bodoni 72 Oldstyle'
 185 Font(name='BodoniSvtyTwoOSITCTT-Book', family='Bodoni 72 Oldstyle', size=12, weight=5) at 0x108981310
 186+Font(name='BodoniSvtyTwoOSITCTT-Book', family='Bodoni 72 Oldstyle', size=24, weight=5) at 0x108972e10
 187 Font(name='BodoniSvtyTwoOSITCTT-BookIt', family='Bodoni 72 Oldstyle', size=12, traits='Italic', weight=5) at 0x1089814d0
 188+Font(name='BodoniSvtyTwoOSITCTT-BookIt', family='Bodoni 72 Oldstyle', size=24, traits='Italic', weight=5) at 0x108981650
 189 Font(name='BodoniSvtyTwoOSITCTT-Bold', family='Bodoni 72 Oldstyle', size=12, traits='Bold', weight=9) at 0x108981750
 190+Font(name='BodoniSvtyTwoOSITCTT-Bold', family='Bodoni 72 Oldstyle', size=24, traits='Bold', weight=9) at 0x108981710
 --- Family 'Bodoni 72 Smallcaps'
 191 Font(name='BodoniSvtyTwoSCITCTT-Book', family='Bodoni 72 Smallcaps', size=12, traits='SmallCaps', weight=5) at 0x108981a50
 192+Font(name='BodoniSvtyTwoSCITCTT-Book', family='Bodoni 72 Smallcaps', size=24, traits='SmallCaps', weight=5) at 0x108981cd0
 --- Family 'Bodoni Ornaments'
 193 Font(name='BodoniOrnamentsITCTT', family='Bodoni Ornaments', size=12, weight=5) at 0x108981d90
 194+Font(name='BodoniOrnamentsITCTT', family='Bodoni Ornaments', size=24, weight=5) at 0x108981f10
 --- Family 'Bordeaux Roman Bold LET'
 195 Font(name='BordeauxRomanBoldLetPlain', family='Bordeaux Roman Bold LET', size=12, traits='Bold', weight=9) at 0x10898e150
 196+Font(name='BordeauxRomanBoldLetPlain', family='Bordeaux Roman Bold LET', size=24, traits='Bold', weight=9) at 0x10898e410
 --- Family 'Bradley Hand'
 197 Font(name='BradleyHandITCTT-Bold', family='Bradley Hand', size=12, traits='Bold Expanded', weight=9) at 0x10898e4d0
 198+Font(name='BradleyHandITCTT-Bold', family='Bradley Hand', size=24, traits='Bold Expanded', weight=9) at 0x10898e490
 --- Family 'Brush Script MT'
 199 Font(name='BrushScriptMT', family='Brush Script MT', size=12, traits='Italic', weight=5) at 0x10898e710
 200+Font(name='BrushScriptMT', family='Brush Script MT', size=24, weight=5) at 0x10898e450
 --- Family 'Capitals'
 201 Font(name='CapitalsRegular', family='Capitals', size=12, traits='Bold Condensed', weight=9) at 0x10898e850
 202+Font(name='CapitalsRegular', family='Capitals', size=24, traits='Bold Condensed', weight=9) at 0x10898e9d0
 --- Family 'Casual'
 203 Font(name='AppleCasual', family='Casual', size=12, weight=5) at 0x10898ec90
 204+Font(name='AppleCasual', family='Casual', size=24, weight=5) at 0x10898e9d0
 --- Family 'Chalkboard'
 205 Font(name='Chalkboard', family='Chalkboard', size=12, weight=5) at 0x10898ef10
 206+Font(name='Chalkboard', family='Chalkboard', size=24, weight=5) at 0x10898e9d0
 207 Font(name='Chalkboard-Bold', family='Chalkboard', size=12, traits='Bold', weight=9) at 0x108994090
 208+Font(name='Chalkboard-Bold', family='Chalkboard', size=24, traits='Bold', weight=9) at 0x108994210
 --- Family 'Chalkboard SE'
 209 Font(name='ChalkboardSE-Regular', family='Chalkboard SE', size=12, weight=5) at 0x1089940d0
 210+Font(name='ChalkboardSE-Regular', family='Chalkboard SE', size=24, weight=5) at 0x1089943d0
 211 Font(name='ChalkboardSE-Light', family='Chalkboard SE', size=12, weight=3) at 0x1089945d0
 212+Font(name='ChalkboardSE-Light', family='Chalkboard SE', size=24, weight=3) at 0x1089940d0
 213 Font(name='ChalkboardSE-Bold', family='Chalkboard SE', size=12, traits='Bold', weight=9) at 0x108994490
 214+Font(name='ChalkboardSE-Bold', family='Chalkboard SE', size=24, traits='Bold', weight=9) at 0x1089945d0
 --- Family 'Chalkduster'
 215 Font(name='Chalkduster', family='Chalkduster', size=12, weight=5) at 0x108994950
 216+Font(name='Chalkduster', family='Chalkduster', size=24, weight=5) at 0x108994b50
 --- Family 'Charter'
 217 Font(name='Charter-Roman', family='Charter', size=12, weight=5) at 0x108994a10
 218+Font(name='Charter-Roman', family='Charter', size=24, weight=5) at 0x108994cd0
 219 Font(name='Charter-Italic', family='Charter', size=12, traits='Italic', weight=5) at 0x108994e50
 220+Font(name='Charter-Italic', family='Charter', size=24, traits='Italic', weight=5) at 0x108994a10
 221 Font(name='Charter-Bold', family='Charter', size=12, traits='Bold', weight=9) at 0x108994f90
 222+Font(name='Charter-Bold', family='Charter', size=24, traits='Bold', weight=9) at 0x10899d050
 223 Font(name='Charter-BoldItalic', family='Charter', size=12, traits='Bold Italic', weight=9) at 0x10899d110
 224+Font(name='Charter-BoldItalic', family='Charter', size=24, traits='Bold Italic', weight=9) at 0x10899d210
 225 Font(name='Charter-Black', family='Charter', size=12, traits='Bold', weight=11) at 0x10899d310
 226+Font(name='Charter-Black', family='Charter', size=24, traits='Bold', weight=11) at 0x10899d110
 227 Font(name='Charter-BlackItalic', family='Charter', size=12, traits='Bold Italic', weight=11) at 0x10899d490
 228+Font(name='Charter-BlackItalic', family='Charter', size=24, traits='Bold Italic', weight=11) at 0x10899d750
 --- Family 'Cochin'
 229 Font(name='Cochin', family='Cochin', size=12, weight=5) at 0x10899d310
 230+Font(name='Cochin', family='Cochin', size=24, weight=5) at 0x10899d750
 231 Font(name='Cochin-Italic', family='Cochin', size=12, traits='Italic', weight=5) at 0x10899d9d0
 232+Font(name='Cochin-Italic', family='Cochin', size=24, traits='Italic', weight=5) at 0x10899d310
 233 Font(name='Cochin-Bold', family='Cochin', size=12, traits='Bold', weight=9) at 0x10899da10
 234+Font(name='Cochin-Bold', family='Cochin', size=24, traits='Bold', weight=9) at 0x10899dcd0
 235 Font(name='Cochin-BoldItalic', family='Cochin', size=12, traits='Bold Italic', weight=9) at 0x10899db90
 236+Font(name='Cochin-BoldItalic', family='Cochin', size=24, traits='Bold Italic', weight=9) at 0x10899df90
 --- Family 'Comic Sans MS'
 237 Font(name='ComicSansMS', family='Comic Sans MS', size=12, traits='SansSerif', weight=5) at 0x10899de90
 238+Font(name='ComicSansMS', family='Comic Sans MS', size=24, traits='SansSerif', weight=5) at 0x10897d190
 239 Font(name='ComicSansMS-Bold', family='Comic Sans MS', size=12, traits='Bold SansSerif', weight=9) at 0x10897d1d0
 240+Font(name='ComicSansMS-Bold', family='Comic Sans MS', size=24, traits='Bold SansSerif', weight=9) at 0x10897d390
 --- Family 'Copperplate'
 241 Font(name='Copperplate', family='Copperplate', size=12, weight=5) at 0x10897d450
 242+Font(name='Copperplate', family='Copperplate', size=24, weight=5) at 0x10897d610
 243 Font(name='Copperplate-Light', family='Copperplate', size=12, weight=3) at 0x10897d5d0
 244+Font(name='Copperplate-Light', family='Copperplate', size=24, weight=3) at 0x10897d6d0
 245 Font(name='Copperplate-Bold', family='Copperplate', size=12, traits='Bold', weight=9) at 0x10897d450
 246+Font(name='Copperplate-Bold', family='Copperplate', size=24, traits='Bold', weight=9) at 0x10897d5d0
 --- Family 'Corsiva Hebrew'
 247 Font(name='CorsivaHebrew', family='Corsiva Hebrew', size=12, weight=5) at 0x10897d950
 248+Font(name='CorsivaHebrew', family='Corsiva Hebrew', size=24, weight=5) at 0x10897db90
 249 Font(name='CorsivaHebrew-Bold', family='Corsiva Hebrew', size=12, traits='Bold', weight=9) at 0x10897db50
 250+Font(name='CorsivaHebrew-Bold', family='Corsiva Hebrew', size=24, traits='Bold', weight=9) at 0x10897d950
 --- Family 'Courier'
 251 Font(name='Courier', family='Courier', size=12, traits='MonoSpace', weight=5) at 0x10897dd10
 252+Font(name='Courier', family='Courier', size=24, traits='MonoSpace', weight=5) at 0x10897df50
 253 Font(name='Courier-Oblique', family='Courier', size=12, traits='Italic MonoSpace', weight=5) at 0x10897dd90
 254+Font(name='Courier-Oblique', family='Courier', size=24, traits='Italic MonoSpace', weight=5) at 0x10897dd10
 255 Font(name='Courier-Bold', family='Courier', size=12, traits='Bold MonoSpace', weight=9) at 0x10896c190
 256+Font(name='Courier-Bold', family='Courier', size=24, traits='Bold MonoSpace', weight=9) at 0x10897dd90
 257 Font(name='Courier-BoldOblique', family='Courier', size=12, traits='Bold Italic MonoSpace', weight=9) at 0x10896c2d0
 258+Font(name='Courier-BoldOblique', family='Courier', size=24, traits='Bold Italic MonoSpace', weight=9) at 0x10896c190
 --- Family 'Courier New'
 259 Font(name='CourierNewPSMT', family='Courier New', size=12, traits='MonoSpace', weight=5) at 0x10896c450
 260+Font(name='CourierNewPSMT', family='Courier New', size=24, traits='MonoSpace', weight=5) at 0x10896c5d0
 261 Font(name='CourierNewPS-ItalicMT', family='Courier New', size=12, traits='Italic MonoSpace', weight=5) at 0x10896c6d0
 262+Font(name='CourierNewPS-ItalicMT', family='Courier New', size=24, traits='Italic MonoSpace', weight=5) at 0x10896c450
 263 Font(name='CourierNewPS-BoldMT', family='Courier New', size=12, traits='Bold MonoSpace', weight=9) at 0x10896c8d0
 264+Font(name='CourierNewPS-BoldMT', family='Courier New', size=24, traits='Bold MonoSpace', weight=9) at 0x10896c6d0
 265 Font(name='CourierNewPS-BoldItalicMT', family='Courier New', size=12, traits='Bold Italic MonoSpace', weight=9) at 0x10896c450
 266+Font(name='CourierNewPS-BoldItalicMT', family='Courier New', size=24, traits='Bold Italic MonoSpace', weight=9) at 0x10896c6d0
 --- Family 'Cracked'
 267 Font(name='Cracked', family='Cracked', size=12, weight=5) at 0x10896c950
 268+Font(name='Cracked', family='Cracked', size=24, weight=5) at 0x10896c6d0
 --- Family 'Damascus'
 269 Font(name='Damascus', family='Damascus', size=12, weight=5) at 0x10896cc90
 270+Font(name='Damascus', family='Damascus', size=24, weight=5) at 0x1091d3150
 271 Font(name='DamascusLight', family='Damascus', size=12, weight=3) at 0x1091d3110
 272+Font(name='DamascusLight', family='Damascus', size=24, weight=3) at 0x1091d3050
 273 Font(name='DamascusMedium', family='Damascus', size=12, weight=6) at 0x1091d31d0
 274+Font(name='DamascusMedium', family='Damascus', size=24, weight=6) at 0x1091d3210
 275 Font(name='DamascusSemiBold', family='Damascus', size=12, traits='Bold', weight=9) at 0x1091d32d0
 276+Font(name='DamascusBold', family='Damascus', size=24, traits='Bold', weight=9) at 0x1091d31d0
 277 Font(name='DamascusBold', family='Damascus', size=12, traits='Bold', weight=9) at 0x1091d3590
 278+Font(name='DamascusBold', family='Damascus', size=24, traits='Bold', weight=9) at 0x1091d3790
 --- Family 'DecoType Naskh'
 279 Font(name='DecoTypeNaskh', family='DecoType Naskh', size=12, weight=5) at 0x1091d3890
 280+Font(name='DecoTypeNaskh', family='DecoType Naskh', size=24, weight=5) at 0x1091d3a10
 --- Family 'Devanagari MT'
 281 Font(name='DevanagariMT', family='Devanagari MT', size=12, weight=5) at 0x1091d39d0
 282+Font(name='DevanagariMT', family='Devanagari MT', size=24, weight=5) at 0x1091d3c10
 283 Font(name='DevanagariMT-Bold', family='Devanagari MT', size=12, traits='Bold', weight=9) at 0x1091d3910
 284+Font(name='DevanagariMT-Bold', family='Devanagari MT', size=24, traits='Bold', weight=9) at 0x1091d39d0
 --- Family 'Devanagari Sangam MN'
 285 Font(name='DevanagariSangamMN', family='Devanagari Sangam MN', size=12, weight=5) at 0x1091d3d90
 286+Font(name='DevanagariSangamMN', family='Devanagari Sangam MN', size=24, weight=5) at 0x1091e00d0
 287 Font(name='DevanagariSangamMN-Bold', family='Devanagari Sangam MN', size=12, traits='Bold', weight=9) at 0x1091e0110
 288+Font(name='DevanagariSangamMN-Bold', family='Devanagari Sangam MN', size=24, traits='Bold', weight=9) at 0x1091e0190
 --- Family 'Didot'
 289 Font(name='Didot', family='Didot', size=12, weight=5) at 0x1091e0390
 290+Font(name='Didot', family='Didot', size=24, weight=5) at 0x1091e0190
 291 Font(name='Didot-Italic', family='Didot', size=12, traits='Italic', weight=5) at 0x1091e0510
 292+Font(name='Didot-Italic', family='Didot', size=24, traits='Italic', weight=5) at 0x1091e05d0
 293 Font(name='Didot-Bold', family='Didot', size=12, traits='Bold', weight=9) at 0x1091e02d0
 294+Font(name='Didot-Bold', family='Didot', size=24, traits='Bold', weight=9) at 0x1091e0850
 --- Family 'DIN Alternate'
 295 Font(name='DINAlternate-Bold', family='DIN Alternate', size=12, traits='Bold', weight=9) at 0x1091e0a10
 296+Font(name='DINAlternate-Bold', family='DIN Alternate', size=24, traits='Bold', weight=9) at 0x1091e0ad0
 --- Family 'DIN Condensed'
 297 Font(name='DINCondensed-Bold', family='DIN Condensed', size=12, traits='Bold Condensed', weight=9) at 0x1091e0d50
 298+Font(name='DINCondensed-Bold', family='DIN Condensed', size=24, traits='Bold Condensed', weight=9) at 0x1091e0cd0
 --- Family 'Diwan Kufi'
 299 Font(name='DiwanKufi', family='Diwan Kufi', size=12, weight=5) at 0x1091f1090
 300+Font(name='DiwanKufi', family='Diwan Kufi', size=24, weight=5) at 0x1091f1190
 --- Family 'Diwan Thuluth'
 301 Font(name='DiwanThuluth', family='Diwan Thuluth', size=12, weight=5) at 0x1091f1350
 302+Font(name='DiwanThuluth', family='Diwan Thuluth', size=24, weight=5) at 0x1091f1450
 --- Family 'Euphemia UCAS'
 303 Font(name='EuphemiaUCAS', family='Euphemia UCAS', size=12, weight=5) at 0x1091f15d0
 304+Font(name='EuphemiaUCAS', family='Euphemia UCAS', size=24, weight=5) at 0x1091f1790
 305 Font(name='EuphemiaUCAS-Italic', family='Euphemia UCAS', size=12, traits='Italic', weight=5) at 0x1091f1510
 306+Font(name='EuphemiaUCAS-Italic', family='Euphemia UCAS', size=24, traits='Italic', weight=5) at 0x1091f15d0
 307 Font(name='EuphemiaUCAS-Bold', family='Euphemia UCAS', size=12, traits='Bold', weight=9) at 0x1091f1910
 308+Font(name='EuphemiaUCAS-Bold', family='Euphemia UCAS', size=24, traits='Bold', weight=9) at 0x1091f1510
 --- Family 'Farah'
 309 Font(name='Farah', family='Farah', size=12, weight=5) at 0x1091f1b90
 310+Font(name='Farah', family='Farah', size=24, weight=5) at 0x1091f1510
 --- Family 'Farisi'
 311 Font(name='Farisi', family='Farisi', size=12, weight=5) at 0x1091f1e10
 312+Font(name='Farisi', family='Farisi', size=24, weight=5) at 0x1091f1ed0
 --- Family 'Futura'
 313 Font(name='Futura-Medium', family='Futura', size=12, weight=6) at 0x1091fc050
 314+Font(name='Futura-Medium', family='Futura', size=24, weight=6) at 0x1091fc090
 315 Font(name='Futura-MediumItalic', family='Futura', size=12, traits='Italic', weight=7) at 0x1091fc350
 316+Font(name='Futura-MediumItalic', family='Futura', size=24, traits='Italic', weight=7) at 0x1091fc050
 317 Font(name='Futura-Bold', family='Futura', size=12, traits='Bold', weight=9) at 0x1091fc2d0
 318+Font(name='Futura-Bold', family='Futura', size=24, traits='Bold', weight=9) at 0x1091fc490
 319 Font(name='Futura-CondensedMedium', family='Futura', size=12, traits='Condensed', weight=7) at 0x1091fc5d0
 320+Font(name='Futura-CondensedMedium', family='Futura', size=24, traits='Condensed', weight=7) at 0x1091fc2d0
 321 Font(name='Futura-CondensedExtraBold', family='Futura', size=12, traits='Bold Condensed', weight=11) at 0x1091fca10
 322+Font(name='Futura-CondensedExtraBold', family='Futura', size=24, traits='Bold Condensed', weight=11) at 0x1091fcbd0
 --- Family 'GB18030 Bitmap'
 323 Font(name='GB18030Bitmap', family='GB18030 Bitmap', size=12, traits='MonoSpace', weight=5) at 0x1091fcc90
 324+Font(name='GB18030Bitmap', family='GB18030 Bitmap', size=24, traits='MonoSpace', weight=5) at 0x1091fc2d0
 --- Family 'Geeza Pro'
 325 Font(name='GeezaPro', family='Geeza Pro', size=12, weight=5) at 0x1091fcd10
 326+Font(name='GeezaPro', family='Geeza Pro', size=24, weight=5) at 0x1091cf110
 327 Font(name='GeezaPro-Bold', family='Geeza Pro', size=12, traits='Bold', weight=9) at 0x1091cf190
 328+Font(name='GeezaPro-Bold', family='Geeza Pro', size=24, traits='Bold', weight=9) at 0x1091cf110
 --- Family 'Geneva'
 329 Font(name='Geneva', family='Geneva', size=12, weight=5) at 0x1091cf3d0
 330+Font(name='Geneva', family='Geneva', size=24, weight=5) at 0x1091cf110
 --- Family 'Georgia'
 331 Font(name='Georgia', family='Georgia', size=12, weight=5) at 0x1091cf5d0
 332+Font(name='Georgia', family='Georgia', size=24, weight=5) at 0x1091cf110
 333 Font(name='Georgia-Italic', family='Georgia', size=12, traits='Italic', weight=5) at 0x1091cf810
 334+Font(name='Georgia-Italic', family='Georgia', size=24, traits='Italic', weight=5) at 0x1091cf5d0
 335 Font(name='Georgia-Bold', family='Georgia', size=12, traits='Bold', weight=9) at 0x1091cf850
 336+Font(name='Georgia-Bold', family='Georgia', size=24, traits='Bold', weight=9) at 0x1091cfb10
 337 Font(name='Georgia-BoldItalic', family='Georgia', size=12, traits='Bold Italic', weight=9) at 0x1091cf9d0
 338+Font(name='Georgia-BoldItalic', family='Georgia', size=24, traits='Bold Italic', weight=9) at 0x1091cfd10
 --- Family 'Gill Sans'
 339 Font(name='GillSans', family='Gill Sans', size=12, traits='SansSerif', weight=5) at 0x1091cf850
 340+Font(name='GillSans', family='Gill Sans', size=24, traits='SansSerif', weight=5) at 0x109ef80d0
 341 Font(name='GillSans-Italic', family='Gill Sans', size=12, traits='Italic SansSerif', weight=5) at 0x109ef8050
 342+Font(name='GillSans-Italic', family='Gill Sans', size=24, traits='Italic SansSerif', weight=5) at 0x109ef8210
 343 Font(name='GillSans-Light', family='Gill Sans', size=12, traits='SansSerif', weight=3) at 0x109ef82d0
 344+Font(name='GillSans-Light', family='Gill Sans', size=24, traits='SansSerif', weight=3) at 0x109ef8050
 345 Font(name='GillSans-LightItalic', family='Gill Sans', size=12, traits='Italic SansSerif', weight=3) at 0x109ef8150
 346+Font(name='GillSans-LightItalic', family='Gill Sans', size=24, traits='Italic SansSerif', weight=3) at 0x109ef82d0
 347 Font(name='GillSans-SemiBold', family='Gill Sans', size=12, traits='Bold SansSerif', weight=9) at 0x109ef8710
 348+Font(name='GillSans-Bold', family='Gill Sans', size=24, traits='Bold SansSerif', weight=9) at 0x109ef8150
 349 Font(name='GillSans-SemiBoldItalic', family='Gill Sans', size=12, traits='Bold Italic SansSerif', weight=9) at 0x109ef88d0
 350+Font(name='GillSans-BoldItalic', family='Gill Sans', size=24, traits='Bold Italic SansSerif', weight=9) at 0x109ef8150
 351 Font(name='GillSans-Bold', family='Gill Sans', size=12, traits='Bold SansSerif', weight=9) at 0x109ef8b10
 352+Font(name='GillSans-Bold', family='Gill Sans', size=24, traits='Bold SansSerif', weight=9) at 0x109ef8150
 353 Font(name='GillSans-BoldItalic', family='Gill Sans', size=12, traits='Bold Italic SansSerif', weight=9) at 0x109ef8c10
 354+Font(name='GillSans-BoldItalic', family='Gill Sans', size=24, traits='Bold Italic SansSerif', weight=9) at 0x109ef8c50
 355 Font(name='GillSans-UltraBold', family='Gill Sans', size=12, traits='Bold SansSerif', weight=11) at 0x109ef88d0
 356+Font(name='GillSans-UltraBold', family='Gill Sans', size=24, traits='Bold SansSerif', weight=11) at 0x109ef8d10
 --- Family 'Gujarati MT'
 357 Font(name='GujaratiMT', family='Gujarati MT', size=12, weight=5) at 0x109ef8d50
 358+Font(name='GujaratiMT', family='Gujarati MT', size=24, weight=5) at 0x109ef8f50
 359 Font(name='GujaratiMT-Bold', family='Gujarati MT', size=12, traits='Bold', weight=9) at 0x109ef8c10
 360+Font(name='GujaratiMT-Bold', family='Gujarati MT', size=24, traits='Bold', weight=9) at 0x109f04050
 --- Family 'Gujarati Sangam MN'
 361 Font(name='GujaratiSangamMN', family='Gujarati Sangam MN', size=12, weight=5) at 0x109f04090
 362+Font(name='GujaratiSangamMN', family='Gujarati Sangam MN', size=24, weight=5) at 0x109f04110
 363 Font(name='GujaratiSangamMN-Bold', family='Gujarati Sangam MN', size=12, traits='Bold', weight=9) at 0x109f04290
 364+Font(name='GujaratiSangamMN-Bold', family='Gujarati Sangam MN', size=24, traits='Bold', weight=9) at 0x109f04490
 --- Family 'Gurmukhi MN'
 365 Font(name='GurmukhiMN', family='Gurmukhi MN', size=12, weight=5) at 0x109f044d0
 366+Font(name='GurmukhiMN', family='Gurmukhi MN', size=24, weight=5) at 0x109f04790
 367 Font(name='GurmukhiMN-Bold', family='Gurmukhi MN', size=12, traits='Bold', weight=9) at 0x109f048d0
 368+Font(name='GurmukhiMN-Bold', family='Gurmukhi MN', size=24, traits='Bold', weight=9) at 0x109f044d0
 --- Family 'Gurmukhi MT'
 369 Font(name='MonotypeGurmukhi', family='Gurmukhi MT', size=12, weight=5) at 0x109f04a50
 370+Font(name='MonotypeGurmukhi', family='Gurmukhi MT', size=24, weight=5) at 0x109f04cd0
 --- Family 'Gurmukhi Sangam MN'
 371 Font(name='GurmukhiSangamMN', family='Gurmukhi Sangam MN', size=12, weight=5) at 0x109f04c10
 372+Font(name='GurmukhiSangamMN', family='Gurmukhi Sangam MN', size=24, weight=5) at 0x109f04e50
 373 Font(name='GurmukhiSangamMN-Bold', family='Gurmukhi Sangam MN', size=12, traits='Bold', weight=9) at 0x109f04f10
 374+Font(name='GurmukhiSangamMN-Bold', family='Gurmukhi Sangam MN', size=24, traits='Bold', weight=9) at 0x109f0c050
 --- Family 'Handwriting - Dakota'
 375 Font(name='Handwriting-Dakota', family='Handwriting - Dakota', size=12, weight=5) at 0x109f0c110
 376+Font(name='Handwriting-Dakota', family='Handwriting - Dakota', size=24, weight=5) at 0x109f0c250
 --- Family 'Heiti SC'
 377 Font(name='STHeitiSC-Light', family='Heiti SC', size=12, weight=3) at 0x109f0c410
 378+Font(name='STHeitiSC-Light', family='Heiti SC', size=24, weight=3) at 0x109f0c590
 379 Font(name='STHeitiSC-Medium', family='Heiti SC', size=12, traits='Bold', weight=9) at 0x109f0c6d0
 380+Font(name='STHeitiSC-Medium', family='Heiti SC', size=24, traits='Bold', weight=9) at 0x109f0c410
 --- Family 'Heiti TC'
 381 Font(name='STHeitiTC-Light', family='Heiti TC', size=12, weight=3) at 0x109f0c850
 382+Font(name='STHeitiTC-Light', family='Heiti TC', size=24, weight=3) at 0x109f0c6d0
 383 Font(name='STHeitiTC-Medium', family='Heiti TC', size=12, traits='Bold', weight=9) at 0x109f0cbd0
 384+Font(name='STHeitiTC-Medium', family='Heiti TC', size=24, traits='Bold', weight=9) at 0x109f0c850
 --- Family 'Helvetica'
 385 Font(name='Helvetica', family='Helvetica', size=12, weight=5) at 0x109f0cd10
 386+Font(name='Helvetica', family='Helvetica', size=24, weight=5) at 0x109f0c850
 387 Font(name='Helvetica-Oblique', family='Helvetica', size=12, traits='Italic', weight=5) at 0x109f0ced0
 388+Font(name='Helvetica-Oblique', family='Helvetica', size=24, traits='Italic', weight=5) at 0x109f0cd10
 389 Font(name='Helvetica-Light', family='Helvetica', size=12, weight=3) at 0x109f1c090
 390+Font(name='Helvetica-Light', family='Helvetica', size=24, weight=3) at 0x109f0ced0
 391 Font(name='Helvetica-LightOblique', family='Helvetica', size=12, traits='Italic', weight=3) at 0x109f1c1d0
 392+Font(name='Helvetica-LightOblique', family='Helvetica', size=24, traits='Italic', weight=3) at 0x109f1c090
 393 Font(name='Helvetica-Bold', family='Helvetica', size=12, traits='Bold', weight=9) at 0x109f1c490
 394+Font(name='Helvetica-Bold', family='Helvetica', size=24, traits='Bold', weight=9) at 0x109f1c390
 395 Font(name='Helvetica-BoldOblique', family='Helvetica', size=12, traits='Bold Italic', weight=9) at 0x109f1c5d0
 396+Font(name='Helvetica-BoldOblique', family='Helvetica', size=24, traits='Bold Italic', weight=9) at 0x109f1c490
 --- Family 'Helvetica Neue'
 397 Font(name='HelveticaNeue', family='Helvetica Neue', size=12, weight=5) at 0x109f1c510
 398+Font(name='HelveticaNeue', family='Helvetica Neue', size=24, weight=5) at 0x109f1c910
 399 Font(name='HelveticaNeue-Italic', family='Helvetica Neue', size=12, traits='Italic', weight=5) at 0x109f1c390
 400+Font(name='HelveticaNeue-Italic', family='Helvetica Neue', size=24, traits='Italic', weight=5) at 0x109f1ca50
 401 Font(name='HelveticaNeue-UltraLight', family='Helvetica Neue', size=12, weight=2) at 0x109f1ca90
 402+Font(name='HelveticaNeue-UltraLight', family='Helvetica Neue', size=24, weight=2) at 0x109f1ccd0
 403 Font(name='HelveticaNeue-UltraLightItalic', family='Helvetica Neue', size=12, traits='Italic', weight=2) at 0x109f1c390
 404+Font(name='HelveticaNeue-UltraLightItalic', family='Helvetica Neue', size=24, traits='Italic', weight=2) at 0x109f1c9d0
 405 Font(name='HelveticaNeue-Thin', family='Helvetica Neue', size=12, weight=3) at 0x109f1c850
 406+Font(name='HelveticaNeue-Thin', family='Helvetica Neue', size=24, weight=3) at 0x109f1cfd0
 407 Font(name='HelveticaNeue-ThinItalic', family='Helvetica Neue', size=12, traits='Italic', weight=3) at 0x109f1ce10
 408+Font(name='HelveticaNeue-LightItalic', family='Helvetica Neue', size=24, traits='Italic', weight=3) at 0x10ab9f290
 409 Font(name='HelveticaNeue-Light', family='Helvetica Neue', size=12, weight=3) at 0x10ab9f350
 410+Font(name='HelveticaNeue-Thin', family='Helvetica Neue', size=24, weight=3) at 0x109f1ce10
 411 Font(name='HelveticaNeue-LightItalic', family='Helvetica Neue', size=12, traits='Italic', weight=3) at 0x10ab9f290
 412+Font(name='HelveticaNeue-LightItalic', family='Helvetica Neue', size=24, traits='Italic', weight=3) at 0x10ab9f3d0
 413 Font(name='HelveticaNeue-Medium', family='Helvetica Neue', size=12, weight=6) at 0x10ab9f490
 414+Font(name='HelveticaNeue-Medium', family='Helvetica Neue', size=24, weight=6) at 0x10ab9f650
 415 Font(name='HelveticaNeue-MediumItalic', family='Helvetica Neue', size=12, traits='Italic', weight=7) at 0x10ab9f6d0
 416+Font(name='HelveticaNeue-MediumItalic', family='Helvetica Neue', size=24, traits='Italic', weight=7) at 0x10ab9f410
 417 Font(name='HelveticaNeue-Bold', family='Helvetica Neue', size=12, traits='Bold', weight=9) at 0x10ab9f7d0
 418+Font(name='HelveticaNeue-Bold', family='Helvetica Neue', size=24, traits='Bold', weight=9) at 0x10ab9f790
 419 Font(name='HelveticaNeue-BoldItalic', family='Helvetica Neue', size=12, traits='Bold Italic', weight=9) at 0x10ab9f0d0
 420+Font(name='HelveticaNeue-BoldItalic', family='Helvetica Neue', size=24, traits='Bold Italic', weight=9) at 0x10ab9f7d0
 421 Font(name='HelveticaNeue-CondensedBold', family='Helvetica Neue', size=12, traits='Bold Condensed', weight=9) at 0x10ab9fad0
 422+Font(name='HelveticaNeue-Bold', family='Helvetica Neue', size=24, traits='Bold', weight=9) at 0x10ab9f7d0
 423 Font(name='HelveticaNeue-CondensedBlack', family='Helvetica Neue', size=12, traits='Bold Condensed', weight=11) at 0x10ab9fd50
 424+Font(name='HelveticaNeue-CondensedBlack', family='Helvetica Neue', size=24, traits='Bold Condensed', weight=11) at 0x10ab9fbd0
 --- Family 'Herculanum'
 425 Font(name='Herculanum', family='Herculanum', size=12, weight=5) at 0x10ab9fad0
 426+Font(name='Herculanum', family='Herculanum', size=24, weight=5) at 0x10ab9fbd0
 --- Family 'Hiragino Kaku Gothic Pro'
 427 Font(name='HiraKakuPro-W3', family='Hiragino Kaku Gothic Pro', size=12, weight=4) at 0x10ab9fed0
 428+Font(name='HiraKakuPro-W3', family='Hiragino Kaku Gothic Pro', size=24, weight=4) at 0x10aba2210
 429 Font(name='HiraKakuPro-W6', family='Hiragino Kaku Gothic Pro', size=12, traits='Bold', weight=8) at 0x10aba2110
 430+Font(name='HiraKakuPro-W6', family='Hiragino Kaku Gothic Pro', size=24, traits='Bold', weight=8) at 0x10aba2210
 --- Family 'Hiragino Kaku Gothic ProN'
 431 Font(name='HiraKakuProN-W3', family='Hiragino Kaku Gothic ProN', size=12, weight=4) at 0x10aba22d0
 432+Font(name='HiraKakuProN-W3', family='Hiragino Kaku Gothic ProN', size=24, weight=4) at 0x10aba2610
 433 Font(name='HiraKakuProN-W6', family='Hiragino Kaku Gothic ProN', size=12, traits='Bold', weight=8) at 0x10aba2210
 434+Font(name='HiraKakuProN-W6', family='Hiragino Kaku Gothic ProN', size=24, traits='Bold', weight=8) at 0x10aba25d0
 --- Family 'Hiragino Kaku Gothic Std'
 435 Font(name='HiraKakuStd-W8', family='Hiragino Kaku Gothic Std', size=12, traits='Bold', weight=10) at 0x10aba2210
 436+Font(name='HiraKakuStd-W8', family='Hiragino Kaku Gothic Std', size=24, traits='Bold', weight=10) at 0x10aba2750
 --- Family 'Hiragino Kaku Gothic StdN'
 437 Font(name='HiraKakuStdN-W8', family='Hiragino Kaku Gothic StdN', size=12, traits='Bold', weight=10) at 0x10aba2210
 438+Font(name='HiraKakuStdN-W8', family='Hiragino Kaku Gothic StdN', size=24, traits='Bold', weight=10) at 0x10aba2b90
 --- Family 'Hiragino Maru Gothic Pro'
 439 Font(name='HiraMaruPro-W4', family='Hiragino Maru Gothic Pro', size=12, weight=5) at 0x10aba2210
 440+Font(name='HiraMaruPro-W4', family='Hiragino Maru Gothic Pro', size=24, weight=5) at 0x10aba2e50
 --- Family 'Hiragino Maru Gothic ProN'
 441 Font(name='HiraMaruProN-W4', family='Hiragino Maru Gothic ProN', size=12, weight=5) at 0x10abb2110
 442+Font(name='HiraMaruProN-W4', family='Hiragino Maru Gothic ProN', size=24, weight=5) at 0x10abb2290
 --- Family 'Hiragino Mincho Pro'
 443 Font(name='HiraMinPro-W3', family='Hiragino Mincho Pro', size=12, weight=4) at 0x10abb23d0
 444+Font(name='HiraMinPro-W3', family='Hiragino Mincho Pro', size=24, weight=4) at 0x10abb2510
 445 Font(name='HiraMinPro-W6', family='Hiragino Mincho Pro', size=12, traits='Bold', weight=8) at 0x10abb2490
 446+Font(name='HiraMinPro-W6', family='Hiragino Mincho Pro', size=24, traits='Bold', weight=8) at 0x10abb23d0
 --- Family 'Hiragino Mincho ProN'
 447 Font(name='HiraMinProN-W3', family='Hiragino Mincho ProN', size=12, weight=4) at 0x10abb2710
 448+Font(name='HiraMinProN-W3', family='Hiragino Mincho ProN', size=24, weight=4) at 0x10abb28d0
 449 Font(name='HiraMinProN-W6', family='Hiragino Mincho ProN', size=12, traits='Bold', weight=8) at 0x10abb23d0
 450+Font(name='HiraMinProN-W6', family='Hiragino Mincho ProN', size=24, traits='Bold', weight=8) at 0x10abb2990
 --- Family 'Hiragino Sans'
 451 Font(name='HiraginoSans-W0', family='Hiragino Sans', size=12, traits='SansSerif', weight=2) at 0x10abb2a10
 452+Font(name='HiraginoSans-W0', family='Hiragino Sans', size=24, traits='SansSerif', weight=2) at 0x10abb29d0
 453 Font(name='HiraginoSans-W1', family='Hiragino Sans', size=12, traits='SansSerif', weight=3) at 0x10abb2ed0
 454+Font(name='HiraginoSans-W1', family='Hiragino Sans', size=24, traits='SansSerif', weight=3) at 0x10abb2a10
 455 Font(name='HiraginoSans-W2', family='Hiragino Sans', size=12, traits='SansSerif', weight=3) at 0x10abbb190
 456+Font(name='HiraginoSans-W1', family='Hiragino Sans', size=24, traits='SansSerif', weight=3) at 0x10abb2ed0
 457 Font(name='HiraginoSans-W3', family='Hiragino Sans', size=12, traits='SansSerif', weight=4) at 0x10abbb2d0
 458+Font(name='HiraginoSans-W3', family='Hiragino Sans', size=24, traits='SansSerif', weight=4) at 0x10abbb190
 459 Font(name='HiraginoSans-W4', family='Hiragino Sans', size=12, traits='SansSerif', weight=5) at 0x10abbb550
 460+Font(name='HiraginoSans-W4', family='Hiragino Sans', size=24, traits='SansSerif', weight=5) at 0x10abbb2d0
 461 Font(name='HiraginoSans-W5', family='Hiragino Sans', size=12, traits='Bold SansSerif', weight=9) at 0x10abbb750
 462+Font(name='HiraginoSans-W7', family='Hiragino Sans', size=24, traits='Bold SansSerif', weight=9) at 0x10abbb8d0
 463 Font(name='HiraginoSans-W6', family='Hiragino Sans', size=12, traits='Bold SansSerif', weight=9) at 0x10abbb550
 464+Font(name='HiraginoSans-W7', family='Hiragino Sans', size=24, traits='Bold SansSerif', weight=9) at 0x10abbb810
 465 Font(name='HiraginoSans-W7', family='Hiragino Sans', size=12, traits='Bold SansSerif', weight=9) at 0x10abbb8d0
 466+Font(name='HiraginoSans-W7', family='Hiragino Sans', size=24, traits='Bold SansSerif', weight=9) at 0x10abbb990
 467 Font(name='HiraginoSans-W8', family='Hiragino Sans', size=12, traits='Bold SansSerif', weight=10) at 0x10abbb810
 468+Font(name='HiraginoSans-W8', family='Hiragino Sans', size=24, traits='Bold SansSerif', weight=10) at 0x10abbbb10
 469 Font(name='HiraginoSans-W9', family='Hiragino Sans', size=12, traits='Bold SansSerif', weight=12) at 0x10abbb8d0
 470+Font(name='HiraginoSans-W9', family='Hiragino Sans', size=24, traits='Bold SansSerif', weight=12) at 0x10abbbd10
 --- Family 'Hiragino Sans GB'
 471 Font(name='HiraginoSansGB-W3', family='Hiragino Sans GB', size=12, traits='SansSerif', weight=4) at 0x10abbbf10
 472+Font(name='HiraginoSansGB-W3', family='Hiragino Sans GB', size=24, traits='SansSerif', weight=4) at 0x10abc7050
 473 Font(name='HiraginoSansGB-W6', family='Hiragino Sans GB', size=12, traits='Bold SansSerif', weight=8) at 0x10abc7250
 474+Font(name='HiraginoSansGB-W6', family='Hiragino Sans GB', size=24, traits='Bold SansSerif', weight=8) at 0x10abc7150
 --- Family 'Hoefler Text'
 475 Font(name='HoeflerText-Regular', family='Hoefler Text', size=12, weight=5) at 0x10abc7050
 476+Font(name='HoeflerText-Regular', family='Hoefler Text', size=24, weight=5) at 0x10abc7550
 477 Font(name='HoeflerText-Ornaments', family='Hoefler Text', size=12, weight=5) at 0x10abc7510
 478+Font(name='HoeflerText-Regular', family='Hoefler Text', size=24, weight=5) at 0x10abc7050
 479 Font(name='HoeflerText-Italic', family='Hoefler Text', size=12, traits='Italic', weight=5) at 0x10abc7710
 480+Font(name='HoeflerText-Italic', family='Hoefler Text', size=24, traits='Italic', weight=5) at 0x10abc7510
 481 Font(name='HoeflerText-Black', family='Hoefler Text', size=12, traits='Bold', weight=9) at 0x10abc77d0
 482+Font(name='HoeflerText-Black', family='Hoefler Text', size=24, traits='Bold', weight=9) at 0x10abc7710
 483 Font(name='HoeflerText-BlackItalic', family='Hoefler Text', size=12, traits='Bold Italic', weight=9) at 0x10abc7990
 484+Font(name='HoeflerText-BlackItalic', family='Hoefler Text', size=24, traits='Bold Italic', weight=9) at 0x10abc77d0
 --- Family 'Impact'
 485 Font(name='Impact', family='Impact', size=12, traits='Bold Condensed', weight=11) at 0x10abc7a50
 486+Font(name='Impact', family='Impact', size=24, traits='Bold Condensed', weight=11) at 0x10abc7d50
 --- Family 'InaiMathi'
 487 Font(name='InaiMathi', family='InaiMathi', size=12, weight=5) at 0x10abc77d0
 488+Font(name='InaiMathi', family='InaiMathi', size=24, weight=5) at 0x10abc7d50
 489 Font(name='InaiMathi-Bold', family='InaiMathi', size=12, traits='Bold', weight=9) at 0x10abd1090
 490+Font(name='InaiMathi-Bold', family='InaiMathi', size=24, traits='Bold', weight=9) at 0x10abd10d0
 --- Family 'Iowan Old Style'
 491 Font(name='IowanOldStyle-Roman', family='Iowan Old Style', size=12, weight=5) at 0x10abd1210
 492+Font(name='IowanOldStyle-Roman', family='Iowan Old Style', size=24, weight=5) at 0x10abd1410
 493 Font(name='IowanOldStyle-Titling', family='Iowan Old Style', size=12, weight=5) at 0x10abd13d0
 494+Font(name='IowanOldStyle-Roman', family='Iowan Old Style', size=24, weight=5) at 0x10abd1210
 495 Font(name='IowanOldStyle-Italic', family='Iowan Old Style', size=12, traits='Italic', weight=5) at 0x10abd16d0
 496+Font(name='IowanOldStyle-Italic', family='Iowan Old Style', size=24, traits='Italic', weight=5) at 0x10abd1690
 497 Font(name='IowanOldStyle-Bold', family='Iowan Old Style', size=12, traits='Bold', weight=9) at 0x10abd1810
 498+Font(name='IowanOldStyle-Bold', family='Iowan Old Style', size=24, traits='Bold', weight=9) at 0x10abd1510
 499 Font(name='IowanOldStyle-BoldItalic', family='Iowan Old Style', size=12, traits='Bold Italic', weight=9) at 0x10abd1410
 500+Font(name='IowanOldStyle-BoldItalic', family='Iowan Old Style', size=24, traits='Bold Italic', weight=9) at 0x10abd1810
 501 Font(name='IowanOldStyle-Black', family='Iowan Old Style', size=12, traits='Bold', weight=11) at 0x10abd1b50
 502+Font(name='IowanOldStyle-Black', family='Iowan Old Style', size=24, traits='Bold', weight=11) at 0x10abd1a90
 503 Font(name='IowanOldStyle-BlackItalic', family='Iowan Old Style', size=12, traits='Bold Italic', weight=11) at 0x10abd19d0
 504+Font(name='IowanOldStyle-BlackItalic', family='Iowan Old Style', size=24, traits='Bold Italic', weight=11) at 0x10abd1b50
 --- Family 'ITF Devanagari'
 505 Font(name='ITFDevanagari-Book', family='ITF Devanagari', size=12, weight=5) at 0x10abdc050
 506+Font(name='ITFDevanagari-Book', family='ITF Devanagari', size=24, weight=5) at 0x10abd1ed0
 507 Font(name='ITFDevanagari-Light', family='ITF Devanagari', size=12, weight=3) at 0x10abdc150
 508+Font(name='ITFDevanagari-Light', family='ITF Devanagari', size=24, weight=3) at 0x10abdc250
 509 Font(name='ITFDevanagari-Medium', family='ITF Devanagari', size=12, weight=6) at 0x10abdc050
 510+Font(name='ITFDevanagari-Medium', family='ITF Devanagari', size=24, weight=6) at 0x10abdc150
 511 Font(name='ITFDevanagari-Demi', family='ITF Devanagari', size=12, traits='Bold', weight=9) at 0x10abdc4d0
 512+Font(name='ITFDevanagari-Bold', family='ITF Devanagari', size=24, traits='Bold', weight=9) at 0x10abdc550
 513 Font(name='ITFDevanagari-Bold', family='ITF Devanagari', size=12, traits='Bold', weight=9) at 0x10abdc350
 514+Font(name='ITFDevanagari-Bold', family='ITF Devanagari', size=24, traits='Bold', weight=9) at 0x10abdc990
 --- Family 'ITF Devanagari Marathi'
 515 Font(name='ITFDevanagariMarathi-Book', family='ITF Devanagari Marathi', size=12, weight=5) at 0x10abdc9d0
 516+Font(name='ITFDevanagariMarathi-Book', family='ITF Devanagari Marathi', size=24, weight=5) at 0x10abdc990
 517 Font(name='ITFDevanagariMarathi-Light', family='ITF Devanagari Marathi', size=12, weight=3) at 0x10abdcc50
 518+Font(name='ITFDevanagariMarathi-Light', family='ITF Devanagari Marathi', size=24, weight=3) at 0x10abdc990
 519 Font(name='ITFDevanagariMarathi-Medium', family='ITF Devanagari Marathi', size=12, weight=6) at 0x10abdc9d0
 520+Font(name='ITFDevanagariMarathi-Medium', family='ITF Devanagari Marathi', size=24, weight=6) at 0x10abdc990
 521 Font(name='ITFDevanagariMarathi-Demi', family='ITF Devanagari Marathi', size=12, traits='Bold', weight=9) at 0x10abdcad0
 522+Font(name='ITFDevanagariMarathi-Bold', family='ITF Devanagari Marathi', size=24, traits='Bold', weight=9) at 0x10abdcdd0
 523 Font(name='ITFDevanagariMarathi-Bold', family='ITF Devanagari Marathi', size=12, traits='Bold', weight=9) at 0x10abb5310
 524+Font(name='ITFDevanagariMarathi-Bold', family='ITF Devanagari Marathi', size=24, traits='Bold', weight=9) at 0x10abdcad0
 --- Family 'Jazz LET'
 525 Font(name='JazzLetPlain', family='Jazz LET', size=12, traits='Bold Expanded', weight=11) at 0x10abb5490
 526+Font(name='JazzLetPlain', family='Jazz LET', size=24, traits='Bold Expanded', weight=11) at 0x10abdcf50
 --- Family 'Kailasa'
 527 Font(name='Kailasa', family='Kailasa', size=12, weight=5) at 0x10abb55d0
 528+Font(name='Kailasa', family='Kailasa', size=24, weight=5) at 0x10abb5890
 529 Font(name='Kailasa-Bold', family='Kailasa', size=12, traits='Bold', weight=9) at 0x10abb5850
 530+Font(name='Kailasa-Bold', family='Kailasa', size=24, traits='Bold', weight=9) at 0x10abb5490
 --- Family 'Kannada MN'
 531 Font(name='KannadaMN', family='Kannada MN', size=12, weight=5) at 0x10abb55d0
 532+Font(name='KannadaMN', family='Kannada MN', size=24, weight=5) at 0x10abb5490
 533 Font(name='KannadaMN-Bold', family='Kannada MN', size=12, traits='Bold', weight=9) at 0x10abb5d90
 534+Font(name='KannadaMN-Bold', family='Kannada MN', size=24, traits='Bold', weight=9) at 0x10abb55d0
 --- Family 'Kannada Sangam MN'
 535 Font(name='KannadaSangamMN', family='Kannada Sangam MN', size=12, weight=5) at 0x10abb5ed0
 536+Font(name='KannadaSangamMN', family='Kannada Sangam MN', size=24, weight=5) at 0x10fd8c0d0
 537 Font(name='KannadaSangamMN-Bold', family='Kannada Sangam MN', size=12, traits='Bold', weight=9) at 0x10fd8c050
 538+Font(name='KannadaSangamMN-Bold', family='Kannada Sangam MN', size=24, traits='Bold', weight=9) at 0x10fd8c0d0
 --- Family 'Kefa'
 539 Font(name='Kefa-Regular', family='Kefa', size=12, weight=5) at 0x10fd8c4d0
 540+Font(name='Kefa-Regular', family='Kefa', size=24, weight=5) at 0x10fd8c0d0
 541 Font(name='Kefa-Bold', family='Kefa', size=12, traits='Bold', weight=9) at 0x10fd8c710
 542+Font(name='Kefa-Bold', family='Kefa', size=24, traits='Bold', weight=9) at 0x10fd8c5d0
 --- Family 'Khmer MN'
 543 Font(name='KhmerMN', family='Khmer MN', size=12, weight=5) at 0x10fd8c4d0
 544+Font(name='KhmerMN', family='Khmer MN', size=24, weight=5) at 0x10fd8c5d0
 545 Font(name='KhmerMN-Bold', family='Khmer MN', size=12, traits='Bold', weight=9) at 0x10fd8cc10
 546+Font(name='KhmerMN-Bold', family='Khmer MN', size=24, traits='Bold', weight=9) at 0x10fd8ca90
 --- Family 'Khmer Sangam MN'
 547 Font(name='KhmerSangamMN', family='Khmer Sangam MN', size=12, weight=5) at 0x10fd8ce50
 548+Font(name='KhmerSangamMN', family='Khmer Sangam MN', size=24, weight=5) at 0x10fd8cf50
 --- Family 'Kohinoor Bangla'
 549 Font(name='KohinoorBangla-Regular', family='Kohinoor Bangla', size=12, weight=5) at 0x10fd96090
 550+Font(name='KohinoorBangla-Regular', family='Kohinoor Bangla', size=24, weight=5) at 0x10fd96210
 551 Font(name='KohinoorBangla-Light', family='Kohinoor Bangla', size=12, weight=3) at 0x10fd96390
 552+Font(name='KohinoorBangla-Light', family='Kohinoor Bangla', size=24, weight=3) at 0x10fd96490
 553 Font(name='KohinoorBangla-Medium', family='Kohinoor Bangla', size=12, weight=6) at 0x10fd96610
 554+Font(name='KohinoorBangla-Medium', family='Kohinoor Bangla', size=24, weight=6) at 0x10fd964d0
 555 Font(name='KohinoorBangla-Semibold', family='Kohinoor Bangla', size=12, traits='Bold', weight=9) at 0x10fd96390
 556+Font(name='KohinoorBangla-Bold', family='Kohinoor Bangla', size=24, traits='Bold', weight=9) at 0x10fd96350
 557 Font(name='KohinoorBangla-Bold', family='Kohinoor Bangla', size=12, traits='Bold', weight=9) at 0x10fd96610
 558+Font(name='KohinoorBangla-Bold', family='Kohinoor Bangla', size=24, traits='Bold', weight=9) at 0x10fd96490
 --- Family 'Kohinoor Devanagari'
 559 Font(name='KohinoorDevanagari-Regular', family='Kohinoor Devanagari', size=12, weight=5) at 0x10fd96ad0
 560+Font(name='KohinoorDevanagari-Regular', family='Kohinoor Devanagari', size=24, weight=5) at 0x10fd96490
 561 Font(name='KohinoorDevanagari-Light', family='Kohinoor Devanagari', size=12, weight=3) at 0x10fd96cd0
 562+Font(name='KohinoorDevanagari-Light', family='Kohinoor Devanagari', size=24, weight=3) at 0x10fd96490
 563 Font(name='KohinoorDevanagari-Medium', family='Kohinoor Devanagari', size=12, weight=6) at 0x10fd96ad0
 564+Font(name='KohinoorDevanagari-Medium', family='Kohinoor Devanagari', size=24, weight=6) at 0x10fd96d50
 565 Font(name='KohinoorDevanagari-Semibold', family='Kohinoor Devanagari', size=12, traits='Bold', weight=9) at 0x10fda1110
 566+Font(name='KohinoorDevanagari-Bold', family='Kohinoor Devanagari', size=24, traits='Bold', weight=9) at 0x10fd96ad0
 567 Font(name='KohinoorDevanagari-Bold', family='Kohinoor Devanagari', size=12, traits='Bold', weight=9) at 0x10fda1290
 568+Font(name='KohinoorDevanagari-Bold', family='Kohinoor Devanagari', size=24, traits='Bold', weight=9) at 0x10fd96490
 --- Family 'Kohinoor Telugu'
 569 Font(name='KohinoorTelugu-Regular', family='Kohinoor Telugu', size=12, weight=5) at 0x10fda14d0
 570+Font(name='KohinoorTelugu-Regular', family='Kohinoor Telugu', size=24, weight=5) at 0x10fda1650
 571 Font(name='KohinoorTelugu-Light', family='Kohinoor Telugu', size=12, weight=3) at 0x10fda1510
 572+Font(name='KohinoorTelugu-Light', family='Kohinoor Telugu', size=24, weight=3) at 0x10fda1750
 573 Font(name='KohinoorTelugu-Medium', family='Kohinoor Telugu', size=12, weight=6) at 0x10fda18d0
 574+Font(name='KohinoorTelugu-Medium', family='Kohinoor Telugu', size=24, weight=6) at 0x10fda1790
 575 Font(name='KohinoorTelugu-Semibold', family='Kohinoor Telugu', size=12, traits='Bold', weight=9) at 0x10fda1510
 576+Font(name='KohinoorTelugu-Bold', family='Kohinoor Telugu', size=24, traits='Bold', weight=9) at 0x10fda1150
 577 Font(name='KohinoorTelugu-Bold', family='Kohinoor Telugu', size=12, traits='Bold', weight=9) at 0x10fda18d0
 578+Font(name='KohinoorTelugu-Bold', family='Kohinoor Telugu', size=24, traits='Bold', weight=9) at 0x10fda1750
 --- Family 'Kokonor'
 579 Font(name='Kokonor', family='Kokonor', size=12, weight=5) at 0x10fda1c50
 580+Font(name='Kokonor', family='Kokonor', size=24, weight=5) at 0x10fda1750
 --- Family 'Krungthep'
 581 Font(name='Krungthep', family='Krungthep', size=12, traits='Bold', weight=9) at 0x10fda1c50
 582+Font(name='Krungthep', family='Krungthep', size=24, traits='Bold', weight=9) at 0x10fdae210
 --- Family 'KufiStandardGK'
 583 Font(name='KufiStandardGK', family='KufiStandardGK', size=12, weight=5) at 0x10fdae0d0
 584+Font(name='KufiStandardGK', family='KufiStandardGK', size=24, weight=5) at 0x10fdae450
 --- Family 'Lao MN'
 585 Font(name='LaoMN', family='Lao MN', size=12, weight=5) at 0x10fdae390
 586+Font(name='LaoMN', family='Lao MN', size=24, weight=5) at 0x10fdae450
 587 Font(name='LaoMN-Bold', family='Lao MN', size=12, traits='Bold', weight=9) at 0x10fdae750
 588+Font(name='LaoMN-Bold', family='Lao MN', size=24, traits='Bold', weight=9) at 0x10fdae5d0
 --- Family 'Lao Sangam MN'
 589 Font(name='LaoSangamMN', family='Lao Sangam MN', size=12, weight=5) at 0x10fdae990
 590+Font(name='LaoSangamMN', family='Lao Sangam MN', size=24, weight=5) at 0x10fdae390
 --- Family 'Lucida Grande'
 591 Font(name='LucidaGrande', family='Lucida Grande', size=12, weight=5) at 0x10fdaec10
 592+Font(name='LucidaGrande', family='Lucida Grande', size=24, weight=5) at 0x10fdaedd0
 593 Font(name='LucidaGrande-Bold', family='Lucida Grande', size=12, traits='Bold', weight=9) at 0x10fdaeb50
 594+Font(name='LucidaGrande-Bold', family='Lucida Grande', size=24, traits='Bold', weight=9) at 0x10fdaec10
 --- Family 'Luminari'
 595 Font(name='Luminari-Regular', family='Luminari', size=12, weight=5) at 0x118b96050
 596+Font(name='Luminari-Regular', family='Luminari', size=24, weight=5) at 0x118b96150
 --- Family 'Malayalam MN'
 597 Font(name='MalayalamMN', family='Malayalam MN', size=12, weight=5) at 0x118b96250
 598+Font(name='MalayalamMN', family='Malayalam MN', size=24, weight=5) at 0x118b96050
 599 Font(name='MalayalamMN-Bold', family='Malayalam MN', size=12, traits='Bold', weight=9) at 0x118b96590
 600+Font(name='MalayalamMN-Bold', family='Malayalam MN', size=24, traits='Bold', weight=9) at 0x118b96250
 --- Family 'Malayalam Sangam MN'
 601 Font(name='MalayalamSangamMN', family='Malayalam Sangam MN', size=12, weight=5) at 0x118b966d0
 602+Font(name='MalayalamSangamMN', family='Malayalam Sangam MN', size=24, weight=5) at 0x118b96590
 603 Font(name='MalayalamSangamMN-Bold', family='Malayalam Sangam MN', size=12, traits='Bold', weight=9) at 0x118b96a50
 604+Font(name='MalayalamSangamMN-Bold', family='Malayalam Sangam MN', size=24, traits='Bold', weight=9) at 0x118b966d0
 --- Family 'Marion'
 605 Font(name='Marion-Regular', family='Marion', size=12, weight=5) at 0x118b96b50
 606+Font(name='Marion-Regular', family='Marion', size=24, weight=5) at 0x118b96d90
 607 Font(name='Marion-Italic', family='Marion', size=12, traits='Italic', weight=5) at 0x118b96ed0
 608+Font(name='Marion-Italic', family='Marion', size=24, traits='Italic', weight=5) at 0x118b96b50
 609 Font(name='Marion-Bold', family='Marion', size=12, traits='Bold', weight=9) at 0x10fd82050
 610+Font(name='Marion-Bold', family='Marion', size=24, traits='Bold', weight=9) at 0x10fd82090
 --- Family 'Marker Felt'
 611 Font(name='MarkerFelt-Thin', family='Marker Felt', size=12, weight=3) at 0x10fd821d0
 612+Font(name='MarkerFelt-Thin', family='Marker Felt', size=24, weight=3) at 0x10fd82550
 613 Font(name='MarkerFelt-Wide', family='Marker Felt', size=12, traits='Bold', weight=9) at 0x10fd824d0
 614+Font(name='MarkerFelt-Wide', family='Marker Felt', size=24, traits='Bold', weight=9) at 0x10fd821d0
 --- Family 'Menlo'
 615 Font(name='Menlo-Regular', family='Menlo', size=12, traits='MonoSpace', weight=5) at 0x10fd825d0
 616+Font(name='Menlo-Regular', family='Menlo', size=24, traits='MonoSpace', weight=5) at 0x10fd82990
 617 Font(name='Menlo-Italic', family='Menlo', size=12, traits='Italic MonoSpace', weight=5) at 0x10fd82a10
 618+Font(name='Menlo-Italic', family='Menlo', size=24, traits='Italic MonoSpace', weight=5) at 0x10fd82c10
 619 Font(name='Menlo-Bold', family='Menlo', size=12, traits='Bold MonoSpace', weight=9) at 0x10fd82c50
 620+Font(name='Menlo-Bold', family='Menlo', size=24, traits='Bold MonoSpace', weight=9) at 0x10fd82dd0
 621 Font(name='Menlo-BoldItalic', family='Menlo', size=12, traits='Bold Italic MonoSpace', weight=9) at 0x10fd82e10
 622+Font(name='Menlo-BoldItalic', family='Menlo', size=24, traits='Bold Italic MonoSpace', weight=9) at 0x10fd82f90
 --- Family 'Microsoft Sans Serif'
 623 Font(name='MicrosoftSansSerif', family='Microsoft Sans Serif', size=12, traits='SansSerif', weight=5) at 0x118baa090
 624+Font(name='MicrosoftSansSerif', family='Microsoft Sans Serif', size=24, traits='SansSerif', weight=5) at 0x118baa1d0
 --- Family 'Mishafi'
 625 Font(name='DiwanMishafi', family='Mishafi', size=12, weight=5) at 0x118baa410
 626+Font(name='DiwanMishafi', family='Mishafi', size=24, weight=5) at 0x118baa1d0
 --- Family 'Mishafi Gold'
 627 Font(name='DiwanMishafiGold', family='Mishafi Gold', size=12, weight=5) at 0x118baa650
 628+Font(name='DiwanMishafiGold', family='Mishafi Gold', size=24, weight=5) at 0x118baa750
 --- Family 'Mona Lisa Solid ITC TT'
 629 Font(name='MonaLisaSolidITCTT', family='Mona Lisa Solid ITC TT', size=12, traits='Bold Condensed', weight=9) at 0x118baa950
 630+Font(name='MonaLisaSolidITCTT', family='Mona Lisa Solid ITC TT', size=24, traits='Bold Condensed', weight=9) at 0x118baab10
 --- Family 'Monaco'
 631 Font(name='Monaco', family='Monaco', size=12, traits='MonoSpace', weight=5) at 0x118baab90
 632+Font(name='Monaco', family='Monaco', size=24, traits='MonoSpace', weight=5) at 0x118baab50
 --- Family 'Mshtakan'
 633 Font(name='Mshtakan', family='Mshtakan', size=12, weight=5) at 0x118baaf50
 634+Font(name='Mshtakan', family='Mshtakan', size=24, weight=5) at 0x118bb7190
 635 Font(name='MshtakanOblique', family='Mshtakan', size=12, traits='Italic', weight=5) at 0x118bb7150
 636+Font(name='MshtakanOblique', family='Mshtakan', size=24, traits='Italic', weight=5) at 0x118bb7190
 637 Font(name='MshtakanBold', family='Mshtakan', size=12, traits='Bold', weight=9) at 0x118bb7090
 638+Font(name='MshtakanBold', family='Mshtakan', size=24, traits='Bold', weight=9) at 0x118bb7450
 639 Font(name='MshtakanBoldOblique', family='Mshtakan', size=12, traits='Bold Italic', weight=9) at 0x118bb7310
 640+Font(name='MshtakanBoldOblique', family='Mshtakan', size=24, traits='Bold Italic', weight=9) at 0x118bb7710
 --- Family 'Muna'
 641 Font(name='Muna', family='Muna', size=12, weight=5) at 0x118bb7090
 642+Font(name='Muna', family='Muna', size=24, weight=5) at 0x118bb7710
 643 Font(name='MunaBold', family='Muna', size=12, traits='Bold', weight=9) at 0x118bb7990
 644+Font(name='MunaBold', family='Muna', size=24, traits='Bold', weight=9) at 0x118bb79d0
 645 Font(name='MunaBlack', family='Muna', size=12, traits='Bold', weight=11) at 0x118bb7a90
 646+Font(name='MunaBlack', family='Muna', size=24, traits='Bold', weight=11) at 0x118bb7090
 --- Family 'Myanmar MN'
 647 Font(name='MyanmarMN', family='Myanmar MN', size=12, weight=5) at 0x118bb7990
 648+Font(name='MyanmarMN', family='Myanmar MN', size=24, weight=5) at 0x118bb7090
 649 Font(name='MyanmarMN-Bold', family='Myanmar MN', size=12, traits='Bold', weight=9) at 0x118bc0110
 650+Font(name='MyanmarMN-Bold', family='Myanmar MN', size=24, traits='Bold', weight=9) at 0x118bc0050
 --- Family 'Myanmar Sangam MN'
 651 Font(name='MyanmarSangamMN', family='Myanmar Sangam MN', size=12, weight=5) at 0x118bc0250
 652+Font(name='MyanmarSangamMN', family='Myanmar Sangam MN', size=24, weight=5) at 0x118bc0110
 653 Font(name='MyanmarSangamMN-Bold', family='Myanmar Sangam MN', size=12, traits='Bold', weight=9) at 0x118bc0410
 654+Font(name='MyanmarSangamMN-Bold', family='Myanmar Sangam MN', size=24, traits='Bold', weight=9) at 0x118bc0610
 --- Family 'Nadeem'
 655 Font(name='Nadeem', family='Nadeem', size=12, weight=5) at 0x118bc0850
 656+Font(name='Nadeem', family='Nadeem', size=24, weight=5) at 0x118bc0610
 --- Family 'New Peninim MT'
 657 Font(name='NewPeninimMT', family='New Peninim MT', size=12, weight=5) at 0x118bc0910
 658+Font(name='NewPeninimMT', family='New Peninim MT', size=24, weight=5) at 0x118bc0c10
 659 Font(name='NewPeninimMT-Inclined', family='New Peninim MT', size=12, traits='Italic', weight=5) at 0x118bc0a50
 660+Font(name='NewPeninimMT-Inclined', family='New Peninim MT', size=24, traits='Italic', weight=5) at 0x118bc0d90
 661 Font(name='NewPeninimMT-Bold', family='New Peninim MT', size=12, traits='Bold', weight=9) at 0x118bc0e90
 662+Font(name='NewPeninimMT-Bold', family='New Peninim MT', size=24, traits='Bold', weight=9) at 0x118bc0910
 663 Font(name='NewPeninimMT-BoldInclined', family='New Peninim MT', size=12, traits='Bold Italic', weight=9) at 0x118bc0cd0
 664+Font(name='NewPeninimMT-BoldInclined', family='New Peninim MT', size=24, traits='Bold Italic', weight=9) at 0x118bc0e90
 --- Family 'Noteworthy'
 665 Font(name='Noteworthy-Light', family='Noteworthy', size=12, weight=3) at 0x118bcd210
 666+Font(name='Noteworthy-Light', family='Noteworthy', size=24, weight=3) at 0x118bcd310
 667 Font(name='Noteworthy-Bold', family='Noteworthy', size=12, traits='Bold', weight=9) at 0x118bcd450
 668+Font(name='Noteworthy-Bold', family='Noteworthy', size=24, traits='Bold', weight=9) at 0x118bcd210
 --- Family 'Noto Nastaliq Urdu'
 669 Font(name='NotoNastaliqUrdu', family='Noto Nastaliq Urdu', size=12, weight=5) at 0x118bcd6d0
 670+Font(name='NotoNastaliqUrdu', family='Noto Nastaliq Urdu', size=24, weight=5) at 0x118bcd7d0
 --- Family 'Optima'
 671 Font(name='Optima-Regular', family='Optima', size=12, weight=5) at 0x118bcd8d0
 672+Font(name='Optima-Regular', family='Optima', size=24, weight=5) at 0x118bcd6d0
 673 Font(name='Optima-Italic', family='Optima', size=12, traits='Italic', weight=5) at 0x118bcdc10
 674+Font(name='Optima-Italic', family='Optima', size=24, traits='Italic', weight=5) at 0x118bcd8d0
 675 Font(name='Optima-Bold', family='Optima', size=12, traits='Bold', weight=9) at 0x118bcdb90
 676+Font(name='Optima-Bold', family='Optima', size=24, traits='Bold', weight=9) at 0x118bcde90
 677 Font(name='Optima-BoldItalic', family='Optima', size=12, traits='Bold Italic', weight=9) at 0x118bcdd50
 678+Font(name='Optima-BoldItalic', family='Optima', size=24, traits='Bold Italic', weight=9) at 0x118bcdb90
 679 Font(name='Optima-ExtraBlack', family='Optima', size=12, traits='Bold', weight=11) at 0x119791090
 680+Font(name='Optima-ExtraBlack', family='Optima', size=24, traits='Bold', weight=11) at 0x119791310
 --- Family 'Oriya MN'
 681 Font(name='OriyaMN', family='Oriya MN', size=12, weight=5) at 0x119791350
 682+Font(name='OriyaMN', family='Oriya MN', size=24, weight=5) at 0x119791310
 683 Font(name='OriyaMN-Bold', family='Oriya MN', size=12, traits='Bold', weight=9) at 0x1197916d0
 684+Font(name='OriyaMN-Bold', family='Oriya MN', size=24, traits='Bold', weight=9) at 0x119791550
 --- Family 'Oriya Sangam MN'
 685 Font(name='OriyaSangamMN', family='Oriya Sangam MN', size=12, weight=5) at 0x119791350
 686+Font(name='OriyaSangamMN', family='Oriya Sangam MN', size=24, weight=5) at 0x1197916d0
 687 Font(name='OriyaSangamMN-Bold', family='Oriya Sangam MN', size=12, traits='Bold', weight=9) at 0x1197919d0
 688+Font(name='OriyaSangamMN-Bold', family='Oriya Sangam MN', size=24, traits='Bold', weight=9) at 0x119791350
 --- Family 'Osaka'
 689 Font(name='Osaka', family='Osaka', size=12, weight=5) at 0x119791dd0
 690+Font(name='Osaka', family='Osaka', size=24, weight=5) at 0x119791350
 --- Family 'Palatino'
 691 Font(name='Palatino-Roman', family='Palatino', size=12, weight=5) at 0x118bb5090
 692+Font(name='Palatino-Roman', family='Palatino', size=24, weight=5) at 0x118bb5190
 693 Font(name='Palatino-Italic', family='Palatino', size=12, traits='Italic', weight=5) at 0x118bb5310
 694+Font(name='Palatino-Italic', family='Palatino', size=24, traits='Italic', weight=5) at 0x118bb5090
 695 Font(name='Palatino-Bold', family='Palatino', size=12, traits='Bold', weight=9) at 0x118bb5390
 696+Font(name='Palatino-Bold', family='Palatino', size=24, traits='Bold', weight=9) at 0x118bb5310
 697 Font(name='Palatino-BoldItalic', family='Palatino', size=12, traits='Bold Italic', weight=9) at 0x118bb5590
 698+Font(name='Palatino-BoldItalic', family='Palatino', size=24, traits='Bold Italic', weight=9) at 0x118bb5650
 --- Family 'Papyrus'
 699 Font(name='Papyrus', family='Papyrus', size=12, weight=5) at 0x118bb5390
 700+Font(name='Papyrus', family='Papyrus', size=24, weight=5) at 0x118bb5650
 701 Font(name='Papyrus-Condensed', family='Papyrus', size=12, traits='Condensed', weight=5) at 0x118bb5a90
 702+Font(name='Papyrus', family='Papyrus', size=24, weight=5) at 0x118bb5c50
 --- Family 'Party LET'
 703 Font(name='PartyLetPlain', family='Party LET', size=12, traits='Italic', weight=5) at 0x118bb5cd0
 704+Font(name='PartyLetPlain', family='Party LET', size=24, traits='Italic', weight=5) at 0x118bb5d90
 --- Family 'Phosphate'
 705 Font(name='Phosphate-Inline', family='Phosphate', size=12, weight=5) at 0x1197a5050
 706+Font(name='Phosphate-Inline', family='Phosphate', size=24, weight=5) at 0x1197a5110
 707 Font(name='Phosphate-Solid', family='Phosphate', size=12, weight=5) at 0x1197a5310
 708+Font(name='Phosphate-Inline', family='Phosphate', size=24, weight=5) at 0x1197a5050
 --- Family 'PingFang HK'
 709 Font(name='PingFangHK-Regular', family='PingFang HK', size=12, weight=5) at 0x1197a5110
 710+Font(name='PingFangHK-Regular', family='PingFang HK', size=24, weight=5) at 0x1197a5590
 711 Font(name='PingFangHK-Ultralight', family='PingFang HK', size=12, weight=2) at 0x1197a5550
 712+Font(name='PingFangHK-Ultralight', family='PingFang HK', size=24, weight=2) at 0x1197a5110
 713 Font(name='PingFangHK-Thin', family='PingFang HK', size=12, weight=3) at 0x1197a5910
 714+Font(name='PingFangHK-Thin', family='PingFang HK', size=24, weight=3) at 0x1197a5550
 715 Font(name='PingFangHK-Light', family='PingFang HK', size=12, weight=3) at 0x1197a5a50
 716+Font(name='PingFangHK-Thin', family='PingFang HK', size=24, weight=3) at 0x1197a5550
 717 Font(name='PingFangHK-Medium', family='PingFang HK', size=12, weight=6) at 0x1197a5910
 718+Font(name='PingFangHK-Medium', family='PingFang HK', size=24, weight=6) at 0x1197a5590
 719 Font(name='PingFangHK-Semibold', family='PingFang HK', size=12, traits='Bold', weight=8) at 0x1197a5a50
 720+Font(name='PingFangHK-Semibold', family='PingFang HK', size=24, traits='Bold', weight=8) at 0x1197a5910
 --- Family 'PingFang SC'
 721 Font(name='PingFangSC-Regular', family='PingFang SC', size=12, weight=5) at 0x1197a5f50
 722+Font(name='PingFangSC-Regular', family='PingFang SC', size=24, weight=5) at 0x1197b3050
 723 Font(name='PingFangSC-Ultralight', family='PingFang SC', size=12, weight=2) at 0x1197b3110
 724+Font(name='PingFangSC-Ultralight', family='PingFang SC', size=24, weight=2) at 0x1197b3250
 725 Font(name='PingFangSC-Thin', family='PingFang SC', size=12, weight=3) at 0x1197b33d0
 726+Font(name='PingFangSC-Thin', family='PingFang SC', size=24, weight=3) at 0x1197b3110
 727 Font(name='PingFangSC-Light', family='PingFang SC', size=12, weight=3) at 0x1197b3510
 728+Font(name='PingFangSC-Thin', family='PingFang SC', size=24, weight=3) at 0x1197b3110
 729 Font(name='PingFangSC-Medium', family='PingFang SC', size=12, weight=6) at 0x1197b33d0
 730+Font(name='PingFangSC-Medium', family='PingFang SC', size=24, weight=6) at 0x1197b3050
 731 Font(name='PingFangSC-Semibold', family='PingFang SC', size=12, traits='Bold', weight=8) at 0x1197b3510
 732+Font(name='PingFangSC-Semibold', family='PingFang SC', size=24, traits='Bold', weight=8) at 0x1197b33d0
 --- Family 'PingFang TC'
 733 Font(name='PingFangTC-Regular', family='PingFang TC', size=12, weight=5) at 0x1197b3910
 734+Font(name='PingFangTC-Regular', family='PingFang TC', size=24, weight=5) at 0x1197b3b10
 735 Font(name='PingFangTC-Ultralight', family='PingFang TC', size=12, weight=2) at 0x1197b3ad0
 736+Font(name='PingFangTC-Ultralight', family='PingFang TC', size=24, weight=2) at 0x1197b3910
 737 Font(name='PingFangTC-Thin', family='PingFang TC', size=12, weight=3) at 0x1197b3e50
 738+Font(name='PingFangTC-Thin', family='PingFang TC', size=24, weight=3) at 0x1197b3ad0
 739 Font(name='PingFangTC-Light', family='PingFang TC', size=12, weight=3) at 0x1197b3c10
 740+Font(name='PingFangTC-Thin', family='PingFang TC', size=24, weight=3) at 0x1197b3ad0
 741 Font(name='PingFangTC-Medium', family='PingFang TC', size=12, weight=6) at 0x1197be190
 742+Font(name='PingFangTC-Medium', family='PingFang TC', size=24, weight=6) at 0x1197b3c10
 743 Font(name='PingFangTC-Semibold', family='PingFang TC', size=12, traits='Bold', weight=8) at 0x1197be110
 744+Font(name='PingFangTC-Semibold', family='PingFang TC', size=24, traits='Bold', weight=8) at 0x1197be190
 --- Family 'Plantagenet Cherokee'
 745 Font(name='PlantagenetCherokee', family='Plantagenet Cherokee', size=12, weight=5) at 0x1197be110
 746+Font(name='PlantagenetCherokee', family='Plantagenet Cherokee', size=24, weight=5) at 0x1197be650
 --- Family 'PoemScriptW00-Regular'
 747 Font(name='PoemScriptW00-Regular', family='PoemScriptW00-Regular', size=12, weight=5) at 0x1197be790
 748+Font(name='PoemScriptW00-Regular', family='PoemScriptW00-Regular', size=24, weight=5) at 0x1197be650
 --- Family 'PortagoITC TT'
 749 Font(name='PortagoITCTT', family='PortagoITC TT', size=12, traits='Bold Condensed', weight=11) at 0x1197be9d0
 750+Font(name='PortagoITCTT', family='PortagoITC TT', size=24, traits='Bold Condensed', weight=11) at 0x1197bea50
 --- Family 'Princetown LET'
 751 Font(name='PrincetownLET', family='Princetown LET', size=12, traits='Bold', weight=9) at 0x1197beb90
 752+Font(name='PrincetownLET', family='Princetown LET', size=24, traits='Bold', weight=9) at 0x1197becd0
 --- Family 'PT Mono'
 753 Font(name='PTMono-Regular', family='PT Mono', size=12, traits='MonoSpace', weight=5) at 0x1197bef50
 754+Font(name='PTMono-Regular', family='PT Mono', size=24, traits='MonoSpace', weight=5) at 0x11ed39150
 755 Font(name='PTMono-Bold', family='PT Mono', size=12, traits='Bold MonoSpace', weight=9) at 0x11ed391d0
 756+Font(name='PTMono-Bold', family='PT Mono', size=24, traits='Bold MonoSpace', weight=9) at 0x11ed393d0
 --- Family 'PT Sans'
 757 Font(name='PTSans-Regular', family='PT Sans', size=12, traits='SansSerif', weight=5) at 0x11ed39150
 758+Font(name='PTSans-Regular', family='PT Sans', size=24, traits='SansSerif', weight=5) at 0x11ed39590
 759 Font(name='PTSans-Italic', family='PT Sans', size=12, traits='Italic SansSerif', weight=5) at 0x11ed395d0
 760+Font(name='PTSans-Italic', family='PT Sans', size=24, traits='Italic SansSerif', weight=5) at 0x11ed396d0
 761 Font(name='PTSans-Bold', family='PT Sans', size=12, traits='Bold SansSerif', weight=9) at 0x11ed39910
 762+Font(name='PTSans-Bold', family='PT Sans', size=24, traits='Bold SansSerif', weight=9) at 0x11ed399d0
 763 Font(name='PTSans-BoldItalic', family='PT Sans', size=12, traits='Bold Italic SansSerif', weight=9) at 0x11ed39ad0
 764+Font(name='PTSans-BoldItalic', family='PT Sans', size=24, traits='Bold Italic SansSerif', weight=9) at 0x11ed399d0
 --- Family 'PT Sans Caption'
 765 Font(name='PTSans-Caption', family='PT Sans Caption', size=12, traits='SansSerif', weight=5) at 0x11ed39c10
 766+Font(name='PTSans-Caption', family='PT Sans Caption', size=24, traits='SansSerif', weight=5) at 0x11ed39d50
 767 Font(name='PTSans-CaptionBold', family='PT Sans Caption', size=12, traits='Bold SansSerif', weight=9) at 0x11ed39fd0
 768+Font(name='PTSans-CaptionBold', family='PT Sans Caption', size=24, traits='Bold SansSerif', weight=9) at 0x11ed39c10
 --- Family 'PT Sans Narrow'
 769 Font(name='PTSans-Narrow', family='PT Sans Narrow', size=12, traits='Condensed Narrow SansSerif', weight=5) at 0x11ed441d0
 770+Font(name='PTSans-Narrow', family='PT Sans Narrow', size=24, traits='Condensed Narrow SansSerif', weight=5) at 0x11ed44350
 771 Font(name='PTSans-NarrowBold', family='PT Sans Narrow', size=12, traits='Bold Condensed Narrow SansSerif', weight=9) at 0x11ed44390
 772+Font(name='PTSans-NarrowBold', family='PT Sans Narrow', size=24, traits='Bold Condensed Narrow SansSerif', weight=9) at 0x11ed44550
 --- Family 'PT Serif'
 773 Font(name='PTSerif-Regular', family='PT Serif', size=12, weight=5) at 0x11ed44690
 774+Font(name='PTSerif-Regular', family='PT Serif', size=24, weight=5) at 0x11ed44750
 775 Font(name='PTSerif-Italic', family='PT Serif', size=12, traits='Italic', weight=5) at 0x11ed448d0
 776+Font(name='PTSerif-Italic', family='PT Serif', size=24, traits='Italic', weight=5) at 0x11ed44690
 777 Font(name='PTSerif-Bold', family='PT Serif', size=12, traits='Bold', weight=9) at 0x11ed44950
 778+Font(name='PTSerif-Bold', family='PT Serif', size=24, traits='Bold', weight=9) at 0x11ed44a10
 779 Font(name='PTSerif-BoldItalic', family='PT Serif', size=12, traits='Bold Italic', weight=9) at 0x11ed44b50
 780+Font(name='PTSerif-BoldItalic', family='PT Serif', size=24, traits='Bold Italic', weight=9) at 0x11ed448d0
 --- Family 'PT Serif Caption'
 781 Font(name='PTSerif-Caption', family='PT Serif Caption', size=12, weight=5) at 0x11ed44950
 782+Font(name='PTSerif-Caption', family='PT Serif Caption', size=24, weight=5) at 0x1197ae050
 783 Font(name='PTSerif-CaptionItalic', family='PT Serif Caption', size=12, traits='Italic', weight=5) at 0x1197ae0d0
 784+Font(name='PTSerif-CaptionItalic', family='PT Serif Caption', size=24, traits='Italic', weight=5) at 0x1197ae050
 --- Family 'Raanana'
 785 Font(name='Raanana', family='Raanana', size=12, weight=5) at 0x105a04a90
 786+Font(name='Raanana', family='Raanana', size=24, weight=5) at 0x105a046d0
 787 Font(name='RaananaBold', family='Raanana', size=12, traits='Bold', weight=9) at 0x101f43ad0
 788+Font(name='RaananaBold', family='Raanana', size=24, traits='Bold', weight=9) at 0x101f4f510
 --- Family 'Rockwell'
 789 Font(name='Rockwell-Regular', family='Rockwell', size=12, weight=5) at 0x105a2b6d0
 790+Font(name='Rockwell-Regular', family='Rockwell', size=24, weight=5) at 0x105a21610
 791 Font(name='Rockwell-Italic', family='Rockwell', size=12, traits='Italic', weight=5) at 0x105a21c10
 792+Font(name='Rockwell-Italic', family='Rockwell', size=24, traits='Italic', weight=5) at 0x105a26450
 793 Font(name='Rockwell-Bold', family='Rockwell', size=12, traits='Bold', weight=9) at 0x105a26850
 794+Font(name='Rockwell-Bold', family='Rockwell', size=24, traits='Bold', weight=9) at 0x106527d10
 795 Font(name='Rockwell-BoldItalic', family='Rockwell', size=12, traits='Bold Italic', weight=9) at 0x1065112d0
 796+Font(name='Rockwell-BoldItalic', family='Rockwell', size=24, traits='Bold Italic', weight=9) at 0x106511dd0
 --- Family 'Sana'
 797 Font(name='Sana', family='Sana', size=12, weight=5) at 0x10651c910
 798+Font(name='Sana', family='Sana', size=24, weight=5) at 0x105a2d650
 --- Family 'Santa Fe LET'
 799 Font(name='SantaFeLetPlain', family='Santa Fe LET', size=12, traits='Bold Italic', weight=9) at 0x105a3ea50
 800+Font(name='SantaFeLetPlain', family='Santa Fe LET', size=24, traits='Bold Italic', weight=9) at 0x105a3e310
 --- Family 'Sathu'
 801 Font(name='Sathu', family='Sathu', size=12, weight=5) at 0x106501e90
 802+Font(name='Sathu', family='Sathu', size=24, weight=5) at 0x105a3e310
 --- Family 'Savoye LET'
 803 Font(name='SavoyeLetPlain', family='Savoye LET', size=12, traits='Italic', weight=5) at 0x108981650
 804+Font(name='SavoyeLetPlain', family='Savoye LET', size=24, traits='Italic', weight=5) at 0x108972ad0
 --- Family 'SchoolHouse Cursive B'
 805 Font(name='SchoolHouseCursiveB', family='SchoolHouse Cursive B', size=12, traits='Italic', weight=5) at 0x1091d31d0
 806+Font(name='SchoolHouseCursiveB', family='SchoolHouse Cursive B', size=24, traits='Italic', weight=5) at 0x10899da90
 --- Family 'SchoolHouse Printed A'
 807 Font(name='SchoolHousePrintedA', family='SchoolHouse Printed A', size=12, weight=5) at 0x108994190
 808+Font(name='SchoolHousePrintedA', family='SchoolHouse Printed A', size=24, weight=5) at 0x1091e0810
 --- Family 'Seravek'
 809 Font(name='Seravek', family='Seravek', size=12, weight=5) at 0x10896c190
 810+Font(name='Seravek', family='Seravek', size=24, weight=5) at 0x10897d950
 811 Font(name='Seravek-Italic', family='Seravek', size=12, traits='Italic', weight=5) at 0x10897d6d0
 812+Font(name='Seravek-Italic', family='Seravek', size=24, traits='Italic', weight=5) at 0x1091cf1d0
 813 Font(name='Seravek-ExtraLight', family='Seravek', size=12, weight=2) at 0x1091cfd10
 814+Font(name='Seravek-ExtraLight', family='Seravek', size=24, weight=2) at 0x109ef8510
 815 Font(name='Seravek-ExtraLightItalic', family='Seravek', size=12, traits='Italic', weight=2) at 0x109f0c590
 816+Font(name='Seravek-ExtraLightItalic', family='Seravek', size=24, traits='Italic', weight=2) at 0x1091fc590
 817 Font(name='Seravek-Light', family='Seravek', size=12, weight=3) at 0x1091fcbd0
 818+Font(name='Seravek-Light', family='Seravek', size=24, weight=3) at 0x109f0c190
 819 Font(name='Seravek-LightItalic', family='Seravek', size=12, traits='Italic', weight=3) at 0x1091fc050
 820+Font(name='Seravek-LightItalic', family='Seravek', size=24, traits='Italic', weight=3) at 0x10aba2ad0
 821 Font(name='Seravek-Medium', family='Seravek', size=12, weight=6) at 0x109f04950
 822+Font(name='Seravek-Medium', family='Seravek', size=24, weight=6) at 0x109f04e50
 823 Font(name='Seravek-MediumItalic', family='Seravek', size=12, traits='Italic', weight=7) at 0x10ab9f590
 824+Font(name='Seravek-MediumItalic', family='Seravek', size=24, traits='Italic', weight=7) at 0x109f04950
 825 Font(name='Seravek-Bold', family='Seravek', size=12, traits='Bold', weight=9) at 0x10abd1ad0
 826+Font(name='Seravek-Bold', family='Seravek', size=24, traits='Bold', weight=9) at 0x10ab9f590
 827 Font(name='Seravek-BoldItalic', family='Seravek', size=12, traits='Bold Italic', weight=9) at 0x10abc7510
 828+Font(name='Seravek-BoldItalic', family='Seravek', size=24, traits='Bold Italic', weight=9) at 0x10abd1ad0
 --- Family 'Shree Devanagari 714'
 829 Font(name='ShreeDev0714', family='Shree Devanagari 714', size=12, weight=5) at 0x10abbb710
 830+Font(name='ShreeDev0714', family='Shree Devanagari 714', size=24, weight=5) at 0x10abdc550
 831 Font(name='ShreeDev0714-Italic', family='Shree Devanagari 714', size=12, traits='Italic', weight=5) at 0x10abdc690
 832+Font(name='ShreeDev0714-Italic', family='Shree Devanagari 714', size=24, traits='Italic', weight=5) at 0x10fd8c5d0
 833 Font(name='ShreeDev0714-Bold', family='Shree Devanagari 714', size=12, traits='Bold', weight=9) at 0x10abb5110
 834+Font(name='ShreeDev0714-Bold', family='Shree Devanagari 714', size=24, traits='Bold', weight=9) at 0x10abdc690
 835 Font(name='ShreeDev0714-BoldItalic', family='Shree Devanagari 714', size=12, traits='Bold Italic', weight=9) at 0x10fda1750
 836+Font(name='ShreeDev0714-BoldItalic', family='Shree Devanagari 714', size=24, traits='Bold Italic', weight=9) at 0x10abb5890
 --- Family 'SignPainter'
 837 Font(name='SignPainter-HouseScript', family='SignPainter', size=12, traits='Condensed', weight=5) at 0x118b965d0
 838+Font(name='SignPainter-HouseScript', family='SignPainter', size=24, traits='Condensed', weight=5) at 0x10fd96d50
 839 Font(name='SignPainter-HouseScriptSemibold', family='SignPainter', size=12, traits='Bold Condensed', weight=8) at 0x118bc0d90
 840+Font(name='SignPainter-HouseScriptSemibold', family='SignPainter', size=24, traits='Bold Condensed', weight=8) at 0x118baa350
 --- Family 'Silom'
 841 Font(name='Silom', family='Silom', size=12, traits='Bold', weight=9) at 0x118bb7410
 842+Font(name='Silom', family='Silom', size=24, traits='Bold', weight=9) at 0x118bcdc50
 --- Family 'Sinhala MN'
 843 Font(name='SinhalaMN', family='Sinhala MN', size=12, weight=5) at 0x118bcd4d0
 844+Font(name='SinhalaMN', family='Sinhala MN', size=24, weight=5) at 0x118bcdc50
 845 Font(name='SinhalaMN-Bold', family='Sinhala MN', size=12, traits='Bold', weight=9) at 0x119791bd0
 846+Font(name='SinhalaMN-Bold', family='Sinhala MN', size=24, traits='Bold', weight=9) at 0x10fd821d0
 --- Family 'Sinhala Sangam MN'
 847 Font(name='SinhalaSangamMN', family='Sinhala Sangam MN', size=12, weight=5) at 0x10fd82110
 848+Font(name='SinhalaSangamMN', family='Sinhala Sangam MN', size=24, weight=5) at 0x109f1c110
 849 Font(name='SinhalaSangamMN-Bold', family='Sinhala Sangam MN', size=12, traits='Bold', weight=9) at 0x109f1ce90
 850+Font(name='SinhalaSangamMN-Bold', family='Sinhala Sangam MN', size=24, traits='Bold', weight=9) at 0x10abb28d0
 --- Family 'Skia'
 851 Font(name='Skia-Regular', family='Skia', size=12, weight=5) at 0x11ed39250
 852+Font(name='Skia-Regular', family='Skia', size=24, weight=5) at 0x11ed44950
 853 Font(name='Skia-Regular_Light', family='Skia', size=12, weight=3) at 0x1197a5cd0
 854+Font(name='Skia-Regular_Light', family='Skia', size=24, weight=3) at 0x1197b3050
 855 Font(name='Skia-Regular_Bold', family='Skia', size=12, traits='Bold', weight=9) at 0x1197bea50
 856+Font(name='Skia-Regular_Bold', family='Skia', size=24, traits='Bold', weight=9) at 0x1197ae050
 857 Font(name='Skia-Regular_Black', family='Skia', size=12, traits='Bold', weight=11) at 0x1197ae190
 858+Font(name='Skia-Regular_Black', family='Skia', size=24, traits='Bold', weight=11) at 0x1197ae050
 859 Font(name='Skia-Regular_Extended', family='Skia', size=12, weight=5) at 0x1197ae490
 860+Font(name='Skia-Regular', family='Skia', size=24, weight=5) at 0x1197ae190
 861 Font(name='Skia-Regular_Light-Extended', family='Skia', size=12, weight=3) at 0x1197ae890
 862+Font(name='Skia-Regular_Light', family='Skia', size=24, weight=3) at 0x1197ae490
 863 Font(name='Skia-Regular_Black-Extended', family='Skia', size=12, traits='Bold', weight=11) at 0x1197ae990
 864+Font(name='Skia-Regular_Black', family='Skia', size=24, traits='Bold', weight=11) at 0x1197aeb90
 865 Font(name='Skia-Regular_Condensed', family='Skia', size=12, traits='Condensed', weight=5) at 0x1197ae7d0
 866+Font(name='Skia-Regular', family='Skia', size=24, weight=5) at 0x1197aed50
 867 Font(name='Skia-Regular_Light-Condensed', family='Skia', size=12, traits='Condensed', weight=3) at 0x1197ae550
 868+Font(name='Skia-Regular_Light', family='Skia', size=24, weight=3) at 0x1197aeed0
 869 Font(name='Skia-Regular_Black-Condensed', family='Skia', size=12, traits='Bold Condensed', weight=11) at 0x1197aebd0
 870+Font(name='Skia-Regular_Black', family='Skia', size=24, traits='Bold', weight=11) at 0x1197ae550
 --- Family 'Snell Roundhand'
 871 Font(name='SnellRoundhand', family='Snell Roundhand', size=12, traits='Italic', weight=5) at 0x10fd9c090
 872+Font(name='SnellRoundhand', family='Snell Roundhand', size=24, traits='Italic', weight=5) at 0x10fd9c150
 873 Font(name='SnellRoundhand-Bold', family='Snell Roundhand', size=12, traits='Bold Italic', weight=9) at 0x10fd9c250
 874+Font(name='SnellRoundhand-Bold', family='Snell Roundhand', size=24, traits='Bold Italic', weight=9) at 0x10fd9c350
 875 Font(name='SnellRoundhand-Black', family='Snell Roundhand', size=12, traits='Bold Italic', weight=11) at 0x10fd9c150
 876+Font(name='SnellRoundhand-Black', family='Snell Roundhand', size=24, traits='Bold Italic', weight=11) at 0x10fd9c250
 --- Family 'Songti SC'
 877 Font(name='STSongti-SC-Regular', family='Songti SC', size=12, weight=5) at 0x10fd9c350
 878+Font(name='STSongti-SC-Regular', family='Songti SC', size=24, weight=5) at 0x10fd9c7d0
 879 Font(name='STSongti-SC-Light', family='Songti SC', size=12, weight=3) at 0x10fd9c910
 880+Font(name='STSongti-SC-Light', family='Songti SC', size=24, weight=3) at 0x10fd9c8d0
 881 Font(name='STSongti-SC-Bold', family='Songti SC', size=12, traits='Bold', weight=9) at 0x10fd9c990
 882+Font(name='STSongti-SC-Bold', family='Songti SC', size=24, traits='Bold', weight=9) at 0x10fd9c910
 883 Font(name='STSongti-SC-Black', family='Songti SC', size=12, traits='Bold', weight=11) at 0x10fd9cb50
 884+Font(name='STSongti-SC-Black', family='Songti SC', size=24, traits='Bold', weight=11) at 0x10fd9c990
 --- Family 'Songti TC'
 885 Font(name='STSongti-TC-Regular', family='Songti TC', size=12, weight=5) at 0x10fd9ce10
 886+Font(name='STSongti-TC-Regular', family='Songti TC', size=24, weight=5) at 0x11ed5f090
 887 Font(name='STSongti-TC-Light', family='Songti TC', size=12, weight=3) at 0x11ed5f1d0
 888+Font(name='STSongti-TC-Light', family='Songti TC', size=24, weight=3) at 0x11ed5f150
 889 Font(name='STSongti-TC-Bold', family='Songti TC', size=12, traits='Bold', weight=9) at 0x11ed5f210
 890+Font(name='STSongti-TC-Bold', family='Songti TC', size=24, traits='Bold', weight=9) at 0x11ed5f1d0
 --- Family 'STIXGeneral'
 891 Font(name='STIXGeneral-Regular', family='STIXGeneral', size=12, weight=5) at 0x11ed5f490
 892+Font(name='STIXGeneral-Regular', family='STIXGeneral', size=24, weight=5) at 0x11ed5f690
 893 Font(name='STIXGeneral-Italic', family='STIXGeneral', size=12, traits='Italic', weight=5) at 0x11ed5f650
 894+Font(name='STIXGeneral-Italic', family='STIXGeneral', size=24, traits='Italic', weight=5) at 0x11ed5f490
 895 Font(name='STIXGeneral-Bold', family='STIXGeneral', size=12, traits='Bold', weight=9) at 0x11ed5f990
 896+Font(name='STIXGeneral-Bold', family='STIXGeneral', size=24, traits='Bold', weight=9) at 0x11ed5f650
 897 Font(name='STIXGeneral-BoldItalic', family='STIXGeneral', size=12, traits='Bold Italic', weight=9) at 0x11ed5fb90
 898+Font(name='STIXGeneral-BoldItalic', family='STIXGeneral', size=24, traits='Bold Italic', weight=9) at 0x11ed5f990
 --- Family 'STIXIntegralsD'
 899 Font(name='STIXIntegralsD-Regular', family='STIXIntegralsD', size=12, weight=5) at 0x11ed5fdd0
 900+Font(name='STIXIntegralsD-Regular', family='STIXIntegralsD', size=24, weight=5) at 0x11ed5ff10
 901 Font(name='STIXIntegralsD-Bold', family='STIXIntegralsD', size=12, traits='Bold', weight=9) at 0x11fb980d0
 902+Font(name='STIXIntegralsD-Bold', family='STIXIntegralsD', size=24, traits='Bold', weight=9) at 0x11ed5f990
 --- Family 'STIXIntegralsSm'
 903 Font(name='STIXIntegralsSm-Regular', family='STIXIntegralsSm', size=12, weight=5) at 0x11fb98290
 904+Font(name='STIXIntegralsSm-Regular', family='STIXIntegralsSm', size=24, weight=5) at 0x11fb98390
 905 Font(name='STIXIntegralsSm-Bold', family='STIXIntegralsSm', size=12, traits='Bold', weight=9) at 0x11fb98510
 906+Font(name='STIXIntegralsSm-Bold', family='STIXIntegralsSm', size=24, traits='Bold', weight=9) at 0x11fb98450
 --- Family 'STIXIntegralsUp'
 907 Font(name='STIXIntegralsUp-Regular', family='STIXIntegralsUp', size=12, weight=5) at 0x11fb98650
 908+Font(name='STIXIntegralsUp-Regular', family='STIXIntegralsUp', size=24, weight=5) at 0x11fb989d0
 909 Font(name='STIXIntegralsUp-Bold', family='STIXIntegralsUp', size=12, traits='Bold', weight=9) at 0x11fb98890
 910+Font(name='STIXIntegralsUp-Bold', family='STIXIntegralsUp', size=24, traits='Bold', weight=9) at 0x11fb98a10
 --- Family 'STIXIntegralsUpD'
 911 Font(name='STIXIntegralsUpD-Regular', family='STIXIntegralsUpD', size=12, weight=5) at 0x11fb98b10
 912+Font(name='STIXIntegralsUpD-Regular', family='STIXIntegralsUpD', size=24, weight=5) at 0x11fb98e90
 913 Font(name='STIXIntegralsUpD-Bold', family='STIXIntegralsUpD', size=12, traits='Bold', weight=9) at 0x11fb98d50
 914+Font(name='STIXIntegralsUpD-Bold', family='STIXIntegralsUpD', size=24, traits='Bold', weight=9) at 0x11fb98ed0
 --- Family 'STIXIntegralsUpSm'
 915 Font(name='STIXIntegralsUpSm-Regular', family='STIXIntegralsUpSm', size=12, weight=5) at 0x11fba1150
 916+Font(name='STIXIntegralsUpSm-Regular', family='STIXIntegralsUpSm', size=24, weight=5) at 0x11fb98b10
 917 Font(name='STIXIntegralsUpSm-Bold', family='STIXIntegralsUpSm', size=12, traits='Bold', weight=9) at 0x11fba1250
 918+Font(name='STIXIntegralsUpSm-Bold', family='STIXIntegralsUpSm', size=24, traits='Bold', weight=9) at 0x11fba13d0
 --- Family 'STIXNonUnicode'
 919 Font(name='STIXNonUnicode-Regular', family='STIXNonUnicode', size=12, weight=5) at 0x11fba1610
 920+Font(name='STIXNonUnicode-Regular', family='STIXNonUnicode', size=24, weight=5) at 0x11fba1850
 921 Font(name='STIXNonUnicode-Italic', family='STIXNonUnicode', size=12, traits='Italic', weight=5) at 0x11fba1710
 922+Font(name='STIXNonUnicode-Italic', family='STIXNonUnicode', size=24, traits='Italic', weight=5) at 0x11fba1890
 923 Font(name='STIXNonUnicode-Bold', family='STIXNonUnicode', size=12, traits='Bold', weight=9) at 0x11fba1990
 924+Font(name='STIXNonUnicode-Bold', family='STIXNonUnicode', size=24, traits='Bold', weight=9) at 0x11fba1950
 925 Font(name='STIXNonUnicode-BoldItalic', family='STIXNonUnicode', size=12, traits='Bold Italic', weight=9) at 0x11fba13d0
 926+Font(name='STIXNonUnicode-BoldItalic', family='STIXNonUnicode', size=24, traits='Bold Italic', weight=9) at 0x11fba1990
 --- Family 'STIXSizeFiveSym'
 927 Font(name='STIXSizeFiveSym-Regular', family='STIXSizeFiveSym', size=12, weight=5) at 0x11fba1e10
 928+Font(name='STIXSizeFiveSym-Regular', family='STIXSizeFiveSym', size=24, weight=5) at 0x11fba1c50
 --- Family 'STIXSizeFourSym'
 929 Font(name='STIXSizeFourSym-Regular', family='STIXSizeFourSym', size=12, weight=5) at 0x123e8b090
 930+Font(name='STIXSizeFourSym-Regular', family='STIXSizeFourSym', size=24, weight=5) at 0x123e8b390
 931 Font(name='STIXSizeFourSym-Bold', family='STIXSizeFourSym', size=12, traits='Bold', weight=9) at 0x123e8b250
 932+Font(name='STIXSizeFourSym-Bold', family='STIXSizeFourSym', size=24, traits='Bold', weight=9) at 0x123e8b3d0
 --- Family 'STIXSizeOneSym'
 933 Font(name='STIXSizeOneSym-Regular', family='STIXSizeOneSym', size=12, weight=5) at 0x123e8b4d0
 934+Font(name='STIXSizeOneSym-Regular', family='STIXSizeOneSym', size=24, weight=5) at 0x123e8b850
 935 Font(name='STIXSizeOneSym-Bold', family='STIXSizeOneSym', size=12, traits='Bold', weight=9) at 0x123e8b710
 936+Font(name='STIXSizeOneSym-Bold', family='STIXSizeOneSym', size=24, traits='Bold', weight=9) at 0x123e8b890
 --- Family 'STIXSizeThreeSym'
 937 Font(name='STIXSizeThreeSym-Regular', family='STIXSizeThreeSym', size=12, weight=5) at 0x123e8b990
 938+Font(name='STIXSizeThreeSym-Regular', family='STIXSizeThreeSym', size=24, weight=5) at 0x123e8bb90
 939 Font(name='STIXSizeThreeSym-Bold', family='STIXSizeThreeSym', size=12, traits='Bold', weight=9) at 0x123e8bd10
 940+Font(name='STIXSizeThreeSym-Bold', family='STIXSizeThreeSym', size=24, traits='Bold', weight=9) at 0x123e8bc50
 --- Family 'STIXSizeTwoSym'
 941 Font(name='STIXSizeTwoSym-Regular', family='STIXSizeTwoSym', size=12, weight=5) at 0x123e8bf90
 942+Font(name='STIXSizeTwoSym-Regular', family='STIXSizeTwoSym', size=24, weight=5) at 0x123e8be10
 943 Font(name='STIXSizeTwoSym-Bold', family='STIXSizeTwoSym', size=12, traits='Bold', weight=9) at 0x123e98090
 944+Font(name='STIXSizeTwoSym-Bold', family='STIXSizeTwoSym', size=24, traits='Bold', weight=9) at 0x123e98250
 --- Family 'STIXVariants'
 945 Font(name='STIXVariants-Regular', family='STIXVariants', size=12, weight=5) at 0x123e98350
 946+Font(name='STIXVariants-Regular', family='STIXVariants', size=24, weight=5) at 0x123e98550
 947 Font(name='STIXVariants-Bold', family='STIXVariants', size=12, traits='Bold', weight=9) at 0x123e98750
 948+Font(name='STIXVariants-Bold', family='STIXVariants', size=24, traits='Bold', weight=9) at 0x123e98610
 --- Family 'Stone Sans ITC TT'
 949 Font(name='StoneSansITCTT-Bold', family='Stone Sans ITC TT', size=12, traits='Bold SansSerif', weight=9) at 0x123e988d0
 950+Font(name='StoneSansITCTT-Bold', family='Stone Sans ITC TT', size=24, traits='Bold SansSerif', weight=9) at 0x123e98a50
 --- Family 'Stone Sans Sem ITC TT'
 951 Font(name='StoneSansITCTT-Semi', family='Stone Sans Sem ITC TT', size=12, traits='Bold Italic SansSerif', weight=8) at 0x123e98a10
 952+Font(name='StoneSansITCTT-Semi', family='Stone Sans Sem ITC TT', size=24, traits='Bold Italic SansSerif', weight=8) at 0x123e98a50
 953 Font(name='StoneSansITCTT-SemiIta', family='Stone Sans Sem ITC TT', size=12, traits='Bold Italic SansSerif', weight=8) at 0x123e98f90
 954+Font(name='StoneSansITCTT-Semi', family='Stone Sans Sem ITC TT', size=24, traits='Bold Italic SansSerif', weight=8) at 0x123e98f10
 --- Family 'STSong'
 955 Font(name='STSong', family='STSong', size=12, weight=5) at 0x123e9f1d0
 956+Font(name='STSong', family='STSong', size=24, weight=5) at 0x123e98f10
 --- Family 'Sukhumvit Set'
 957 Font(name='SukhumvitSet-Text', family='Sukhumvit Set', size=12, weight=5) at 0x123e9f210
 958+Font(name='SukhumvitSet-Text', family='Sukhumvit Set', size=24, weight=5) at 0x123e9f1d0
 959 Font(name='SukhumvitSet-Light', family='Sukhumvit Set', size=12, weight=3) at 0x123e9f4d0
 960+Font(name='SukhumvitSet-Light', family='Sukhumvit Set', size=24, weight=3) at 0x123e9f590
 961 Font(name='SukhumvitSet-Medium', family='Sukhumvit Set', size=12, weight=6) at 0x123e9f210
 962+Font(name='SukhumvitSet-Medium', family='Sukhumvit Set', size=24, weight=6) at 0x123e9f690
 963 Font(name='SukhumvitSet-SemiBold', family='Sukhumvit Set', size=12, traits='Bold', weight=9) at 0x123e9f4d0
 964+Font(name='SukhumvitSet-Bold', family='Sukhumvit Set', size=24, traits='Bold', weight=9) at 0x123e9f210
 965 Font(name='SukhumvitSet-Bold', family='Sukhumvit Set', size=12, traits='Bold', weight=9) at 0x123e9fad0
 966+Font(name='SukhumvitSet-Bold', family='Sukhumvit Set', size=24, traits='Bold', weight=9) at 0x123e9f810
 967 Font(name='SukhumvitSet-Thin', family='Sukhumvit Set', size=12, weight=3) at 0x123e9fc10
 968+Font(name='SukhumvitSet-Light', family='Sukhumvit Set', size=24, weight=3) at 0x123e9f810
 --- Family 'Superclarendon'
 969 Font(name='Superclarendon-Regular', family='Superclarendon', size=12, weight=5) at 0x123e9fad0
 970+Font(name='Superclarendon-Regular', family='Superclarendon', size=24, weight=5) at 0x123e9ff10
 971 Font(name='Superclarendon-Italic', family='Superclarendon', size=12, traits='Italic', weight=5) at 0x11fb94090
 972+Font(name='Superclarendon-Italic', family='Superclarendon', size=24, traits='Italic', weight=5) at 0x123e9fad0
 973 Font(name='Superclarendon-Light', family='Superclarendon', size=12, weight=3) at 0x11fb941d0
 974+Font(name='Superclarendon-Light', family='Superclarendon', size=24, weight=3) at 0x11fb94390
 975 Font(name='Superclarendon-LightItalic', family='Superclarendon', size=12, traits='Italic', weight=3) at 0x11fb94510
 976+Font(name='Superclarendon-LightItalic', family='Superclarendon', size=24, traits='Italic', weight=3) at 0x11fb94050
 977 Font(name='Superclarendon-Bold', family='Superclarendon', size=12, traits='Bold', weight=9) at 0x11fb944d0
 978+Font(name='Superclarendon-Bold', family='Superclarendon', size=24, traits='Bold', weight=9) at 0x11fb943d0
 979 Font(name='Superclarendon-BoldItalic', family='Superclarendon', size=12, traits='Bold Italic', weight=9) at 0x11fb940d0
 980+Font(name='Superclarendon-BoldItalic', family='Superclarendon', size=24, traits='Bold Italic', weight=9) at 0x11fb944d0
 981 Font(name='Superclarendon-Black', family='Superclarendon', size=12, traits='Bold', weight=11) at 0x11fb948d0
 982+Font(name='Superclarendon-Black', family='Superclarendon', size=24, traits='Bold', weight=11) at 0x11fb94810
 983 Font(name='Superclarendon-BlackItalic', family='Superclarendon', size=12, traits='Bold Italic', weight=11) at 0x11fb94c10
 984+Font(name='Superclarendon-BlackItalic', family='Superclarendon', size=24, traits='Bold Italic', weight=11) at 0x11fb94c90
 --- Family 'Symbol'
 985 Font(name='Symbol', family='Symbol', size=12, weight=5) at 0x11fb94d50
 986+Font(name='Symbol', family='Symbol', size=24, weight=5) at 0x11fb94c90
 --- Family 'Synchro LET'
 987 Font(name='SynchroLET', family='Synchro LET', size=12, traits='Bold', weight=9) at 0x123eb6050
 988+Font(name='SynchroLET', family='Synchro LET', size=24, traits='Bold', weight=9) at 0x123eb6110
 --- Family 'Tahoma'
 989 Font(name='Tahoma', family='Tahoma', size=12, weight=5) at 0x123eb6250
 990+Font(name='Tahoma', family='Tahoma', size=24, weight=5) at 0x123eb6110
 991 Font(name='Tahoma-Bold', family='Tahoma', size=12, traits='Bold', weight=9) at 0x123eb6490
 992+Font(name='Tahoma-Bold', family='Tahoma', size=24, traits='Bold', weight=9) at 0x123eb6610
 --- Family 'Tamil MN'
 993 Font(name='TamilMN', family='Tamil MN', size=12, weight=5) at 0x123eb6250
 994+Font(name='TamilMN', family='Tamil MN', size=24, weight=5) at 0x123eb6610
 995 Font(name='TamilMN-Bold', family='Tamil MN', size=12, traits='Bold', weight=9) at 0x123eb6990
 996+Font(name='TamilMN-Bold', family='Tamil MN', size=24, traits='Bold', weight=9) at 0x123eb6810
 --- Family 'Tamil Sangam MN'
 997 Font(name='TamilSangamMN', family='Tamil Sangam MN', size=12, weight=5) at 0x123eb6250
 998+Font(name='TamilSangamMN', family='Tamil Sangam MN', size=24, weight=5) at 0x123eb6990
 999 Font(name='TamilSangamMN-Bold', family='Tamil Sangam MN', size=12, traits='Bold', weight=9) at 0x123eb6c90
1000+Font(name='TamilSangamMN-Bold', family='Tamil Sangam MN', size=24, traits='Bold', weight=9) at 0x123eb6250
 --- Family 'Telugu MN'
1001 Font(name='TeluguMN', family='Telugu MN', size=12, weight=5) at 0x123ec3090
1002+Font(name='TeluguMN', family='Telugu MN', size=24, weight=5) at 0x123ec31d0
1003 Font(name='TeluguMN-Bold', family='Telugu MN', size=12, traits='Bold', weight=9) at 0x123ec3350
1004+Font(name='TeluguMN-Bold', family='Telugu MN', size=24, traits='Bold', weight=9) at 0x123ec3090
 --- Family 'Telugu Sangam MN'
1005 Font(name='TeluguSangamMN', family='Telugu Sangam MN', size=12, weight=5) at 0x123ec3490
1006+Font(name='TeluguSangamMN', family='Telugu Sangam MN', size=24, weight=5) at 0x123ec3350
1007 Font(name='TeluguSangamMN-Bold', family='Telugu Sangam MN', size=12, traits='Bold', weight=9) at 0x123ec3650
1008+Font(name='TeluguSangamMN-Bold', family='Telugu Sangam MN', size=24, traits='Bold', weight=9) at 0x123ec3490
 --- Family 'Thonburi'
1009 Font(name='Thonburi', family='Thonburi', size=12, weight=5) at 0x123ec3950
1010+Font(name='Thonburi', family='Thonburi', size=24, weight=5) at 0x123ec3490
1011 Font(name='Thonburi-Light', family='Thonburi', size=12, weight=3) at 0x123ec3c10
1012+Font(name='Thonburi-Light', family='Thonburi', size=24, weight=3) at 0x123ec3c50
1013 Font(name='Thonburi-Bold', family='Thonburi', size=12, traits='Bold', weight=9) at 0x123ec3cd0
1014+Font(name='Thonburi-Bold', family='Thonburi', size=24, traits='Bold', weight=9) at 0x123ec3c10
 --- Family 'Times'
1015 Font(name='Times-Roman', family='Times', size=12, weight=5) at 0x124879090
1016+Font(name='Times-Roman', family='Times', size=24, weight=5) at 0x124879050
1017 Font(name='Times-Italic', family='Times', size=12, traits='Italic', weight=5) at 0x124879310
1018+Font(name='Times-Italic', family='Times', size=24, traits='Italic', weight=5) at 0x124879390
1019 Font(name='Times-Bold', family='Times', size=12, traits='Bold', weight=9) at 0x124879150
1020+Font(name='Times-Bold', family='Times', size=24, traits='Bold', weight=9) at 0x124879590
1021 Font(name='Times-BoldItalic', family='Times', size=12, traits='Bold Italic', weight=9) at 0x124879090
1022+Font(name='Times-BoldItalic', family='Times', size=24, traits='Bold Italic', weight=9) at 0x124879790
 --- Family 'Times New Roman'
1023 Font(name='TimesNewRomanPSMT', family='Times New Roman', size=12, weight=5) at 0x124879310
1024+Font(name='TimesNewRomanPSMT', family='Times New Roman', size=24, weight=5) at 0x124879a50
1025 Font(name='TimesNewRomanPS-ItalicMT', family='Times New Roman', size=12, traits='Italic', weight=5) at 0x124879a10
1026+Font(name='TimesNewRomanPS-ItalicMT', family='Times New Roman', size=24, traits='Italic', weight=5) at 0x124879b90
1027 Font(name='TimesNewRomanPS-BoldMT', family='Times New Roman', size=12, traits='Bold', weight=9) at 0x124879c90
1028+Font(name='TimesNewRomanPS-BoldMT', family='Times New Roman', size=24, traits='Bold', weight=9) at 0x124879310
1029 Font(name='TimesNewRomanPS-BoldItalicMT', family='Times New Roman', size=12, traits='Bold Italic', weight=9) at 0x124879e10
1030+Font(name='TimesNewRomanPS-BoldItalicMT', family='Times New Roman', size=24, traits='Bold Italic', weight=9) at 0x124879c90
 --- Family 'Trattatello'
1031 Font(name='Trattatello', family='Trattatello', size=12, weight=5) at 0x124879e10
1032+Font(name='Trattatello', family='Trattatello', size=24, weight=5) at 0x1248881d0
 --- Family 'Trebuchet MS'
1033 Font(name='TrebuchetMS', family='Trebuchet MS', size=12, weight=5) at 0x124888190
1034+Font(name='TrebuchetMS', family='Trebuchet MS', size=24, weight=5) at 0x1248883d0
1035 Font(name='TrebuchetMS-Italic', family='Trebuchet MS', size=12, traits='Italic', weight=5) at 0x124888050
1036+Font(name='TrebuchetMS-Italic', family='Trebuchet MS', size=24, traits='Italic', weight=5) at 0x124888190
1037 Font(name='TrebuchetMS-Bold', family='Trebuchet MS', size=12, traits='Bold', weight=9) at 0x124888550
1038+Font(name='TrebuchetMS-Bold', family='Trebuchet MS', size=24, traits='Bold', weight=9) at 0x124888050
1039 Font(name='Trebuchet-BoldItalic', family='Trebuchet MS', size=12, traits='Bold Italic', weight=9) at 0x124888710
1040+Font(name='Trebuchet-BoldItalic', family='Trebuchet MS', size=24, traits='Bold Italic', weight=9) at 0x124888550
 --- Family 'Type Embellishments One LET'
1041 Font(name='TypeEmbellishmentsOneLetPlain', family='Type Embellishments One LET', size=12, weight=5) at 0x124888990
1042+Font(name='TypeEmbellishmentsOneLetPlain', family='Type Embellishments One LET', size=24, weight=5) at 0x124888550
 --- Family 'Verdana'
1043 Font(name='Verdana', family='Verdana', size=12, weight=5) at 0x124888c90
1044+Font(name='Verdana', family='Verdana', size=24, weight=5) at 0x124888550
1045 Font(name='Verdana-Italic', family='Verdana', size=12, traits='Italic', weight=5) at 0x124888d50
1046+Font(name='Verdana-Italic', family='Verdana', size=24, traits='Italic', weight=5) at 0x124888e50
1047 Font(name='Verdana-Bold', family='Verdana', size=12, traits='Bold', weight=9) at 0x124893090
1048+Font(name='Verdana-Bold', family='Verdana', size=24, traits='Bold', weight=9) at 0x124893150
1049 Font(name='Verdana-BoldItalic', family='Verdana', size=12, traits='Bold Italic', weight=9) at 0x124893110
1050+Font(name='Verdana-BoldItalic', family='Verdana', size=24, traits='Bold Italic', weight=9) at 0x124893350
 --- Family 'Waseem'
1051 Font(name='Waseem', family='Waseem', size=12, weight=5) at 0x124893090
1052+Font(name='Waseem', family='Waseem', size=24, weight=5) at 0x124893350
1053 Font(name='WaseemLight', family='Waseem', size=12, weight=3) at 0x124893650
1054+Font(name='WaseemLight', family='Waseem', size=24, weight=3) at 0x124893350
 --- Family 'Webdings'
1055 Font(name='Webdings', family='Webdings', size=12, weight=5) at 0x124893810
1056+Font(name='Webdings', family='Webdings', size=24, weight=5) at 0x124893350
 --- Family 'Wingdings'
1057 Font(name='Wingdings-Regular', family='Wingdings', size=12, weight=5) at 0x124893b10
1058+Font(name='Wingdings-Regular', family='Wingdings', size=24, weight=5) at 0x124893a90
 --- Family 'Wingdings 2'
1059 Font(name='Wingdings2', family='Wingdings 2', size=12, weight=5) at 0x124893d10
1060+Font(name='Wingdings2', family='Wingdings 2', size=24, weight=5) at 0x124893f50
 --- Family 'Wingdings 3'
1061 Font(name='Wingdings3', family='Wingdings 3', size=12, weight=5) at 0x124893e50
1062+Font(name='Wingdings3', family='Wingdings 3', size=24, weight=5) at 0x12489e190
 --- Family 'Zapf Dingbats'
1063 Font(name='ZapfDingbatsITC', family='Zapf Dingbats', size=12, weight=5) at 0x12489e090
1064+Font(name='ZapfDingbatsITC', family='Zapf Dingbats', size=24, weight=5) at 0x12489e390
 --- Family 'Zapfino'
1065 Font(name='Zapfino', family='Zapfino', size=12, weight=5) at 0x12489e410
1066+Font(name='Zapfino', family='Zapfino', size=24, weight=5) at 0x12489e390
 --- Family 'Apple Braille'
1067 Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=12, traits='MonoSpace', weight=5) at 0x12489e5d0
1068+Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=24, traits='MonoSpace', weight=5) at 0x12489e890
1069 Font(name='AppleBraille-Outline8Dot', family='Apple Braille', size=12, traits='MonoSpace', weight=5) at 0x12489e990
1070+Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=24, traits='MonoSpace', weight=5) at 0x12489e5d0
1071 Font(name='AppleBraille-Pinpoint6Dot', family='Apple Braille', size=12, traits='MonoSpace', weight=5) at 0x12489eb90
1072+Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=24, traits='MonoSpace', weight=5) at 0x12489e990
1073 Font(name='AppleBraille-Pinpoint8Dot', family='Apple Braille', size=12, traits='MonoSpace', weight=5) at 0x12489ed50
1074+Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=24, traits='MonoSpace', weight=5) at 0x12489eb90
1075 Font(name='AppleBraille', family='Apple Braille', size=12, traits='MonoSpace', weight=5) at 0x12489ef10
1076+Font(name='AppleBraille-Outline6Dot', family='Apple Braille', size=24, traits='MonoSpace', weight=5) at 0x12489ed50
 --- Family 'Apple Chancery'
1077 Font(name='Apple-Chancery', family='Apple Chancery', size=12, weight=5) at 0x1248a70d0
1078+Font(name='Apple-Chancery', family='Apple Chancery', size=24, weight=5) at 0x12489ed10
 --- Family 'Apple Color Emoji'
1079 Font(name='AppleColorEmoji', family='Apple Color Emoji', size=12, traits='MonoSpace', weight=5) at 0x1248a7210
1080+Font(name='AppleColorEmoji', family='Apple Color Emoji', size=24, traits='MonoSpace', weight=5) at 0x1248a7350
 --- Family 'Apple SD Gothic Neo'
1081 Font(name='AppleSDGothicNeo-Regular', family='Apple SD Gothic Neo', size=12, weight=5) at 0x1248a7510
1082+Font(name='AppleSDGothicNeo-Regular', family='Apple SD Gothic Neo', size=24, weight=5) at 0x1248a7350
1083 Font(name='AppleSDGothicNeo-Thin', family='Apple SD Gothic Neo', size=12, weight=3) at 0x1248a77d0
1084+Font(name='AppleSDGothicNeo-Thin', family='Apple SD Gothic Neo', size=24, weight=3) at 0x1248a7350
1085 Font(name='AppleSDGothicNeo-UltraLight', family='Apple SD Gothic Neo', size=12, weight=3) at 0x1248a7510
1086+Font(name='AppleSDGothicNeo-Thin', family='Apple SD Gothic Neo', size=24, weight=3) at 0x1248a7910
1087 Font(name='AppleSDGothicNeo-Light', family='Apple SD Gothic Neo', size=12, weight=3) at 0x1248a7350
1088+Font(name='AppleSDGothicNeo-Thin', family='Apple SD Gothic Neo', size=24, weight=3) at 0x1248a77d0
1089 Font(name='AppleSDGothicNeo-Medium', family='Apple SD Gothic Neo', size=12, weight=6) at 0x1248a7910
1090+Font(name='AppleSDGothicNeo-Medium', family='Apple SD Gothic Neo', size=24, weight=6) at 0x1248a77d0
1091 Font(name='AppleSDGothicNeo-SemiBold', family='Apple SD Gothic Neo', size=12, traits='Bold', weight=9) at 0x1248a7350
1092+Font(name='AppleSDGothicNeo-Bold', family='Apple SD Gothic Neo', size=24, traits='Bold', weight=9) at 0x1248a7f10
1093 Font(name='AppleSDGothicNeo-Bold', family='Apple SD Gothic Neo', size=12, traits='Bold', weight=9) at 0x1248a7e10
1094+Font(name='AppleSDGothicNeo-Bold', family='Apple SD Gothic Neo', size=24, traits='Bold', weight=9) at 0x1248a7e50
1095 Font(name='AppleSDGothicNeo-ExtraBold', family='Apple SD Gothic Neo', size=12, traits='Bold', weight=10) at 0x1248b0110
1096+Font(name='AppleSDGothicNeo-ExtraBold', family='Apple SD Gothic Neo', size=24, traits='Bold', weight=10) at 0x1248a7e10
1097 Font(name='AppleSDGothicNeo-Heavy', family='Apple SD Gothic Neo', size=12, traits='Bold', weight=10) at 0x1248b0350
1098+Font(name='AppleSDGothicNeo-ExtraBold', family='Apple SD Gothic Neo', size=24, traits='Bold', weight=10) at 0x1248b0110
 --- Family 'Apple Symbols'
1099 Font(name='AppleSymbols', family='Apple Symbols', size=12, weight=5) at 0x1248b0610
1100+Font(name='AppleSymbols', family='Apple Symbols', size=24, weight=5) at 0x1248b06d0
 --- Family 'AppleGothic'
1101 Font(name='AppleGothic', family='AppleGothic', size=12, weight=5) at 0x1248b0590
1102+Font(name='AppleGothic', family='AppleGothic', size=24, weight=5) at 0x1248b0890
 --- Family 'AppleMyungjo'
1103 Font(name='AppleMyungjo', family='AppleMyungjo', size=12, weight=5) at 0x1248b07d0
1104+Font(name='AppleMyungjo', family='AppleMyungjo', size=24, weight=5) at 0x1248b0a50
'''
del _

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2023 -- mrJean1 at Gmail -- All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
