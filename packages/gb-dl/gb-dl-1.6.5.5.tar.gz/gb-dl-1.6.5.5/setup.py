from distutils.core import setup


from setuptools import setup

# read the contents of your README file
from os import path

try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except:
    with open('README.md', 'r') as f:
        long_description = f.read()





setup(
    name='gb-dl',
    version='1.6.5.5',
    scripts=['gb-dl.py'],

    url='https://github.com/barakagb/gb-dl',
    classifiers=[
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
    ],
    keywords='infosec4tc stackskills-dl ehacking-dl teachable-dl coding mosh academy-dl designerup gb-dl course downloader -dl',
    python_requires='>=2.6',
    install_requires=[
          'requests',
	  'unidecode',
          'beautifulsoup4',
          'youtube-dl',
          'lxml',
          'wget',
	  'cfscraper',
      ],

    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='barakagb',
    author_email='barakagb@gmail.com',
    description='A python based utility to download courses from infosec4tc.teachable.com ,ehacking.net ,stackskills.com and designerup.co ...etc for personal offline use.',
    include_package_data=True,
    zip_safe=False
)

