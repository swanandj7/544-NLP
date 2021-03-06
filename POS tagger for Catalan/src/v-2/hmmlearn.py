import string,pickle,math,sys
from collections import *
emissionMat=defaultdict(int)
transitionMat=defaultdict(int)
model=defaultdict(int)
tagCount=defaultdict(int)
content=[]
def readFile(file):
        
    filename=file
    with open(filename) as f:
    	content = f.readlines()
    return content


def train(content):
	for s in content:
		sentence=s.split()
		pointer=0
		for i in sentence:
			#transition
			tag=i.split('/')
			if pointer==0:
				temp='q0/'+tag[len(tag)-1]
				pointer=1
			else:
				temp=prev+'/'+tag[len(tag)-1]

						
										#if temp in transitionMat:
			try:
				transitionMat[temp]+=1	
			except KeyError:
				transitionMat[temp]=1
			prev=tag[len(tag)-1]			
			
			#emission
										#if i in emissionMat:
			try:
				emissionMat[i]+=1
			except KeyError:
				emissionMat[i]=1

										#if tag[len(tag)-1] in tagCount:
			try:				
				tagCount[tag[len(tag)-1]]+=1
			except KeyError:
				tagCount[tag[len(tag)-1]]=1
		
	for key in emissionMat:
		tag=key.split('/')
		count=int(tagCount.get(tag[len(tag)-1]))
		value=int(emissionMat.get(key))
		newValue=float(value)/count
		emissionMat[key]=newValue
	
	for key1 in tagCount:
		temp1='q0/'+key1
		if temp1 not in transitionMat:
			transitionMat[temp1]=1	
		for key2 in tagCount:
			temp=key1+'/'+key2
			if temp not in transitionMat:
				transitionMat[temp]=1	

	for key in transitionMat:
		tag=key.split('/')
		value=int(transitionMat.get(key))
		if tag[0]=='q0':
			newValue=float(value)/len(content)
		else:
			count=int(tagCount.get(tag[0]))
			if tag[0]=='FF':			
				count=count-len(content)
			newValue=float(value)/count	
		
		transitionMat[key]=newValue
	
	 	
	return emissionMat,transitionMat

content=readFile('/home/swanand/hmm-post/catalan_corpus_train_tagged.txt')
#content=readFile('/home/swanand/hmm-post/sample.txt')
#content=readFile(sys.argv[1])
train(content)
print str(len(transitionMat))
print str(len(emissionMat))
model.update(transitionMat)
model.update(emissionMat)
print str(len(model))
with open('hmmmodel.txt', 'wb') as handle:
      pickle.dump(model, handle)
with open('tagCount.txt', 'wb') as handle:
      pickle.dump(tagCount, handle)
