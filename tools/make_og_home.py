# Image de partage de l'accueil (assets/og.jpg, 1200x630) : titre + 4 couvertures. Usage : python3 tools/make_og_home.py
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
LIL=R+'assets/fonts/lilita-one.woff'; NUN=R+'assets/fonts/nunito.woff'
W,H=1200,630
im=Image.new('RGB',(W,H),(26,18,56)); px=im.load()
for y in range(H):
    for x in range(W):
        t=x/W; a=0.30*(1-t)**1.5; c=(255,159,46); px[x,y]=tuple(int((26,18,56)[i]*(1-a)+c[i]*a) for i in range(3))
im=im.convert('RGBA')
covs=[('art/La-Derniere-Torche/02-les-huit-heros.webp',(255,159,46)),('art/WYRMSTORM/12-affiche-heros.webp',(178,107,255)),('assets/gt-cover.webp',(79,168,255)),('art/Infinite-Dungeon/02-couverture.webp',(255,181,71))]
ch=330; xs=[440,630,815,1010]; ys=[250,110,260,100]; rot=[-5,3,-3,5]
order=[0,3,1,2]
for (p,col),x,y,r in [(covs[i],xs[i],ys[i],rot[i]) for i in order]:
    a=Image.open(R+p).convert('RGBA'); a=a.resize((int(a.width*ch/a.height),ch),Image.LANCZOS)
    m=Image.new('L',a.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0)+a.size,radius=24,fill=255)
    o=Image.new('RGBA',(a.width+10,a.height+10),(0,0,0,0)); ImageDraw.Draw(o).rounded_rectangle((0,0,o.width-1,o.height-1),radius=28,fill=col+(255,)); o.paste(a,(5,5),m)
    o=o.rotate(r,expand=True,resample=Image.BICUBIC)
    sh=Image.new('RGBA',(o.width+100,o.height+100),(0,0,0,0)); sh.paste((0,0,0,150),(50,50),mask=o.split()[3]); sh=sh.filter(ImageFilter.GaussianBlur(14))
    im.alpha_composite(sh,(x-50+8,y-50+14)); im.alpha_composite(o,(x,y))
d=ImageDraw.Draw(im)
d.text((62,88),'MAXLOL',font=ImageFont.truetype(LIL,118),fill=(255,181,71)); d.text((62,206),'GAMES',font=ImageFont.truetype(LIL,118),fill=(236,230,255))
f=ImageFont.truetype(LIL,34); y=368
for n,c in (('La Dernière Torche',(255,255,255)),('WYRMSTORM',(205,170,255)),('Gravity Turn',(150,200,255)),('Infinite Dungeon',(255,205,130))):
    d.text((66,y),n,font=f,fill=c); y+=46
d.text((66,H-52),'maxlolgames.com',font=ImageFont.truetype(NUN,28),fill=(190,180,230))
im.convert('RGB').save(R+'assets/og.jpg',quality=84,optimize=True,progressive=True); print(os.path.getsize(R+'assets/og.jpg')//1024,'Ko')
