from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
W,H=1080,1920
A='/home/claude/top8/assets'; O='/home/claude/top8/build'
FB='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
FX='/usr/share/fonts/truetype/google-fonts/Poppins-ExtraBold.ttf'
FS='/usr/share/fonts/truetype/google-fonts/Poppins-SemiBold.ttf'
FM='/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
for f in [FX,FS,FM]:
    if not os.path.exists(f): print('missing',f)
def F(p,s): return ImageFont.truetype(p if os.path.exists(p) else FB,s)
NAVY=(16,42,120); NAVY2=(10,30,95); LBLUE=(56,200,250); WHITE=(255,255,255)

# logo
end=Image.open(f'{A}/end.png').convert('RGBA')
cx,cy,r=556,896,398
logo=end.crop((cx-r,cy-r,cx+r,cy+r))
m=Image.new('L',logo.size,0); ImageDraw.Draw(m).ellipse((0,0,2*r,2*r),fill=255)
logo.putalpha(m); logo.save(f'{A}/logo.png')

def shadowed(base, draw_fn, blur=14, off=(0,6), alpha=110):
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); draw_fn(ImageDraw.Draw(sh), shadow=True)
    a=sh.split()[3].point(lambda v: alpha if v>0 else 0)
    s=Image.new('RGBA',(W,H),(0,0,0,0)); s.putalpha(a); s=s.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(s,off); draw_fn(ImageDraw.Draw(base), shadow=False)

def ctext(d,y,txt,font,fill=WHITE,stroke=0,sfill=NAVY2):
    w=d.textlength(txt,font=font); d.text(((W-w)/2,y),txt,font=font,fill=fill,stroke_width=stroke,stroke_fill=sfill)

