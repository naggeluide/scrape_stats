from matplotlib.dates import date2num,num2date,DateFormatter
import pandas as pd
import os
import numpy as np
from wordcloud import WordCloud, STOPWORDS
from collections import Counter

CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']


def all_stats_plot_work(xls_file,sheet_title,subs=False,wc=False,kfac=10.,perhit=False):
  '''plot stats for a single work. Options: subs=True to plot subscription counts, wc=True to plot word count, kfac is the factor to divide hits by on the plot, perhit=True divides all other fields by number of hits'''
  xls = pd.ExcelFile(xls_file)
  df=pd.read_excel(xls, sheet_title)
  xaxv=df.index
  quants=['Bookmarks','Public Bookmarks','Comment Threads']
  fig,ax=plt.subplots(2,sharex=True,figsize=[10,8])
  if not perhit:
      ax[0].plot_date(xaxv,np.array(df['Hits'])/kfac,'-o',c=CB_color_cycle[0], label = 'Hits/'+str(int(kfac)))
      norm=1
  else:
      norm=np.array(df['Hits'])
  ax[0].plot_date(xaxv,df['Kudos']/norm,'-o',c=CB_color_cycle[1], label = 'Kudos')
  for i,q in enumerate(quants): #put these on subplot underneath cuz y-ax scale will be different
      ax[1].plot_date(xaxv,df[q]/norm,'-o', c=CB_color_cycle[i+2],label = q)
  if subs:
      ax[1].plot_date(xaxv,df['Subscriptions']/norm,'-o',c=CB_color_cycle[-2], label= 'Subscriptions')
  if wc:
      ax[1].plot_date(xaxv,df['Word Count']/1000,'-o',c=CB_color_cycle[-1], label= 'Word Count (K)')

  box1=ax[0].get_position()
  box2=ax[1].get_position()
  ax[0].set_position([box1.x0,box1.y0*.7,box1.width,box1.height*1.5])
  ax[1].set_position([box2.x0,box2.y0,box2.width,box2.height*.7])

  ax[1].set_xlabel('Date')
  if perhit:
      ax[0].set_ylabel('Per Hit')
  ax[0].legend(loc='upper left')
  ax[1].legend(loc='upper left')
  ax[0].set_title(sheet_title)
  myFmt = DateFormatter('%D')
  ax[1].xaxis.set_major_formatter(myFmt)
  plt.gcf().autofmt_xdate()
  fig.show()

def wordcloud(xls,field='Additional Tags',fandom='all'):
    ''' make a wordcloud of your tags, characters, etc (metadata) for a particular fandom or for all works'''
    dfdict={}
    sheet_names=pd.ExcelFile(xls).sheet_names
    sheet_names.remove('Totals')
    for s in sheet_names:
        dfdict[s]=pd.read_excel(xls,s)

    #does field exist?
    if field not in dfdict[s].keys():
        print 'Field ' + field + ' does not exist! please pick one of: ' + dfdict[s].keys() #should throw a proper exception instead...
        return

    #select data
    words=[]
    if fandom !='all':
        flist=[dfdict[s]['Fandom'][0] for s in sheet_names]
        slist=[]
        for f,s in zip(flist,sheet_names):
            if fandom in f:
                slist.append(s)
    else:
        slist=sheet_names

    for s in slist:
        all_vals=dfdict[s][field].values
        words.append([v for v in all_vals if type(v) !=float])

    #if words is [] then fandom probably written wrong
    llist=[w for w in words[0]]#buff=",".join(words[0])
    for ww in words[1:]:
        for w in ww:
            llist.append(w)

    freqs=Counter(llist)

    #comment_words = ''
    stopwords = set(STOPWORDS)

    wordcloud = WordCloud(width = 800, height = 800,
                regexp=r"\w[\w' ],",
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate_from_frequencies(freqs)

    # plot the WordCloud image
    fig,ax=plt.subplots(figsize = (8, 8), facecolor = None)
    ax.imshow(wordcloud)
    ax.axis("off")
    fig.tight_layout(pad = 0)
    fig.show()
