#!/bin/bash
if [ $1 == "run" ];
then
    python function_app.py
elif [ $1 == "format" ];
then
    python -m autoflake function_app.py app
    python -m isort function_app.py app
    python -m black function_app.py app
    python -m flake8 function_app.py app
    python -m mypy function_app.py app
else
    echo "Command not found"
fi