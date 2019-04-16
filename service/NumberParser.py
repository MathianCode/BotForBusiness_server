A={"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10}
B={"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19}
C={"twenty":20,"thirty":30,"fourty":40,"fifty":50,"sixty":60,"seventy":70,"eighty":80,"ninty":90}
D={"hundred":100,"thousand":1000,"lakh":100000,"crore":10000000,"million":1000000,"billion":1000000000,"trillion":1000000000000}
#sentence = "three hundred thirty nine"
#sentence="twenty ten"
#sentence="twenty ten"
#sentence="hundred billion two hundred fifty million five hundred sixty thousand seven hundred thirteen"
#100,250,560,713
#25,05,60,713
#100,050,061,413
#sentence="nineteen lakh eighty five thousand"
#sentence="one lakh thirty nine thousand four hundred fourty nine"
patterns={"CD":"*","CA":"+","AD":"*","BD":"*","CAD":"+*","A":"","B":"","C":"","D":""}
def isthere(regex):
  if regex in patterns:
    return True
  return False
def findValue(numbers,regex,pos,sentence):
  if(regex=="CD") or regex=="AD" or regex=="BD":
    return numbers[0]*numbers[1]
  elif(regex=="CA"):
    if(numbers[1]==10 and pos==len(sentence.split(' '))):
      return int(str(numbers[0])+str(numbers[1]))
    return numbers[0]+numbers[1]
  elif(regex=="CAD"):
    return (numbers[0]+numbers[1])*numbers[2]
  else:
    return numbers[0]
def getValue(numbers,found,val,types,pos,prev,sentence):
  #print(types,numbers,pos)
  if found[len(found)-1]=="D":
    if(len(found)==1):
      if val==0:
        val=1
      return val*findValue(numbers,found,pos,sentence)
    val=val+findValue(numbers,found,pos,sentence)
  else:
    if pos==len(sentence.split(' ')):
      #print("came")
      if(types=="B" or types=="C"):
        if(prev[len(prev)-1]=="D"):
          val=val+findValue(numbers,found,pos,sentence)
        else:
          val=int(str(val)+str(findValue(numbers,found,pos,sentence)))
      else:
        if(prev[len(prev)-1]=="D"):
          val=val+findValue(numbers,found,pos,sentence)
        else:
          val=int(str(val)+str(findValue(numbers,found,pos,sentence)))
    else:
      val=int(str(val)+str(findValue(numbers,found,pos,sentence)))
  return val
def numberParser(sentence):
  found=str()
  numbers=list()
  val=0
  pos=0
  last=""
  prev=" "
  for i in sentence.split(" "):
    if i in A:
      last="A"
      if len(found)==0:
        found=found+"A"
        numbers.append(A[i])
      else:
        if isthere(found+"A"):
          found=found+"A"
          numbers.append(A[i])
        else:
          val=getValue(numbers,found,val,"A",pos,prev,sentence)
          prev=found
          found="A"
          numbers=list()
          numbers.append(A[i])
    if i in B:
      last="B"
      if len(found)==0:
        found=found+"B"
        numbers.append(B[i])
      else:
        if isthere(found+"B"):
          found=found+"B"
          numbers.append(B[i])
        else:
          val=getValue(numbers,found,val,"B",pos,prev,sentence)
          prev=found
          found="B"
          numbers=list()
          numbers.append(B[i])
    if i in C:
      last="C"
      if len(found)==0:
        found=found+"C"
        numbers.append(C[i])
      else:
        if isthere(found+"C"):
          found=found+"C"
          numbers.append(C[i])
        else:
          val=getValue(numbers,found,val,"C",pos,prev,sentence)
          prev=found
          found="C"
          numbers=list()
          numbers.append(C[i])
    if i in D:
      last="D"
      if len(found)==0:
        found=found+"D"
        numbers.append(D[i])
      else:
        if isthere(found+"D"):
          found=found+"D"
          numbers.append(D[i])
        else:
          val=getValue(numbers,found,val,"D",pos,prev,sentence)
          prev=found
          found="D"
          numbers=list()
          numbers.append(D[i])
    pos=pos+1
  val=getValue(numbers,found,val,last,pos,prev,sentence)
  print(val)
  return val
#numberParser(sentence)