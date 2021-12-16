#!/bin/bash
if [ $# == 1 ]
then
    git add test
    git commit -m "$1"
    git checkout utils/__pycache__
    git checkout utils/request_utls/__pycache__
else
    echo "参数错误"
fi
