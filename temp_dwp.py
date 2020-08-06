import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

__author__ = "Jason Godwin"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jason Godwin"
__email__ = "jason.godwin@noaa.gov"
__status__ = "Production"

'''
Download archived METAR here: 
https://mesonet.agron.iastate.edu/request/download.phtml

1. Select Station/Network (select only ONE location you are interested in).
2. Select from Available Data: make sure to select air temperature (F) and
   dew point (F).
3. Specific Date Range: select which every period of time you want.
4. Timezone of Observation Times: theoretically, local time may be more
   accurate, but I've gotten sensible results with UTC as well.
5. Download Options
   5a. Data Format: Comma Delimited (No DEBUG headers).
   5b. Include Latitude + Longitude: No.
   5c. (Important!) How to represent missing data? Use 'null'.
   5d. How to represent trace reports? Use 'T'. (Shouldn't matter).
   5e. Save result data to file on computer.
6. Limit Report Types. I just kept this as the default setting.
   "MADIS HFMETAR" and "Routine + SPECIals" were both selected.
7. Get Data.

Under the setup section below, set your filepath to point to the CSV you
downloaded from ISU. The outfile name is something like the site ID. 
"_plot.png" will be appended when it is finally saved. locname is a 
descriptive name that will go in the plot title. The setup block should
be the only thing you need to modify to make the code run "out of the box".
'''

def main():

# setup
    filepath = 'DFW.txt'
    outfile = 'dfw'
    locname = 'Dallas/Fort Worth, TX'

    # import the data
    data = pd.read_csv(filepath,index_col='valid')

    # some modifications to the data
    data = data.dropna(subset=['tmpf','dwpf'])
    data.index = pd.to_datetime(data.index)

    # compute the 7-day moving averages
    data['tmpf_7d'] = data['tmpf'].rolling('7D').mean()
    data['dwpf_7d'] = data['dwpf'].rolling('7D').mean()

    # compute the daily max
    data['tmpf_max'] = data['tmpf'].rolling('1D').max()
    data['tmpf_min'] = data['tmpf'].rolling('1D').min()

    # plot everything
    plt.clf()
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(1,1,1)
    plt.plot(data['tmpf'],label='Temperature Observations',marker='o',\
        markerfacecolor='None',markeredgecolor='red',markersize=2,linestyle='None')
    plt.plot(data['dwpf'],label='Dewpoint Observations',marker='o',\
        markerfacecolor='None',markeredgecolor='green',markersize=2,linestyle='None')
    plt.plot(data['tmpf_7d'],label='Temperature 7-Day Avg.',marker=None,\
        color='red',linewidth=4)
    plt.plot(data['dwpf_7d'],label='Dewpoint 7-Day Avg.',marker=None,\
        color='green',linewidth=4)
    plt.plot(data['tmpf_max'].rolling('7D').mean(),label='7-Day Avg. Max Temp',marker=None,\
        color='orange',linewidth=2,linestyle='--')
    plt.plot(data['tmpf_min'].rolling('7D').mean(),label='7-Day Avg. Min Temp',marker=None,\
        color='blue',linewidth=2,linestyle='--')

    # plot aesthetics
    plt.title('Observed/Average Temperature and Dewpoint at %s' % locname)

    plt.xlim([data.index[0],data.index[-1]])
    plt.xticks(rotation=90)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))

    ymin = math.floor(data['dwpf'].min() / 5) * 5
    ymax = math.ceil(data['tmpf'].max() / 5) * 5
    ax.tick_params(axis='y',labelright=True)
    plt.yticks(np.arange(ymin-5,ymax+5,5))
    plt.ylabel('Temperature (F)')

    plt.grid()
    plt.legend()

    plt.savefig('%s_plot.png' % outfile,bbox_inches='tight')

if __name__ == '__main__':
    main()
