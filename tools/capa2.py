import json,sys,subprocess
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageEnhance
C=json.load(open(sys.argv[1])); K=C['capa']
W,H=1080,1920; FB='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; FM='/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
NAVY2=(14,34,100); LBLUE=(56,200,250); WHITE=(255,255,255); YEL=(255,222,60)
F=lambda p,s: ImageFont.truetype(p,s)
subprocess.run(['ffmpeg','-v','error','-y','-ss',str(K['t']),'-i',K['clip'],'-frames:v','1','/tmp/capa_bg.png'])
im=ImageEnhance.Brightness(Image.open('/tmp/capa_bg.png').convert('RGB')).enhance(0.9).convert('RGBA')
def st(y,txt,size,stroke,fill=WHITE,blur=12):
    f=F(FB,size); d=ImageDraw.Draw(im)
    while d.textlength(txt,font=f)>1020: size-=4; f=F(FB,size)
    w=d.textlength(txt,font=f); x=(W-w)/2
    sh=Image.new('RGBA',(W,H)); ImageDraw.Draw(sh).text((x,y+8),txt,font=f,fill=(0,0,0,140),stroke_width=stroke,stroke_fill=(0,0,0,140))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur))); ImageDraw.Draw(im).text((x,y),txt,font=f,fill=fill,stroke_width=stroke,stroke_fill=NAVY2)
logo=Image.open('logo_camel.png').convert('RGBA').resize((250,250),Image.LANCZOS); im.alpha_composite(logo,(415,150))
st(470,K['top'],300,14); st(820,K['l1'],120,9); st(950,K['l2'],120,9)
d=ImageDraw.Draw(im); f=F(FB,64); t=K['saindo']; w=d.textlength(t,font=f)
d.rounded_rectangle(((W-w)/2-42,1100,(W+w)/2+42,1205),radius=34,fill=LBLUE); d.text(((W-w)/2,1112),t,font=f,fill=NAVY2)
d.rounded_rectangle((170,1330,910,1610),radius=50,fill=WHITE)
f=F(FB,44); t="A PARTIR DE"; w=d.textlength(t,font=f)
d.rounded_rectangle(((W-w)/2-34,1292,(W+w)/2+34,1368),radius=38,fill=NAVY2,outline=LBLUE,width=4); d.text(((W-w)/2,1300),t,font=f,fill=WHITE)
fp=F(FB,170); fr=F(FB,64); p=K['price']; wp=d.textlength(p,font=fp); wr=d.textlength("R$",font=fr); sx=(W-wp-wr-20)/2
d.text((sx,1480),"R$",font=fr,fill=NAVY2); d.text((sx+wr+20,1370),p,font=fp,fill=NAVY2)
f=F(FM,38); t=K['sub']; w=d.textlength(t,font=f); d.text(((W-w)/2,1550),t,font=f,fill=(60,75,120))
st(1640,K['tag'],48,4,fill=YEL,blur=6)
y=1720
for ln in K['dest']: st(y,ln,44,4,blur=6); y+=58
im.convert('RGB').save('/mnt/user-data/outputs/'+K['out'],quality=92)
