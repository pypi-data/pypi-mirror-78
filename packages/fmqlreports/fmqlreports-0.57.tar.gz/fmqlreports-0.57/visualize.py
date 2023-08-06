#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import json
import re
from collections import defaultdict, Counter

import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import matplotlib.dates as mdates
from matplotlib.sankey import Sankey
import pandas as pd
try:
    import seaborn as sns
except:
    print("Ned to pip install 'seaborn'")
    raise SystemExit("Missing Required Package")
    
"""
TODO NOW:
- simple overview of when bar, boxplot, scatter + shows seaborn (simple) of all
  - https://towardsdatascience.com/a-beginners-guide-to-plotting-your-data-python-r-11e435262ac1 [review to tighten own]
- style: https://medium.com/analytics-vidhya/drastically-beautifying-visualizations-with-one-line-styling-plots-35a5712c4f54 <------ shows built in plt styles (not just seaborn) and can invoke easily. [FRIDAY] ex/ 538 or etc
  - see how these style files created (plt.style.use = https://matplotlib.org/3.3.0/tutorials/introductory/customizing.html) ... take one and then work own over months
- and review overall: http://www.storytellingwithdata.com/

Playfair's bars
- its orientation (vertical and horizontal bar charts) [H or V]
- and its arrangement (e.g. grouped and stacked bar charts) [G or S] 
ie/ denote types ... and variations of all these bars
"""

