import json,sys,os,subprocess,glob
from ovlib import *
from sent import sentences
C=json.load(open(sys.argv[1])); NAME=C['name']; B=f'/home/claude/top5/v_{NAME}'; os.makedirs(B+'/ov',exist_ok=True); os.makedirs(B+'/clips',exist_ok=True)
run=lambda a: subprocess.run(a,stdin=subprocess.DEVNULL,check=True)
V="/mnt/user-data/uploads/Projeto Top8/videos"
def card_aereo(im, datas, linha, preco):
    x0,y0,x1,y1=150,1170,930,1530
    def dr(d,shadow):
        d.rounded_rectangle((x0,y0,x1,y1),radius=46,fill=(0,0,0,255) if shadow else (255,255,255,248))
        if shadow: return
        fc=F(FB,34); w=d.textlength(datas,font=fc)+70; cx0=(W-w)/2
        d.rounded_rectangle((cx0,y0-32,cx0+w,y0+32),radius=32,fill=NAVY,outline=LBLUE,width=3); d.text((cx0+35,y0-25),datas,font=fc,fill=WHITE)
        ctext(d,y0+52,linha,F(FM,32),fill=(60,75,120))
        fr=F(FB,58); fp=F(FB,150); wr=d.textlength("R$",font=fr); wp=d.textlength(preco,font=fp); sx=(W-wr-18-wp)/2
        d.text((sx,y0+160),"R$",font=fr,fill=NAVY); d.text((sx+wr+18,y0+80),preco,font=fp,fill=NAVY)
        ctext(d,y0+262,"por pessoa",F(FB,42),fill=NAVY); ctext(d,y0+315,"somente passagem aérea",F(FB,30),fill=(20,150,215))
    shadowed(im,dr)
def card_vh(im, datas, preco, pp, hotel, orig):
    x0,y0,x1,y1=140,1150,940,1590
    def dr(d,shadow):
        d.rounded_rectangle((x0,y0,x1,y1),radius=46,fill=(0,0,0,255) if shadow else (255,255,255,248))
        if shadow: return
        fc=F(FB,34); w=d.textlength(datas,font=fc)+70; cx0=(W-w)/2
        d.rounded_rectangle((cx0,y0-32,cx0+w,y0+32),radius=32,fill=NAVY,outline=LBLUE,width=3); d.text((cx0+35,y0-25),datas,font=fc,fill=WHITE)
        ctext(d,y0+50,f"7 noites  •  voo + hotel  •  saindo de {orig}",F(FM,32),fill=(60,75,120))
        fr=F(FB,58); fp=F(FB,150); wr=d.textlength("R$",font=fr); wp=d.textlength(preco,font=fp); sx=(W-wr-18-wp)/2
        d.text((sx,y0+160),"R$",font=fr,fill=NAVY); d.text((sx+wr+18,y0+78),preco,font=fp,fill=NAVY)
        ctext(d,y0+262,"pacote para 2 adultos",F(FB,44),fill=NAVY); ctext(d,y0+318,f"só R$ {pp} por pessoa",F(FB,34),fill=(20,150,215))
        ctext(d,y0+372,hotel+"  •  café da manhã",F(FM,28),fill=(90,100,130))
    shadowed(im,dr)
O=B+'/ov'
# overlays
im=new(); add_logo(im,230,170); bigtext(im,[C['top']],560,260,stroke=12); bigtext(im,C['title'],880,120 if len(C['title'][-1])<=12 else 104,gap=0,stroke=8)
tarja(im,1180,C['saindo'],56); tarja(im,1300,C['intro_tag'],40,bg=WHITE,fg=NAVY); im.save(f'{O}/ov_intro.png')
im=new(); add_logo(im); bigtext(im,["A Nº 1 TÁ","IMPERDÍVEL"],700,130,stroke=10); tarja(im,1010,C['saindo'],48); im.save(f'{O}/ov_hook.png')
for it in C['items']:
    im=new(); add_logo(im); badge(im,it['rank'],it['city'],it['sub'])
    if C['kind']=='aereo': card_aereo(im,it['dates'],it['line'],it['price'])
    else: card_vh(im,it['dates'],it['price'],it['pp'],it['hotel'],C['orig'])
    im.save(f"{O}/ov_{it['rank']}.png")
    if it['rank']==1:
        tarja(im,1600 if C['kind']=='aereo' else 1660,C['tag1'],40,bg=NAVY,fg=WHITE); im.save(f'{O}/ov_1b.png')
