import os,string,pickle,math,sys
import collections
model={}
tagCount={}
content=[]
retSeq=''
def readFile(inp):
        
    filename=inp
    with open(filename) as f:
    	content = f.readlines()
    return content

def readModel():
    with open('hmmmodel.txt', 'rb') as handle:
        model = pickle.loads(handle.read())
    with open('tagCount.txt', 'rb') as handle:
        tagCount = pickle.loads(handle.read())
    
    return model
def readTag():
    with open('tagCount.txt', 'rb') as handle:
        tagCount = pickle.loads(handle.read())
    
    return tagCount



def viterbi(s): 
	prob={}
	back={}
	t=1
	words=s.split()
	for word in words:
		for key in tagCount:
			emitIndex=word+'/'+key
			index=key+'/'+str(t)
			if t==1:
				transIndex='q0/'+key
				if emitIndex in model:
					prob[index]=model[transIndex]*model[emitIndex]
				else:
					prob[index]=model[transIndex]*0.01782
				back[index]='q0/0'			
			else:
				maxProb=0
				maxKey='null'
				for key2 in tagCount:
					prevTime=str(t-1)
					checkKey=key2+'/'+prevTime					
					if maxProb< prob[checkKey]:
						maxProb=prob[checkKey]
						maxKey=checkKey
				
				maxKeyIndex=maxKey.split('/')					
				transIndex=maxKeyIndex[0]+'/'+key
				if emitIndex in model:
					prob[index]=model[transIndex]*model[emitIndex]
				else:
					prob[index]=model[transIndex]*0.01782
								 
				back[index]=maxKey
				
		#termination
		if t == len(words):
			#print back
			maxProb=0
			maxKey='null'
			for key2 in tagCount:
				prevTime=t
				checkKey=key2+'/'+str(prevTime)					
				if maxProb< prob[checkKey]:
					maxProb=prob[checkKey]
					maxKey=checkKey
			finalTime=str(t)	
			maxKeyList=maxKey.split('/')
			mostProbableState=maxKeyList[0]		
		t=t+1
	#backpointers
	t-=1	
	while t!=0:
		index=mostProbableState+'/'+finalTime
		words[t-1]=words[t-1]+'/'+mostProbableState
		nextState=back[index]
		nextStateList=nextState.split('/')
		mostProbableState=nextStateList[0]
		finalTime=nextStateList[1]
		t=t-1
	seq=' '.join(words)
	return seq 	

#content=readFile('/home/swanand/hmm-post/catalan_corpus_dev_raw.txt')
content=readFile(sys.argv[1])
model=readModel()
tagCount=readTag()
print model['Un/DI']
out = open("/home/swanand/hmm-post/hmmout.txt", "w")
for s in content:
	seq=viterbi(s)
	out.write(seq+'\n')

out.close()	

