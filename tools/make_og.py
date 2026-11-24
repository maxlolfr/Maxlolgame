# Génère les images de partage 1200x630 par jeu (assets/og/<slug>.jpg). Usage : python3 tools/make_og.py (depuis la racine du site)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
LIL=R+'assets/fonts/lilita-one.woff'; NUN=R+'assets/fonts/nunito.woff'
GAMES={'la-derniere-torche':('La Dernière Torche',(255,159,46),'art/La-Derniere-Torche/02-les-huit-heros.webp'),'wyrmstorm':('WYRMSTORM',(178,107,255),'art/WYRMSTORM/12-affiche-heros.webp'),
       'gravity-turn':('Gravity Turn',(79,168,255),None),'infinite-dungeon':('Infinite Dungeon',(255,181,71),'art/Infinite-Dungeon/02-couverture.webp')}
W,H=1200,630
def grad(c):
    im=Image.new('RGB',(W,H)); px=im.load(); base=(26,18,56)
    for y in range(H):
        for x in range(0,W):
            t=min(1,max(0,(x/W)*0.9+(1-y/H)*0.25)); a=0.38*(1-t)**1.6
            px[x,y]=tuple(int(base[i]*(1-a)+c[i]*a) for i in range(3))
    return im
def fit(img,h):
    r=h/img.height; return img.resize((int(img.width*r),h),Image.LANCZOS)
def card(img,h,col):
    img=fit(img.convert('RGBA'),h); m=Image.new('L',img.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0)+img.size,radius=34,fill=255)
    out=Image.new('RGBA',(img.width+12,img.height+12),(0,0,0,0)); d=ImageDraw.Draw(out); d.rounded_rectangle((0,0,out.width-1,out.height-1),radius=40,fill=col+(255,))
    out.paste(img,(6,6),m); return out
for slug,(name,col,art) in GAMES.items():
    if slug=='gravity-turn' and os.path.exists(R+'art/Gravity-Turn/01-banniere-logo.png'):   # visuel officiel : pas de recomposition
        _b=Image.open(R+'art/Gravity-Turn/01-banniere-logo.png').convert('RGB'); _o=Image.new('RGB',(W,H),(26,18,56)); _o.paste(_b.resize((W,628),Image.LANCZOS),(0,1)); os.makedirs(R+'assets/og',exist_ok=True); _o.save(R+'assets/og/gravity-turn.jpg',quality=84,optimize=True,progressive=True); continue
    im=grad(col).convert('RGBA')
    # visuel à droite, légèrement incliné
    if art: v=Image.open(R+art)
    else:
        v=Image.new('RGBA',(520,520),(0,0,0,0)); j=Image.open(R+'assets/gt-jelly.webp').convert('RGBA').resize((400,400)); l=Image.open(R+'assets/gt-logo.webp').convert('RGBA'); l=l.resize((470,int(470*l.height/l.width)))
        bg=Image.new('RGBA',(520,520),(35,60,140,255)); bg.paste(j,(60,30),j); bg.paste(l,(25,380),l); v=bg
    c=card(v,500 if art else 500,col).rotate(-4,expand=True,resample=Image.BICUBIC)
    sh=Image.new('RGBA',(c.width+120,c.height+120),(0,0,0,0)); sh.paste((0,0,0,140),(60,60),mask=c.split()[3]); sh=sh.filter(ImageFilter.GaussianBlur(18))
    x=W-c.width-70; y=(H-c.height)//2
    im.alpha_composite(sh,(x+10-60,y+16-60)); im.alpha_composite(c,(x,y))
    d=ImageDraw.Draw(im)
    size=104
    while True:
        f=ImageFont.truetype(LIL,size); w=d.textlength(name,font=f)
        if w<=W-c.width-150 or size<56: break
        size-=4
    # coupe en deux lignes si trop long
    lines=[name]
    if d.textlength(name,font=f)>W-c.width-150 and ' ' in name:
        a,b=name.rsplit(' ',1); lines=[a,b]; f=ImageFont.truetype(LIL,84)
    ty=210-(len(lines)-1)*45
    for ln in lines:
        d.text((72,ty+4),ln,font=f,fill=(0,0,0,110)); d.text((70,ty),ln,font=f,fill=(255,255,255)); ty+=int(f.size*1.05)
    d.rounded_rectangle((70,ty+22,70+230,ty+22+8),radius=4,fill=col)
    f2=ImageFont.truetype(NUN,34); d.text((70,ty+50),'Jouable dans le navigateur',font=f2,fill=(210,200,245)) if False else None
    f3=ImageFont.truetype(LIL,38); d.text((70,H-92),'Maxlol Games',font=f3,fill=(255,255,255)); d.text((70,H-48),'maxlolgames.com',font=ImageFont.truetype(NUN,26),fill=(190,180,230))
    ic=Image.open(R+'assets/brand/logo-maxlol-games-icon-ml.png').convert('RGBA').resize((64,64),Image.LANCZOS); im.alpha_composite(ic,(W-64-72,H-64-44)) if False else None
    os.makedirs(R+'assets/og',exist_ok=True); im.convert('RGB').save(R+'assets/og/%s.jpg'%slug,quality=84,optimize=True,progressive=True)
    print(slug,os.path.getsize(R+'assets/og/%s.jpg'%slug)//1024,'Ko')
