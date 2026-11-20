cd "$(dirname "$0")" && mkdir -p data && cd data
dl(){ a=$1;b=$2;x0=$3;x1=$4;f=b_${a}_${x0}.nc; [ -s $f ] && return; for t in 1 2 3; do code=$(curl -s -m 290 -o $f -w "%{http_code}" "https://coastwatch.pfeg.noaa.gov/erddap/griddap/ETOPO_2022_v1_15s.nc?z%5B($a):4:($b)%5D%5B($x0):4:($x1)%5D"); echo "$a $x0 $code $(stat -c%s $f 2>/dev/null)"; [ "$code" = 200 ] && return; rm -f $f; sleep 10; done; }
dl -57 -46 -29 23
dl -46 -36 -31 7
dl -36 -26 -31 0
dl -26 -16 -27 0
dl -16 -6 -26 0
dl -6 -1 -44 0
dl -1 4 -44 0
dl 4 14 -58 -17
dl 14 24 -58 -32
dl 24 34 -58 -20
dl 34 44 -51 -12
dl 44 54 -53 -11
dl 54 64 -53 9
dl 64 69 -45 51
dl 69 74 -45 51
dl 74 79 -70 62
dl 79 84 -70 62
dl 84 86.5 -70 62