"""    
> vis = Visualize()
> vis.isHasBH ... etc

Modeled on sns in particular and its one liners. 
    
Using: Matplotlib, Seaborn and Pandas (DF), Numpy for static, PDF/printable graphics

REM: numpy and its expansion of Python's array to multi-dimensional arrays (see DF interplay)

Later, once static works, will try plotDy: web, dynamic versions (see: https://towardsdatascience.com/pyviz-simplifying-the-data-visualisation-process-in-python-1b6d2cb728f1, https://towardsdatascience.com/plotly-dash-vs-streamlit-which-is-the-best-library-for-building-data-dashboard-web-apps-97d7c98b938c )

Refine based on Medium etc articles.

Specific FM data context: [1] complete VISN 20 centric picture within and between VistAs + [2] size and shape of VistA data.

TODO:
- refine/maximize matplotlib
- get more into seaborn (nice wrapper on matplotlib)
- dataframes (see webReportDirectoriesLess)
  - filling/dropping
  - https://towardsdatascience.com/do-you-know-python-has-a-built-in-database-d553989c87bd has to/from sql ... see other formats
- others (more interactive, maps etc): plotly, Altair
  - geopandas and must I go plotly? https://medium.com/towards-artificial-intelligence/data-visualisation-using-pandas-and-plotly-970df88fba6f

Approach to code: this is THE GENERIC VERSION. Reports may have custom plotrs too in a separate module - ex/ plotUsers.py etc.

BACKGROUND (on the "art"):
===========================

> We have Playfair to thank for many of the popular graphs that we use today, including the bar graph (why pies bad: http://www.perceptualedge.com/articles/08-21-07.pdf) + get posters.
   - https://www.amazon.com/Playfairs-Commercial-Political-Statistical-Breviary/dp/0521855543
[note Priestly did first timeline charts: https://en.wikipedia.org/wiki/William_Playfair] 

but 

> Edward Tufte once said that “the only worse design than a pie chart is several of them, for then the viewer is asked to compare quantities located in spatial disarray both within and between pies” ... see ([save pies for the desert](http://www.perceptualedge.com/articles/08-21-07.pdf))
    
This [article](https://medium.com/nightingale/3rd-wave-data-visualization-824c5dc84967) goes into the first (Tufte) and Second (D3 et al) waves with references to other essays on forms and approaches. TODO <------- follow it around and people like:
    - https://twitter.com/jburnmurdoch
    
Visuals to Add:
================
- Radial (for time series) ... by year ... relative additions ... https://medium.com/nightingale/from-the-battlefield-to-basketball-a-data-visualization-journey-with-florence-nightingale-c39571686dfc
  and https://www.pythonprogramming.in/plot-polar-graph-in-matplotlib.html [polar]
  ... can see max ever and then each year within it and then each system in that
- TreeMap (squares size wanted for Workload per site and then relative
size of each square for each clinic/entity?)
  - import plotly.graph_objects as go / fig = go.Figure(go.Treemap
  
  
Not much magic here. We import lru_cache and decorate a function that generates Fibonacci numbers with it.

    @lru_cache(maxsize=None)
    def do(x):  

"""
class Visualize:

    def __init__(self, flushToDirectory=""): 
        self.__flushToDirectory = flushToDirectory or "Images"
        
    def svgPlotFile(self, plotName, plotMethodName): # rem: kargs inside plotName
        """
        So don't have to make the plot but can know its name as making md
        Compatible with __flushPlot's naming of SVG's
        """
        coreMethodName = re.sub("plot", "", plotMethodName)
        coreMethodNameU = coreMethodName[0].upper() + coreMethodName[1:]
        plotFilePrefix = f'{plotName}{coreMethodNameU}'
        plotFile = f'{self.__flushToDirectory}/{plotFilePrefix}BGW.svg'
        return plotFile
        
    def makeDF(self, data, columns, rows):
        """
        Note: 'rows' == 'index' == first column values stuffed in columns
        
        REM: index could be a column (again) if you .reset_index(inplace=True)
        
        Ex/ 
        
            data = [
                ("val col1", "val col2", "val col3") # of row 1
                ("val col1", "val col2", "val col3") # of row 2
            ]
            columns: ["col1 name", "col2 name", "col3 name"],
            rows: ["row 1", "row 2"]
        
        """
        df = pd.DataFrame(
            data, 
            columns=columns,
            index=rows
        )
        return df
        
    def plotIsHasBH(self, countsNTotal, title, plotName, usePerc=True):
        plotIsHasBH(countsNTotal, usePerc) # title is ignored
        plotFilePrefix = f'{plotName}IsHasBH' # add gr type to prefix
        return self.__flushPlots(plotFilePrefix)
                
    def plotCategoryBH(self, df, title, plotName):
        plotCategoryBH(df, title)
        plotFilePrefix = f'{plotName}CategoryBH' # add gr type to prefix
        return self.__flushPlots(plotFilePrefix)
        
    def plotOutOtherSankey(self, specs, title, plotName):
        plotOutOtherSankey(specs["outValues"], specs["toOtherTTL"], specs["fromLabel"], title)
        plotFilePrefix = f'{plotName}OutOtherSankey' # add gr type to prefix        
        return self.__flushPlots(plotFilePrefix)
        
    # Two variations - absolute and usePerc
    def plotCategoryBSV(self, totalsByCatagByStackId, title, plotName, usePerc=False):
        plotCategoryBSV(totalsByCatagByStackId, title, usePerc)
        plotFilePrefix = f'{plotName}CategoryBSV'    
        return self.__flushPlots(plotFilePrefix)
                        
    def plotDailies(self, dailies, title, plotName, vistaNamesPlus, start='2020-01', end='2020-02'):
        plotDailies(dailies, title, vistaNamesPlus, start, end)
        plotFilePrefix = f'{plotName}Dailies{start}-{end}' # add gr type to prefix
        return self.__flushPlots(plotFilePrefix)

    def plot365RollingMean(self, dailies, title, plotName, vistaNamesPlus, start="1987-01", end=""):
        plot365RollingMean(dailies, title, vistaNamesPlus, start, end)
        plotFilePrefix = f'{plotName}365RollingMean{start}-{end}' # add gr type to prefix
        return self.__flushPlots(plotFilePrefix)

    def plotMonthlyResamples(self, dailies, title, plotName, vistaNamesPlus, start='2018-01', end='2020-02'):
        plotMonthlyResamples(dailies, title, vistaNamesPlus, start, end)
        plotFilePrefix = f'{plotName}MonthlyResamples{start}-{end}' # add gr type to prefix
        return self.__flushPlots(plotFilePrefix)

    def plotTotalsPerYear(self, dailies, title, plotName, vistaNamesPlus, start="2015", end="2020"):
        plotTotalsPerYear(dailies, title, vistaNamesPlus, start, end)
        plotFilePrefix = f'{plotName}TotalsPerYear{start}-{end}' # add gr type to prefix
        return self.__flushPlots(plotFilePrefix)

    def __flushPlots(self, plotFilePrefix):
        """
        Four variations - may move to two transparent (svg and png)

        # TODO: see the grid color settings - default is white which would disappear in
        # a transparent to white bg. So need to work grid darker but fine?
        # ... 
        #
        # ? bbox_inches="tight" as extra or rely on explicit above?
        """
        fullPlotFilePrefix = f'{self.__flushToDirectory}/{plotFilePrefix}'
        
        plt.savefig(f'{fullPlotFilePrefix}.png', transparent=True)
        plt.savefig(f'{fullPlotFilePrefix}BGW.png', transparent=False)
        fullBGWSVGFile = f'{fullPlotFilePrefix}BGW.svg'
        try:
            plt.savefig(f'{fullPlotFilePrefix}.svg', transparent=True, format="svg")
            plt.savefig(f'{fullBGWSVGFile}', transparent=False, format="svg")
        except:
            print(f'Flushed 2 images \'{fullPlotFilePrefix}...png\' - svg failed (Redhat?)')    
        else:
            print(f'Flushed 4 images \'{fullPlotFilePrefix}...png/svg\'')
        return fullBGWSVGFile
        
