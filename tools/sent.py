import subprocess,re,sys
def sentences(f,thr=0.7):
    out=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','silencedetect=noise=-35dB:d=0.25','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    sil=list(zip(st,en+[dur]))
    segs=[];cur=0.0
    for a,b in sil:
        if b-a>=thr:
            if a>cur+0.05: segs.append((cur,a))
            cur=b
    if cur<dur-0.1: segs.append((cur,dur))
    return segs
if __name__=='__main__':
    for f in sys.argv[1:]:
        s=sentences(f); print(f,len(s)); print(' '.join(f'{a:.2f}-{b:.2f}' for a,b in s))
