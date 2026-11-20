# Subset Fontsource slices to the characters this page uses, merge per weight, emit fonts.css
import re, os, sys, io, html as H
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.merge import Merger
SRC=sys.argv[1]; OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True)
txt=open(SRC,encoding='utf-8').read()
txt=H.unescape(re.sub(r'<[^>]+>',' ',txt))+H.unescape(txt)
used=set(ord(c) for c in txt if ord(c)>=32)|set(range(32,127))|{0x2019,0x201c,0x201d,0x2014,0x2013,0x2026,0x00b7,0x2032,0x00b0,0x2191,0x2197}
P='build/fontsource/'
specs=[("Noto Serif SC","noto-serif-sc-5.3.1",["300","400","600"],"normal"),
       ("Cormorant Garamond","cormorant-garamond-5.3.0",["300","400"],"normal"),
       ("Cormorant Garamond","cormorant-garamond-5.3.0",["300","400"],"italic"),
       ("IBM Plex Mono","ibm-plex-mono-5.3.0",["400"],"normal")]
def rng(s):
    out=set()
    for part in s.split(','):
        part=part.strip().replace('U+','').replace('u+','')
        if '-' in part: a,b=part.split('-'); out|=set(range(int(a,16),int(b,16)+1))
        elif '?' in part: out|=set(range(int(part.replace('?','0'),16),int(part.replace('?','f'),16)+1))
        else: out.add(int(part,16))
    return out
css=[]; total=0
for fam,pkg,weights,style in specs:
    for w in weights:
        cssf=f"{P}{pkg}/package/{w}{'-italic' if style=='italic' else ''}.css"
        blocks=re.findall(r'@font-face\s*\{(.*?)\}',open(cssf).read(),re.S)
        parts=[]; covered=set()
        for b in blocks:
            src=re.search(r"url\(\./files/([^)]+\.woff2)\)",b).group(1)
            ur=re.search(r'unicode-range:\s*([^;]+);',b); r=rng(ur.group(1)) if ur else set(range(0,0x110000))
            need=(r&(used if not (pkg.startswith('noto') and w=='600') else {ord('浮')}))-covered
            if not need: continue
            f=TTFont(P+pkg+'/package/files/'+src)
            cmap=set(f.getBestCmap().keys()); need&=cmap
            if not need: continue
            opt=subset.Options(); opt.layout_features=['*']; opt.notdef_outline=True; opt.name_IDs=['*']; opt.hinting=False
            ss=subset.Subsetter(opt); ss.populate(unicodes=need); ss.subset(f)
            f.flavor=None; tmp=f"build/fontsource/part_{len(parts)}.ttf"; f.save(tmp); parts.append(tmp); covered|=need
        name=f"{pkg.rsplit('-',1)[0]}-{w}{'-italic' if style=='italic' else ''}"
        try:
            mg=Merger(); font=mg.merge(parts) if len(parts)>1 else TTFont(parts[0])
        except Exception as e:
            print('merge failed',name,e); raise
        font.flavor='woff2'; out=f"{OUT}/{name}.woff2"; font.save(out); sz=os.path.getsize(out); total+=sz
        print(name,len(parts),'slices',len(covered),'chars',sz//1024,'KB')
        css.append(f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{w};font-display:swap;src:url(./{name}.woff2) format('woff2')}}")
        for p in parts: os.remove(p)
open(OUT+'/fonts.css','w').write("\n".join(css)+"\n"); print('total',total//1024,'KB')
