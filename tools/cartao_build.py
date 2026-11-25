import subprocess,glob,sys,os
sys.path.insert(0,'/home/claude/top5'); from sent import sentences
run=lambda a: subprocess.run(a,stdin=subprocess.DEVNULL,check=True)
V="/mnt/user-data/uploads/Projeto Top8/videos"
def files(c): return sorted(glob.glob(f"{V}/{c}/*.mp4"))
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
narr=sys.argv[1] if len(sys.argv)>1 else None
if narr:
    S=sentences(narr); print(len(S),[f'{a:.2f}' for a,b in S]); assert len(S)==12,len(S)
    st=lambda i: max(0,S[i][0]-0.15)
    T=dict(bsb=st(2),sp=st(3),rio=st(4),ps=st(5),end=st(7))
else: sys.exit('precisa da narracao')
segs=[('intro',[('rio_de_janeiro',5,0.1,'')],0,T['bsb'],'i_intro'),
('bsb',[('brasilia',0,0.3,''),('brasilia',4,0.2,'')],T['bsb'],T['sp'],'b_bsb'),
('sp',[('sao_paulo',0,0.2,''),('sao_paulo',3,0.3,'')],T['sp'],T['rio'],'b_sp'),
('rio',[('rio_de_janeiro',0,0.15,''),('rio_de_janeiro',2,0.6,'')],T['rio'],T['ps'],'b_rio'),
('ps',[('porto_seguro',2,0.15,''),('porto_seguro',3,0.5,'transpose=2,')],T['ps'],T['end'],'b_ps')]
os.makedirs('w2',exist_ok=True); parts=[]
for name,clips,a,b,_ in segs:
    each=(b-a)/len(clips)
    for k,(c,i,fr,pre) in enumerate(clips):
        n=round((a+each*(k+1))*30)-round((a+each*k)*30); f=files(c)[i]; out=f'w2/{name}{k}.mp4'
        run(['ffmpeg','-v','error','-y','-ss',f'{dur(f)*fr:.2f}','-i',f,'-frames:v',str(n),'-an','-vf',pre+'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out]); parts.append(out)
open('w2/list.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','w2/list.txt','-c','copy','w2/clips.mp4'])
inp=['-i','w2/clips.mp4']; fc=''; last='[0:v]'
for k,(name,_,a,b,ov) in enumerate(segs):
    inp+=['-i',f'{ov}.png']; d0=0.2 if name!='intro' else 0
    fc+=f"{last}[{k+1}:v]overlay=0:0:enable='between(t,{a+d0:.3f},{b-0.02:.3f})'[v{k}];"; last=f'[v{k}]'
run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',fc.rstrip(';'),'-map',last,'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','w2/body.mp4'])
q=7; quer,facil,toca,esc,pre=[S[q+i] for i in range(5)]; endt=pre[1]+0.3
TUT=[('tut1_0',toca[0]-0.2),('tut1_1',esc[0]-0.2),('tut2_0',(esc[0]+esc[1])/2),('tut2_1',pre[0]-0.2),('tut3_1',pre[0]+(pre[1]-pre[0])*0.45),('tut3_2',endt)]
prev=T['end']; names=[]
for k,(img,until) in enumerate(TUT):
    n=round(until*30)-round(prev*30); prev=until; o=f'w2/tut{k}.mp4'; names.append(o)
    run(['ffmpeg','-v','error','-y','-loop','1','-i',f'/home/claude/top5/build/{img}.png','-frames:v',str(n),'-vf','fps=30,format=yuv420p'+(',fade=in:st=0:d=0.3' if k==0 else ''),'-c:v','libx264','-preset','veryfast','-crf','18',o])
END=4.5; T['fim']=round(endt*30)/30+END
run(['ffmpeg','-v','error','-y','-loop','1','-t',str(END),'-i','end2.png','-vf','fps=30,format=yuv420p,fade=in:st=0:d=0.4','-c:v','libx264','-preset','veryfast','-crf','18','w2/endc.mp4'])
open('w2/l2.txt','w').write(f"file '{os.path.abspath('w2/body.mp4')}'\n"+''.join(f"file '{os.path.abspath(x)}'\n" for x in names)+f"file '{os.path.abspath('w2/endc.mp4')}'\n")
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','w2/l2.txt','-c','copy','w2/vid.mp4'])
out='w2/vid.mp4'
if narr:
    out='/mnt/user-data/outputs/CamelViagens_CartaoEmbarque_Ofertas.mp4'; tot=T['fim']
    run(['ffmpeg','-v','error','-y','-i','w2/vid.mp4','-i',narr,'-filter_complex',f'[1:a]apad,atrim=0:{tot:.2f},afade=out:st={tot-1:.2f}:d=1[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',out])
run(['ffmpeg','-v','error','-y','-i',out,'-vf','fps=1/1.5,scale=180:320,tile=9x2','-frames:v','1','w2/check.jpg'])
print('OK',out,T)
