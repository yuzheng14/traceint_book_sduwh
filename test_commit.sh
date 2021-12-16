#!/bin/bash
if [ $# == 1 ]
then
    git add test
    git commit -m "$1"
else
    echo "参数错误"
fi
