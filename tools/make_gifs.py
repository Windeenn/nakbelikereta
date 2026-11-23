"""Jana semua GIF animasi untuk laman. Jalankan: python3 tools/make_gifs.py"""
import math
from PIL import Image, ImageDraw, ImageFilter

A = 'assets/'
CORAL, GREEN, BLUE, GOLD, RED = (232,92,74), (29,74,55), (58,98,181), (227,163,60), (217,38,43)
WHITE = (255,255,255)

def flat(im, bg=(246,244,241)):
    """Ratakan tekstur kertas supaya GIF lebih ringan."""
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            if r > 222 and g > 218 and b > 212: px[x, y] = bg
    return im

def save(frames, path, ms=70, colors=96):
    ref = frames[0].convert('RGB').quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = [f.convert('RGB').quantize(palette=ref, dither=Image.Dither.NONE) for f in frames]
    pal[0].save(path, save_all=True, append_images=pal[1:], duration=ms, loop=0, optimize=True, disposal=2)

def star(d, cx, cy, r, col):
    k = r * .28
    d.polygon([(cx,cy-r),(cx+k,cy-k),(cx+r,cy),(cx+k,cy+k),(cx,cy+r),(cx-k,cy+k),(cx-r,cy),(cx-k,cy-k)], fill=col)

# 1. Produk hero: kilauan + bintang berkelip
def produk():
    base = Image.open(A+'produk.jpg').convert('RGB')
    base = flat(base.resize((560, round(base.height*560/base.width)), Image.LANCZOS))
    W, H = base.size
    sparks = [(130,35,GOLD),(375,22,CORAL),(525,80,GOLD),(410,220,WHITE),(80,265,BLUE),(490,350,CORAL),(262,335,GOLD)]
    N = 18; frames = []
    for i in range(N):
        t = i / N
        f = base.copy()
        # sapuan kilauan pepenjuru
        shine = Image.new('L', (W, H), 0); sd = ImageDraw.Draw(shine)
        x = -200 + t * (W + 400)
        sd.polygon([(x,0),(x+70,0),(x-110,H),(x-180,H)], fill=90)
        shine = shine.filter(ImageFilter.GaussianBlur(18))
        f = Image.composite(Image.new('RGB', (W,H), WHITE), f, shine)
        d = ImageDraw.Draw(f)
        for j, (sx, sy, c) in enumerate(sparks):
            s = max(0, math.sin(2*math.pi*(t + j/len(sparks))))
            if s > .05: star(d, sx, sy, 4 + 12*s, c)
        frames.append(f)
    save(frames, A+'produk.gif', 80)

# 2. Clicker berayun
def clicker():
    im = Image.open(A+'clicker.jpg').convert('RGB')
    im = flat(im.resize((180, round(im.height*180/im.width)), Image.LANCZOS))
    bg = im.getpixel((5, 5))
    pad = 40
    canvas = Image.new('RGB', (im.width + pad*2, im.height + 20), bg)
    canvas.paste(im, (pad, 10))
    frames = []
    for i in range(20):
        ang = 9 * math.sin(2*math.pi*i/20)
        frames.append(canvas.rotate(ang, resample=Image.BICUBIC, center=(canvas.width/2, 22), fillcolor=bg))
    save(frames, A+'clicker.gif', 70)

# 3. Ikon ciri (dilukis 2x, kecilkan ke 112px)
S = 224
def icon(draw_fn, path, n=20, bg=WHITE):
    frames = []
    for i in range(n):
        f = Image.new('RGB', (S, S), bg); draw_fn(ImageDraw.Draw(f), i/n)
        frames.append(f.resize((112,112), Image.LANCZOS))
    save(frames, path, 80)

def cal_frame(d, col):
    d.rounded_rectangle((32,48,192,196), 18, fill=WHITE, outline=col, width=8)
    d.rectangle((36,52,188,84), fill=col)
    for x in (72,152): d.rounded_rectangle((x-6,32,x+6,64), 6, fill=GREEN)

def haid(d, t):
    cal_frame(d, CORAL)
    lit = int(t*10)
    for k in range(9):
        cx, cy = 66 + (k%3)*46, 110 + (k//3)*28
        d.ellipse((cx-10,cy-10,cx+10,cy+10), fill=CORAL if k < lit else (240,228,224))
    s = 1 + .15*math.sin(2*math.pi*t*2)
    cx, cy, r = 178, 168, 26*s
    d.ellipse((cx-r, cy-r*.6, cx+r, cy+r*1.2), fill=RED)
    d.polygon([(cx-r*.75, cy), (cx+r*.75, cy), (cx, cy-r*1.6)], fill=RED)

def cuti(d, t):
    cal_frame(d, GREEN)
    hi = int(t*6) % 6
    for k in range(6):
        cx, cy = 70 + (k%3)*42, 118 + (k//3)*42
        if k == hi: d.ellipse((cx-17,cy-17,cx+17,cy+17), fill=GOLD)
        d.rectangle((cx-7,cy-7,cx+7,cy+7), fill=GREEN if k != hi else WHITE)
    y = 20 + 8*math.sin(2*math.pi*t)
    d.polygon([(176,y+20),(212,y+38),(176,y+56)], fill=CORAL); d.line((176,y+16,176,y+92), fill=GREEN, width=6)

def mutabaah(d, t):
    d.rounded_rectangle((40,28,184,200), 18, fill=WHITE, outline=BLUE, width=8)
    done = int(t*5)
    for k in range(4):
        y = 62 + k*36
        d.rounded_rectangle((60,y-12,84,y+12), 6, outline=BLUE, width=5, fill=BLUE if k < done else WHITE)
        if k < done: d.line([(65,y),(71,y+7),(80,y-7)], fill=WHITE, width=5)
        d.rounded_rectangle((98,y-5,164,y+5), 5, fill=(200,212,238))

def hijrah(d, t):
    d.ellipse((50,40,170,160), fill=GOLD); d.ellipse((82,28,192,138), fill=WHITE)
    for j, (x, y) in enumerate([(160,140),(190,80),(120,180),(60,180)]):
        s = max(0, math.sin(2*math.pi*(t + j/4)))
        star(d, x, y, 5 + 14*s, GOLD if j % 2 else BLUE)

produk(); clicker()
icon(haid, A+'ic-haid.gif'); icon(cuti, A+'ic-cuti.gif'); icon(mutabaah, A+'ic-mutabaah.gif'); icon(hijrah, A+'ic-hijrah.gif')
print('siap')
