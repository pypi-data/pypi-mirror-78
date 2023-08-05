import setuptools
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setuptools.setup(
    name='cpa_std',
    version='0.03',
    description='根据企业会计准则规范会计科目名称',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Wang Qi',
    author_email='wangmarkqi@gmail.com',
    url='https://github.com/wangmarkqi/cpa_std',
    packages=setuptools.find_packages(),
    keywords=['会计', '科目', '规范'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)


'''
# 上传source 包
python setup.py sdist
twine upload dist/*

'''
