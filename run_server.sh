#!/bin/bash

if [ $PYTHON_ENV = "staging" ]; then 
    python -c "import houdini; houdini.run()"
fi 

if [ $PYTHON_ENV = "development" ]; then
    export NLTK_DATA="/app/bin/nltk_data/"
    (jupyter notebook --notebook-dir='/app/playground' --ip=0.0.0.0 --allow-root)
fi