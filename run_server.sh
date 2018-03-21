#!/bin/bash
(cd app/notebook; jupyter notebook --notebook-dir='/app/playground' --ip=0.0.0.0 --allow-root)