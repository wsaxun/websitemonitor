#!/bin/bash


function main(){
    current_path=$(cd `dirname $0`; pwd)
    project_path=$(dirname $current_path)
    main_path=${project_path}"/monitor/main.py"
    /data/env/lyf/bin/python3 $main_path
}


main
