#%% IMPORT MODULES
import os , matplotlib.pyplot as plt , pandas as pd , numpy as np , datetime as dt
from REQPY_Module import REQPYrotdnn, load_PEERNGA_record
plt.close("all")
#%% 
basla = dt.datetime.now()
def metinInfo( message , topLine = "-" , bottomLine = "-"):
    simdi = dt.datetime.now()
    text = f"{simdi} | {message} | {simdi-basla}"
    print( f"{ topLine * len( text)}\n{text}\n{ bottomLine * len( text )} " )

# %%
metinInfo("Basla")

seed1     = 'RSN730_SPITAK_GUK000.at2'   # seeed record comp1[g]
seed2     = 'RSN730_SPITAK_GUK090.at2'   # seeed record comp2[g]
target   = 'ASCE7.txt'                        # target spectrum (T,PSA)
dampratio = 0.05                              # damping ratio for spectra
TL1 = 0; TL2 = 0                           # define period range for matching 
                                              # (T1=T2=0 matches the whole spectrum)
# load target spectrum and seed record:

s1,dt,n,name1 = load_PEERNGA_record(seed1)    # dt: time step, s: accelertion series
s2,dt,n,name2 = load_PEERNGA_record(seed2)

fs   = 1/dt                # sampling frequency (Hz)
tso = np.loadtxt(target)
To = tso[:,0]              # original target spectrum periods
dso = tso[:,1]             # original target spectrum psa

nn = 100                   # percentile 100 for RotD100, 50 for RotD50, ...

(scc1,scc2,cvel1,cvel2,cdisp1,cdisp2,
 PSArotnn,PSArotnnor,T,misfit,rms) = REQPYrotdnn(s1,s2,fs,dso,To,nn,
                                                 T1=TL1,T2=TL2,zi=dampratio,
                                                 nit=15,NS=100,
                                                 baseline=1,plots=1)

#%% GORELİM
plt.figure( figsize = (10,5))
for i in [PSArotnn,PSArotnnor]:
    plt.plot( T , i )

data_df = pd.read_csv( target, names = ["T_target" , "SA_target"], header = None, delim_whitespace= True)

plt.plot( data_df["T_target" ] , data_df["SA_target"] )

plt.xlim( 0 , 4)

# %%
