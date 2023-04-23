from setuptools import setup

# build instructions
#  python3 setup.py sdist
# twine upload dist/*

setup(name='pinyin_jyutping',
      version='0.8',
      description='Convert a Chinese sentence to Pinyin or Jyutping',
      long_description=open('README.rst', encoding='utf-8').read(),
      url='https://github.com/Language-Tools/pinyin-jyutping',
      author='LucW',
      author_email='languagetools@mailc.net',
      classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Text Processing :: Linguistic',
      ],      
      license='GPL',
      packages=['pinyin_jyutping'],
      install_requires=[
          'jieba',
      ],      
      zip_safe=False,
      include_package_data=True)