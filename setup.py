from distutils.core import setup
setup(
  name = 'hcgamelib',
  packages = ['hcgamelib'],
  version = '0.3.14',
  license='MIT',
  description = 'Games!',
  author = 'Doppelganger',
  author_email = 'admin@doppelganger.eu.org',
  url = 'https://github.com/Doppelganger-phi',
  download_url = 'https://github.com/Doppelganger-phi/hcgamelib/archive/refs/tags/v0.3.14.tar.gz',
  keywords = ['games','hc'],
  install_requires=[
    'numpy',
    'websocket',
    'websocket-client',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
  ],
)