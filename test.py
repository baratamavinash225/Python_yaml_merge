# -*- coding: utf-8 -*-
"""
Created on Wed May 22 15:31:47 2019

@author: abaratam
"""


import yaml

with open("pre_validate.yaml", 'r') as stream:
    try:
        job_type = yaml.safe_load(stream)['spark_pre_validate']
        print job_type[0]
    except yaml.YAMLError as exc:
        print exc

