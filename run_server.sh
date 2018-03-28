#!/bin/bash

export NLTK_DATA="/app/bin/nltk_data/"

(cd app/playground; jupyter notebook --notebook-dir='/app/playground' --ip=0.0.0.0 --allow-root)D