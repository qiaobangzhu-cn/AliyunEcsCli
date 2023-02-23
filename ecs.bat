@echo off

set ml=%1
cd %~dp0
python ecs.py %*
