from setuptools import setup, Extension

with open('README.md') as f:
	readme = f.read()

setup(
  name = 'quick_ml',         # How you named your package folder (MyLib)
  packages = ['quick_ml'],   # Chose the same as "name"
  version = '1.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'quick_ml : ML For Everyone. Official Website -> www.antoreepjana.wixsite.com/quick-ml. Making Deep Learning through TPUs accessible to everyone. Lesser Code, faster computation, better modelling.',   # Give a short description about your library
  long_description = readme,
  long_description_content_type = 'text/markdown',
  author = 'Antoreep Jana',                   # Type in your name
  author_email = 'antoreepjana@gmail.com',      # Type in your E-Mail
  url = 'https://gitlab.com/antoreep_jana/quick_ml',   # Provide either the link to your github or to your website
  download_url = 'https://gitlab.com/antoreep_jana/quick_ml/-/archive/v1.1.1/quick_ml-v1.1.1.tar.gz',    # I explain this later on
  keywords = ['quick_ml','quick ml','TPU', 'Deep Learning TPU', 'tensorflow', 'deep learning'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'tensorflow==2.2.0'
      ],

  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)