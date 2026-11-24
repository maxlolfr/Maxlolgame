# Images de partage 1200x630 : bannière 16:9 plein cadre + bandeau sombre + titre lisible. Remplace make_og.py / make_og_home.py.
# Usage : python3 -I tools/make_og2.py (depuis tools/ ou la racine)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
LIL=R+'assets/fonts/lilita-one.woff'; NUN=R+'assets/fonts/nunito.woff'
W,H=1200,630
G={'la-derniere-torche':('La Dernière Torche',(255,159,46),'left'),'wyrmstorm':('WYRMSTORM',(178,107,255),'left'),
   'gravity-turn':('Gravity Turn',(79,168,255),'left'),'infinite-dungeon':('Infinite Dungeon',(255,181,71),'left')}
def banner(slug,crop_y=0.5):
    b=Image.open(R+'assets/b/%s.webp'%slug).convert('RGB'); b=b.resize((W,int(W*b.height/b.width)),Image.LANCZOS)
    top=int((b.height-H)*crop_y); return b.crop((0,top,W,top+H)).convert('RGBA')
def veil(im,col):
    v=Image.new('RGBA',(W,H),(0,0,0,0)); px=v.load()
    for x in range(W):
        a=int(235*max(0,1-x/(W*0.62))**1.25)
        for y in range(H): px[x,y]=(14,9,34,a)
    im.alpha_composite(v)
    bar=Image.new('RGBA',(W,150),(0,0,0,0)); bp=bar.load()
    for y in range(150):
        for x in range(W): bp[x,y]=(14,9,34,int(200*(y/150)**1.4))
    im.alpha_composite(bar,(0,H-150))
def title(im,text,col,y,maxw):
    d=ImageDraw.Draw(im); size=118
    while size>56:
        f=ImageFont.truetype(LIL,size)
        if d.textlength(text,font=f)<=maxw: break
        size-=4
    lines=[text]
    if d.textlength(text,font=f)>maxw and ' ' in text:
        a,b=text.rsplit(' ',1); lines=[a,b]; f=ImageFont.truetype(LIL,92)
    for ln in lines:
        for dx,dy in [(-3,0),(3,0),(0,-3),(0,3),(0,7)]: d.text((64+dx,y+dy),ln,font=f,fill=(20,10,40))
        d.text((64,y),ln,font=f,fill=(255,255,255)); y+=int(f.size*1.04)
    d.rounded_rectangle((66,y+14,66+250,y+14+9),radius=4,fill=col)
def foot(im):
    d=ImageDraw.Draw(im); d.text((64,H-84),'Maxlol Games',font=ImageFont.truetype(LIL,40),fill=(255,255,255)); d.text((64,H-38),'maxlolgames.com',font=ImageFont.truetype(NUN,26),fill=(205,195,240))
os.makedirs(R+'assets/og',exist_ok=True)
for slug,(name,col,_) in G.items():
    im=banner(slug); veil(im,col); title(im,name,col,170,520); foot(im)
    im.convert('RGB').save(R+'assets/og/%s.jpg'%slug,quality=84,optimize=True,progressive=True); print(slug,os.path.getsize(R+'assets/og/%s.jpg'%slug)//1024,'Ko')
# accueil : mosaïque 2x2 des bannières + titre central
h=Image.new('RGB',(W,H)); cw,ch=W//2,H//2
for i,s in enumerate(['la-derniere-torche','wyrmstorm','infinite-dungeon','gravity-turn']):
    b=Image.open(R+'assets/b/%s.webp'%s).convert('RGB'); r=max(cw/b.width,ch/b.height); b=b.resize((int(b.width*r)+1,int(b.height*r)+1),Image.LANCZOS)
    h.paste(b.crop((0,0,cw,ch)),((i%2)*cw,(i//2)*ch))
h=h.convert('RGBA'); sh=Image.new('RGBA',(W,H),(14,9,34,0)); ImageDraw.Draw(sh).rounded_rectangle((150,205,W-150,H-205),radius=40,fill=(14,9,34,205)); h.alpha_composite(sh)
d=ImageDraw.Draw(h); f=ImageFont.truetype(LIL,104); t='Maxlol Games'; w=d.textlength(t,font=f)
for dx,dy in [(-3,0),(3,0),(0,-3),(0,3),(0,6)]: d.text(((W-w)/2+dx,226+dy),t,font=f,fill=(20,10,40))
d.text(((W-w)/2,226),t,font=f,fill=(255,200,90))
f2=ImageFont.truetype(NUN,32); u='maxlolgames.com'; d.text(((W-d.textlength(u,font=f2))/2,H-205-62),u,font=f2,fill=(225,218,250))
h.convert('RGB').save(R+'assets/og.jpg',quality=84,optimize=True,progressive=True); print('home',os.path.getsize(R+'assets/og.jpg')//1024,'Ko')
