import subprocess,glob,sys,os
sys.path.insert(0,'/home/claude/top5'); from sent import sentences
from board import frame,W,H
run=lambda a: subprocess.run(a,stdin=subprocess.DEVNULL,check=True)
V="/mnt/user-data/uploads/Projeto Top8/videos"
def fl(c,i): return sorted(glob.glob(f"{V}/{c}/*.mp4"))[i]
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
narr=sys.argv[1] if len(sys.argv)>1 else None
if narr:
    S=sentences(narr); print(len(S)); assert len(S)==15,len(S)
    st=lambda i: max(0,S[i][0]-0.15); R=[st(i) for i in range(2,9)]; TUT=st(10)
else:
    R=[4,7.5,10.5,13,15.5,18.5,22.5]; TUT=27; S=None
bgs=[('rio_de_janeiro',5,0.1),('brasilia',0,0.3),('sao_paulo',0,0.2),('rio_de_janeiro',0,0.15),('curitiba',2,0.15),('florianopolis',0,0.15),('porto_seguro',2,0.15),('porto_de_galinhas',1,0.15)]
bounds=[0]+R+[TUT]
os.makedirs('w',exist_ok=True); parts=[]
for k,(c,i,fr) in enumerate(bgs):
    a,b=bounds[k],bounds[k+1]; n=round(b*30)-round(a*30); f=fl(c,i); out=f'w/bg{k}.mp4'
    ss=dur(f)*fr; L=n/30
    # loop if clip shorter
    run(['ffmpeg','-v','error','-y','-stream_loop','3','-ss',f'{ss:.2f}','-i',f,'-frames:v',str(n),'-an','-vf','scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,eq=brightness=-0.06:saturation=1.1','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out]); parts.append(out)
open('w/list.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','w/list.txt','-c','copy','w/bg.mp4'])
NF=round(TUT*30); SCR=0.75
p=subprocess.Popen(['ffmpeg','-v','error','-y','-i','w/bg.mp4','-f','rawvideo','-pix_fmt','rgba','-s','1080x1920','-r','30','-i','-','-filter_complex','[0:v][1:v]overlay=0:0:shortest=1','-frames:v',str(NF),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','w/body.mp4'],stdin=subprocess.PIPE)
cache={}
for fi in range(NF):
    t=fi/30; states=[]; key=[]
    for r,rt in enumerate(R):
        if t<rt: break
        pr=(t-rt)/SCR
        if pr>=1: states.append((r,'final')); key.append((r,'f'))
        else:
            q=int(pr*SCR*15)/ (SCR*15)  # change every 2 frames
            states.append((r,('scr',r*100+int(pr*SCR*15),q))); key.append((r,int(pr*SCR*15)))
    k=tuple(key)
    if k not in cache:
        if len(cache)>40: cache.clear()
        cache[k]=frame(states).tobytes()
    p.stdin.write(cache[k])
p.stdin.close(); p.wait()
if not narr: sys.exit(print('preview ok'))
q=10; quer,facil,toca,esc,pre=[S[q+i] for i in range(5)]; endt=pre[1]+0.3
TT=[('tut1_0',toca[0]-0.2),('tut1_1',esc[0]-0.2),('tut2_0',(esc[0]+esc[1])/2),('tut2_1',pre[0]-0.2),('tut3_1',pre[0]+(pre[1]-pre[0])*0.45),('tut3_2',endt)]
prev=NF/30; names=[]
for k,(img,until) in enumerate(TT):
    n=round(until*30)-round(prev*30); prev=until; o=f'w/tut{k}.mp4'; names.append(o)
    run(['ffmpeg','-v','error','-y','-loop','1','-i',f'/home/claude/top5/build/{img}.png','-frames:v',str(n),'-vf','fps=30,format=yuv420p'+(',fade=in:st=0:d=0.3' if k==0 else ''),'-c:v','libx264','-preset','veryfast','-crf','18',o])
END=4.5
run(['ffmpeg','-v','error','-y','-loop','1','-t',str(END),'-i','/home/claude/janela/end2.png','-vf','fps=30,format=yuv420p,fade=in:st=0:d=0.4','-c:v','libx264','-preset','veryfast','-crf','18','w/endc.mp4'])
open('w/l2.txt','w').write(f"file '{os.path.abspath('w/body.mp4')}'\n"+''.join(f"file '{os.path.abspath(x)}'\n" for x in names)+f"file '{os.path.abspath('w/endc.mp4')}'\n")
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','w/l2.txt','-c','copy','w/vid.mp4'])
tot=round(endt*30)/30+END; out='/mnt/user-data/outputs/CamelViagens_PainelPartidas.mp4'
run(['ffmpeg','-v','error','-y','-i','w/vid.mp4','-i',narr,'-filter_complex',f'[1:a]apad,atrim=0:{tot:.2f},afade=out:st={tot-1:.2f}:d=1[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',out])
run(['ffmpeg','-v','error','-y','-i',out,'-vf','fps=1/2,scale=180:320,tile=10x3','-frames:v','1','w/check.jpg'])
print('OK',out,tot,R,TUT)