# ----------------------- Individual Plots -------------------------#

"""
Individual plots made but NOT saved or shown - plt

To use:
    plotX(args)
Then either:
    plt.show()
        or
    plt.savefig("to...", ...)
"""
        
# ####################### Stacked Bar x 3 ###########################

def plotIsHasBH(countsNTotal, usePerc=True):
    """
    IsHas (one abs value out of total) - Bar Horizontal
    
    For:
    - [1] comparison of attributes (ex/ is Male, is Deceased, ...) for a total (ex/ 
    patients) of one entity (ex/ patient directory). Attributes are the Y Axis
    and the LVALUE of the dictionary passed in.
    - [2] side by side comparison of percent of one attribute (ex/ Male)
    for many entities (ex/ VistA 1, VistA 2 ...). Entities are the Y Axis and the 
    LVALUE of the dictionary passed in.
    
    Options: usePerc - use percentages vs usePerc = False => absolutes shown
    
    Not For: category/enum information (ex/ Male-Female, ALL | 1 | 2 | 3 VistAs etc)
    
        {
            "__entityName": ...
            "__total": #,
            "Y1": # <= total,
            ...
        }
        
    The Percents are calculated inside this function. The #'s passed are absolutes. The
    attributes are reordered by size.
    
    TODO (cosmetic)
    - see if can do a DF perc (see tip at bottom of this: 
    https://python-graph-gallery.com/13-percent-stacked-barplot/ with axis etc)
    - ala WSJ
      - X bar on top (PERC or ABS) ... perc -- only 0% has it/ 5 / 10 etc.
      - left align labels
      - white BG
      - no horiz lines (got this); verticals light grey not white so show
    """
    if not ("__entityName" in countsNTotal and "__total" in countsNTotal):
        raise Exception("'countsNTotal' needs __entityName and __total")
    name = countsNTotal["__entityName"]
    total = countsNTotal["__total"]
    index = []
    data = {"SET": [], "NOTSET": []}
    for ya in sorted([x for x in countsNTotal if not re.match(r'__', x)], key=lambda x: countsNTotal[x]): 
        if not isinstance(countsNTotal[ya], int):
            raise Exception("must be a simple count")
        index.append(ya)
        if usePerc:
            setValue = 100 * countsNTotal[ya]/total
            notSetValue = 100 - setValue
        else:
            setValue = countsNTotal[ya]
            notSetValue = total - countsNTotal[ya]
        data["SET"].append(setValue)
        data["NOTSET"].append(notSetValue)

    sns.set() 
    fig, ax = plt.subplots(figsize=(11, 4)) # fixed 11/4
    ax.set_title("{:,} {}".format(total, name.capitalize()))
    width = .75 # the width of the bars: can also be len(x) sequence
    ax.barh(index, data["SET"], width, edgecolor="none")
    ax.barh(index, data["NOTSET"], width, left=data["SET"], color="lightgray", edgecolor="none")
    ax.xaxis.set_major_formatter(plt.NullFormatter())
    # ax.xaxis.set_major_formatter(tick.FuncFormatter(reformat_large_tick_values));
    ax.margins(0) # this gets rid of the right spine's extra margin (ax.spines["right"])
    ax.yaxis.set_tick_params(pad=15) # note: couldn't bold em easily ... LaTeX TODO
    ax.tick_params(axis='both', which='both',length=0)
    for i, x in enumerate(data["SET"]):
        if usePerc:
            if x < 90:
                xpos = x + 1.25
            else:
                xpos = x - 5
            valToShow = "{:,}%".format(round(x, 1))
        else:
            if x/total < 0.90:
                xpos = x + total/100
            else:
                xpos = x - total/12
            valToShow = "{:,}".format(reformat_large_tick_values(x))
        plt.text(xpos, i, valToShow, fontsize=11, fontweight="bold", va='center')  
    plt.tight_layout()
    
