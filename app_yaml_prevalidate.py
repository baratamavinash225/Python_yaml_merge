# -*- coding: utf-8 -*-
"""
Created on Tue May 21 14:42:38 2019

@author: abaratam
"""

import yaml
import sys
def main():
    app_yaml_file = 'spark_app_config.yaml'
    env=''
    pre_validate_config_file = 'pre_validate.yaml'
    pre_validate_app_yaml_config(app_yaml_file, env, pre_validate_config_file)

def pre_validate_app_yaml_config(app_yaml_file, env, pre_validate_config_file):
    with open(app_yaml_file, 'r') as stream:
        try:
            job_type = yaml.safe_load(stream)['job_type']
            if job_type !=None or job_type !='':
                with open(pre_validate_config_file, 'r') as pre_validate_stream:
                    try:
                        if job_type == 'spark':
                            spark_keys_validate = yaml.safe_load(pre_validate_stream)['spark_pre_validate']
                            pre_validate_spark_yaml_config(app_yaml_file, env, spark_keys_validate)
                    except yaml.YAMLError as exc:
                        print exc
            else:
                sys.exit("No job_type Found")
        except yaml.YAMLError as exc:
            print exc

def pre_validate_spark_yaml_config(app_yaml_file, env, spark_keys_validate):
    message = ''
    with open(app_yaml_file, 'r') as stream:
        try: 
            app_config = yaml.safe_load(stream)['Configurations']  
            #print app_config
            for i in range(len(app_config)):
                message = message + validate_pre_spark_configs_dict(app_config[i]['config'][0]['spark_configs'][0], app_config[i]['config'][0]['Environment'], spark_keys_validate)
            print message
            #if message.__contains__("Error:"):
                #exit(1)
        except yaml.YAMLError as exc:
            print exc

def validate_pre_spark_configs_dict(conf_dict, environment, spark_keys_validate):
    message = ''
    for i in spark_keys_validate:
        if not i in conf_dict.keys():
            message = message + "[ERROR: configuration param " + i + " is not available in the given yaml config for " + environment + " environment] \n"
        else:
            if conf_dict[i] is None or conf_dict[i] == '' :
                message = message + "[Error: configuration param " + i + " is either empty or null in the given yaml config for " + environment + " environment] \n"
    if not message.__contains__("Error"):
        message = "[INFO: Pre validation successful for the environment " +  environment + "] \n"
    return message
if __name__ == "__main__":
    main()