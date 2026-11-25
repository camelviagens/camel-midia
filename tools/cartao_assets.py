from PIL import Image,ImageDraw,ImageFont,ImageFilter
W,H=1080,1920; FB='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; FM='/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'; FR='/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf'
F=lambda p,s: ImageFont.truetype(p,s)
WH=(255,255,255); LB=(56,200,250); YEL=(255,214,64); NAVY=(16,42,120); NAVY2=(9,22,66); GRY=(110,120,150)
logo=Image.open('logo_camel.png').convert('RGBA')
def ct(d,y,t,f,fill=WH,x0=0,x1=W):
    w=d.textlength(t,font=f); d.text((x0+(x1-x0-w)/2,y),t,font=f,fill=fill)
def grad(o,y0,y1,a0,a1):
    g=Image.new('RGBA',(W,H)); gd=ImageDraw.Draw(g)
    for y in range(y0,y1): gd.line((0,y,W,y),fill=(5,12,40,int(a0+(a1-a0)*(y-y0)/(y1-y0))))
    o.alpha_composite(g)
# intro overlay
o=Image.new('RGBA',(W,H)); grad(o,0,700,170,0); grad(o,1100,1920,0,200)
o.alpha_composite(logo.resize((200,200),Image.LANCZOS),((W-200)//2,120))
d=ImageDraw.Draw(o)
def stx(y,t,size,fill=WH):
    f=F(FB,size); w=d.textlength(t,font=f)
    sh=Image.new('RGBA',(W,H)); ImageDraw.Draw(sh).text(((W-w)/2,y+6),t,font=f,fill=(0,0,0,170),stroke_width=8,stroke_fill=(0,0,0,170)); o.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(o).text(((W-w)/2,y),t,font=f,fill=fill,stroke_width=8,stroke_fill=NAVY2)
stx(1250,"ATENÇÃO,",118); stx(1385,"PASSAGEIRO!",118)
f=F(FB,44); t="seu próximo embarque já tem destino"; w=d.textlength(t,font=f)
d.rounded_rectangle(((W-w)/2-34,1560,(W+w)/2+34,1640),radius=40,fill=LB); d.text(((W-w)/2,1570),t,font=f,fill=NAVY2)
o.save('i_intro.png')
# boarding pass
def bp(name,code,city,uf,date,tipo,voo,price,unit,tag):
    o=Image.new('RGBA',(W,H)); grad(o,1000,1920,0,190)
    x0,y0,x1,y1=70,1120,1010,1700
    sh=Image.new('RGBA',(W,H)); ImageDraw.Draw(sh).rounded_rectangle((x0,y0+14,x1,y1+14),radius=36,fill=(0,0,0,170)); o.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    d=ImageDraw.Draw(o)
    d.rounded_rectangle((x0,y0,x1,y1),radius=36,fill=WH)
    d.rounded_rectangle((x0,y0,x1,y0+86),radius=36,fill=NAVY); d.rectangle((x0,y0+50,x1,y0+86),fill=NAVY)
    d.text((x0+36,y0+20),"CARTÃO DE EMBARQUE",font=F(FB,36),fill=WH)
    t="CAMEL VIAGENS"; w=d.textlength(t,font=F(FB,30)); d.text((x1-36-w,y0+24),t,font=F(FB,30),fill=LB)
    # stub divider
    sx=x1-300
    for yy in range(y0+100,y1-10,26): d.line((sx,yy,sx,yy+13),fill=(190,200,220),width=4)
    # left: route
    d.text((x0+40,y0+110),"UDI",font=F(FB,108),fill=NAVY2)
    d.text((x0+40,y0+232),"Uberlândia",font=F(FM,28),fill=GRY)
    pw=d.textlength("UDI",font=F(FB,108)); ax=x0+40+pw+26
    ay=y0+180; d.line((ax,ay,ax+62,ay),fill=(20,150,215),width=10); d.polygon([(ax+56,ay-22),(ax+84,ay),(ax+56,ay+22)],fill=(20,150,215))
    cx=ax+108; d.text((cx,y0+110),code,font=F(FB,108),fill=NAVY2); d.text((cx,y0+232),city,font=F(FM,28),fill=GRY)
    # fields
    fy=y0+300
    for i,(k,v) in enumerate([("QUANDO",date),("TIPO",tipo),("VOO",voo)]):
        fx=x0+40+i*190
        d.text((fx,fy),k,font=F(FB,22),fill=(150,160,185)); d.text((fx,fy+28),v,font=F(FB,30),fill=NAVY2)
    # tag
    fw=F(FB,28); tw=d.textlength(tag,font=fw); d.rounded_rectangle((x0+40,y1-92,x0+40+tw+40,y1-38),radius=27,fill=YEL); d.text((x0+60,y1-88),tag,font=fw,fill=NAVY2)
    # stub: price
    ct(d,y0+130,"A PARTIR DE",F(FB,26),GRY,sx,x1)
    ct(d,y0+176,"R$",F(FB,40),(20,150,215),sx,x1)
    fp=F(FB,92 if len(price)<=3 else 74); ct(d,y0+222,price,fp,NAVY2,sx,x1)
    ct(d,y0+350,unit,F(FB,26),GRY,sx,x1)
    lg=logo.resize((110,110),Image.LANCZOS); o.alpha_composite(lg,(int(sx+(x1-sx-110)/2),y1-140))
    # city title top
    stx2=ImageDraw.Draw(o)
    o.save(f'{name}.png')
bp('b_bsb','BSB','Brasília','DF','set/2027','ida e volta','direto','496','por pessoa','PASSAGEM AÉREA')
bp('b_sp','GRU','São Paulo','SP','mar/mai 27','ida e volta','direto','517','por pessoa','PASSAGEM AÉREA')
bp('b_rio','RIO','Rio de Janeiro','RJ','mar/2027','ida e volta','1 parada','595','por pessoa','PASSAGEM AÉREA')
bp('b_ps','BPS','Porto Seguro','BA','out/2027','7 noites','+ hotel','3.280','o casal','PACOTE VOO + HOTEL • CAFÉ')
# end
im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
for y in range(H):
    t=1-abs(y/H-0.45)*2; d.line((0,y,W,y),fill=(int(10+20*t),int(40+60*t),int(130+70*t),255))
im.alpha_composite(logo.resize((440,440),Image.LANCZOS),((W-440)//2,280))
ct(d,790,"Seu embarque",F(FB,74)); ct(d,880,"começa aqui!",F(FB,74))
d.rounded_rectangle((140,1050,940,1170),radius=60,fill=WH); ct(d,1075,"COTAÇÃO GRÁTIS",F(FB,62),NAVY2)
ct(d,1220,"no link da bio",F(FB,60),LB); ct(d,1300,"receba pelo WhatsApp!",F(FB,50),YEL)
ct(d,1420,"@agenciacamelviagens",F(FM,44)); ct(d,1500,"Valores sujeitos a disponibilidade",F(FR,30),(170,200,240))
im.convert('RGB').save('end2.png')
