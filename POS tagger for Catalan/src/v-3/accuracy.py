import string,pickle,math,sys
content_test=[]
content_op=[]

def readFile(file):
        
    filename=file
    with open(filename) as f:
    	content = f.readlines()
    return content


content_test=readFile('/home/swanand/hmm-post/catalan_corpus_dev_tagged.txt')
content_op=readFile('/home/swanand/hmm-post/hmmoutput.txt')
print 'length of content: '+ str(len(content_test)) 
total=0
correct=0
count=0

while count!=len(content_test):
	sentence1=content_test[count].split()
	#print sentence1 
	sentence2=content_op[count].split()
	#print sentence2
	senLength=0	
	while senLength!=len(sentence1):
		total+=1		
		tag1=sentence1[senLength].split('/')
		#print tag1[len(tag1)-1]		
		tag2=sentence2[senLength].split('/')
		#print tag2[len(tag2)-1]		
		if tag1[len(tag1)-1]==tag2[len(tag2)-1]:
			correct+=1
		else:
			print 'tag1:'+str(tag1) + 'tag2:'+ str(tag2) 		
		senLength+=1
	count+=1
print 'Correct: '+str(correct)+' TOtal: '+str(total)
acc=(correct*1.0)/total
print str(acc)
