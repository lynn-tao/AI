import sys; args = sys.argv[1:]
idx = int(args[0])-30

myRegexLst = [
  r"/^0$|^100$|^101$/i",
  r"/^[01]*$/i",
  r"/0$/i",
  r"/\b\w*[aeiou]\w*[aeiou]\w*\b/i",
  r"/^1[01]*0$|^0$/i",
  r"/^[01]*110[01]*$/i",
  r"/^.{2,4}$/is",
  r"/ *^ *\d{3} *-? *\d{2} *-? *\d{4} *$/i",
  r"/^[^d\n]*\b\S*d\S*\b/im",
  r"/^0[01]*0$|^1[01]*1$|^[01]?$/i"
  ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])
  

# Lynn Tao, 1, 2023
