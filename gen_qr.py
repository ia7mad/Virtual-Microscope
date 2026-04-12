import base64, pathlib

# Embed the Al Baha Health Cluster banner image
img_path = 'C:/Users/alallah/.gemini/antigravity/scratch/virtual_microscope/photo_2026-04-12_20-00-00.jpg'
img_b64  = base64.b64encode(pathlib.Path(img_path).read_bytes()).decode()
img_data = f'data:image/jpeg;base64,{img_b64}'

# Image is 1280x719 (≈16:9). At svg_w=560 the natural height = 560*719/1280 = 315px.
# Pure black background → zero clipping, zero overlay, seamless merge with dark SVG.
# Image is 1280x719. At target width=340, height = 340*719/1280 ≈ 190px.
LOGO_W   = 340
LOGO_H   = 190
SHIFT    = 180   # Vertical space for header
GAP      = 10    # Space between logo and first title

matrix_rows = [
  '111111100101100010101010101111111',
  '100000100001011010001010101000001',
  '101110101010110011011111101011101',
  '101110101100001111111111101011101',
  '101110100010100101011000001011101',
  '100000100101000101101101101000001',
  '111111101010101010101010101111111',
  '000000000011000011101011000000000',
  '000110110011101001110001100001100',
  '111000010111101010101001010110000',
  '000111101000010110100111011100111',
  '100110010110010111110000100110101',
  '100100110111011110010111101101001',
  '100111000001011100001101000101010',
  '001110101111001100100000001100000',
  '111011011000100111110000110101111',
  '001101111010010011111001011111001',
  '101000010011001100110110111111001',
  '100101110111101111110101000101111',
  '011011000000110100100011111001101',
  '101110101111111101100000100001000',
  '111011000101100011110011000110000',
  '101000101001010101100101001110111',
  '101101001101110101110011100010110',
  '110111100111000010001000111110000',
  '000000001000110010010100100010100',
  '111111101001010011111001101011000',
  '100000100100111000100111100011110',
  '101110101101010000010111111110010',
  '101110101010101001011010010100001',
  '101110100100110011110101100010011',
  '100000100011100101101100001001111',
  '111111100111011111011011100010000',
]

matrix = [[c == '1' for c in row] for row in matrix_rows]
size = len(matrix)

svg_w  = 560
SHIFT  = 180   # push all content down by this
svg_h  = 780 + SHIFT
mod    = 10
qr_px  = size * mod        # 330
margin_x = (svg_w - qr_px) // 2
margin_y = 210 + SHIFT

logo_s, logo_e = 12, 21

def is_finder(r, c):
    return (r < 7 and c < 7) or (r < 7 and c >= size-7) or (r >= size-7 and c < 7)

def in_logo(r, c):
    return logo_s <= r < logo_e and logo_s <= c < logo_e

# Strings — exact text from the welcome page
en_title  = 'VIRTUAL MICROSCOPE'
ar_title  = '\u0627\u0644\u0645\u062c\u0647\u0631 \u0627\u0644\u0627\u0641\u062a\u0631\u0627\u0636\u064a'        # المجهر الافتراضي
en_sub1   = 'Discover the Unseen.'
en_sub2   = 'See the microscopic world through the eyes of a laboratory.'
ar_sub1   = '\u0627\u0643\u062a\u0634\u0641 \u0645\u0627 \u0644\u0627 \u062a\u0631\u0627\u0647 \u0627\u0644\u0639\u064a\u0646.'   # اكتشف ما لا تراه العين.
ar_sub2   = '\u0627\u0633\u062a\u0643\u0634\u0641 \u0627\u0644\u0639\u0627\u0644\u0645 \u0627\u0644\u0645\u062c\u0647\u0631\u064a \u062a\u0645\u0627\u0645\u0627\u064b \u0643\u0645\u0627 \u064a\u0631\u0627\u0647 \u0627\u0644\u0645\u062e\u062a\u0628\u0631'  # استكشف العالم المجهري تماماً كما يراه المختبر
ar_footer = '\u0645\u062c\u0647\u0631 \u0627\u0641\u062a\u0631\u0627\u0636\u064a \u062a\u0641\u0627\u0639\u0644\u064a \u2014 \u0645\u062c\u0627\u0646\u064a\u060c \u0644\u0644\u062c\u0645\u064a\u0639'

