py main.py -pga -v -sd -g 4,5,5 -fp Tables_CIE
py main.py -pga -sd -g 4,500,500 -fp Tables_CIE
py main.py -pga -sd -g 4,500,500 -fp SURFACE
py main.py -pga -sd -g 4,500,500 -fp KAI
py main.py -pga -sd -g 4,500,500 -fp METAS
py main.py -pga -sd -g 4,500,500 -fp LCPC

py main.py --partitiongeneticalgorithm

sleep 50

shutdown -s -t 0
```
