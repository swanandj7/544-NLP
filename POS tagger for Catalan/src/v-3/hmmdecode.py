import string,json,math,sys
from collections import defaultdict	
tagCount=defaultdict(int)
em={}
tm={}
content=[]
def readFile(file):
        
    filename=file
    with open(filename) as f:
    	content = f.readlines()
    return content

def readModel():
    with open('hmmmodel.txt', 'rb') as handle:
        data = json.loads(handle.read())
    return data

prob={}
back={}
	
def viterbi(s): 
	prob={}
	back={}
	t=1
	words=s.split()
	for word in words:
		prob[str(t)]={}
		back[str(t)]={}
		#word.replace('/','')
		word = unicode(word, "utf-8")
		#print word
		if word in em:
			for tag in em[word]:
				if tag=='q0':
					#print 'breaking'
					continue
				if t==1:
					prob[str(t)][tag]=tm['q0'][tag]*em[word][tag]
					back[str(t)][tag]='q0'
				else:
					maxP=0
					maxTag=None				
					for prevTag in prob[str(t-1)]:
						checkP=prob[str(t-1)][prevTag]*tm[prevTag][tag]*em[word][tag]
						if maxP<=checkP:
							maxP=checkP
							maxTag=prevTag
				
					prob[str(t)][tag]=maxP
					back[str(t)][tag]=maxTag				
		else:	
			#print 'came here'	
			for tag in states:
				if tag=='q0':
					#print 'breaking'
					continue
				if t==1:
					prob[str(t)][tag]=tm['q0'][tag]
					back[str(t)][tag]='q0'
				else:
					maxP=0
					maxTag=None				
					for prevTag in prob[str(t-1)]:
						checkP=prob[str(t-1)][prevTag]*tm[prevTag][tag]
						if maxP<=checkP:
							maxP=checkP
							maxTag=prevTag
				
					prob[str(t)][tag]=maxP
					back[str(t)][tag]=maxTag
		#termination
		if t==len(words):
			maxP=int(0)
			mostLikeyTag=None				
			for prevTag in prob[str(t)]:
				checkP=prob[str(t)][prevTag]
				if maxP<=checkP:
					maxP=checkP
					mostLikeyTag=prevTag
		t+=1
					   
	t-=1
	while t!=0:
		#print words[t-1]+" "+str(mostLikeyTag)
		words[t-1]=str(words[t-1])+'/'+str(mostLikeyTag)		
		mostLikeyTag=back[str(t)][str(mostLikeyTag)]
		t-=1
	seq=' '.join(words)
	return seq 	


content=readFile('/home/swanand/hmm-post/catalan_corpus_dev_raw.txt')
#content=readFile('/home/swanand/hmm-post/tryTest.txt')
#content=readFile(sys.argv[1])
data=readModel()
em=data['EM']
tm=data['TM']
#print em
states=list(tm.keys())
file = open("/home/swanand/hmm-post/hmmoutput.txt", "w")
for s in content:
	#print s
	seq=viterbi(s)
	#print seq
	file.write(seq+'\n')

file.close()	