def plotCategoryBH(df, title):
    """
    Category (vs isHas) Bar Horizontal for:
    - different items with the same category breakdowns 
    ... do more to refine (could do all same totals => show total?)
    
    Tip: put a # based message in the title
        
    Accepts df. Ex/
        rows = ["consults", "services", "users", "patients"]
        columns = ["non ifc", "ifc", "both"]
        data = [(89361, 5907, 0), (262, 209, 0), (390, 336, 44), (13151, 3454, 500)]    
        df = pd.DataFrame(
            data,
            columns=columns,
            index=rows
        )
    Will turn into percentages.
    (Tip: df = df.drop("services"))

    TODO more: 
    - see ... more on score inside 
    - consider % on right if #'s don't all total to the same ie/ ala my % of % tables
    as this is a replacement and also order down on those? ie/ lessor total % in lower
    rows
    https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html#sphx-glr-gallery-lines-bars-and-markers-horizontal-barchart-distribution-py <--- NOT this method but the look side to side is ok
    
    """        

    # perc version used for all but end total!
    dfp = df.div(df.sum(axis=1), axis=0).mul(100).round(3) 
        
    sns.set() 
    figsize = (9, 2 * len(df.index))
    fig, ax = plt.subplots(figsize=figsize)
    ax.margins(0) # this gets rid of the right spine's extra margin (ax.spines["right"])
    ax.yaxis.set_tick_params(pad=15) # note: couldn't bold em easily ... LaTeX TODO
    ax.xaxis.set_visible(False)
    if len(dfp[df.columns[0]].values) == 1:
        ax.yaxis.set_visible(False)
    ax.set_title(title)
    
    width = .75 # the width of the bars: can also be len(x) sequence
    """
    Col by Col added across all y's (df.index) with shift right each time
        y: df.index (all the "first col" values), 
        x: dfp[colName].values (this cols values)
        label == y label ie/ of horizontal bar
    REM: y first as barh
    
    Alt would be put index (first col) into rows at pos 0 and always give its
    values and then values of next col's index in all rows but better to keep
    columns (index) separate
    
    or TODO: iterrows (as just in => cols only)
    
        con = []
        for i, row in df.iterrows():
            g = {‘Customer ID #: ‘+str(row[‘customer_id’]): 
              {‘Address’: row[‘address’],
               ‘Post Code’: row[‘postcode’],
               ‘State’: row[‘state’], 
               ‘Country’: row[‘country’]
            }}
            con.append(g)
    """    
    for i, colName in enumerate(dfp.columns):
        # TODO: want first on top -- must fix
        # ys = list(reversed(df.index)) # as horiz - want first row on top
        if i == 0:
            ax.barh(df.index, dfp[colName].values, width, label=colName)
            ttlsSoFar = dfp[colName].values[:]
            continue
        ax.barh(df.index, dfp[colName].values, width, left=ttlsSoFar, label=colName)
        ttlsSoFar = [a + b for a, b in zip(ttlsSoFar, dfp[colName].values)]
    ax.legend(fontsize=10, loc='upper left')
    
    rowValSoFarByRowIdx = Counter()
    for colName in df.columns: # go across
        for i, val in enumerate(dfp[colName]): # go down
            rowValSoFarByRowIdx[i] += val
            if val < 3:
                continue
            display = f'{round(val)}%'
            xoffset = round(len(display)/1.25)
            xForVAL = rowValSoFarByRowIdx[i] - (round(val/2) + xoffset)
            plt.text(xForVAL, i, display, fontsize=11, fontweight='bold', va='center')
    ttls = df.sum(axis=1)
    for i, ttl in enumerate(ttls):
        ttlToShow = reformat_large_tick_values(ttl)
        x = 100 + round(figsize[0] * 0.25)
        plt.text(x, i, ttlToShow, fontsize=11, fontweight='bold', va='center')
    plt.tight_layout()
    
