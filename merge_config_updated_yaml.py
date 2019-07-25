"""
Created on Fri May  3 15:16:52 2019

@author: abaratam
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:24:05 2019

@author: abaratam
"""
import yaml
import os
def main():
    environment = 'DEV'
    app_config_file = "spark_app_config.yaml";
    default_config_file = "spark_dag_config_default.yaml";
    #default_config_file = sys.argv[1]
    #app_config_file = sys.argv[2]
    create_merge_yaml_file(return_merge_config_dict(return_app_config_dict(app_config_file, environment), return_default_config_dict(default_config_file)), environment)

def return_app_config_dict(app_config_file, environment):
    conf_app_take = {}
    with open(app_config_file, 'r') as stream:
        try:
            app_config = yaml.safe_load(stream)['Configurations']
            for i in range(len(app_config)):
                config = app_config[i]['config'][0]['Environment']
                if config == environment:
                    conf_app_take = app_config[i]['config'][0]
                    del conf_app_take['Environment']
        except yaml.YAMLError as exc:
            print exc
    return conf_app_take
def return_default_config_dict(default_config_file):
    conf_default_take = {}
    with open(default_config_file, 'r') as stream:
        try:
            default_config = yaml.safe_load(stream)['Configurations']
            conf_default_take = default_config[0]['config'][0]
        except yaml.YAMLError as exc:
            print exc
    return conf_default_take
def return_merge_config_dict(conf_app_take, conf_default_take):
    conf_final_take = {}
    for key, value in conf_default_take.iteritems():
        configs_dict = {}
        for dictkey, value1 in (conf_default_take[key][0]).iteritems():
            if dictkey in (conf_app_take[key][0]):
                configs_dict[dictkey] = conf_app_take[key][0][dictkey]
            else:
                configs_dict[dictkey] = conf_default_take[key][0][dictkey]
        conf_final_take[key] = [configs_dict]
    return conf_final_take
def create_merge_yaml_file(conf_final_take, environment):
    with open('spark_'+environment+'_dag_config.yaml', 'w') as outfile:
        yaml.dump(conf_final_take, outfile, default_flow_style=False)

if __name__ == '__main__':
    main()
	