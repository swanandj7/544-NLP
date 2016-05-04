import os,string,pickle,math,sys

emissionMat={}
transitionMat={}
tagCount={}
content=[]
def readFile(file):
        
    filename=file
    with open(filename) as f:
    	content = f.readlines()
    return content


def train(content):
	file = open("/home/swanand/HMM-post/tags.txt", "w")
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

						
			if temp in transitionMat:
				count=int(transitionMat.get(temp))
				transitionMat[temp]=count+1	
			else:
				transitionMat[temp]=1
			prev=tag[len(tag)-1]			
			
			#emission
			if i in emissionMat:
				count=int(emissionMat.get(i))
				emissionMat[i]=count+1
			else:
				emissionMat[i]=1

			if tag[len(tag)-1] in tagCount:
				count=int(tagCount.get(tag[len(tag)-1]))
				tagCount[tag[len(tag)-1]]=count+1
			else:
				tagCount[tag[len(tag)-1]]=1
		
	for key in emissionMat:
		tag=key.split('/')
		count=int(tagCount.get(tag[len(tag)-1]))
		#print 'Count for '+tag[0]+': '+str(count)		
		value=int(emissionMat.get(key))
		#print 'Value before for '+key+': '+str(value)		
		newValue=float(value)/count
		emissionMat[key]=newValue
		#print 'Value after for '+key+': '+str(newValue)		
	
	for key in transitionMat:
		tag=key.split('/')
		value=int(transitionMat.get(key))
		file.write(key + ': '+ str(value)+'\n')

		#print key + ': '+ str(value)
	
		if tag[0]=='q0':
			newValue=float(value)/len(content)
		else:
			count=int(tagCount.get(tag[0]))
			if tag[0]=='FF':			
				count=count-len(content)
			newValue=float(value)/count	
		
		transitionMat[key]=newValue
	
	file.close()
	return emissionMat,transitionMat

content=readFile('/home/swanand/HMM-post/catalan_corpus_train_tagged.txt')
#content=readFile('/home/swanand/HMM-post/try.txt')
train(content)
print(len(transitionMat))
print(len(emissionMat))


