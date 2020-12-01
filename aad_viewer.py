
#
# %%
import matplotlib.pyplot as plt , os, pandas as pd

#%%
fileList = [item for item in os.listdir() if "AAD-c" in item]

#%%

fig, ax = plt.subplots( nrows=2 , sharey = True , figsize=(10,5))
for counter, fileName in enumerate( fileList):
    data_df = pd.read_csv( fileName, skiprows=1, header=None)
    ax[counter].plot( data_df.iloc[:] )
# %%
