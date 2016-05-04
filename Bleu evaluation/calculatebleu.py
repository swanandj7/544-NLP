import sys,string,os
from collections import Counter
import math
from itertools import tee, islice
content=[]
def ngrams(lst, n):
  tlst = lst
  while True:
    a, b = tee(tlst)
    l = tuple(islice(a, n))
    if len(l) == n:
      yield l
      next(b)
      tlst = b
    else:
      break

def readFile(file):
    content2=[]
    filename=file
    with open(filename) as f:
    	content = f.readlines()
    #for line in content:
    #	line=line.strip("\n").strip()
    #	content2.append(line)
    	
    return content

candi_path="candidate-4.txt"
candi_content=readFile(candi_path)
c_length=0
r_lengths=[]
for line in candi_content:
	c_length+=len(line.split())
all_map={}
flag=1;
ref_path="/home/swanand/blue-score/ref"
if ".txt" in ref_path:
	ref_content=readFile(ref_path)
	for i in range(0,len(candi_content)):
		all_map[candi_content[i]]=[]
		all_map[candi_content[i]].append(ref_content[i])
		r_length=0
		for line in ref_content:
			r_length+=len(line.split())
	r_lengths.append(r_length)
else:
	for root, dirs, files in os.walk(ref_path):
	            for file in files:
	            	print root+'/'+file
	            	ref_content=readFile(root+'/'+file)
	            	r_length=0
	            	for line in ref_content:
	            		r_length+=len(line.split())
	            	r_lengths.append(r_length)
	            	for i in range(0,len(candi_content)):
	            		if flag==1:
	            			all_map[candi_content[i]]=[]
	            			all_map[candi_content[i]].append(ref_content[i])
	            		else:
	            			temp=all_map[candi_content[i]]
	            			temp.append(ref_content[i])
	            			all_map[candi_content[i]]=temp
	            	flag=0

def bleu(n):
	numerator =0
	denominator=0
	for line in candi_content:
		candi_wordList=line.split()
		candi_map=Counter(ngrams(candi_wordList, n))
		#print candi_map
		if len(candi_map)==0:
			continue
		max_counts={}
		clipped_counts={}
		ref_content=all_map[line]
		for ref in ref_content:
			ref_wordList=ref.split()
			ref_map=Counter(ngrams(ref_wordList, n))
			for key in ref_map:
				if key in max_counts:
					max_counts[key]=max(max_counts[key],ref_map[key])
				else:
					max_counts[key]=ref_map[key]
		print max_counts
		for key in candi_map:

			if key not in max_counts:
				clipped_counts[key]=0
			else:
				clipped_counts[key]=min(candi_map[key],max_counts[key])
		print sum(	clipped_counts.values())
		numerator+=sum(clipped_counts.values())
		denominator+=sum(candi_map.values())
	#print "Final bleu for ",n," gram is: ", 1.0*numerator/denominator
	#print "N: ",numerator
	#print "D: ", denominator
	return 1.0*numerator/denominator


p1=bleu(1)
p2=bleu(2)
p3=bleu(3)
p4=bleu(4)
r=0

for key in all_map:
	clength=len(key.split())
	tempList=all_map[key]
	minDiff=sys.maxint
	for eachR in tempList:
		check=len(eachR.split())
		str1=""
		if abs(check-clength)<minDiff:
			minDiff=abs(check-clength)
			minR=check
			str1=eachR
#	print str1
#	print clength,minR
	r+=minR
c=c_length
print r,c
BP=0
if c>r:
	BP=1
else:
	BP=math.exp(1-1.0*r/c)
weights=[0.25,0.25,0.25,0.25]
p_array=[p1,p2,p3,p4]
#print p_array
pn=sum(w * math.log(p_n) for w, p_n in zip(weights, p_array))
pn=BP*math.exp(pn)
print BP,"  ",pn
output=open("bleu_out.txt",'w')
output.write(str(pn))
output.close()