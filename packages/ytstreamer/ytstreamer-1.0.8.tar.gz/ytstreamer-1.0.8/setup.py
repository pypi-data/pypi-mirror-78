from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'Latest version is available on all operating systems and does not depend on vlc anymore.(I have deleted all the previous versions)'

setup(
		name ='ytstreamer',
		version ='1.0.8',
		author ='Icelain',
		author_email ='xerneas965@gmail.com',
		url ='https://github.com/Icelain/YTStreamer',
		description ='A lightweight, minimal and cross-platform youtube audio streamer',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='MIT',
		packages = find_packages(),
		entry_points ={
			'console_scripts': [
				'ytstream = ytstream.streamer:main'
			]
		},
		classifiers =(
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		),
		keywords ='youtube audio streamer stream music player',
		install_requires = requirements,
		zip_safe = False
)