"""
Classic Vertical Stackbar (BSV) for a category breakdown, total or same size percentages. 

TODO MORE WHEN TIME: 
> plt.rcParams.update({'font.size': 22})
and
params = {'legend.fontsize': 'large',
          'figure.figsize': (20,8),
          'axes.labelsize': size,
          'axes.titlesize': size,
          'xtick.labelsize': size*0.75,
          'ytick.labelsize': size*0.75,
          'axes.titlepad': 25}
plt.rcParams.update(params)
ie/ calculate and set all

TMP FIRST: just totals ...

        totalsByCatagByStackId = {
            "WWW": {
                NONE: 7499,
                2: 7802,
                3: 27625,
                ALL: 177852
            },
            "SPO": {
                NONE: 20478,
                2: 33649,
                3: 92134,
                ALL: 177852
            },
            ...
        }

TODO:
- GENERALIZE (ex/ https://medium.com/swlh/converting-nested-json-structures-to-pandas-dataframes-e8106c59976e + https://python-graph-gallery.com/13-percent-stacked-barplot/ comments)
- df
- break in two ... 
- option to side by side (extra wrapper)

https://matplotlib.org/gallery/lines_bars_and_markers/bar_stacked.html#sphx-glr-gallery-lines-bars-and-markers-bar-stacked-py

Key TODO for this and the totals above is to move to DataFrame proper 

    # TODO: how to make DF do the percent 
    df = pd.DataFrame(data, index)
    df[1].value_counts()
    print(df.head())
    print(data)
    print(index)
    
ie/ want DF from data, index and then [1] percentage from base one (don't 
manually calc) [2] as below for TimeSeries, drive off DF
"""
def plotCategoryBSV(totalsByCatagByStackId, title, usePerc=False): # bar, stacked, vertical

    """
    matplotlib direct: https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.bar.html#matplotlib.axes.Axes.bar
    pandas.dataframes.plot (kind="barh")
    """
        
    """
    Turn StackId into index and catag "owns" dictionary ie/
        www: {"ALL": # ---> {"ALL: [# for WWW, ...
    which lets us paint the graph layer by layer from bottom to top
    
    X axis (index) of VistA (SNO) (vs date in time series)
    Y axis as int amounts (same as time series)
    Legend/color/column shown to be 1, 2, 3, 4 (ala VistA (SNO) in time series)
    """
    # want in order of size, smallest to the right
    index = []
    data = defaultdict(list) # index is legend/Y ie/ ALL, 3, ...; X is list index
    masterCatagOrder = [] # ensuring stacks have same order
    for i, stackId in enumerate(sorted(totalsByCatagByStackId, key=lambda x: sum(totalsByCatagByStackId[x][k] for k in totalsByCatagByStackId[x]))):
        index.append(stackId)
        stackTTL = sum(totalsByCatagByStackId[stackId][catag] for catag in totalsByCatagByStackId[stackId])
        for j, catag in enumerate(totalsByCatagByStackId[stackId]): # assuming ordered
            if i == 0:
                masterCatagOrder.append(catag)
            elif masterCatagOrder[j] != catag:
                raise Exception("Stacks passed in don't have categories in same order")
            # str(catag) as JSON dump turns lvalue ints to strs
            if usePerc == False:
                data[catag].append(totalsByCatagByStackId[stackId][str(catag)])
            else:
                data[catag].append(100 * totalsByCatagByStackId[stackId][str(catag)]/stackTTL)
                                 
    sns.set() 
    fig, ax = plt.subplots(figsize=(len(index) * 1.5, 5)) # NEED TO CALC FROM HEIGHT DIFFERENCE TODO
    if usePerc == False:
        ax.yaxis.set_major_formatter(tick.FuncFormatter(reformat_large_tick_values))

    width = .75 # ie/ leave .125 each side between bars
        
    bars = []
    xs = [-0.15, 0.85, 1.85, 2.85, 3.85, 4.85, 5.85]
    ttlsSoFar = [0 for i in range(0, len(totalsByCatagByStackId))]
    firstTTLs = None
    def formatNumber(fnum):
        num = round(fnum, 1)
        if num % 1 == 0:
            return int(num)
        else:
            return num
    for i, catag in enumerate(data):
        barn = ax.bar(index, data[catag], width, bottom=ttlsSoFar) # layer
        bars.append(barn)
        if usePerc: # % inside bar pieces if > 10%
            for j, dp in enumerate(data[catag]):   
                if dp < 10:
                    continue
                plt.text(xs[j], (ttlsSoFar[j] - 1) + dp/2, f'{formatNumber(dp)}%', fontsize=11) 
        ttlsSoFar = [a + b for a, b in zip(ttlsSoFar, data[catag])] 
        if i == 0:
            firstTTLs = ttlsSoFar[:]
    if not usePerc: # total on top of bar
        for i, ttl in enumerate(ttlsSoFar):
            dataStr = reformat_large_tick_values(ttlsSoFar[i], roundTo=2)
            plt.text(xs[i], 1.01 * ttlsSoFar[i], dataStr, fontsize=10) 
        # Only want text first if > 10%
        if len(set(firstTTLs)) == 1 and firstTTLs[0]/ttlsSoFar[-1] > .1: 
            noToShow = firstTTLs[0]
            txt = plt.text(xs[len(totalsByCatagByStackId) - 1], round(firstTTLs[0] * 0.9), reformat_large_tick_values(firstTTLs[0], roundTo=2), fontsize=11)
            
    legendLoc = "upper left" if usePerc == False else "lower left" # as big % first on left while biggest on right for absolutes
    ax.legend(reversed([barn[0] for barn in bars]), reversed(list(data.keys())), fontsize=9, loc=legendLoc) # ncol=len(bars) setting ncol will make legend horizontal
    # Two ways to relabel - use label= as above; the handles code here; legend map
    # handles, labels = ax.get_legend_handles_labels()
    # ax.legend(reversed(handles), reversed(labels), loc='upper right')
    ax.yaxis.get_major_ticks()[0].label1.set_visible(False) # remove '0'   
    
    # ax.set_ylabel("{} Count".format(dirName.capitalize()))
    ax.set_title(title) # whatever passes as auto needs too many overloads
            
    plt.tight_layout()
    
# ####################### Sankey ####################

