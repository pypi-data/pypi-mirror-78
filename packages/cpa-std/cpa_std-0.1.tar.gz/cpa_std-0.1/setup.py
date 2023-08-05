import setuptools

setuptools.setup(
    name='cpa_std',
    version='0.01',
    description='根据企业会计准则规范会计科目名称',
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
