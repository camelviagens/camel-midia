from ovlib import *
import sys
O=sys.argv[1]
VALOR=sys.argv[2]

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
    if not shadow: ctext(d,1365,"COTAÇÃO GRÁTIS",F(FB,64),fill=NAVY)
shadowed(im,dr2)
d=ImageDraw.Draw(im)
ctext(d,1500,"no link da bio",F(FB,64),fill=LBLUE)
ctext(d,1580,"✓ receba no mesmo dia" if False else "receba pelo WhatsApp!",F(FB,50),fill=(255,222,60))
ctext(d,1665,"@agenciacamelviagens",F(FM,46),fill=WHITE)
ctext(d,1735,VALOR,F(FM,32),fill=(170,200,240))
im.convert('RGB').save(f'{O}/end.png')
print('ok')
