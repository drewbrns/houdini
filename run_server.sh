#!/bin/bash
(cd app/notebook; jupyter notebook --notebook-dir='/app/notebook' --ip=0.0.0.0 --allow-root)