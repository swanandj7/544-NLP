import os,string,pickle,math

model={}
tagCount={}
content=[]
def readFile(file):
        
    filename=file
    with open(filename) as f:
    	content = f.readlines()
    return content


def train(content):
	for s in content:
		#print len(content)		
		#print 'in content'		
		sentence=s.split()
		pointer=0
		for i in sentence:
			#print 'in sentence'
			tag=i.split('/')
#transition
			if pointer==0:
				temp='q0/'+tag[1]
				pointer=1
			else:
				temp=prev+'/'+tag[1]

						
			if temp in model:
				count=int(model.get(temp))
				model[temp]=count+1	
			else:
				model[temp]=1
			#print temp+': '+str(model[temp])			
			prev=tag[1]			
#emission
			if i in model:
				count=int(model.get(i))
				model[i]=count+1
			else:
				model[i]=1

			if tag[1] in tagCount:
				count=int(tagCount.get(tag[1]))
				tagCount[tag[1]]=count+1
			else:
				tagCount[tag[1]]=1
		
	for key in model:
		tag=key.split('/')
		count=int(tagCount.get(tag[1]))
		#print 'Count for '+tag[1]+': '+str(count)		
		value=int(model.get(key))
		#print 'Value before for '+key+': '+str(value)		
		newValue=float(value)/count
		model[key]=newValue
		#print 'Value after for '+key+': '+str(newValue)		
	
	for key in model:
		tag=key.split('/')
		value=int(model.get(key))
		print key + ': '+ str(value)
	
		if tag[0]=='q0':
			newValue=float(value)/len(content)
		else:
			count=int(tagCount.get(tag[0]))
			if tag[0]=='FF':			
				count=count-len(content)
			newValue=float(value)/count	
		
		model[key]=newValue
	
	return model

content=readFile('/home/swanand/HMM-post/catalan_corpus_train_tagged.txt')
#content=readFile('/home/swanand/HMM-post/try.txt')
train(content)