"""
TODO:
- % on outs (not absolutes)
- put total into title if want ex/ Travel (X%)
- size --- see if height or width changes make distance better (could use fuller names than BOI etc)
- clean comment below
- see if anything in https://flothesof.github.io/sankey-tutorial-matplotlib.html on angles etc and also on "other"
------
- add a sankey from https://towardsdatascience.com/sankey-diagram-basics-with-pythons-plotly-7a13d557401a (simple and flows better for the many of Travel!)
                and
https://towardsdatascience.com/visualizing-in-app-user-journey-using-sankey-diagrams-in-python-8373a7bb2d22 <------- could do TELER events ... completed transitions! ... show all event flows [for test sets too]

https://het.as.utexas.edu/HET/Software/Matplotlib/api/sankey_api.html

This better tut: https://flothesof.github.io/sankey-tutorial-matplotlib.html

or this https://stackoverflow.com/questions/26677690/connecting-flows-in-matplotlib-sankey-diagram

DO THIS: https://towardsdatascience.com/the-what-why-and-how-of-sankey-diagrams-430cbd4980b5 <---- first

Syrian ref -- total source

(scale matters and as does trunk length ... PERFECT!

AFTER GET THIS CLASS WORKING, do https://github.com/ricklupton/floweaver

and flow from d3 https://www.d3-graph-gallery.com/arc.html

GOAL: get label size right

Mainly based on https://towardsdatascience.com/the-what-why-and-how-of-sankey-diagrams-430cbd4980b5

TODO: 
- WANT AUTO PLACEMENT, scale etc
- remove border

FUTURE:
- ADVANCE - want to combine two ie/ IFC out of VISN

NEXT GO TO IMPROVE SANKEY:
- GITHUB made good normalized versions on top of matplotlib: https://github.com/anazalea/pySankey/blob/master/pysankey/sankey.py

    outValues = [(1355, "PUG"), (680, "POR"), (615, "BOI"), (263, "SPO"), (37, "WCTY")]
    plotOutOtherSankey(outValues, 22, "Other IFCs Placed")
"""
def plotOutOtherSankey(outValues, toOtherTTL, fromLabel, title): 
    
    # Use seaborn style defaults, bg etc
    sns.set() 
    
    outValues = sorted(outValues, key=lambda x: x[0], reverse=True) # big to small north
    outTTL = sum(d[0] for d in outValues)
    
    if outTTL == 0 and toOtherTTL == 0:
        raise Exception(f'Can only OutOther Sankey if there is at least one or other total for OUT or OTHER: {title}')
    
    # outDir = 1 if outTTL > toOtherTTL else -1
    outDir = 1 # keeping one orientation (not differing with size)
    # toOtherDir = 1 if outDir == -1 else -1 
    toOtherDir = -1
    
    flows = [d[0] * -1 for d in outValues] 
    labels = [d[1] for d in outValues]
    orientations = [outDir for d in outValues]
    pathlengths = [0.25 for d in outValues]

    # Only show OTH is there is one!
    if toOtherTTL:
        flows.append(toOtherTTL * -1)
        labels.append("Other VISNs")       
        orientations.append(toOtherDir)
        pathlengths.append(0.25)

    total = outTTL + toOtherTTL
    # labels.insert(0, fromLabel) - don't bother with From as known
    labels.insert(0, "")
    flows.insert(0, total)
    orientations.insert(0, 0)
    pathlengths.insert(0, 0.1)
    
    # Product of scale and total input should be 1 for them but too fat for me
    SCALE_PRODUCT = 0.5  
    scale = SCALE_PRODUCT/total
    
    plt.rcParams['font.size']  = 9 # from https://stackoverflow.com/questions/58900854/sankey-with-matplotlib-positions-of-labels
    
    Sankey(
        scale=scale, # interplay with trunk len as thinkens line
        offset=0.15, # offset of text from arrows - TODO: WWW on left too close still
        # margin=0.4, (around diag in its box, not effect on contents)
        margin=0.3,
        format='%d',
        trunklength = 1, # default is 1
        pathlengths = pathlengths, # default is 0.25
        edgecolor = '#027368', # or white only on smallest!
        facecolor = '#027368',
        flows=flows,
        # labels=["WWW", "PUG", "PORT", "BOISE", "SPOK", "WHITE", "OTHER"],
        labels=labels,
        # pathlengths=[1, 1, 1, 3, 3, 3, 3],
        # patchlabel="Placer Consults",
        orientations=orientations
    ).finish()
    plt.title(title)
    
# ######################## Time Series ########################

