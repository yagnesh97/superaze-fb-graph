#!/bin/bash
if [ $1 == "run" ];
then
    python function_app.py
else
    echo "Command not found"
fi