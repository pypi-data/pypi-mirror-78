#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import json
import re
from collections import defaultdict, Counter

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.sankey import Sankey
import pandas as pd
try:
    import seaborn as sns
except:
    print("Ned to pip install 'seaborn'")
    raise SystemExit("Missing Required Package")
    
from visualize import flushPlots
    
"""
1. sns.barplot(x = "smoker", y = "total_bill", data =tips) ... do for IFC type
and numbers ... yes, no simple
"""
def visualizeTwo():
    ifcSplit = [
        {"type": "Placer", "total": 9999}
        
    ]
    ifcSplit = sns.load_dataset("ifcSplit")
    sns.barplot(x = "type", y = "total", data = ifcSplit)
    plt.show()
    
"""
Want side by side for User directory and steady users

Note: raw data was per day

fig, axes = plt.subplots(2,2)
axes[0, 0].hist(df['data science'])
axes[0, 1].scatter(df['Mes'], df['data science'])
axes[1, 0].plot(df['Mes'], df['machine learning'])
axes[1, 1].plot(df['Mes'], df['deep learning'])
"""

# MORE histogram etc (for trends) to try
"""
Histogram ---- in that article ---- could do spread of # of users per year since the 
start of the directory.

Scatter Plot of Consults in the three placer categories per 

[ie/ work this article]

ie/ three things:
- 1. index or not ... df ... ("Consults", X, Y, Z) ... cols ("Type", ... ... ...)
     ... index just means first column needn't be named out => special?
- 2. Histogram for per day spreads? or put into user first? yeh, user, ... over all the years spread of per year addition of users and patients ie/ median per year if yearly
buckets ...
- 3. Scatter for all three vs ?

AND

plt.annotate('Notice something?', xy=('2014-01-01', 30), xytext=('2006-01-01', 50), arrowprops={'facecolor':'red', 'shrink':0.05})
 <----------- adding annotations --- pointing to highlights
"""

# ####################### Seaborn ###################

"""
https://medium.com/@mukul.mschauhan/data-visualisation-using-seaborn-464b7c0e5122
        and seaborn in 
https://towardsdatascience.com/complete-guide-to-data-visualization-with-python-2dd74df12b5e

https://hackingandslacking.com/plotting-data-with-seaborn-and-pandas-d2499fdf6f01 (simple simple)

Also go into themes: plt.style.use('seaborn-darkgrid')

and

    sns.palplot(sns.color_palette("husl", 8)) ... husl is palette built into seaborn
    
and

    nyc_chart = sns.lineplot(x="day", y="temp", hue='year', data=nyc_df ).set_title('NYC Weather Over Time')

ie/ they do hues etc

[usual mix of snippets from different Medium Articles etc until settle down]

REM: builds over matplotlib already ie/ convenience ala the convenience methods here

Key Points to Try:
1. sns.barplot(x = "smoker", y = "total_bill", data =tips) ... do for IFC type
and numbers ... yes, no simple
2. sns.boxplot(x = , y =, data=) ... boxplot ... smoker yes/no vs IFCs ... ie/
per year do IFC breakdown NEXT?
3. sns.distplot(tips["total_bill"], bins=16, color="purple") ... I like this as a spread of per day IFC totals [or could be users involved?] ie/ distrib of typical 
4. See article has Day of Week (work off create etc date in reductions but just
record that => category color) 
    sns.lmplot(x = "total_bill", y = "tip", data = tips, hue="day")
   Could have day of week 
5. sns.heatmap(df.corr(), annot=True, fmt='.2f') ... to see correlation or otherwise of two or more variables ... do it for volumes of subtypes ie/ do they all take off together?
"""
        
# ############################## TEST DRIVER ################################
    
VISTAS_FNAMES = {"668": "Spokane", "663": "Puget Sound", "648": "Portland", "687": "Walla Walla"}
VISTA_NAMES = {"663": "PUG", "648": "POR", "668": "SPO", "687": "WWW"}
        
def main():

    assert sys.version_info >= (3, 6)
    
    data = [(1355, "PUG"), (680, "POR"), (615, "BOI"), (263, "SPO"), (37, "WCTY")]
    makeVISNSankey(data, 29, "Other IFCs Placed")
    return
        
if __name__ == "__main__":
    main()
