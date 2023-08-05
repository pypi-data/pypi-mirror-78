from distutils.core import setup

setup(
  name = 'kydb',
  packages = ['kydb'],
  version = '0.1',
  license='MIT',
  description = 'kydb (Kinyu Database). NoSQL DB interface.',
  author = 'Tony Yum',
  author_email = 'tony.yum@tayglobal.com',
  url = 'https://github.com/tayglobal/kydb',
  download_url = 'https://github.com/tayglobal/kydb/archive/v_01.tar.gz',
  keywords = ['NoSQL', 'Database', 'DB'],
  install_requires=[            # I get to this in a second
        'boto3',
        's3fs',
        'redis'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
  ],
  python_requires='>=3.8',
)