L = []
L.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">')

L.append('''<defs>
  <radialGradient id="bg" cx="50%" cy="50%" r="75%">
    <stop offset="0%" stop-color="#0f1923"/>
    <stop offset="100%" stop-color="#020509"/>
  </radialGradient>
  <radialGradient id="glow" cx="50%" cy="58%" r="52%">
    <stop offset="0%" stop-color="#00d4ff" stop-opacity="0.13"/>
    <stop offset="100%" stop-color="#00d4ff" stop-opacity="0"/>
  </radialGradient>
  <filter id="f-glow">
    <feGaussianBlur stdDeviation="11" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="f-tglow">
    <feGaussianBlur stdDeviation="5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <linearGradient id="div-grad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%"   stop-color="#00d4ff" stop-opacity="0"/>
    <stop offset="50%"  stop-color="#00d4ff" stop-opacity="0.35"/>
    <stop offset="100%" stop-color="#00d4ff" stop-opacity="0"/>
  </linearGradient>
</defs>''')

L.append(f'<rect width="{svg_w}" height="{svg_h}" rx="22" fill="url(#bg)"/>')
L.append(f'<ellipse cx="280" cy="390" rx="240" ry="280" fill="url(#glow)"/>')

for dx in [38, 76, 114, 152, 190, 228, 266, 304, 342, 380, 418, 456, 494, 522]:
    for dy in range(20, svg_h, 38):
        op = 0.05
        L.append(f'<circle cx="{dx}" cy="{dy}" r="2.5" fill="#00d4ff" opacity="{op}"/>')

L.append(f'<rect x="1" y="1" width="{svg_w-2}" height="{svg_h-2}" rx="22" fill="none" stroke="#00d4ff" stroke-width="1" stroke-opacity="0.2"/>')

# ── Al Baha Health Cluster logo ───────────────────────────
# Centered placement: (svg_w - LOGO_W) / 2 = (560 - 340) / 2 = 110
L.append(f'<image href="{img_data}" x="110" y="15" width="{LOGO_W}" height="{LOGO_H}" preserveAspectRatio="xMidYMid meet"/>')

S = SHIFT  # shorthand
# Title
# Title
L.append(f'<text x="280" y="{35+S}" text-anchor="middle" font-family="Segoe UI,Inter,Arial,sans-serif" font-size="28" font-weight="900" letter-spacing="2" fill="white" filter="url(#f-tglow)">{en_title}</text>')
L.append(f'<text x="280" y="{67+S}" text-anchor="middle" font-family="Segoe UI,Tahoma,Arial,sans-serif" font-size="22" font-weight="800" fill="#00d4ff" filter="url(#f-tglow)" direction="rtl" unicode-bidi="embed">{ar_title}</text>')
L.append(f'<rect x="100" y="{81+S}" width="360" height="1" rx="1" fill="url(#div-grad)"/>')
# Subtitle EN
L.append(f'<text x="280" y="{118+S}" text-anchor="middle" font-family="Segoe UI,Inter,Arial,sans-serif" font-size="13" font-weight="600" fill="#e0eaf5">{en_sub1}</text>')
L.append(f'<text x="280" y="{136+S}" text-anchor="middle" font-family="Segoe UI,Inter,Arial,sans-serif" font-size="11.5" fill="#8b9bb4">{en_sub2}</text>')
# Subtitle AR
L.append(f'<text x="280" y="{158+S}" text-anchor="middle" font-family="Segoe UI,Tahoma,Arial,sans-serif" font-size="13" font-weight="600" fill="#e0eaf5" direction="rtl" unicode-bidi="embed">{ar_sub1}</text>')
L.append(f'<text x="280" y="{176+S}" text-anchor="middle" font-family="Segoe UI,Tahoma,Arial,sans-serif" font-size="11.5" fill="#8b9bb4" direction="rtl" unicode-bidi="embed">{ar_sub2}</text>')
L.append(f'<rect x="80" y="{188+S}" width="400" height="1" rx="1" fill="url(#div-grad)"/>')

