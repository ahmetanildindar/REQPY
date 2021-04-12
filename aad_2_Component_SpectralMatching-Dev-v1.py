#%% IMPORT MODULES
import os , matplotlib.pyplot as plt , pandas as pd , numpy as np , datetime as dt
from REQPY_Module import REQPYrotdnn, load_PEERNGA_record , RSFD

plt.close("all")
plt.rcParams.update({ "font.size" : 12})

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
time_1 = [ dt * item for item in range( len( s1))]
s2,dt,n,name2 = load_PEERNGA_record(seed2)
time_2 = [ dt * item for item in range( len( s2))]

fs   = 1/dt                # sampling frequency (Hz)
tso = np.loadtxt(target)
To = tso[:,0]              # original target spectrum periods
dso = tso[:,1]             # original target spectrum psa

# Spectrum hesaplayalım
metinInfo("Orjinal kayıtların spektrumları hesaplansı")

PSA_1, PSV_1, SA_1, SV_1, SD_1 = RSFD(To , s1 , dampratio , dt )
PSA_2, PSV_2, SA_2, SV_2, SD_2 = RSFD(To , s2 , dampratio , dt )


# Ölçekleme işi yapılsın
metinInfo( "Ölçekleme işi yapılsın")
nn = 100                   # percentile 100 for RotD100, 50 for RotD50, ...

(scc1,scc2,cvel1,cvel2,cdisp1,cdisp2,
 PSArotnn,PSArotnnor,T,misfit,rms) = REQPYrotdnn(s1,s2,fs,dso,To,nn,
                                                 T1=TL1,T2=TL2,zi=dampratio,
                                                 nit=15,NS=100,
                                                 baseline=1,plots=1)
# HEDEF SPECTRUM OKUMAS                                                 
data_df = pd.read_csv( target, names = ["T_target" , "SA_target"], header = None, delim_whitespace= True)

#%% GORELİM
metinInfo("Görselleştirme başlasın")

plt.figure( figsize = (10,5))
plt.plot( T , PSArotnn ,"r--", lw = 2 , label="Scaled Spectrum" )
plt.plot( T , PSArotnnor , "b" , label = "Original Spectrum")
plt.plot( data_df["T_target" ] , data_df["SA_target"] , "c" , lw = 1.5 , label = "Target Spectrum")
plt.plot( To , PSA_1 , "gray" , label = "H1 Spectrum" )
plt.plot( To , PSA_2 , "gray" , label = "H2 Spectrum" )
plt.xlim( 0 , 4)
plt.xlabel( "Period (s)")
plt.legend()
plt.ylabel("Sa (g)")
plt.rcParams.update({ "font.size" : 14 , "font.family":"Times" })
plt.box(False)
plt.axhline( color = "k" )
plt.axvline( color = "k" )
#%%
fig, ax = plt.subplots( nrows = 2 , ncols = 1 , sharex = True, sharey = True, figsize = ( 10 , 8 ) , frameon = None )

for count , ( timeList , signalScale , signalOrigin , labelY ) in enumerate( zip( [time_1 , time_2] , [s1,s2] , [scc1,scc2] , [ seed1 , seed2 ]) ):
    ax[ count ].plot( time_1 , signalOrigin , "r-", lw = 1 , label = "Scaled Signal")
    ax[ count ].plot( timeList , signalScale , "b", lw = 2 , label = "Original  Signal")
    ax[ count ].set_ylabel( labelY )
    ax[ count ].set_xlabel( "Time (s)")

    ax[ count ].legend()
    ax[ count ].axhline( color = "k" )
    ax[ count ].axvline( color = "k" )
    ax[ count ].set_xlim(left = 0)
    ax[ count ].set(frame_on=False)  # New

plt.rcParams.update({ "font.size" : 14 , "font.family":"Times" })

# %%

# %%
