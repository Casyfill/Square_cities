#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pandas as pd
import pylab as plt 


import requests
s = requests.get("https://raw.githubusercontent.com/Casyfill/CUSP_templates/master/Py/fbMatplotlibrc.json").json()
plt.rcParams.update(s)



def main(dataPath):
	'''renders stats and plots for chosen datum'''

	cols = ['genCategory',
			'category',
			'name',
			'lon',
			'lat',
			'checkIns',
			'tips',
			'users',
			'createdAt',
			'tileID',
			'ID',
			'query',
			'time',
			'verified',
			'price',
			'rating',
			'tags',
			'photoCount',
			'description']

	df = pd.read_csv(dataPath, index_col=0, encoding='utf8')[cols]

	cats = df[['genCategory','category','checkIns','tips','users','photoCount']].groupby('category').agg({'genCategory':lambda x: x.iloc[0],
                                                                                                              "checkIns":sum,
                                                                                                              'tips':sum, 
                                                                                                              'users':sum,
                                                                                                              'photoCount':sum})
	cats.reset_index(inplace=1)


	def annotate_plot(frame, label_col, plot_col1,plot_col2, **kwargs):
	    for label, x, y in zip(frame[label_col], frame[plot_col1], frame[plot_col2]):
	        plt.annotate(label, xy=(x, y), **kwargs)

	


if __name__ == '__main__':
	main()