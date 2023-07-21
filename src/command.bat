
py ellifant.py -ea -fp Tables_CIE -s R1 -pa 0,10,90,130,180 -sh -pt or -fc
py ellifant.py -ea -fp Tables_CIE -s W4 -pa 0,15,130,180
py ellifant.py -ea -fp Tables_CIE -s W1 -pa part/Wet.xlsx,4_ell
py ellifant.py -pga -v -sd -g 3,2,5 -fp DryAll -si
py ellifant.py -pga -v -sd -g 3,2,5 -fp WetAll -si

py ellifant.py -pga -sd -g 3,100,1000 -fp WetAll -si -v
py ellifant.py -pga -sd -g 4,100,1000 -fp WetAll -si -v

py ellifant.py -pga -sd -g 3,100,1000 -fp DryAll -si -v
py ellifant.py -pga -sd -g 4,100,1000 -fp DryAll -si -v
py ellifant.py -pga -sd -g 5,100,1000 -fp DryAll -si -v

timeout /t 100 /nobreak


