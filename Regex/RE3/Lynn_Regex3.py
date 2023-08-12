import sys; args = sys.argv[1:]
idx = int(args[0])-50

myRegexLst = [
  r"/\w*(\w)\w*\1\w*/i",
  r"/\w*(\w)(\w*\1\w*){3}/i",
  r"/^([01])[01]*\1$|^[01]?$/i",
  r"/(?=\b\w{6}\b)\w*cat\w*/i",
  r"/(?=\b\w{5,9}\b)(?=\w*bri)(?=\w*ing)\w*/is",
  r"/(?=\b\w{6}\b)(?!\w*cat)\w*/i",
  r"/\b(?:(\w)(?!\w*\1))+\b/i",
  r"/^((?!10011)[01])*$/i",
  r"/\w*([aeiou])(?!\1)[aeiou]\w*/i",
  r"/^((?!101|111)[01])*$/i"
  ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])
  
# Lynn Tao, 1, 2023