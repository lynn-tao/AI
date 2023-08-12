import sys; args = sys.argv[1:]
idx = int(args[0])-40

myRegexLst = [
  r"/^[x.o]{64}$/is",
  r"/^[xo]*[.][xo]*$/is",
  r"/^[.].*|.*[.]$|^[x]+[o]*[.].*$|^.*[.][o]*[x]+$/i",
  r"/^.(..)*$/is",
  r"/^0([01][01])*$|^1[10]([01][01])*$/i",
  r"/\w*[a][eiou]\w*|\w*[e][aiou]\w*|\w*[i][aeou]\w*|\w*[o][aeiu]\w*|\w*[u][aeio]\w*/i",
  r"/^(0|10)*1*$/i",
  r"/^[bc]+a?[bc]*$|^[bc]*a?[bc]+$|^a$/",
  r"/^[bc]+([a][bc]*[a][bc]*)*$|^([a][bc]*[a][bc]*)+$/",
  r"/^2[02]+([1][02]*[1][02]*)*$|^([1][02]*[1][02]*)+$/i"
  ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])
  
# ^.*([aeiou])(?!\1)[aeiou].*$
# Lynn Tao, 1, 2023