# QR modules
for r in range(size):
    for c in range(size):
        if not matrix[r][c] or in_logo(r, c):
            continue
        x = margin_x + c * mod
        y = margin_y + r * mod
        if is_finder(r, c):
            L.append(f'<rect x="{x+0.8}" y="{y+0.8}" width="8.4" height="8.4" rx="2" fill="#00d4ff"/>')
        else:
            cx2 = x + mod/2
            cy2 = y + mod/2
            L.append(f'<circle cx="{cx2}" cy="{cy2}" r="3.6" fill="#00d4ff" opacity="0.92"/>')

# Logo disc
lx  = margin_x + logo_s * mod
ly  = margin_y + logo_s * mod
lw  = (logo_e - logo_s) * mod
cx0 = lx + lw/2
cy0 = ly + lw/2

L.append(f'<circle cx="{cx0}" cy="{cy0}" r="46" fill="#060e1a"/>')
L.append(f'<circle cx="{cx0}" cy="{cy0}" r="44" fill="none" stroke="#00d4ff" stroke-width="1.2" stroke-opacity="0.4"/>')

sc = 1.55
tx = cx0 - 31*sc
ty = cy0 - 34*sc
L.append(f'<g transform="translate({tx:.1f},{ty:.1f}) scale({sc})" fill="#00d4ff" filter="url(#f-glow)">')
L.append('  <rect x="28" y="6" width="6" height="14" rx="3"/>')
L.append('  <rect x="24" y="18" width="14" height="5" rx="2"/>')
L.append('  <rect x="29" y="22" width="4" height="22" rx="2"/>')
L.append('  <rect x="18" y="44" width="26" height="3" rx="1.5"/>')
L.append('  <rect x="12" y="56" width="38" height="4" rx="2"/>')
L.append('  <rect x="22" y="30" width="14" height="3" rx="1.5"/>')
L.append('  <ellipse cx="31" cy="50" rx="10" ry="3" fill="none" stroke="#00d4ff" stroke-width="2"/>')
L.append('  <rect x="28" y="42" width="6" height="4" rx="1" fill="#00c4ef"/>')
L.append('</g>')

# Footer
qr_bottom = margin_y + qr_px   # 530

L.append(f'<rect x="80" y="{qr_bottom+16}" width="400" height="1" rx="1" fill="url(#div-grad)"/>')
L.append(f'<rect x="155" y="{qr_bottom+30}" width="250" height="34" rx="17" fill="#00d4ff" fill-opacity="0.07" stroke="#00d4ff" stroke-width="1" stroke-opacity="0.3"/>')
L.append(f'<text x="280" y="{qr_bottom+52}" text-anchor="middle" font-family="Segoe UI,Inter,Arial,sans-serif" font-size="13" font-weight="700" letter-spacing="0.8" fill="#00d4ff" opacity="0.85">virtual-microscope.online</text>')
L.append(f'<text x="280" y="{qr_bottom+92}" text-anchor="middle" font-family="Segoe UI,Tahoma,Arial,sans-serif" font-size="12" font-weight="500" fill="#8b9bb4" opacity="0.5" direction="rtl" unicode-bidi="embed">{ar_footer}</text>')
L.append(f'<text x="280" y="{qr_bottom+112}" text-anchor="middle" font-family="Segoe UI,Inter,Arial,sans-serif" font-size="11" fill="#8b9bb4" opacity="0.4" letter-spacing="0.3">Interactive Virtual Microscope &#8212; Free &amp; Open for Everyone</text>')

L.append('</svg>')

out = '\n'.join(L)
path = 'C:/Users/alallah/.gemini/antigravity/scratch/virtual_microscope/qr-showcase.svg'
with open(path, 'w', encoding='utf-8') as f:
    f.write(out)
print('done', len(out), 'chars')
