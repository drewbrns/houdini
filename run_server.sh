#!/bin/bash

export NLTK_DATA="/app/bin/nltk_data/"

(jupyter notebook --notebook-dir='/app/playground' --ip=0.0.0.0 --allow-root)