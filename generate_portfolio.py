from bs4 import BeautifulSoup as bs
from pathlib import Path
import pandas as pd


img_html = '''
<div class="col-md-4">
	<div class="thumbnail">
	  <a href="{0}" data-toggle="lightbox" data-footer="" data-gallery="front-page">
	    <img src="{1}" alt="{2}" style="width:100%">
	  </a>
	</div>
</div>
'''

def generate_portfolio(img_dir, out_file):

	template = open('port_template.html', 'rb').read()
	soup = bs(template, features='lxml')

	img_dir = Path(img_dir)
	img_list = sorted(list(img_dir.glob('*.*')))
	img_df = pd.DataFrame(data=img_list, columns=['path'])
	img_df['pos'] = img_df['path'].apply(lambda x: int(Path(x).name.split('_')[0]))

	gallery_div = soup.find('div', {'class': 'gallery'}) 

	def new_row():
		row = soup.new_tag('div')
		row['class'] = "row no-gutters"
		return row

	row = new_row()

	for i, (_, imgs) in enumerate(img_df.groupby('pos')):

		img_full = imgs.iloc[0]['path']
		img_crop = imgs.iloc[1]['path'] if len(imgs) == 2 else img_full
		img_div = img_html.format(img_full, img_crop, '')

		row.append(bs(img_div, 'html.parser'))

		if (i + 1) % 3 == 0:
			gallery_div.append(row)
			row = new_row()

	html = str(soup.prettify())
	with open(out_file, "w") as file:
		file.write(html)
	
if __name__ == '__main__':

	import sys
	img_dir, out_file = sys.argv[1:]
	generate_portfolio(img_dir, out_file)