import subprocess,glob,sys,os
sys.path.insert(0,'/home/claude/top5'); from sent import sentences
run=lambda a: subprocess.run(a,stdin=subprocess.DEVNULL,check=True)
V="/mnt/user-data/uploads/Projeto Top8/videos"
def pg(i): return sorted(glob.glob(f"{V}/porto_de_galinhas/*.mp4"))[i]
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
narr=sys.argv[1]; S=sentences(narr); print(len(S)); assert len(S)==15,len(S)
st=lambda i: max(0,S[i][0]-0.15)
T=dict(t1=st(2),t2=st(4),t3=st(5),t4=st(7),t5=st(8),off=st(9),tut=st(10))
R='ref.mp4'
segs=[('intro',[(R,0.5)],0,T['t1'],'i_intro'),
('t1',[(R,38),(pg(3),0.45*dur(pg(3)))],T['t1'],T['t2'],'t1'),
('t2',[(pg(1),0.15*dur(pg(1))),(pg(1),0.85*dur(pg(1)))],T['t2'],T['t3'],'t2'),
('t3',[(pg(0),0.45*dur(pg(0))),(R,30)],T['t3'],T['t4'],'t3'),
('t4',[(R,12),(pg(4),0.15*dur(pg(4)))],T['t4'],T['t5'],'t4'),
('t5',[(R,20),(R,4)],T['t5'],T['off'],'t5'),
('off',[(pg(1),0.5*dur(pg(1))),(R,44)],T['off'],T['tut'],'offer')]
os.makedirs('w',exist_ok=True); parts=[]
for name,clips,a,b,_ in segs:
    each=(b-a)/len(clips)
    for k,(f,ss) in enumerate(clips):
        n=round((a+each*(k+1))*30)-round((a+each*k)*30); out=f'w/{name}{k}.mp4'
        run(['ffmpeg','-v','error','-y','-ss',f'{ss:.2f}','-i',f,'-frames:v',str(n),'-an','-vf','scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out]); parts.append(out)
open('w/list.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','w/list.txt','-c','copy','w/clips.mp4'])
inp=['-i','w/clips.mp4']; fc=''; last='[0:v]'
for k,(name,_,a,b,ov) in enumerate(segs):
    inp+=['-i',f'{ov}.png']; d0=0.15 if name!='intro' else 0
    fc+=f"{last}[{k+1}:v]overlay=0:0:enable='between(t,{a+d0:.3f},{b-0.02:.3f})'[v{k}];"; last=f'[v{k}]'
run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',fc.rstrip(';'),'-map',last,'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','w/body.mp4'])
q=10; quer,facil,toca,esc,pre=[S[q+i] for i in range(5)]; endt=pre[1]+0.3
TUT=[('tut1_0',toca[0]-0.2),('tut1_1',esc[0]-0.2),('tut2_0',(esc[0]+esc[1])/2),('tut2_1',pre[0]-0.2),('tut3_1',pre[0]+(pre[1]-pre[0])*0.45),('tut3_2',endt)]
prev=T['tut']; names=[]
for k,(img,until) in enumerate(TUT):
    n=round(until*30)-round(prev*30); prev=until; o=f'w/tut{k}.mp4'; names.append(o)
    run(['ffmpeg','-v','error','-y','-loop','1','-i',f'/home/claude/top5/build/{img}.png','-frames:v',str(n),'-vf','fps=30,format=yuv420p'+(',fade=in:st=0:d=0.3' if k==0 else ''),'-c:v','libx264','-preset','veryfast','-crf','18',o])
END=4.5
run(['ffmpeg','-v','error','-y','-loop','1','-t',str(END),'-i','/home/claude/janela/end2.png','-vf','fps=30,format=yuv420p,fade=in:st=0:d=0.4','-c:v','libx264','-preset','veryfast','-crf','18','w/endc.mp4'])
open('w/l2.txt','w').write(f"file '{os.path.abspath('w/body.mp4')}'\n"+''.join(f"file '{os.path.abspath(x)}'\n" for x in names)+f"file '{os.path.abspath('w/endc.mp4')}'\n")
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','w/l2.txt','-c','copy','w/vid.mp4'])
tot=round(endt*30)/30+END; out='/mnt/user-data/outputs/CamelViagens_Dicas_PortoDeGalinhas.mp4'
run(['ffmpeg','-v','error','-y','-i','w/vid.mp4','-i',narr,'-filter_complex',f'[1:a]apad,atrim=0:{tot:.2f},afade=out:st={tot-1:.2f}:d=1[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',out])
run(['ffmpeg','-v','error','-y','-i',out,'-vf','fps=1/2.5,scale=180:320,tile=10x3','-frames:v','1','w/check.jpg'])
print('OK',out,tot,T)
