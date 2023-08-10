from fuzzywuzzy import fuzz

str1 = "artnetominator"
str2 = "Artnetominator"
print(fuzz.ratio(str1, str2))

str3 = "BarcoEventMaster"
str4 = "Barco-Event-Master.exe"
print(fuzz.ratio(str3, str4))
