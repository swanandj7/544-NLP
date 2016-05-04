import os,string,pickle

stopwords=[]
vocab=set()
negativeDict={}
positiveDict={}
truthDict={}
fakeDict={}


def createStopwords():
    with open("stopwords.txt","r") as stopfile:
        stopwords= stopfile.readlines(1)
    stopwords=[x.strip('\n') for x in stopwords]
    return stopwords

def findClass(root):
    if 'negative' in root:
        if 'deceptive' in root:
            return [0,0]
        else:
            return [0,1]
    else:
        if 'deceptive' in root:
            return [1,0]
        else:
            return [1,1]
    return

def readFile(root,file):
        
    filename=root+'\\'+file
    inp=open(filename,"r")
    s=inp.readline()
    exclude=set(string.punctuation)
    s = ''.join(ch for ch in s if ch not in exclude)
    s = s.lower()
    s = ''.join(i for i in s if not i.isdigit()) 
    stopwords=createStopwords()
    s = ' '.join([word for word in s.split() if word not in stopwords])
    inp.close()
    return s.split()


def trainNB():
    global negativeCount
    global positiveCount
    global truthCount
    global fakeCount

    negativeCount=0
    positiveCount=0
    truthCount=0
    fakeCount=0


    for root, dirs, files in os.walk("op_spam_train"):
        if 'fold1' not in root:
            for file in files:
                if file.endswith('.txt') and file !='README.txt' :
                    labelClasses=findClass(root)
                    document=readFile(root,file)
                    for word in document:
                        vocab.add(word)
                        if labelClasses==[0,0]:
                            negativeCount+=1
                            fakeCount+=1        
                            if word in negativeDict:
                                count=negativeDict[word]
                                count+=1
                                negativeDict[word]=count
                            else:
                                negativeDict[word]=1
                         
                            if word in fakeDict:
                                 count=fakeDict[word]
                                 count+=1
                                 fakeDict[word]=count
                            else:
                                fakeDict[word]=1
                    
                        elif labelClasses==[0,1]:
                             negativeCount+=1
                             truthCount+=1        
                             if word in negativeDict:
                                 count=negativeDict[word]
                                 count+=1
                                 negativeDict[word]=count
                             else:
                                 negativeDict[word]=1
                             
                             if word in truthDict:
                                 count=truthDict[word]
                                 count+=1
                                 truthDict[word]=count
                             else:
                                 truthDict[word]=1
                     
                        elif labelClasses==[1,0]:
                             positiveCount+=1
                             fakeCount+=1        
                             if word in positiveDict:
                                 count=positiveDict[word]
                                 count+=1
                                 positiveDict[word]=count
                             else:
                                 positiveDict[word]=1
                             
                             if word in fakeDict:
                                 count=fakeDict[word]
                                 count+=1
                                 fakeDict[word]=count
                             else:
                                 fakeDict[word]=1
                        else:
                             positiveCount+=1
                             truthCount+=1        
                             
                             if word in positiveDict:
                                 count=positiveDict[word]
                                 count+=1
                                 positiveDict[word]=count
                             else:
                                 positiveDict[word]=1
                             
                             if word in truthDict:
                                 count=truthDict[word]
                                 count+=1
                                 truthDict[word]=count
                             else:
                                 truthDict[word]=1
    return
    
def writeModel():
    vocabList=list(vocab)
    model={}
    for word in vocab:
        classList=[]
        if word in negativeDict:
            prob=1.0*(negativeDict[word]+1)/(negativeCount+len(vocab))
        else:
            prob=1.0/(negativeCount+len(vocab))
        classList.append(prob)
        if word in positiveDict:
            prob=1.0*(positiveDict[word]+1)/(positiveCount+len(vocab))
        else:
            prob=1.0/(positiveCount+len(vocab))
        classList.append(prob)
        if word in fakeDict:
            prob=1.0*(fakeDict[word]+1)/(fakeCount+len(vocab))
        else:
            prob=1.0/(fakeCount+len(vocab))
        classList.append(prob)
        if word in truthDict:
            prob=1.0*(truthDict[word]+1)/(truthCount+len(vocab))
        else:
            prob=1.0/(truthCount+len(vocab))
        classList.append(prob)
        model[word]=classList
    vocabSize=len(vocab)
    with open('nbmodel.txt', 'wb') as handle:
      pickle.dump(model, handle)
    return

trainNB()
writeModel()