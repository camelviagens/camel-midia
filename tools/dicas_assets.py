from PIL import Image,ImageDraw,ImageFont,ImageFilter
W,H=1080,1920; FB='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; FM='/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'; FR='/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf'
F=lambda p,s: ImageFont.truetype(p,s)
WH=(255,255,255); LB=(56,200,250); YEL=(255,214,64); NAVY=(16,42,120); NAVY2=(9,22,66); GRY=(95,105,135)
logo=Image.open('logo_camel.png').convert('RGBA')
def grad(o,y0,y1,a0,a1):
    g=Image.new('RGBA',(W,H)); gd=ImageDraw.Draw(g)
    for y in range(y0,y1): gd.line((0,y,W,y),fill=(5,12,40,int(a0+(a1-a0)*(y-y0)/(y1-y0))))
    o.alpha_composite(g)
def stx(o,y,t,size,fill=WH,stroke=8):
    d=ImageDraw.Draw(o); f=F(FB,size)
    while d.textlength(t,font=f)>1000: size-=4; f=F(FB,size)
    w=d.textlength(t,font=f)
    sh=Image.new('RGBA',(W,H)); ImageDraw.Draw(sh).text(((W-w)/2,y+6),t,font=f,fill=(0,0,0,170),stroke_width=stroke,stroke_fill=(0,0,0,170)); o.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(o).text(((W-w)/2,y),t,font=f,fill=fill,stroke_width=stroke,stroke_fill=NAVY2)
def header(o):
    grad(o,0,420,170,0)
    o.alpha_composite(logo.resize((120,120),Image.LANCZOS),(60,70))
    d=ImageDraw.Draw(o); d.text((200,82),"PORTO DE GALINHAS",font=F(FB,46),fill=WH); d.text((202,140),"Pernambuco  •  5 dicas da Camel",font=F(FM,30),fill=LB)
o=Image.new('RGBA',(W,H)); grad(o,0,700,170,0); grad(o,1050,1920,0,210)
o.alpha_composite(logo.resize((200,200),Image.LANCZOS),((W-200)//2,120))
stx(o,1120,"5 DICAS",170); stx(o,1320,"antes de ir para",62,LB,6); stx(o,1410,"PORTO DE GALINHAS",96)
o.save('i_intro.png')
def wrap(d,t,f,maxw):
    ws=t.split(); ls=['']
    for w in ws:
        s=(ls[-1]+' '+w).strip()
        if d.textlength(s,font=f)>maxw: ls.append(w)
        else: ls[-1]=s
    return ls
tips=[("As piscinas naturais aparecem na maré baixa","Confira a tábua de marés antes de marcar o passeio"),
("Passeio de jangada até as piscinas","Elas ficam pertinho da areia"),
("Leve máscara de mergulho","Dá pra ver os peixinhos coloridos de pertinho"),
("Conheça Muro Alto e Maracaípe","Mar calminho em Muro Alto; surf e cavalos-marinhos em Maracaípe"),
("Melhor época: setembro a março","É quando chove menos na região")]
for i,(t,s) in enumerate(tips,1):
    o=Image.new('RGBA',(W,H)); header(o); grad(o,1100,1920,0,200)
    x0,y0,x1=70,1290,1010
    d=ImageDraw.Draw(o); ft=F(FB,50); fs=F(FM,34)
    lt=wrap(d,t,ft,x1-x0-200); ls=wrap(d,s,fs,x1-x0-200)
    y1=y0+60+len(lt)*64+len(ls)*46+40
    sh=Image.new('RGBA',(W,H)); ImageDraw.Draw(sh).rounded_rectangle((x0,y0,x1,y1),radius=40,fill=(0,0,0,170)); o.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    d=ImageDraw.Draw(o); d.rounded_rectangle((x0,y0,x1,y1),radius=40,fill=(255,255,255,246))
    d.ellipse((x0+36,y0+40,x0+156,y0+160),fill=LB); f=F(FB,80); w=d.textlength(str(i),font=f); d.text((x0+96-w/2,y0+42),str(i),font=f,fill=NAVY2)
    y=y0+40
    for ln in lt: d.text((x0+186,y),ln,font=ft,fill=NAVY2); y+=64
    y+=8
    for ln in ls: d.text((x0+186,y),ln,font=fs,fill=GRY); y+=46
    o.save(f't{i}.png')
# offer
o=Image.new('RGBA',(W,H)); header(o); grad(o,1000,1920,0,200)
x0,y0,x1,y1=110,1150,970,1660
sh=Image.new('RGBA',(W,H)); ImageDraw.Draw(sh).rounded_rectangle((x0,y0,x1,y1),radius=44,fill=(0,0,0,170)); o.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
d=ImageDraw.Draw(o); d.rounded_rectangle((x0,y0,x1,y1),radius=44,fill=WH)
def ct(y,t,f,fill):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill)
fw=F(FB,32); t="PACOTE VOO + HOTEL"; tw=d.textlength(t,font=fw); d.rounded_rectangle(((W-tw)/2-30,y0-30,(W+tw)/2+30,y0+30),radius=30,fill=YEL); d.text(((W-tw)/2,y0-24),t,font=fw,fill=NAVY2)
ct(y0+50,"saindo de Uberlândia  •  10/04 a 17/04/2027",F(FM,30),GRY)
ct(y0+96,"7 noites  •  Pousada Suná  •  café da manhã",F(FM,30),GRY)
fr=F(FB,60); fp=F(FB,150); wr=d.textlength("R$",font=fr); wp=d.textlength("4.110",font=fp); sx=(W-wr-16-wp)/2
d.text((sx,y0+250),"R$",font=fr,fill=NAVY); d.text((sx+wr+16,y0+150),"4.110",font=fp,fill=NAVY)
ct(y0+345,"para o casal",F(FB,44),NAVY); ct(y0+410,"só R$ 2.055 por pessoa",F(FB,36),(20,150,215))
o.save('offer.png')