"""
Based on https://www.dataquest.io/blog/tutorial-time-series-analysis-with-pandas/
- pandas time series
- matplotlib
- sns (need more info)

TODO: Typer and More
- Fill in gaps in Patient date created data
- Feed to subtyping (needs to be more compact if its to keep dailies!)
  - DatetimeIndex, the data type datetime64[ns] indicates that the underlying data is stored as 64-bit integers, in units of nanoseconds (ns). This data structure allows pandas to compactly store large sequences of date/time values and efficiently perform vectorized operations using NumPy datetime64 arrays.
  ... consider timestamps compacted. What effect on size ... try one as an experiment 
  - down sample ala combining subtypes ... ease of indexing/totaling by month => any datetime byValueCount -- can do one matrix of MONTH: value subtype one, value subtype two etc
    - overall keep creates to day => show below for any type

Not used:
=========

sns' boxplots as no great monthly variation to showcase ...

    fig, axes = plt.subplots(3, 1, figsize=(11, 4), sharex=True)
    for name, ax in zip(['663', '668', '687'], axes):
        sns.boxplot(data=dailies, x='month', y=name, ax=ax)
    ax.set_ylabel('Creations')
    ax.set_title(name)
    # Remove the automatic x-axis label from all but the bottom subplot
    if ax != axes[-1]:
        ax.set_xlabel('')
    plt.show()
    return
"""
def plotDailies(dailies, title, vistaNamesPlus, start='2020-01', end='2020-02'):

    # Use seaborn style defaults, bg etc
    sns.set() 
       
    fig, ax = plt.subplots(figsize=(11, 6))
    # Hone in further and add a marker and line style
    # ... must plot directly with matplotlib and not the facade as date
    # calculation for the date formatters differs a little and sets markers off
    for sno in vistaNamesPlus: # not 'columns' as > sno's in cols now
        if not re.match(r'\d+$', sno):
            continue # exclude ALL but VistAs ... no 'overall' or total users
        ax.plot(dailies.loc[start:end, sno], marker='o', linestyle='-', label=vistaNamesPlus[sno])
    ax.set_title(title)
    ax.set_ylabel('Daily Addition')
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    # Format x-tick labels as 3-letter month name and day number (strftime form)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d')) # '%b %d'
    # ax.xaxis.grid(color='blue', alpha=0.5) -- work the axis color for 
    ax.legend()
    
    plt.tight_layout()
    
"""
365-day rolling mean - note 7-day rolling mean largely follows actual dailies

> An easy way to plot these trends is with rolling means at different time scales
...
> Rolling window operations are another important transformation for time series data. Similar to downsampling, rolling windows split the data into time windows and and the data in each window is aggregated with a function such as mean(), median(), sum() ... unlike downsampling, where the time bins do not overlap and the output is at a lower frequency than the input, rolling windows overlap and “roll” along at the same frequency as the data, so the transformed time series is at the same frequency as the original time series.
"""
def plot365RollingMean(dailies, title, vistaNamesPlus, start="1987-01", end=""):
        
    # 365-day rolling mean 
    _365DayRollingMeans = dailies.loc[start:, list(vistaNamesPlus)].rolling(window=365, center=True).mean()    
    sns.set() # makes bg and lines
    fig, ax = plt.subplots(figsize=(11, 6))
    for sno in vistaNamesPlus:
        if not re.match(r'\d+$', sno):
            continue # exclude ALL but VistAs ... no 'overall' or total users
        ax.plot(_365DayRollingMeans[sno], label=vistaNamesPlus[sno])
    # Set x-ticks to yearly interval, adjust y-axis limits, add legend and labels
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y'))
    ax.legend()
    ax.set_ylabel('Added')
    ax.set_title(title)
    
    plt.tight_layout()

"""
resample the data to monthly frequency, aggregating with sum totals instead of the mean.

Note: article used stacked for some subdata
    opsd_monthly[['Wind', 'Solar']].plot.area(ax=ax, linewidth=0)
"""
def plotMonthlyResamples(dailies, title, vistaNamesPlus, start='2018-01', end='2020-02'):
    
    monthlies = dailies[list(vistaNamesPlus)].resample('M').sum()
    
    sns.set() # makes bg and lines
    fig, ax = plt.subplots()
    for snop in vistaNamesPlus: # snop as showing overall if present too (for User)
        # color='black', green orange red
        ax.plot(monthlies.loc[start:end, snop], label=vistaNamesPlus[snop])
    # ax.xaxis.set_major_locator(mdates.YearLocator())
    # ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    # Format x-tick labels as 3-letter month name and day number (strftime form)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    ax.legend()
    ax.set_ylabel('Monthly Total')
    ax.set_title(title)
    
    plt.tight_layout()
    
