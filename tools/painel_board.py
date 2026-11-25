from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random
W,H=1080,1920
FMB='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'; FB='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; FM='/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
F=lambda p,s: ImageFont.truetype(p,s)
YEL=(255,204,0); WH=(255,255,255); LB=(56,200,250); NAVY2=(9,22,66)
ROWS=[("SET","BRASÍLIA","R$ 496","VOO DIRETO • EMBARQUE IMEDIATO"),
("MAR","SÃO PAULO","R$ 517","VOO DIRETO • GUARULHOS"),
("MAR","RIO DE JANEIRO","R$ 595","IDA E VOLTA • POR PESSOA"),
("JAN","CURITIBA","R$ 756","IDA E VOLTA • POR PESSOA"),
("MAR","FLORIANÓPOLIS","R$ 828","IDA E VOLTA • POR PESSOA"),
("OUT","PORTO SEGURO","R$3.280","VOO + HOTEL • O CASAL"),
("ABR","P. GALINHAS","R$4.110","VOO + HOTEL • O CASAL")]
BX,BY,BW=40,640,1000; TW,TH=35,62; RH=136
COLS=[(BX+24,3),(BX+24+3*TW+26,14),(BX+24+17*TW+52,7)]
CH="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$"
def tiles(d,x,y,text,n,color):
    f=F(FMB,46)
    for i in range(n):
        tx=x+i*TW; d.rounded_rectangle((tx,y,tx+TW-4,y+TH),radius=6,fill=(28,30,36))
        d.line((tx,y+TH//2,tx+TW-4,y+TH//2),fill=(8,8,10),width=2)
        c=text[i] if i<len(text) else ' '
        if c!=' ':
            w=d.textlength(c,font=f); d.text((tx+(TW-4-w)/2,y+4),c,font=f,fill=color)
def base():
    o=Image.new('RGBA',(W,H)); 
    g=Image.new('RGBA',(W,H)); gd=ImageDraw.Draw(g)
    for y in range(0,520): gd.line((0,y,W,y),fill=(5,10,25,int(190*(1-y/520))))
    o.alpha_composite(g)
    o.alpha_composite(Image.open('logo_camel.png').convert('RGBA').resize((130,130),Image.LANCZOS),(60,70))
    d=ImageDraw.Draw(o)
    d.text((215,72),"PARTIDAS",font=F(FB,78),fill=YEL)
    d.text((219,170),"DEPARTURES  •  UBERLÂNDIA (UDI)",font=F(FM,30),fill=WH)
    sh=Image.new('RGBA',(W,H)); ImageDraw.Draw(sh).rounded_rectangle((BX,BY-90,BX+BW,BY+7*RH+30),radius=30,fill=(0,0,0,200)); o.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)))
    d=ImageDraw.Draw(o); d.rounded_rectangle((BX,BY-90,BX+BW,BY+7*RH+30),radius=30,fill=(12,13,18,205))
    for (x,n),lab in zip(COLS,["MÊS","DESTINO","A PARTIR"]): d.text((x,BY-70),lab,font=F(FB,26),fill=(150,150,160))
    d.line((BX+20,BY-24,BX+BW-20,BY-24),fill=(60,60,70),width=2)
    return o
B=base()
def frame(states):
    # states: list of (rowidx, mode) mode 'final' | ('scr',seed,progress)
    o=B.copy(); d=ImageDraw.Draw(o)
    for r,mode in states:
        y=BY+r*RH; row=ROWS[r]
        vals=[row[0],row[1],row[2]]
        if mode!='final':
            rnd=random.Random(mode[1]); p=mode[2]
            out=[]
            for (x,n),v in zip(COLS,vals):
                v=v.ljust(n); s=''
                for i,c in enumerate(v):
                    settle=(i+1)/len(v)*0.85
                    s+= c if p>=settle or c==' ' else rnd.choice(CH)
                out.append(s)
            vals=out
        for (x,n),v,col in zip(COLS,vals,[WH,YEL,WH]): tiles(d,x,y,v,n,col)
        if mode=='final' or mode[2]>0.9:
            d.text((COLS[1][0],y+TH+8),row[3],font=F(FB,24),fill=(52,199,89) if 'IMEDIATO' in row[3] else LB)
    return o
if __name__=='__main__':
    im=frame([(0,'final'),(1,'final'),(2,('scr',3,0.5))])
    bg=Image.new('RGBA',(W,H),(60,110,150,255)); bg.alpha_composite(im); bg.convert('RGB').resize((540,960)).save('/tmp/board.jpg')
    im=frame([(i,'final') for i in range(7)]); bg=Image.new('RGBA',(W,H),(60,110,150,255)); bg.alpha_composite(im); bg.convert('RGB').resize((540,960)).save('/tmp/board2.jpg')
