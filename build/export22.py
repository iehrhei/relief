import numpy as np, json, io
from PIL import Image
from skimage import measure
S=np.load('build/data/S.npy'); LAT=np.load('build/data/SLAT.npy'); LON=np.load('build/data/SLON.npy'); rows=np.load('build/data/rows2.npy')
NR,NC=S.shape
np.clip(np.round(S),-32768,32767).astype('<i2').tofile('./relief.bin')
# coastlines
cs=measure.find_contours(S,0.0)
lines=[]
for c in cs:
    if len(c)<4: continue
    c=measure.approximate_polygon(c,0.35)
    if len(c)<2: continue
    if len(c)<6 and np.ptp(c[:,0])<2 and np.ptp(c[:,1])<2: continue
    lines.append([int(round(x*4)) for p in c for x in (p[1],p[0])])  # x=col*4, y=row*4
# axis column = center
feat=[
 ("格陵兰","Greenland",78.0,-22.0,1),("斯瓦尔巴","Svalbard",78.6,15.5,1),("扬马延岛","Jan Mayen",71.0,-8.4,1),("冰岛","Iceland",64.9,-18.6,1),
 ("亚速尔群岛","Azores",38.47,-28.4,1),("圣彼得和圣保罗岩","St Peter and St Paul Rocks",0.92,-29.35,1),("阿森松岛","Ascension Island",-7.93,-14.37,1),
 ("特里斯坦-达库尼亚","Tristan da Cunha",-37.11,-12.28,1),("戈夫岛","Gough Island",-40.32,-9.94,1),("布韦岛","Bouvet Island",-54.42,3.36,1),
 ("莫洛伊深渊","Molloy Deep",79.14,2.8,0),("克尼波维奇海岭","Knipovich Ridge",76.6,7.8,0),("莫恩斯海岭","Mohns Ridge",72.6,1.0,0),("科尔拜因塞海岭","Kolbeinsey Ridge",69.0,-16.5,0),
 ("雷克雅内斯海岭","Reykjanes Ridge",59.5,-30.0,0),("查理-吉布斯断裂带","Charlie-Gibbs Fracture Zone",52.6,-33.0,0),("失落之城","Lost City",30.125,-42.118,0),
 ("凯恩断裂带","Kane Fracture Zone",23.7,-45.5,0),("维马断裂带","Vema Fracture Zone",10.75,-42.5,0),("罗曼什断裂带","Romanche Fracture Zone",-0.25,-18.6,0),
 ("阿森松断裂带","Ascension Fracture Zone",-7.0,-12.5,0),("布韦三联点","Bouvet Triple Junction",-54.85,-1.0,0)]
labels=[]
for zh,en,la,lo,land in feat:
    dlat=LAT-la; dlon=(LON-lo)*np.cos(np.radians(la)); d=dlat**2+dlon**2
    r,c=np.unravel_index(np.argmin(d),d.shape); dist=np.sqrt(d[r,c])*111
    ok=dist<15 and 1<c<NC-2
    print(zh,round(dist,1),r,c,int(S[r,c]),'OK' if ok else 'OUT')
    if ok:
        ns='N' if la>=0 else 'S'; latstr=f"{abs(int(la))}°{int(round((abs(la)%1)*60)):02d}′{ns}"
        labels.append({"zh":zh,"en":en,"r":int(r),"c":int(c),"land":land,"lat":latstr,"z":int(S[r,c])})
meta={"nr":NR,"nc":NC,"latTop":float(rows[0]),"dRow":1/30,"cellKm":3.7,"axisCol":NC//2,"format":"int16-le","unit":"m","coast":lines,"labels":labels,
 "src":"NOAA NCEI ETOPO 2022 v1 (15 arc-second, surface), via NOAA CoastWatch ERDDAP, sampled every 1 arc-minute and averaged to 2 arc-minutes"}
json.dump(meta,open('./relief.json','w'),separators=(',',':'),ensure_ascii=False)
import os;print('png',os.path.getsize('./relief.bin'),'json',os.path.getsize('./relief.json'),'coast lines',len(lines))
# compact transport: per-row delta along columns, split into low/high byte planes, gzip
import gzip
A=np.fromfile('./relief.bin','<i2').reshape(NR,NC)
D=A.copy(); D[:,1:]=np.diff(A.astype(np.int32),axis=1).astype('<i2')
b=D.astype('<i2').view(np.uint8).reshape(-1,2)
open('./relief.bin.gz','wb').write(gzip.compress(np.concatenate([b[:,0],b[:,1]]).tobytes(),9))
print('gz',os.path.getsize('./relief.bin.gz'))
