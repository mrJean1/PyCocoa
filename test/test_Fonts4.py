
# -*- coding: utf-8 -*-

# List all Fonts.

import run as __  # PYCHOK sys.path
from pycocoa import fontfamilies, fontsof4, fontTraitstrs

__version__ = '23.01.18'

if __name__ == '__main__':

    import sys

    i = 0
    for fam in fontfamilies():
        print(' --- Family %r' % (fam,))
        for f4 in fontsof4(fam):
            i += 1
            t = ' '.join(fontTraitstrs(f4[3]))
            print('%4d %r %s' % (i, f4, t))

    sys.exit(0 if i > 500 else 1)

# sample output, using Font.traitsup
_ = '''
% python -m test.test_Fonts
 --- Family 'Academy Engraved LET'
   1 ('AcademyEngravedLetPlain', 'Plain', 5, 0)
 --- Family 'Al Bayan'
   2 ('AlBayan', 'Plain', 5, 0)
   3 ('AlBayan-Bold', 'Bold', 9, 2) Bold
 --- Family 'Al Nile'
   4 ('AlNile', 'Regular', 5, 0)
   5 ('AlNile-Bold', 'Bold', 9, 2) Bold
 --- Family 'Al Tarikh'
   6 ('AlTarikh', 'Regular', 5, 0)
 --- Family 'American Typewriter'
   7 ('AmericanTypewriter', 'Regular', 5, 0)
   8 ('AmericanTypewriter-Light', 'Light', 3, 0)
   9 ('AmericanTypewriter-Semibold', 'Semibold', 8, 2) Bold
  10 ('AmericanTypewriter-Bold', 'Bold', 9, 2) Bold
  11 ('AmericanTypewriter-Condensed', 'Condensed', 5, 64) Condensed
  12 ('AmericanTypewriter-CondensedLight', 'Condensed Light', 3, 64) Condensed
  13 ('AmericanTypewriter-CondensedBold', 'Condensed Bold', 9, 66) Bold Condensed
 --- Family 'Andale Mono'
  14 ('AndaleMono', 'Regular', 5, 1024) MonoSpace
 --- Family 'Arial'
  15 ('ArialMT', 'Regular', 5, 0)
  16 ('Arial-ItalicMT', 'Italic', 5, 1) Italic
  17 ('Arial-BoldMT', 'Bold', 9, 2) Bold
  18 ('Arial-BoldItalicMT', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'Arial Black'
  19 ('Arial-Black', 'Regular', 11, 2) Bold
 --- Family 'Arial Hebrew'
  20 ('ArialHebrew', 'Regular', 5, 0)
  21 ('ArialHebrew-Light', 'Light', 3, 0)
  22 ('ArialHebrew-Bold', 'Bold', 9, 2) Bold
 --- Family 'Arial Hebrew Scholar'
  23 ('ArialHebrewScholar', 'Regular', 5, 0)
  24 ('ArialHebrewScholar-Light', 'Light', 3, 0)
  25 ('ArialHebrewScholar-Bold', 'Bold', 9, 2) Bold
 --- Family 'Arial Narrow'
  26 ('ArialNarrow', 'Regular', 5, 0)
  27 ('ArialNarrow-Italic', 'Italic', 5, 1) Italic
  28 ('ArialNarrow-Bold', 'Bold', 9, 2) Bold
  29 ('ArialNarrow-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'Arial Rounded MT Bold'
  30 ('ArialRoundedMTBold', 'Regular', 5, 0)
 --- Family 'Arial Unicode MS'
  31 ('ArialUnicodeMS', 'Regular', 5, 0)
 --- Family 'Athelas'
  32 ('Athelas-Regular', 'Regular', 5, 0)
  33 ('Athelas-Italic', 'Italic', 5, 1) Italic
  34 ('Athelas-Bold', 'Bold', 9, 2) Bold
  35 ('Athelas-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'Avenir'
  36 ('Avenir-Book', 'Book', 5, 0)
  37 ('Avenir-Roman', 'Roman', 5, 0)
  38 ('Avenir-BookOblique', 'Book Oblique', 5, 1) Italic
  39 ('Avenir-Oblique', 'Oblique', 5, 1) Italic
  40 ('Avenir-Light', 'Light', 3, 0)
  41 ('Avenir-LightOblique', 'Light Oblique', 3, 1) Italic
  42 ('Avenir-Medium', 'Medium', 6, 0)
  43 ('Avenir-MediumOblique', 'Medium Oblique', 7, 1) Italic
  44 ('Avenir-Heavy', 'Heavy', 10, 2) Bold
  45 ('Avenir-HeavyOblique', 'Heavy Oblique', 10, 3) Bold Italic
  46 ('Avenir-Black', 'Black', 11, 2) Bold
  47 ('Avenir-BlackOblique', 'Black Oblique', 11, 3) Bold Italic
 --- Family 'Avenir Next'
  48 ('AvenirNext-Regular', 'Regular', 5, 0)
  49 ('AvenirNext-Italic', 'Italic', 5, 1) Italic
  50 ('AvenirNext-UltraLight', 'Ultra Light', 2, 0)
  51 ('AvenirNext-UltraLightItalic', 'Ultra Light Italic', 2, 1) Italic
  52 ('AvenirNext-Medium', 'Medium', 6, 0)
  53 ('AvenirNext-MediumItalic', 'Medium Italic', 7, 1) Italic
  54 ('AvenirNext-DemiBold', 'Demi Bold', 8, 2) Bold
  55 ('AvenirNext-DemiBoldItalic', 'Demi Bold Italic', 8, 3) Bold Italic
  56 ('AvenirNext-Bold', 'Bold', 9, 2) Bold
  57 ('AvenirNext-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
  58 ('AvenirNext-Heavy', 'Heavy', 10, 2) Bold
  59 ('AvenirNext-HeavyItalic', 'Heavy Italic', 10, 3) Bold Italic
 --- Family 'Avenir Next Condensed'
  60 ('AvenirNextCondensed-Regular', 'Regular', 5, 64) Condensed
  61 ('AvenirNextCondensed-Italic', 'Italic', 5, 65) Condensed Italic
  62 ('AvenirNextCondensed-UltraLight', 'Ultra Light', 2, 64) Condensed
  63 ('AvenirNextCondensed-UltraLightItalic', 'Ultra Light Italic', 2, 65) Condensed Italic
  64 ('AvenirNextCondensed-Medium', 'Medium', 6, 64) Condensed
  65 ('AvenirNextCondensed-MediumItalic', 'Medium Italic', 7, 65) Condensed Italic
  66 ('AvenirNextCondensed-DemiBold', 'Demi Bold', 8, 66) Bold Condensed
  67 ('AvenirNextCondensed-DemiBoldItalic', 'Demi Bold Italic', 8, 67) Bold Condensed Italic
  68 ('AvenirNextCondensed-Bold', 'Bold', 9, 66) Bold Condensed
  69 ('AvenirNextCondensed-BoldItalic', 'Bold Italic', 9, 67) Bold Condensed Italic
  70 ('AvenirNextCondensed-Heavy', 'Heavy', 10, 66) Bold Condensed
  71 ('AvenirNextCondensed-HeavyItalic', 'Heavy Italic', 10, 67) Bold Condensed Italic
 --- Family 'Ayuthaya'
  72 ('Ayuthaya', 'Regular', 5, 0)
 --- Family 'Baghdad'
  73 ('Baghdad', 'Regular', 5, 0)
 --- Family 'Bangla MN'
  74 ('BanglaMN', 'Regular', 5, 0)
  75 ('BanglaMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Bangla Sangam MN'
  76 ('BanglaSangamMN', 'Regular', 5, 0)
  77 ('BanglaSangamMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Bank Gothic'
  78 ('BankGothic-Light', 'Light', 3, 0)
  79 ('BankGothic-Medium', 'Medium', 6, 0)
 --- Family 'Baskerville'
  80 ('Baskerville', 'Regular', 5, 0)
  81 ('Baskerville-Italic', 'Italic', 5, 1) Italic
  82 ('Baskerville-SemiBold', 'SemiBold', 8, 2) Bold
  83 ('Baskerville-SemiBoldItalic', 'SemiBold Italic', 8, 3) Bold Italic
  84 ('Baskerville-Bold', 'Bold', 9, 2) Bold
  85 ('Baskerville-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'Beirut'
  86 ('Beirut', 'Regular', 9, 2) Bold
 --- Family 'Big Caslon'
  87 ('BigCaslon-Medium', 'Medium', 6, 0)
 --- Family 'Blackmoor LET'
  88 ('BlackmoorLetPlain', 'Plain', 11, 2) Bold
 --- Family 'BlairMdITC TT'
  89 ('BlairMdITCTT-Medium', 'Medium', 6, 0)
 --- Family 'Bodoni 72'
  90 ('BodoniSvtyTwoITCTT-Book', 'Book', 5, 0)
  91 ('BodoniSvtyTwoITCTT-BookIta', 'Book Italic', 5, 1) Italic
  92 ('BodoniSvtyTwoITCTT-Bold', 'Bold', 9, 2) Bold
 --- Family 'Bodoni 72 Oldstyle'
  93 ('BodoniSvtyTwoOSITCTT-Book', 'Book', 5, 0)
  94 ('BodoniSvtyTwoOSITCTT-BookIt', 'Book Italic', 5, 1) Italic
  95 ('BodoniSvtyTwoOSITCTT-Bold', 'Bold', 9, 2) Bold
 --- Family 'Bodoni 72 Smallcaps'
  96 ('BodoniSvtyTwoSCITCTT-Book', 'Book', 5, 0)
 --- Family 'Bodoni Ornaments'
  97 ('BodoniOrnamentsITCTT', 'Regular', 5, 0)
 --- Family 'Bordeaux Roman Bold LET'
  98 ('BordeauxRomanBoldLetPlain', 'Plain', 9, 2) Bold
 --- Family 'Bradley Hand'
  99 ('BradleyHandITCTT-Bold', 'Bold', 9, 34) Bold Expanded
 --- Family 'Brush Script MT'
 100 ('BrushScriptMT', 'Italic', 5, 0)
 --- Family 'Capitals'
 101 ('CapitalsRegular', 'Regular', 9, 66) Bold Condensed
 --- Family 'Casual'
 102 ('AppleCasual', 'Regular', 5, 0)
 --- Family 'Chalkboard'
 103 ('Chalkboard', 'Regular', 5, 0)
 104 ('Chalkboard-Bold', 'Bold', 9, 2) Bold
 --- Family 'Chalkboard SE'
 105 ('ChalkboardSE-Regular', 'Regular', 5, 0)
 106 ('ChalkboardSE-Light', 'Light', 3, 0)
 107 ('ChalkboardSE-Bold', 'Bold', 9, 2) Bold
 --- Family 'Chalkduster'
 108 ('Chalkduster', 'Regular', 5, 0)
 --- Family 'Charter'
 109 ('Charter-Roman', 'Roman', 5, 0)
 110 ('Charter-Italic', 'Italic', 5, 1) Italic
 111 ('Charter-Bold', 'Bold', 9, 2) Bold
 112 ('Charter-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 113 ('Charter-Black', 'Black', 11, 2) Bold
 114 ('Charter-BlackItalic', 'Black Italic', 11, 3) Bold Italic
 --- Family 'Cochin'
 115 ('Cochin', 'Regular', 5, 0)
 116 ('Cochin-Italic', 'Italic', 5, 1) Italic
 117 ('Cochin-Bold', 'Bold', 9, 2) Bold
 118 ('Cochin-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'Comic Sans MS'
 119 ('ComicSansMS', 'Regular', 5, 0)
 120 ('ComicSansMS-Bold', 'Bold', 9, 2) Bold
 --- Family 'Copperplate'
 121 ('Copperplate', 'Regular', 5, 0)
 122 ('Copperplate-Light', 'Light', 3, 0)
 123 ('Copperplate-Bold', 'Bold', 9, 2) Bold
 --- Family 'Corsiva Hebrew'
 124 ('CorsivaHebrew', 'Regular', 5, 0)
 125 ('CorsivaHebrew-Bold', 'Bold', 9, 2) Bold
 --- Family 'Courier'
 126 ('Courier', 'Regular', 5, 1024) MonoSpace
 127 ('Courier-Oblique', 'Oblique', 5, 1025) Italic MonoSpace
 128 ('Courier-Bold', 'Bold', 9, 1026) Bold MonoSpace
 129 ('Courier-BoldOblique', 'Bold Oblique', 9, 1027) Bold Italic MonoSpace
 --- Family 'Courier New'
 130 ('CourierNewPSMT', 'Regular', 5, 1024) MonoSpace
 131 ('CourierNewPS-ItalicMT', 'Italic', 5, 1025) Italic MonoSpace
 132 ('CourierNewPS-BoldMT', 'Bold', 9, 1026) Bold MonoSpace
 133 ('CourierNewPS-BoldItalicMT', 'Bold Italic', 9, 1027) Bold Italic MonoSpace
 --- Family 'Cracked'
 134 ('Cracked', 'Regular', 5, 0)
 --- Family 'Damascus'
 135 ('Damascus', 'Regular', 5, 0)
 136 ('DamascusLight', 'Light', 3, 0)
 137 ('DamascusMedium', 'Medium', 6, 0)
 138 ('DamascusSemiBold', 'Semi Bold', 8, 2) Bold
 139 ('DamascusBold', 'Bold', 9, 2) Bold
 --- Family 'DecoType Naskh'
 140 ('DecoTypeNaskh', 'Regular', 5, 0)
 --- Family 'Devanagari MT'
 141 ('DevanagariMT', 'Regular', 5, 0)
 142 ('DevanagariMT-Bold', 'Bold', 9, 2) Bold
 --- Family 'Devanagari Sangam MN'
 143 ('DevanagariSangamMN', 'Regular', 5, 0)
 144 ('DevanagariSangamMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Didot'
 145 ('Didot', 'Regular', 5, 0)
 146 ('Didot-Italic', 'Italic', 5, 1) Italic
 147 ('Didot-Bold', 'Bold', 9, 2) Bold
 --- Family 'DIN Alternate'
 148 ('DINAlternate-Bold', 'Bold', 9, 2) Bold
 --- Family 'DIN Condensed'
 149 ('DINCondensed-Bold', 'Bold', 9, 66) Bold Condensed
 --- Family 'Diwan Kufi'
 150 ('DiwanKufi', 'Regular', 5, 0)
 --- Family 'Diwan Thuluth'
 151 ('DiwanThuluth', 'Regular', 5, 0)
 --- Family 'Euphemia UCAS'
 152 ('EuphemiaUCAS', 'Regular', 5, 0)
 153 ('EuphemiaUCAS-Italic', 'Italic', 5, 1) Italic
 154 ('EuphemiaUCAS-Bold', 'Bold', 9, 2) Bold
 --- Family 'Farah'
 155 ('Farah', 'Regular', 5, 0)
 --- Family 'Farisi'
 156 ('Farisi', 'Regular', 5, 0)
 --- Family 'Futura'
 157 ('Futura-Medium', 'Medium', 6, 0)
 158 ('Futura-MediumItalic', 'Medium Italic', 7, 1) Italic
 159 ('Futura-Bold', 'Bold', 9, 2) Bold
 160 ('Futura-CondensedMedium', 'Condensed Medium', 7, 64) Condensed
 161 ('Futura-CondensedExtraBold', 'Condensed ExtraBold', 11, 66) Bold Condensed
 --- Family 'GB18030 Bitmap'
 162 ('GB18030Bitmap', 'Regular', 5, 1024) MonoSpace
 --- Family 'Geeza Pro'
 163 ('GeezaPro', 'Regular', 5, 0)
 164 ('GeezaPro-Bold', 'Bold', 9, 2) Bold
 --- Family 'Geneva'
 165 ('Geneva', 'Regular', 5, 0)
 --- Family 'Georgia'
 166 ('Georgia', 'Regular', 5, 0)
 167 ('Georgia-Italic', 'Italic', 5, 1) Italic
 168 ('Georgia-Bold', 'Bold', 9, 2) Bold
 169 ('Georgia-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'Gill Sans'
 170 ('GillSans', 'Regular', 5, 0)
 171 ('GillSans-Italic', 'Italic', 5, 1) Italic
 172 ('GillSans-Light', 'Light', 3, 0)
 173 ('GillSans-LightItalic', 'Light Italic', 3, 1) Italic
 174 ('GillSans-SemiBold', 'SemiBold', 8, 2) Bold
 175 ('GillSans-SemiBoldItalic', 'SemiBold Italic', 8, 3) Bold Italic
 176 ('GillSans-Bold', 'Bold', 9, 2) Bold
 177 ('GillSans-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 178 ('GillSans-UltraBold', 'UltraBold', 11, 2) Bold
 --- Family 'Gujarati MT'
 179 ('GujaratiMT', 'Regular', 5, 0)
 180 ('GujaratiMT-Bold', 'Bold', 9, 2) Bold
 --- Family 'Gujarati Sangam MN'
 181 ('GujaratiSangamMN', 'Regular', 5, 0)
 182 ('GujaratiSangamMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Gurmukhi MN'
 183 ('GurmukhiMN', 'Regular', 5, 0)
 184 ('GurmukhiMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Gurmukhi MT'
 185 ('MonotypeGurmukhi', 'Regular', 5, 0)
 --- Family 'Gurmukhi Sangam MN'
 186 ('GurmukhiSangamMN', 'Regular', 5, 0)
 187 ('GurmukhiSangamMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Handwriting - Dakota'
 188 ('Handwriting-Dakota', 'Regular', 5, 0)
 --- Family 'Heiti SC'
 189 ('STHeitiSC-Light', 'Light', 3, 0)
 190 ('STHeitiSC-Medium', 'Medium', 9, 2) Bold
 --- Family 'Heiti TC'
 191 ('STHeitiTC-Light', 'Light', 3, 0)
 192 ('STHeitiTC-Medium', 'Medium', 9, 2) Bold
 --- Family 'Helvetica'
 193 ('Helvetica', 'Regular', 5, 0)
 194 ('Helvetica-Oblique', 'Oblique', 5, 1) Italic
 195 ('Helvetica-Light', 'Light', 3, 0)
 196 ('Helvetica-LightOblique', 'Light Oblique', 3, 1) Italic
 197 ('Helvetica-Bold', 'Bold', 9, 2) Bold
 198 ('Helvetica-BoldOblique', 'Bold Oblique', 9, 3) Bold Italic
 --- Family 'Helvetica Neue'
 199 ('HelveticaNeue', 'Regular', 5, 0)
 200 ('HelveticaNeue-Italic', 'Italic', 5, 1) Italic
 201 ('HelveticaNeue-UltraLight', 'UltraLight', 2, 0)
 202 ('HelveticaNeue-UltraLightItalic', 'UltraLight Italic', 2, 1) Italic
 203 ('HelveticaNeue-Thin', 'Thin', 3, 65536)
 204 ('HelveticaNeue-ThinItalic', 'Thin Italic', 3, 65537) Italic
 205 ('HelveticaNeue-Light', 'Light', 3, 0)
 206 ('HelveticaNeue-LightItalic', 'Light Italic', 3, 1) Italic
 207 ('HelveticaNeue-Medium', 'Medium', 6, 0)
 208 ('HelveticaNeue-MediumItalic', 'Medium Italic', 7, 1) Italic
 209 ('HelveticaNeue-Bold', 'Bold', 9, 2) Bold
 210 ('HelveticaNeue-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 211 ('HelveticaNeue-CondensedBold', 'Condensed Bold', 9, 66) Bold Condensed
 212 ('HelveticaNeue-CondensedBlack', 'Condensed Black', 11, 66) Bold Condensed
 --- Family 'Herculanum'
 213 ('Herculanum', 'Regular', 5, 0)
 --- Family 'Hiragino Kaku Gothic Pro'
 214 ('HiraKakuPro-W3', 'W3', 4, 0)
 215 ('HiraKakuPro-W6', 'W6', 8, 2) Bold
 --- Family 'Hiragino Kaku Gothic ProN'
 216 ('HiraKakuProN-W3', 'W3', 4, 0)
 217 ('HiraKakuProN-W6', 'W6', 8, 2) Bold
 --- Family 'Hiragino Kaku Gothic Std'
 218 ('HiraKakuStd-W8', 'W8', 10, 2) Bold
 --- Family 'Hiragino Kaku Gothic StdN'
 219 ('HiraKakuStdN-W8', 'W8', 10, 2) Bold
 --- Family 'Hiragino Maru Gothic Pro'
 220 ('HiraMaruPro-W4', 'W4', 5, 0)
 --- Family 'Hiragino Maru Gothic ProN'
 221 ('HiraMaruProN-W4', 'W4', 5, 0)
 --- Family 'Hiragino Mincho Pro'
 222 ('HiraMinPro-W3', 'W3', 4, 0)
 223 ('HiraMinPro-W6', 'W6', 8, 2) Bold
 --- Family 'Hiragino Mincho ProN'
 224 ('HiraMinProN-W3', 'W3', 4, 0)
 225 ('HiraMinProN-W6', 'W6', 8, 2) Bold
 --- Family 'Hiragino Sans'
 226 ('HiraginoSans-W0', 'W0', 2, 0)
 227 ('HiraginoSans-W1', 'W1', 3, 65536)
 228 ('HiraginoSans-W2', 'W2', 3, 0)
 229 ('HiraginoSans-W3', 'W3', 4, 0)
 230 ('HiraginoSans-W4', 'W4', 5, 0)
 231 ('HiraginoSans-W5', 'W5', 6, 2) Bold
 232 ('HiraginoSans-W6', 'W6', 8, 2) Bold
 233 ('HiraginoSans-W7', 'W7', 9, 2) Bold
 234 ('HiraginoSans-W8', 'W8', 10, 2) Bold
 235 ('HiraginoSans-W9', 'W9', 12, 2) Bold
 --- Family 'Hiragino Sans GB'
 236 ('HiraginoSansGB-W3', 'W3', 4, 0)
 237 ('HiraginoSansGB-W6', 'W6', 8, 2) Bold
 --- Family 'Hoefler Text'
 238 ('HoeflerText-Regular', 'Regular', 5, 0)
 239 ('HoeflerText-Ornaments', 'Ornaments', 5, 0)
 240 ('HoeflerText-Italic', 'Italic', 5, 1) Italic
 241 ('HoeflerText-Black', 'Black', 9, 2) Bold
 242 ('HoeflerText-BlackItalic', 'Black Italic', 9, 3) Bold Italic
 --- Family 'Impact'
 243 ('Impact', 'Regular', 11, 66) Bold Condensed
 --- Family 'InaiMathi'
 244 ('InaiMathi', 'Regular', 5, 0)
 245 ('InaiMathi-Bold', 'Bold', 9, 2) Bold
 --- Family 'Iowan Old Style'
 246 ('IowanOldStyle-Roman', 'Roman', 5, 0)
 247 ('IowanOldStyle-Titling', 'Titling', 5, 0)
 248 ('IowanOldStyle-Italic', 'Italic', 5, 1) Italic
 249 ('IowanOldStyle-Bold', 'Bold', 9, 2) Bold
 250 ('IowanOldStyle-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 251 ('IowanOldStyle-Black', 'Black', 11, 2) Bold
 252 ('IowanOldStyle-BlackItalic', 'Black Italic', 11, 3) Bold Italic
 --- Family 'ITF Devanagari'
 253 ('ITFDevanagari-Book', 'Book', 5, 0)
 254 ('ITFDevanagari-Light', 'Light', 3, 0)
 255 ('ITFDevanagari-Medium', 'Medium', 6, 0)
 256 ('ITFDevanagari-Demi', 'Demi', 8, 2) Bold
 257 ('ITFDevanagari-Bold', 'Bold', 9, 2) Bold
 --- Family 'ITF Devanagari Marathi'
 258 ('ITFDevanagariMarathi-Book', 'Book', 5, 0)
 259 ('ITFDevanagariMarathi-Light', 'Light', 3, 0)
 260 ('ITFDevanagariMarathi-Medium', 'Medium', 6, 0)
 261 ('ITFDevanagariMarathi-Demi', 'Demi', 8, 2) Bold
 262 ('ITFDevanagariMarathi-Bold', 'Bold', 9, 2) Bold
 --- Family 'Jazz LET'
 263 ('JazzLetPlain', 'Plain', 11, 34) Bold Expanded
 --- Family 'Kailasa'
 264 ('Kailasa', 'Regular', 5, 0)
 265 ('Kailasa-Bold', 'Bold', 9, 2) Bold
 --- Family 'Kannada MN'
 266 ('KannadaMN', 'Regular', 5, 0)
 267 ('KannadaMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Kannada Sangam MN'
 268 ('KannadaSangamMN', 'Regular', 5, 0)
 269 ('KannadaSangamMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Kefa'
 270 ('Kefa-Regular', 'Regular', 5, 0)
 271 ('Kefa-Bold', 'Bold', 9, 2) Bold
 --- Family 'Khmer MN'
 272 ('KhmerMN', 'Regular', 5, 0)
 273 ('KhmerMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Khmer Sangam MN'
 274 ('KhmerSangamMN', 'Regular', 5, 0)
 --- Family 'Kohinoor Bangla'
 275 ('KohinoorBangla-Regular', 'Regular', 5, 0)
 276 ('KohinoorBangla-Light', 'Light', 3, 0)
 277 ('KohinoorBangla-Medium', 'Medium', 6, 0)
 278 ('KohinoorBangla-Semibold', 'Semibold', 8, 2) Bold
 279 ('KohinoorBangla-Bold', 'Bold', 9, 2) Bold
 --- Family 'Kohinoor Devanagari'
 280 ('KohinoorDevanagari-Regular', 'Regular', 5, 0)
 281 ('KohinoorDevanagari-Light', 'Light', 3, 0)
 282 ('KohinoorDevanagari-Medium', 'Medium', 6, 0)
 283 ('KohinoorDevanagari-Semibold', 'Semibold', 8, 2) Bold
 284 ('KohinoorDevanagari-Bold', 'Bold', 9, 2) Bold
 --- Family 'Kohinoor Telugu'
 285 ('KohinoorTelugu-Regular', 'Regular', 5, 0)
 286 ('KohinoorTelugu-Light', 'Light', 3, 0)
 287 ('KohinoorTelugu-Medium', 'Medium', 6, 0)
 288 ('KohinoorTelugu-Semibold', 'Semibold', 8, 2) Bold
 289 ('KohinoorTelugu-Bold', 'Bold', 9, 2) Bold
 --- Family 'Kokonor'
 290 ('Kokonor', 'Regular', 5, 0)
 --- Family 'Krungthep'
 291 ('Krungthep', 'Regular', 9, 2) Bold
 --- Family 'KufiStandardGK'
 292 ('KufiStandardGK', 'Regular', 5, 0)
 --- Family 'Lao MN'
 293 ('LaoMN', 'Regular', 5, 0)
 294 ('LaoMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Lao Sangam MN'
 295 ('LaoSangamMN', 'Regular', 5, 0)
 --- Family 'Lucida Grande'
 296 ('LucidaGrande', 'Regular', 5, 0)
 297 ('LucidaGrande-Bold', 'Bold', 9, 2) Bold
 --- Family 'Luminari'
 298 ('Luminari-Regular', 'Regular', 5, 0)
 --- Family 'Malayalam MN'
 299 ('MalayalamMN', 'Regular', 5, 0)
 300 ('MalayalamMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Malayalam Sangam MN'
 301 ('MalayalamSangamMN', 'Regular', 5, 0)
 302 ('MalayalamSangamMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Marion'
 303 ('Marion-Regular', 'Regular', 5, 0)
 304 ('Marion-Italic', 'Italic', 5, 1) Italic
 305 ('Marion-Bold', 'Bold', 9, 2) Bold
 --- Family 'Marker Felt'
 306 ('MarkerFelt-Thin', 'Thin', 3, 65536)
 307 ('MarkerFelt-Wide', 'Wide', 9, 2) Bold
 --- Family 'Menlo'
 308 ('Menlo-Regular', 'Regular', 5, 1024) MonoSpace
 309 ('Menlo-Italic', 'Italic', 5, 1025) Italic MonoSpace
 310 ('Menlo-Bold', 'Bold', 9, 1026) Bold MonoSpace
 311 ('Menlo-BoldItalic', 'Bold Italic', 9, 1027) Bold Italic MonoSpace
 --- Family 'Microsoft Sans Serif'
 312 ('MicrosoftSansSerif', 'Regular', 5, 0)
 --- Family 'Mishafi'
 313 ('DiwanMishafi', 'Regular', 5, 0)
 --- Family 'Mishafi Gold'
 314 ('DiwanMishafiGold', 'Regular', 5, 0)
 --- Family 'Mona Lisa Solid ITC TT'
 315 ('MonaLisaSolidITCTT', 'Regular', 9, 66) Bold Condensed
 --- Family 'Monaco'
 316 ('Monaco', 'Regular', 5, 1024) MonoSpace
 --- Family 'Mshtakan'
 317 ('Mshtakan', 'Regular', 5, 0)
 318 ('MshtakanOblique', 'Oblique', 5, 1) Italic
 319 ('MshtakanBold', 'Bold', 9, 2) Bold
 320 ('MshtakanBoldOblique', 'BoldOblique', 9, 3) Bold Italic
 --- Family 'Muna'
 321 ('Muna', 'Regular', 5, 0)
 322 ('MunaBold', 'Bold', 9, 2) Bold
 323 ('MunaBlack', 'Black', 11, 2) Bold
 --- Family 'Myanmar MN'
 324 ('MyanmarMN', 'Regular', 5, 0)
 325 ('MyanmarMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Myanmar Sangam MN'
 326 ('MyanmarSangamMN', 'Regular', 5, 0)
 327 ('MyanmarSangamMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Nadeem'
 328 ('Nadeem', 'Regular', 5, 0)
 --- Family 'New Peninim MT'
 329 ('NewPeninimMT', 'Regular', 5, 0)
 330 ('NewPeninimMT-Inclined', 'Inclined', 5, 1) Italic
 331 ('NewPeninimMT-Bold', 'Bold', 9, 2) Bold
 332 ('NewPeninimMT-BoldInclined', 'Bold Inclined', 9, 3) Bold Italic
 --- Family 'Noteworthy'
 333 ('Noteworthy-Light', 'Light', 3, 0)
 334 ('Noteworthy-Bold', 'Bold', 9, 2) Bold
 --- Family 'Noto Nastaliq Urdu'
 335 ('NotoNastaliqUrdu', 'Regular', 5, 0)
 --- Family 'Optima'
 336 ('Optima-Regular', 'Regular', 5, 0)
 337 ('Optima-Italic', 'Italic', 5, 1) Italic
 338 ('Optima-Bold', 'Bold', 9, 2) Bold
 339 ('Optima-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 340 ('Optima-ExtraBlack', 'ExtraBlack', 11, 2) Bold
 --- Family 'Oriya MN'
 341 ('OriyaMN', 'Regular', 5, 0)
 342 ('OriyaMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Oriya Sangam MN'
 343 ('OriyaSangamMN', 'Regular', 5, 0)
 344 ('OriyaSangamMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Osaka'
 345 ('Osaka', 'Regular', 5, 0)
 --- Family 'Palatino'
 346 ('Palatino-Roman', 'Regular', 5, 0)
 347 ('Palatino-Italic', 'Italic', 5, 1) Italic
 348 ('Palatino-Bold', 'Bold', 9, 2) Bold
 349 ('Palatino-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'Papyrus'
 350 ('Papyrus', 'Regular', 5, 0)
 351 ('Papyrus-Condensed', 'Condensed', 5, 64) Condensed
 --- Family 'Party LET'
 352 ('PartyLetPlain', 'Plain', 5, 1) Italic
 --- Family 'Phosphate'
 353 ('Phosphate-Inline', 'Inline', 5, 0)
 354 ('Phosphate-Solid', 'Solid', 5, 0)
 --- Family 'PingFang HK'
 355 ('PingFangHK-Regular', 'Regular', 5, 0)
 356 ('PingFangHK-Ultralight', 'Ultralight', 2, 0)
 357 ('PingFangHK-Thin', 'Thin', 3, 65536)
 358 ('PingFangHK-Light', 'Light', 3, 0)
 359 ('PingFangHK-Medium', 'Medium', 6, 0)
 360 ('PingFangHK-Semibold', 'Semibold', 8, 2) Bold
 --- Family 'PingFang SC'
 361 ('PingFangSC-Regular', 'Regular', 5, 0)
 362 ('PingFangSC-Ultralight', 'Ultralight', 2, 0)
 363 ('PingFangSC-Thin', 'Thin', 3, 65536)
 364 ('PingFangSC-Light', 'Light', 3, 0)
 365 ('PingFangSC-Medium', 'Medium', 6, 0)
 366 ('PingFangSC-Semibold', 'Semibold', 8, 2) Bold
 --- Family 'PingFang TC'
 367 ('PingFangTC-Regular', 'Regular', 5, 0)
 368 ('PingFangTC-Ultralight', 'Ultralight', 2, 0)
 369 ('PingFangTC-Thin', 'Thin', 3, 65536)
 370 ('PingFangTC-Light', 'Light', 3, 0)
 371 ('PingFangTC-Medium', 'Medium', 6, 0)
 372 ('PingFangTC-Semibold', 'Semibold', 8, 2) Bold
 --- Family 'Plantagenet Cherokee'
 373 ('PlantagenetCherokee', 'Regular', 5, 0)
 --- Family 'PoemScriptW00-Regular'
 374 ('PoemScriptW00-Regular', 'Regular', 5, 0)
 --- Family 'PortagoITC TT'
 375 ('PortagoITCTT', 'Regular', 11, 66) Bold Condensed
 --- Family 'Princetown LET'
 376 ('PrincetownLET', 'Regular', 9, 2) Bold
 --- Family 'PT Mono'
 377 ('PTMono-Regular', 'Regular', 5, 1024) MonoSpace
 378 ('PTMono-Bold', 'Bold', 9, 1026) Bold MonoSpace
 --- Family 'PT Sans'
 379 ('PTSans-Regular', 'Regular', 5, 0)
 380 ('PTSans-Italic', 'Italic', 5, 1) Italic
 381 ('PTSans-Bold', 'Bold', 9, 2) Bold
 382 ('PTSans-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'PT Sans Caption'
 383 ('PTSans-Caption', 'Regular', 5, 0)
 384 ('PTSans-CaptionBold', 'Bold', 9, 2) Bold
 --- Family 'PT Sans Narrow'
 385 ('PTSans-Narrow', 'Regular', 5, 64) Condensed
 386 ('PTSans-NarrowBold', 'Bold', 9, 66) Bold Condensed
 --- Family 'PT Serif'
 387 ('PTSerif-Regular', 'Regular', 5, 0)
 388 ('PTSerif-Italic', 'Italic', 5, 1) Italic
 389 ('PTSerif-Bold', 'Bold', 9, 2) Bold
 390 ('PTSerif-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'PT Serif Caption'
 391 ('PTSerif-Caption', 'Regular', 5, 0)
 392 ('PTSerif-CaptionItalic', 'Italic', 5, 1) Italic
 --- Family 'Raanana'
 393 ('Raanana', 'Regular', 5, 0)
 394 ('RaananaBold', 'Bold', 9, 2) Bold
 --- Family 'Rockwell'
 395 ('Rockwell-Regular', 'Regular', 5, 0)
 396 ('Rockwell-Italic', 'Italic', 5, 1) Italic
 397 ('Rockwell-Bold', 'Bold', 9, 2) Bold
 398 ('Rockwell-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'Sana'
 399 ('Sana', 'Regular', 5, 0)
 --- Family 'Santa Fe LET'
 400 ('SantaFeLetPlain', 'Plain', 9, 3) Bold Italic
 --- Family 'Sathu'
 401 ('Sathu', 'Regular', 5, 0)
 --- Family 'Savoye LET'
 402 ('SavoyeLetPlain', 'Plain', 5, 1) Italic
 --- Family 'SchoolHouse Cursive B'
 403 ('SchoolHouseCursiveB', 'Regular', 5, 1) Italic
 --- Family 'SchoolHouse Printed A'
 404 ('SchoolHousePrintedA', 'Regular', 5, 0)
 --- Family 'Seravek'
 405 ('Seravek', 'Regular', 5, 0)
 406 ('Seravek-Italic', 'Italic', 5, 1) Italic
 407 ('Seravek-ExtraLight', 'ExtraLight', 2, 0)
 408 ('Seravek-ExtraLightItalic', 'ExtraLight Italic', 2, 1) Italic
 409 ('Seravek-Light', 'Light', 3, 0)
 410 ('Seravek-LightItalic', 'Light Italic', 3, 1) Italic
 411 ('Seravek-Medium', 'Medium', 6, 0)
 412 ('Seravek-MediumItalic', 'Medium Italic', 7, 1) Italic
 413 ('Seravek-Bold', 'Bold', 9, 2) Bold
 414 ('Seravek-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'Shree Devanagari 714'
 415 ('ShreeDev0714', 'Regular', 5, 0)
 416 ('ShreeDev0714-Italic', 'Italic', 5, 1) Italic
 417 ('ShreeDev0714-Bold', 'Bold', 9, 2) Bold
 418 ('ShreeDev0714-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'SignPainter'
 419 ('SignPainter-HouseScript', 'HouseScript', 5, 64) Condensed
 420 ('SignPainter-HouseScriptSemibold', 'HouseScript Semibold', 8, 66) Bold Condensed
 --- Family 'Silom'
 421 ('Silom', 'Regular', 9, 2) Bold
 --- Family 'Sinhala MN'
 422 ('SinhalaMN', 'Regular', 5, 0)
 423 ('SinhalaMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Sinhala Sangam MN'
 424 ('SinhalaSangamMN', 'Regular', 5, 0)
 425 ('SinhalaSangamMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Skia'
 426 ('Skia-Regular', 'Regular', 5, 0)
 427 ('Skia-Regular_Light', 'Light', 3, 0)
 428 ('Skia-Regular_Bold', 'Bold', 9, 2) Bold
 429 ('Skia-Regular_Black', 'Black', 11, 2) Bold
 430 ('Skia-Regular_Extended', 'Extended', 5, 32) Expanded
 431 ('Skia-Regular_Light-Extended', 'Light Extended', 3, 32) Expanded
 432 ('Skia-Regular_Black-Extended', 'Black Extended', 11, 34) Bold Expanded
 433 ('Skia-Regular_Condensed', 'Condensed', 5, 64) Condensed
 434 ('Skia-Regular_Light-Condensed', 'Light Condensed', 3, 64) Condensed
 435 ('Skia-Regular_Black-Condensed', 'Black Condensed', 11, 66) Bold Condensed
 --- Family 'Snell Roundhand'
 436 ('SnellRoundhand', 'Regular', 5, 1) Italic
 437 ('SnellRoundhand-Bold', 'Bold', 9, 3) Bold Italic
 438 ('SnellRoundhand-Black', 'Black', 11, 3) Bold Italic
 --- Family 'Songti SC'
 439 ('STSongti-SC-Regular', 'Regular', 5, 0)
 440 ('STSongti-SC-Light', 'Light', 3, 0)
 441 ('STSongti-SC-Bold', 'Bold', 9, 2) Bold
 442 ('STSongti-SC-Black', 'Black', 11, 2) Bold
 --- Family 'Songti TC'
 443 ('STSongti-TC-Regular', 'Regular', 5, 0)
 444 ('STSongti-TC-Light', 'Light', 3, 0)
 445 ('STSongti-TC-Bold', 'Bold', 9, 2) Bold
 --- Family 'STIXGeneral'
 446 ('STIXGeneral-Regular', 'Regular', 5, 0)
 447 ('STIXGeneral-Italic', 'Italic', 5, 1) Italic
 448 ('STIXGeneral-Bold', 'Bold', 9, 2) Bold
 449 ('STIXGeneral-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'STIXIntegralsD'
 450 ('STIXIntegralsD-Regular', 'Regular', 5, 0)
 451 ('STIXIntegralsD-Bold', 'Bold', 9, 2) Bold
 --- Family 'STIXIntegralsSm'
 452 ('STIXIntegralsSm-Regular', 'Regular', 5, 0)
 453 ('STIXIntegralsSm-Bold', 'Bold', 9, 2) Bold
 --- Family 'STIXIntegralsUp'
 454 ('STIXIntegralsUp-Regular', 'Regular', 5, 0)
 455 ('STIXIntegralsUp-Bold', 'Bold', 9, 2) Bold
 --- Family 'STIXIntegralsUpD'
 456 ('STIXIntegralsUpD-Regular', 'Regular', 5, 0)
 457 ('STIXIntegralsUpD-Bold', 'Bold', 9, 2) Bold
 --- Family 'STIXIntegralsUpSm'
 458 ('STIXIntegralsUpSm-Regular', 'Regular', 5, 0)
 459 ('STIXIntegralsUpSm-Bold', 'Bold', 9, 2) Bold
 --- Family 'STIXNonUnicode'
 460 ('STIXNonUnicode-Regular', 'Regular', 5, 0)
 461 ('STIXNonUnicode-Italic', 'Italic', 5, 1) Italic
 462 ('STIXNonUnicode-Bold', 'Bold', 9, 2) Bold
 463 ('STIXNonUnicode-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'STIXSizeFiveSym'
 464 ('STIXSizeFiveSym-Regular', 'Regular', 5, 0)
 --- Family 'STIXSizeFourSym'
 465 ('STIXSizeFourSym-Regular', 'Regular', 5, 0)
 466 ('STIXSizeFourSym-Bold', 'Bold', 9, 2) Bold
 --- Family 'STIXSizeOneSym'
 467 ('STIXSizeOneSym-Regular', 'Regular', 5, 0)
 468 ('STIXSizeOneSym-Bold', 'Bold', 9, 2) Bold
 --- Family 'STIXSizeThreeSym'
 469 ('STIXSizeThreeSym-Regular', 'Regular', 5, 0)
 470 ('STIXSizeThreeSym-Bold', 'Bold', 9, 2) Bold
 --- Family 'STIXSizeTwoSym'
 471 ('STIXSizeTwoSym-Regular', 'Regular', 5, 0)
 472 ('STIXSizeTwoSym-Bold', 'Bold', 9, 2) Bold
 --- Family 'STIXVariants'
 473 ('STIXVariants-Regular', 'Regular', 5, 0)
 474 ('STIXVariants-Bold', 'Bold', 9, 2) Bold
 --- Family 'Stone Sans ITC TT'
 475 ('StoneSansITCTT-Bold', 'Bold', 9, 2) Bold
 --- Family 'Stone Sans Sem ITC TT'
 476 ('StoneSansITCTT-Semi', 'Semi', 8, 3) Bold Italic
 477 ('StoneSansITCTT-SemiIta', 'SemiIta', 8, 3) Bold Italic
 --- Family 'STSong'
 478 ('STSong', 'Regular', 5, 0)
 --- Family 'Sukhumvit Set'
 479 ('SukhumvitSet-Text', 'Text', 5, 0)
 480 ('SukhumvitSet-Light', 'Light', 3, 0)
 481 ('SukhumvitSet-Medium', 'Medium', 6, 0)
 482 ('SukhumvitSet-SemiBold', 'Semi Bold', 8, 2) Bold
 483 ('SukhumvitSet-Bold', 'Bold', 9, 2) Bold
 484 ('SukhumvitSet-Thin', 'Thin', 3, 65600) Condensed
 --- Family 'Superclarendon'
 485 ('Superclarendon-Regular', 'Regular', 5, 0)
 486 ('Superclarendon-Italic', 'Italic', 5, 1) Italic
 487 ('Superclarendon-Light', 'Light', 3, 0)
 488 ('Superclarendon-LightItalic', 'Light Italic', 3, 1) Italic
 489 ('Superclarendon-Bold', 'Bold', 9, 2) Bold
 490 ('Superclarendon-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 491 ('Superclarendon-Black', 'Black', 11, 2) Bold
 492 ('Superclarendon-BlackItalic', 'Black Italic', 11, 3) Bold Italic
 --- Family 'Symbol'
 493 ('Symbol', 'Regular', 5, 0)
 --- Family 'Synchro LET'
 494 ('SynchroLET', 'Regular', 9, 2) Bold
 --- Family 'Tahoma'
 495 ('Tahoma', 'Regular', 5, 0)
 496 ('Tahoma-Bold', 'Bold', 9, 2) Bold
 --- Family 'Tamil MN'
 497 ('TamilMN', 'Regular', 5, 0)
 498 ('TamilMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Tamil Sangam MN'
 499 ('TamilSangamMN', 'Regular', 5, 0)
 500 ('TamilSangamMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Telugu MN'
 501 ('TeluguMN', 'Regular', 5, 0)
 502 ('TeluguMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Telugu Sangam MN'
 503 ('TeluguSangamMN', 'Regular', 5, 0)
 504 ('TeluguSangamMN-Bold', 'Bold', 9, 2) Bold
 --- Family 'Thonburi'
 505 ('Thonburi', 'Regular', 5, 0)
 506 ('Thonburi-Light', 'Light', 3, 0)
 507 ('Thonburi-Bold', 'Bold', 9, 2) Bold
 --- Family 'Times'
 508 ('Times-Roman', 'Regular', 5, 0)
 509 ('Times-Italic', 'Italic', 5, 1) Italic
 510 ('Times-Bold', 'Bold', 9, 2) Bold
 511 ('Times-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'Times New Roman'
 512 ('TimesNewRomanPSMT', 'Regular', 5, 0)
 513 ('TimesNewRomanPS-ItalicMT', 'Italic', 5, 1) Italic
 514 ('TimesNewRomanPS-BoldMT', 'Bold', 9, 2) Bold
 515 ('TimesNewRomanPS-BoldItalicMT', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'Trattatello'
 516 ('Trattatello', 'Regular', 5, 0)
 --- Family 'Trebuchet MS'
 517 ('TrebuchetMS', 'Regular', 5, 0)
 518 ('TrebuchetMS-Italic', 'Italic', 5, 1) Italic
 519 ('TrebuchetMS-Bold', 'Bold', 9, 2) Bold
 520 ('Trebuchet-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'Type Embellishments One LET'
 521 ('TypeEmbellishmentsOneLetPlain', 'Embellishments One LET Plain', 5, 0)
 --- Family 'Verdana'
 522 ('Verdana', 'Regular', 5, 0)
 523 ('Verdana-Italic', 'Italic', 5, 1) Italic
 524 ('Verdana-Bold', 'Bold', 9, 2) Bold
 525 ('Verdana-BoldItalic', 'Bold Italic', 9, 3) Bold Italic
 --- Family 'Waseem'
 526 ('Waseem', 'Regular', 5, 0)
 527 ('WaseemLight', 'Light', 3, 0)
 --- Family 'Webdings'
 528 ('Webdings', 'Regular', 5, 0)
 --- Family 'Wingdings'
 529 ('Wingdings-Regular', 'Regular', 5, 0)
 --- Family 'Wingdings 2'
 530 ('Wingdings2', 'Regular', 5, 0)
 --- Family 'Wingdings 3'
 531 ('Wingdings3', 'Regular', 5, 0)
 --- Family 'Zapf Dingbats'
 532 ('ZapfDingbatsITC', 'Regular', 5, 0)
 --- Family 'Zapfino'
 533 ('Zapfino', 'Regular', 5, 0)
 --- Family 'Apple Braille'
 534 ('AppleBraille-Outline6Dot', 'Outline 6 Dot', 5, 1024) MonoSpace
 535 ('AppleBraille-Outline8Dot', 'Outline 8 Dot', 5, 1024) MonoSpace
 536 ('AppleBraille-Pinpoint6Dot', 'Pinpoint 6 Dot', 5, 1024) MonoSpace
 537 ('AppleBraille-Pinpoint8Dot', 'Pinpoint 8 Dot', 5, 1024) MonoSpace
 538 ('AppleBraille', 'Regular', 5, 1024) MonoSpace
 --- Family 'Apple Chancery'
 539 ('Apple-Chancery', 'Chancery', 5, 0)
 --- Family 'Apple Color Emoji'
 540 ('AppleColorEmoji', 'Regular', 5, 9216) MonoSpace
 --- Family 'Apple SD Gothic Neo'
 541 ('AppleSDGothicNeo-Regular', 'Regular', 5, 0)
 542 ('AppleSDGothicNeo-Thin', 'Thin', 3, 65536)
 543 ('AppleSDGothicNeo-UltraLight', 'UltraLight', 3, 65536)
 544 ('AppleSDGothicNeo-Light', 'Light', 3, 0)
 545 ('AppleSDGothicNeo-Medium', 'Medium', 6, 0)
 546 ('AppleSDGothicNeo-SemiBold', 'SemiBold', 8, 2) Bold
 547 ('AppleSDGothicNeo-Bold', 'Bold', 9, 2) Bold
 548 ('AppleSDGothicNeo-ExtraBold', 'ExtraBold', 10, 2) Bold
 549 ('AppleSDGothicNeo-Heavy', 'Heavy', 10, 2) Bold
 --- Family 'Apple Symbols'
 550 ('AppleSymbols', 'Regular', 5, 0)
 --- Family 'AppleGothic'
 551 ('AppleGothic', 'Regular', 5, 0)
 --- Family 'AppleMyungjo'
 552 ('AppleMyungjo', 'Regular', 5, 0)
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
