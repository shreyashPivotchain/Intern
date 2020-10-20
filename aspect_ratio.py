import pandas as pd
df=pd.read_csv('tatapower_labels.csv')
for i in df[df.columns[0:]]:
	df['aspect_ratio']=(df['xmax']-df['xmin'])/(df['ymax']-df['ymin'])
	

df.to_csv('tatapower_labels.csv')