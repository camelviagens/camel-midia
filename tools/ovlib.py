from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
W,H=1080,1920
A='/home/claude/top5'; O='/home/claude/top5/build'
FB='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
FX='/usr/share/fonts/truetype/google-fonts/Poppins-ExtraBold.ttf'
FS='/usr/share/fonts/truetype/google-fonts/Poppins-SemiBold.ttf'
FM='/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
for f in [FX,FS,FM]:
    if not os.path.exists(f): print('missing',f)
def F(p,s): return ImageFont.truetype(p if os.path.exists(p) else FB,s)
NAVY=(16,42,120); NAVY2=(10,30,95); LBLUE=(56,200,250); WHITE=(255,255,255)



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
    x0,y0,x1,y1=(190,350,890,500) if len(city)>12 else (230,350,850,500)
    def dr(d,shadow):
        d.rounded_rectangle((x0,y0,x1,y1),radius=48,fill=(14,36,110,235) if not shadow else (0,0,0,255),outline=None if shadow else LBLUE,width=4)
        if shadow: return
        d.ellipse((x0+16,y0+17,x0+132,y0+133),fill=LBLUE)
        f=F(FB,60); t=f"{rank}º"; w=d.textlength(t,font=f); d.text((x0+74-w/2,y0+33),t,font=f,fill=NAVY2)
        tx=x0+150; wa=x1-tx-24; sz=64
        while d.textlength(city,font=F(FB,sz))>wa: sz-=2
        fc=F(FB,sz)
        w=d.textlength(city,font=fc); d.text((tx+(wa-w)/2,y0+12),city,font=fc,fill=WHITE)
        ss=34
        while d.textlength(sub,font=F(FM,ss))>wa-10: ss-=2
        fs=F(FM,ss); w=d.textlength(sub,font=fs); d.text((tx+(wa-w)/2,y0+90),sub,font=fs,fill=(150,220,255))
    shadowed(im,dr)


def card(im, datas, preco, pp, hotel):
    x0,y0,x1,y1=140,1150,940,1590
    def dr(d,shadow):
        d.rounded_rectangle((x0,y0,x1,y1),radius=46,fill=(0,0,0,255) if shadow else (255,255,255,248))
        if shadow: return
        fc=F(FB,34); w=d.textlength(datas,font=fc)+70
        cx0=(W-w)/2; d.rounded_rectangle((cx0,y0-32,cx0+w,y0+32),radius=32,fill=NAVY,outline=LBLUE,width=3)
        d.text((cx0+35,y0-25),datas,font=fc,fill=WHITE)
        ctext(d,y0+50,"7 noites  •  voo + hotel  •  saindo de UDI",F(FM,32),fill=(60,75,120))
        fr=F(FB,58); fp=F(FX,150)
        wr=d.textlength("R$",font=fr); wp=d.textlength(preco,font=fp); tot=wr+18+wp; sx=(W-tot)/2
        d.text((sx,y0+160),"R$",font=fr,fill=NAVY); d.text((sx+wr+18,y0+78),preco,font=fp,fill=NAVY)
        ctext(d,y0+262,"pacote para 2 adultos",F(FB,44),fill=NAVY)
        ctext(d,y0+318,f"só R$ {pp} por pessoa",F(FS,34),fill=(20,150,215))
        ctext(d,y0+372,hotel+"  •  café da manhã",F(FM,28),fill=(90,100,130))
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



logo=Image.open(f'{A}/logo_camel.png').convert('RGBA')
