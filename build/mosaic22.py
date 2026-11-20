# ETOPO 2022 (15") sampled every 1' over the strip footprint -> 2' mosaic (2x2 mean)
import numpy as np, glob, json
from scipy.io import netcdf_file
from scipy.ndimage import distance_transform_edt
LA0,LA1,LO0,LO1=-57.0,86.5,-70.0,62.0
n1r=int(round((LA1-LA0)*60))+2; n1c=int(round((LO1-LO0)*60))+2
M1=np.full((n1r,n1c),np.nan,np.float32)
for f in glob.glob('build/data/b_*.nc'):
    n=netcdf_file(f,'r',mmap=False); la=n.variables['latitude'][:]; lo=n.variables['longitude'][:]; z=n.variables['z'][:].astype(np.float32)
    r=np.round((la-LA0)*60).astype(int); c=np.round((lo-LO0)*60).astype(int)
    M1[np.ix_(r,c)]=z
print('nan frac 1min',np.isnan(M1).mean())
R2,C2=n1r//2,n1c//2; A=M1[:R2*2,:C2*2].reshape(R2,2,C2,2)
with np.errstate(all='ignore'): M=np.nanmean(A,axis=(1,3)).astype(np.float32)
nan=np.isnan(M); idx=distance_transform_edt(nan,return_distances=False,return_indices=True); M=M[tuple(idx)]
np.save('build/data/M.npy',M)
# cell (i,j) of M covers 1' rows 2i,2i+1 -> center lat = LA0 + (2i+0.5)/60
json.dump({"la0":LA0+0.5/60,"lo0":LO0+0.5/60,"d":1/30},open('build/data/M.json','w'))
print(M.shape,M.min(),M.max())
