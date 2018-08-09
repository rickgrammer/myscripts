import os

folders = os.listdir()

for folder in folders:
	if os.path.isdir(folder):
		os.chdir(folder)
		for f in os.listdir():
			if f.endswith('.vtt'): os.remove(f)
			if f.endswith('.zip'):
				if not os.path.isdir('files'):
					os.mkdir('files')
				os.rename(f,'./files/'+f)
			if f.endswith('.pdf'):
				if not os.path.isdir('pdfs'):
					os.mkdir('pdfs')
				os.rename(f,'./pdfs/'+f)
			if f.endswith('.css') or f.endswith('.js'):
				if not os.path.isdir('source code'):
					os.mkdir('source code')
				os.rename(f,'./source code/'+f)
			if f.endswith('.jpeg') or f.endswith('.svg') or f.endswith('.png') or f.endswith('.jpg'):
				if not os.path.isdir('images'):
					os.mkdir('images')
				os.rename(f,'./images/'+f)
		os.chdir('..')

