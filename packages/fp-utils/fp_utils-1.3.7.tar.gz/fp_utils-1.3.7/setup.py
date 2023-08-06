from distutils.core import setup

setup(
    name = 'fp_utils',
    packages = ['fp_utils', 'fp_utils.big_query', 'fp_utils.mongo', 'fp_utils.google','fp_utils.clockify'],
    version = '1.3.7',  #
    description = 'Most commonly used Fifth Partners functions in PyPi for easy pip install. ',
    author = 'Nathan Duncan',
    author_email = 'nduncan@fifthpartners.com',
    url = 'https://github.com/fifth-partners/fp-utils',
    download_url = 'https://github.com/fifth-partners/fp-utils/archive/1.3.7.tar.gz',
    keywords = ['fifth_partners', 'utils'],
    install_requires=['google-cloud-bigquery', 'google-api-python-client','google-auth-httplib2', 'google-auth-oauthlib',
    'pymongo', 'datetime', 'bs4', 'pathlib','pandas','numpy','requests','oauth2client','python-dotenv','boto3',
    'pybase64','pandas_gbq'],
    classifiers = [
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)
