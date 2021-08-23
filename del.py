def solution(s):
  factor = 0
  found = True
  upto = (len(s)//2) + 1 
  while factor*3 <= len(s) and found:
    factor += 1
    first = int(s[0:factor])
    second = int(s[factor:factor+factor])
    third = int(s[factor*2:factor*3])
    v1 = second-first
    v2 = third-second
    if (v1 == 1 or v1 == 2) and (v2 == 1 or v2 == 2):
      found = False
  if found == True or (len(s)%factor!=0): return -1
  
  found = False
  ans = None
  for i in range(factor, len(s)+1, factor):
    value = int(s[i:i+factor])
    left = int(s[i-factor:i])
    print(i, value, left, found)
    if (value-left) > 1 and (value-left) <= 2:
      if found == True: return -1
      found = True
      ans = left+1
      temp = s[0:i]
      temp += str(ans)
      temp += s[i:]
      s = temp
    elif (value-left)==1: pass
    else: return -1
  return ans
t = int(input())
for i in range(t):
  print(solution(input()))