"""
Bar Totals per Year, side by side, by Pandas' wrapper of plt, overridden in places

Possible TODO: merge in automatic vs explicit creation breakdown ie/ BAR with
bottom as used above.

Ex annuals.head() ie/ the resample totals the days to years

       663   648  668  687  USER
Date                            
1984   151     0    0    0   151
1985   481     0    0    0   481
1986  1167     0    0    0  1167
1987  1429  2318  369  113  4222
1988  1342   666  168  118  2281

Plot: X axis is the index (DATE), Y has col values and column name (VistA (SNO)) is legend/color/bar

TODO: add in plt.annotate('Notice something?', xy=('2014-01-01', 30), xytext=('2006-01-01', 50), arrowprops={'facecolor':'red', 'shrink':0.05})
... consider doing manuals like this on top of returned plots => save is a separate
step?
"""
def plotTotalsPerYear(dailies, title, vistaNamesPlus, start="2015", end="2020"):

    # Make sure only get VistA (sno) columns, not the total user | patient
    snos = dict((vnp, vistaNamesPlus[vnp]) for vnp in vistaNamesPlus if re.match(r'\d+$', vnp))
    
    annuals = dailies[list(snos)].resample('A').sum()
    annuals = annuals.set_index(annuals.index.year)
    annuals.index.name = 'Year'

    sns.set() # makes bg and lines    
    
    ax = annuals.loc[start:end].plot.bar()
    
    ax.set_title(title)
    
    # The following resets pandas plot wrapper defaults (rotated xticks, SNO not name ...)
    ax.legend(snos.values()) # want PUG, SPO etc
    # plt.xticks([0, 1, 2, 3, 4, 5], ["2015", "16", "17", "18", "19", "2020"], rotation=0)
    xtickLabels = [str(yr) if str(yr) in [start, end] else str(yr)[2:] for yr in range(int(start.split("-")[0]), int(end.split("-")[0])+1)]
    ax.set_xticklabels(xtickLabels, rotation=0) # method 2
    ax.set_xlabel("") # don't need to see "Year"
    ax.yaxis.get_major_ticks()[0].label1.set_visible(False) # remove '0'
    
    plt.tight_layout()
    
# ############################## UTILS ########################

def reformat_large_tick_values(tick_val, pos=0, roundTo=1):

    # code below will keep 4.5M as is but change values such as 4.0M to 4M since that zero after the decimal isn't needed
    def removeTrail0(no):
        # make no into a string value
        nos = str(no)
        index_of_decimal = nos.find(".")
        if index_of_decimal == -1:
            return no    
        value_after_decimal = nos[index_of_decimal+1]
        if value_after_decimal == "0":
            # remove the 0 after the decimal point since it's not needed
            nos = nos[0:index_of_decimal]
            return int(nos)
        return no

    """
    Turns large tick values (in the billions, millions and thousands) such as 4500 into 4.5K and also appropriately turns 4000 into 4K (no zero after the decimal).
    """
    if tick_val >= 1000000000:
        val = round(tick_val/1000000000, roundTo)
        new_tick_format = f'{removeTrail0(val)}B'
    elif tick_val >= 1000000:
        val = round(tick_val/1000000, roundTo)
        new_tick_format = f'{removeTrail0(val)}M'
    elif tick_val >= 1000:
        # val = round(tick_val/1000, roundTo)
        # new_tick_format = f'remoteTrail0(val)K'
        new_tick_format = f'{removeTrail0(round(tick_val, 1)):,}'
    elif tick_val < 1000:
        new_tick_format = f'{removeTrail0(round(tick_val, 1))}'
    else:
        new_tick_format = tick_val
            
    return new_tick_format
    
# ############################## TEST DRIVER ################################
    
# TODO: retire/ deprecate so charts off
VISTAS_FNAMES = {"668": "Spokane", "663": "Puget Sound", "648": "Portland", "687": "Walla Walla"}
VISTA_NAMES = {"663": "PUG", "648": "POR", "668": "SPO", "687": "WWW"}
                
def main():

    assert sys.version_info >= (3, 6)

    viz = Visualize("ImagesHere")
    
    rows = ["consults", "services", "users", "patients"]
    columns = ["non ifc", "ifc", "both"]
    data = [(89361, 5907, 0), (262, 209, 0), (390, 336, 44), (13151, 3454, 500)]    
    df = pd.DataFrame( # direct or could do viz.makeDF
        data,
        columns=columns,
        index=rows
    )    
    print(f'Plot would be stored in {viz.svgPlotFile("ifcAndOther", "plotCategoryBH")}')
    plotCategoryBH(df, "IFCs vs Non IFCs", "visualEx")
    plt.show()
    
    outValues = [(1355, "PUG"), (680, "POR"), (615, "BOI"), (263, "SPO"), (37, "WCT")]
    print(f'Plot would be stored in {viz.svgPlotFile("placerOther", "plotOutOtherSankey")}')
    plotOutOtherSankey(outValues, 22, "WWW", "Other IFCs Placed")
    plt.show()
        
if __name__ == "__main__":
    main()
