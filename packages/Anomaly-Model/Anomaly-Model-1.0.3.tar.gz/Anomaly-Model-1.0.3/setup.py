# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 21:15:00 2020

@author: ZhiWang
"""

from distutils.core import setup
from setuptools import setup, find_packages


setup(
    name='Anomaly-Model',
    keywords = ['anomaly', 'detect'],
    version= "1.0.3",
    description =  'import method for anomaly detection',
        
    long_description = 'import method for anomaly detection',
    author= 'anomaly detect team',
    author_email='wzhi05@126.com',
    maintainer='wangzhi',
    maintainer_email='wzhi05@126.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.ibm.com/PO-GBS/Magna-MIG/tree/master/MIG_Anomaly_Detection/Anomaly_Models',
    install_requires=[
        'numpy',
        'pandas',
    ],
)
