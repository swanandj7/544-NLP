import string,json,math,sys
from collections import *
import codecs
emissionMat={}
transitionMat={}
tagCount={}
content=[]
def readFile(file):
        
    filename=file
    with codecs.open(filename,'r',encoding='utf8') as f:
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
				first='q0'
				pointer=1
			else:
				first=prev

			second=tag[len(tag)-1]

			if transitionMat.has_key(first):
				tagCount[first]+=1				
				if  transitionMat[first].has_key(second):
					transitionMat[first][second]+=1	
				else:
					transitionMat[first][second]=1	
			else:
				tagCount[first]=1				
				transitionMat[first]={}
				transitionMat[first][second]=1
			prev=second			
			
			#emission

			word=' '.join(tag[0:len(tag)-1])
			word=word.replace(' ','/')		
			if emissionMat.has_key(word):
				if emissionMat[word].has_key(second):				
					emissionMat[word][second]+=1
				else:
					emissionMat[word][second]=1
			else:
				emissionMat[word]={}
				emissionMat[word][second]=1

	for key in emissionMat:
		for key2 in emissionMat[key]:
			count=tagCount[key2]
			if key2 =='FF':	
				count+=len(content)
			value=emissionMat[key][key2]
			newValue=float(value)/count
			emissionMat[key][key2]=newValue

	for key1 in tagCount:
		for key2 in tagCount:
			if key2!='q0':			
				if  key2 not in transitionMat[key1]:
					transitionMat[key1][key2]=1
				else:
					transitionMat[key1][key2]+=1
		tagCount[key1]+=len(tagCount)-1

		
	for key in transitionMat:
		for key2 in transitionMat[key]:
			count=tagCount[key]
			value=transitionMat[key][key2]
			newValue=float(value)/count
			transitionMat[key][key2]=newValue
		
	return emissionMat,transitionMat

content=readFile('/home/swanand/hmm-post/catalan_corpus_train_tagged.txt')
#content=readFile('/home/swanand/hmm-post/sample.txt')
#content=readFile(sys.argv[1])
train(content)
with codecs.open('hmmmodel.txt','w',encoding='utf8') as handle:
      	data={'EM':emissionMat,'TM':transitionMat}
	json.dump(data, handle)
