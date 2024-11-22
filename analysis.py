import numpy as np
import mdtraj
from pymbar import timeseries
import sys

def get_stats(fulldata,ind):
  n_fields = 6
  summary = np.zeros( (1,n_fields) )
  row = fulldata[:,ind]
  t0,g,Neff = timeseries.detectEquilibration( row )
  data_equil = row[t0:]
  indices = timeseries.subsampleCorrelatedData(data_equil, g=g)
  sub_data = data_equil[indices]
  print('Detected correlation statistics: t0 {}, efficiency {}, Neff_max {}'.format(t0,g,Neff))

  avg = sub_data.mean()
  std = sub_data.std()
  err = sub_data.std()/np.sqrt( len(indices) )

  summary = [avg,std,err,t0,g,Neff]
  return summary


if __name__ == "__main__":
    import argparse as ap
    parser = ap.ArgumentParser(description="calculated decorrelated statistics")
    parser.add_argument('filename',type=str,help="File name")
    parser.add_argument('column',type=int,help='Column index to calculate statistics on')
    parser.add_argument('-delim',default='\s',type=str,help='Column index to calculate statistics on')
    args = parser.parse_args()

    data = np.loadtxt(args.filename,delimiter=args.delim)
    col = args.column
    summary = get_stats(data,col)
    
    avg,std,err,t0,g,Neff = summary

    print('avg: \t{avg}\nstd:\t{std}\nerr:\t{err}\nt0:\t{t0}\ng\t{g}\nNeff:\t{Neff}'.format(
          avg=avg,std=std,err=err, t0=t0,g=g,Neff=Neff) )