im=new(); add_logo(im); bigtext(im,["E A Nº 1..."],820,140,stroke=10); im.save(f'{O}/ov_susp.png')
run(['python3','endcard.py',O,C['valor']])
# clips
def files(c): return sorted(glob.glob(f"{V}/{c}/*.mp4"))
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
def cut(name,v):
    c,i,fr,z,Y=v[:5]; pre=(v[5]+",") if len(v)>5 else ""
    f=files(c)[i]; ss=max(0,dur(f)*fr)
    vf=pre+"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30"
    if z>1:
        w=int(1080*z)//2*2; h=int(1920*z)//2*2; y=0 if Y=='top' else (h-1920 if Y=='bot' else (h-1920)//2)
        vf+=f",scale={w}:{h},crop=1080:1920:{(w-1080)//2}:{y}"
    out=f'{B}/clips/{name}.mp4'
    if not os.path.exists(out) or '--recut' in sys.argv:
        run(['ffmpeg','-v','error','-y','-ss',f'{ss:.2f}','-i',f,'-t','3.6','-an','-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out])
    return out
P=C['picks']
for seg,lst in P.items():
    for k,v in enumerate(lst): cut(f'{seg}{k}',v)
if '--cutonly' in sys.argv: sys.exit()
# timing
S=sentences(C['narr']); N=len(C['items'])
exp=2+2*(N-1)+3+(1 if C['kind']=='vh' else 0)+2+5
assert len(S)==exp,(len(S),exp)
st=lambda i: max(0,S[i][0]-0.2)
T={'hook':st(1)}
for k in range(N-1): T[f'd{N-k}']=st(2+2*k)
iS=2+2*(N-1); T['susp']=st(iS); T['s1']=st(iS+1)
tagi=iS+3 if C['kind']=='aereo' else iS+4
T['tag']=st(tagi); q=len(S)-5
T['tut']=st(q)
order=[('intro','ov_intro',0,T['hook']),('hook','ov_hook',T['hook'],T[f'd{N}'])]
for r in range(N,1,-1):
    nxt=T[f'd{r-1}'] if r>2 else T['susp']
    order.append((f'd{r}',f'ov_{r}',T[f'd{r}'],nxt))
order+= [('susp','ov_susp',T['susp'],T['s1']),('d1','ov_1',T['s1'],T['tut'])]
parts=[];ov=[];t=0.0
for seg,o,a,b in order:
    clips=[f'{B}/clips/{seg}{k}.mp4' for k in range(len(P[seg]))]
    each=(b-a)/len(clips); assert each<=3.55,(seg,each)
    t0=t
    for k,c in enumerate(clips):
        n=round((a+each*(k+1))*30)-round((a+each*k)*30); out=f'{B}/seg_{seg}_{k}.mp4'
        run(['ffmpeg','-v','error','-y','-i',c,'-frames:v',str(n),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out]); parts.append(out); t+=n/30
    if seg=='d1': ov+=[(o,t0,T['tag']),('ov_1b',T['tag'],t)]
    else: ov.append((o,t0,t))
open(f'{B}/list.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{B}/list.txt','-c','copy',f'{B}/body.mp4'])
inputs=['-i',f'{B}/body.mp4']; fc=''; last='[0:v]'
for k,(o,a,b) in enumerate(ov):
    inputs+=['-i',f'{O}/{o}.png']; nl=f'[v{k}]'; fc+=f"{last}[{k+1}:v]overlay=0:0:enable='between(t,{a:.3f},{b-0.001:.3f})'{nl};"; last=nl
run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',fc.rstrip(';'),'-map',last,'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',f'{B}/body_ov.mp4'])
# tutorial
q=len(S)-5; quer,facil,toca,esc,pre=[S[q+i] for i in range(5)]
endt=pre[1]+0.3
TUT=[('tut1_0',toca[0]-0.2),('tut1_1',esc[0]-0.2),('tut2_0',(esc[0]+esc[1])/2),('tut2_1',pre[0]-0.2),('tut3_1',pre[0]+(pre[1]-pre[0])*0.45),('tut3_2',endt)]
prev=t; names=[]
for k,(img,until) in enumerate(TUT):
    n=round(until*30)-round(prev*30); prev=until; out=f'{B}/tut{k}.mp4'; names.append(out)
    run(['ffmpeg','-v','error','-y','-loop','1','-i',f'/home/claude/top5/build/{img}.png','-frames:v',str(n),'-vf','fps=30,format=yuv420p'+(',fade=in:st=0:d=0.3' if k==0 else ''),'-c:v','libx264','-preset','veryfast','-crf','18',out])
END=4.5
run(['ffmpeg','-v','error','-y','-loop','1','-t',str(END),'-i',f'{O}/end.png','-vf','fps=30,format=yuv420p,fade=in:st=0:d=0.4','-c:v','libx264','-preset','veryfast','-crf','18',f'{B}/endc.mp4'])
open(f'{B}/list2.txt','w').write(f"file '{B}/body_ov.mp4'\n"+''.join(f"file '{x}'\n" for x in names)+f"file '{B}/endc.mp4'\n")
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{B}/list2.txt','-c','copy',f'{B}/vid.mp4'])
total=round(endt*30)/30+END
outp=f"/mnt/user-data/outputs/{C['out']}"
run(['ffmpeg','-v','error','-y','-i',f'{B}/vid.mp4','-i',C['narr'],'-filter_complex',f'[1:a]apad,atrim=0:{total:.2f},afade=out:st={total-1.5:.2f}:d=1.5[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',outp])
run(['ffmpeg','-v','error','-y','-i',outp,'-vf','fps=1/3,scale=180:320,tile=10x3','-frames:v','1',f'{B}/check.jpg'])
print('OK',outp,total,json.dumps(T))