def add_logo(im, size=190, y=135):
    l=logo.resize((size,size),Image.LANCZOS); im.alpha_composite(l,((W-size)//2,y))

def badge(im, rank, city, sub):
    x0,y0,x1,y1=230,350,850,500
    def dr(d,shadow):
        d.rounded_rectangle((x0,y0,x1,y1),radius=48,fill=(14,36,110,235) if not shadow else (0,0,0,255),outline=None if shadow else LBLUE,width=4)
        if shadow: return
        d.ellipse((x0+16,y0+17,x0+132,y0+133),fill=LBLUE)
        f=F(FB,60); t=f"{rank}º"; w=d.textlength(t,font=f); d.text((x0+74-w/2,y0+33),t,font=f,fill=NAVY2)
        fc=F(FB,64 if len(city)<=10 else 54); tx=x0+150; wa=x1-tx-20
        w=d.textlength(city,font=fc); d.text((tx+(wa-w)/2,y0+12),city,font=fc,fill=WHITE)
        fs=F(FM,34); w=d.textlength(sub,font=fs); d.text((tx+(wa-w)/2,y0+90),sub,font=fs,fill=(150,220,255))
    shadowed(im,dr)

def card(im, datas, dias, preco):
    x0,y0,x1,y1=150,1170,930,1530
    def dr(d,shadow):
        d.rounded_rectangle((x0,y0,x1,y1),radius=46,fill=(0,0,0,255) if shadow else (255,255,255,248))
        if shadow: return
        fc=F(FB,34); t="✈  "+datas if False else datas; w=d.textlength(t,font=fc)+70
        cx0=(W-w)/2; d.rounded_rectangle((cx0,y0-32,cx0+w,y0+32),radius=32,fill=NAVY,outline=LBLUE,width=3)
        d.text((cx0+35,y0-25),t,font=fc,fill=WHITE)
        f=F(FM,34); ctext(d,y0+52,f"{dias} dias  •  ida e volta  •  saindo de SP",f,fill=(60,75,120))
        fr=F(FB,58); fp=F(FX,150)
        wr=d.textlength("R$",font=fr); wp=d.textlength(preco,font=fp); tot=wr+18+wp; sx=(W-tot)/2
        d.text((sx,y0+160),"R$",font=fr,fill=NAVY); d.text((sx+wr+18,y0+80),preco,font=fp,fill=NAVY)
        ctext(d,y0+262,"por pessoa",F(FB,42),fill=NAVY)
        ctext(d,y0+315,"somente passagem aérea",F(FS,30),fill=(20,150,215))
    shadowed(im,dr)

def tarja(im, y, txt, size=48, bg=LBLUE, fg=NAVY2, pad=36):
    def dr(d,shadow):
        f=F(FB,size); w=d.textlength(txt,font=f)
        x=(W-w)/2-pad; d.rounded_rectangle((x,y,x+w+2*pad,y+size+40),radius=30,fill=(0,0,0,255) if shadow else bg)
        if not shadow: d.text((x+pad,y+14),txt,font=f,fill=fg)
    shadowed(im,dr)

def bigtext(im, lines, y, size, gap=10, stroke=10):
    def dr(d,shadow):
        yy=y
        for t in lines:
            f=F(FX,size); ctext(d,yy,t,f,fill=(0,0,0,255) if shadow else WHITE,stroke=stroke,sfill=(0,0,0,255) if shadow else NAVY2); yy+=size+gap
    shadowed(im,dr,blur=18,alpha=120)

def new(): return Image.new('RGBA',(W,H),(0,0,0,0))

# intro
im=new(); add_logo(im,230,170)
bigtext(im,["TOP 8"],560,260,stroke=12)
bigtext(im,["VOOS","INTERNACIONAIS"],880,110,gap=0,stroke=8)
tarja(im,1170,"saindo de São Paulo ✈" if False else "saindo de São Paulo",56)
tarja(im,1290,"por pessoa • ida e volta",40,bg=WHITE,fg=NAVY)
im.save(f'{O}/ov_intro.png')
# hook
im=new(); add_logo(im)
bigtext(im,["A Nº 1 TÁ","IMPERDÍVEL"],700,130,stroke=10)
tarja(im,1010,"saindo de São Paulo",48)
im.save(f'{O}/ov_hook.png')
dados=[(8,'ORLANDO','Estados Unidos','26/02 a 13/03/2027',15,'5.233'),
(7,'LISBOA','Portugal','18/02 a 05/03/2027',15,'5.194'),
(6,'CANCÚN','México','29/04 a 14/05/2027',15,'4.996'),
(5,'NOVA IORQUE','Estados Unidos','04/03 a 24/03/2027',20,'4.773'),
(4,'MIAMI','Estados Unidos','29/03 a 13/04/2027',15,'4.689'),
(3,'ASSUNÇÃO','Paraguai','24/12/2026 a 08/01/2027',15,'3.254'),
(2,'SANTIAGO','Chile','04/12 a 19/12/2026',15,'2.637'),
(1,'BUENOS AIRES','Argentina • a mais barata!','06/12 a 21/12/2026',15,'2.126')]
for rk,c,s,dt,di,p in dados:
    im=new(); add_logo(im); badge(im,rk,c,s); card(im,dt,di,p); im.save(f'{O}/ov_{rk}.png')
    if rk==1:
        tarja(im,1620,"SOMENTE PASSAGEM AÉREA • IDA E VOLTA",40,bg=NAVY,fg=WHITE); im.save(f'{O}/ov_1b.png')
# suspense
im=new(); add_logo(im); bigtext(im,["E A Nº 1..."],820,140,stroke=10); im.save(f'{O}/ov_susp.png')
# end card
bg=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(bg)
for y in range(H):
    t=y/H; c=(int(10+20*(1-abs(t-0.45)*2)),int(40+60*(1-abs(t-0.45)*2)),int(130+70*(1-abs(t-0.45)*2)),255); d.line((0,y,W,y),fill=c)
im=bg
def dr(d,shadow):
    ctext(d,190,"Essas promoções",F(FB,76),fill=(0,0,0,255) if shadow else WHITE); ctext(d,285,"mudam todo dia!",F(FB,76),fill=(0,0,0,255) if shadow else WHITE)
shadowed(im,dr)
l=logo.resize((760,760),Image.LANCZOS); im.alpha_composite(l,(160,480))
def dr2(d,shadow):
    d.rounded_rectangle((140,1340,940,1460),radius=60,fill=(0,0,0,255) if shadow else WHITE)
    if not shadow: ctext(d,1365,"FAÇA JÁ A SUA COTAÇÃO",F(FB,60),fill=NAVY)
shadowed(im,dr2)
d=ImageDraw.Draw(im)
ctext(d,1520,"Link na bio",F(FB,64),fill=LBLUE)
ctext(d,1620,"@agenciacamelviagens",F(FM,46),fill=WHITE)
ctext(d,1700,"Valores por pessoa, sujeitos a disponibilidade",F(FM,32),fill=(170,200,240))
im.convert('RGB').save(f'{O}/end.png')
print('ok')
