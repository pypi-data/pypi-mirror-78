#!/usr/bin/env python3

import argparse
import os
import yaml
from datetime import datetime, timezone

##############################################################################

def load_yaml(yaml_file):
    with open(yaml_file) as file:
        yaml_dict = yaml.load(file.read(), Loader=yaml.CLoader)

    return yaml_dict

def main():
    
    cwd = os.getcwd()
    print(cwd)
    print(__file__)
    print(os.path.dirname(__file__))

    parser = argparse.ArgumentParser('recaud')
    parser.add_argument('config')
    parser.add_argument('--output', '-o')

    args = parser.parse_args()

    config_file = args.config
    config = load_yaml(config_file)

    if args.output:
        output_file = args.output
    else:
        date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S')
        output_file = 'alog_' + date_str + '.' + str(config['ext'])

    command = 'ffmpeg -f alsa -ar ' + str(config['ar']) + ' -ac ' + str(config['ac']) + ' -i ' + str(config['mic']) + ' ' + output_file

    os.system(command)


if __name__ == "__main__":
    main()
