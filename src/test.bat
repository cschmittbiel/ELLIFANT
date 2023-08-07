
py ellifant.py -ea -fp Tables_CIE -s R1 -pa 0,10,90,130,180 -sh -pt or -ps 2D_top
py ellifant.py -ea -fp Tables_CIE -s W4 -pa 0,15,130,180
py ellifant.py -ea -fp Tables_CIE -s W1 -pa part/Wet.xlsx,4_ell

py ellifant.py -pga -sd -g 3,2,10 -fp WetAll -si -v
py ellifant.py -pga -sd -g 5,2,10 -fp WetAll -si -v


