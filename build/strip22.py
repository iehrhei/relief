import numpy as np, json
from scipy.ndimage import gaussian_filter, gaussian_filter1d, map_coordinates
from PIL import Image
import json as _j
M=np.load('build/data/M.npy'); _o=_j.load(open('build/data/M.json')); LA0,LO0,d=_o['la0'],_o['lo0'],_o['d']
def samp(lat,lon,A=M,order=1): return map_coordinates(A,[(lat-LA0)/d,(lon-LO0)/d],order=order,mode='nearest')
guess=[(85.5,-6),(84,-5),(82.5,-4),(80.5,0),(79.5,3),(78,7.5),(76,8.5),(74,7),(73,3),(72.3,-2),(71.5,-7),(70.5,-14),(68,-17.5),(66.5,-17.5),(65,-17),(64,-20),(63,-23.5),(60,-29.5),(57,-33),(54,-34.5),(52.5,-31.5),(50,-29),(45,-28),(40,-29.5),(35,-34),(30.5,-42),(25,-45),(20,-46),(15,-45.5),(10,-41),(6,-33),(2,-28),(0,-20),(-3,-13),(-8,-13.5),(-15,-13.8),(-20,-12),(-25,-13.5),(-30,-13.5),(-35,-16),(-40,-16.5),(-45,-14),(-48,-10),(-51,-3),(-54.4,3.4),(-56,6)]
gl=np.array([g[0] for g in guess])[::-1]; gx=np.array([g[1] for g in guess])[::-1]
LATTOP,LATBOT=85.0,-55.6; rows=np.arange(LATTOP,LATBOT-1e-9,-1/30)
Ms=gaussian_filter(M,6)
cen=[]
for lat in rows:
    g=np.interp(lat,gl,gx); w=min(5,300/(111*np.cos(np.radians(lat)))); lons=np.linspace(g-w,g+w,121)
    z=samp(np.full_like(lons,lat),lons,Ms); cen.append(lons[np.argmax(z)])
cen=np.array(cen); cen=.4*cen+.6*np.interp(rows,gl,gx); cen=gaussian_filter1d(cen,50,mode='nearest')
CELL=3.7; HW=1150.0; NC=int(2*HW/CELL)|1; km=np.linspace(-HW,HW,NC)
R=6371.0
def dest(lat,lon,brg,dist):
    p1=np.radians(lat); l1=np.radians(lon); b=np.radians(brg); a=dist/R
    p2=np.arcsin(np.sin(p1)*np.cos(a)+np.cos(p1)*np.sin(a)*np.cos(b))
    l2=l1+np.arctan2(np.sin(b)*np.sin(a)*np.cos(p1),np.cos(a)-np.sin(p1)*np.sin(p2))
    return np.degrees(p2),np.degrees(l2)
S=np.zeros((len(rows),NC),np.float32); LAT=np.zeros_like(S); LON=np.zeros_like(S)
for i,lat in enumerate(rows):
    pl,ll=dest(lat,cen[i],np.where(km>=0,90.0,270.0),np.abs(km)); LAT[i]=pl; LON[i]=ll
    S[i]=samp(pl,ll)
np.save('build/data/S.npy',S); np.save('build/data/SLAT.npy',LAT); np.save('build/data/SLON.npy',LON); np.save('build/data/rows2.npy',rows)
print(S.shape,S.min(),S.max(), 'lon range',LON.min(),LON.max())
gy,gx2=np.gradient(S,CELL*1000,CELL*1000); L=np.array([-.6,-.6,.53]); n=np.dstack([-gx2*6,-gy*6,np.ones_like(gx2)]); n/=np.linalg.norm(n,axis=2,keepdims=True)
s=np.clip(n@L,0,1); s[S>0]=1
img=Image.fromarray((s*255).astype(np.uint8)).resize((S.shape[1]//2,S.shape[0]//2))
ims=[img.crop((0,k*530,img.width,min(img.height,(k+1)*530))) for k in range(4)]
c=Image.new('L',(img.width*4+30,530),255)
for k,im in enumerate(ims): c.paste(im,(k*(img.width+10),0))
c.save('build/data/montage2.png')
