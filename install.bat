@echo off

:start
cls
set python_ver=39

python get-pip.py

cd \
cd \python%python_ver%\Scripts\
pip install networkx
pip install pygame

pause
exit