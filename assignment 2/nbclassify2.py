import os,string,pickle,math,sys

stopwords=[]
vocab=set()

def createStopwords():
    with open("stopwords.txt","r") as stopfile:
        stopwords= stopfile.readlines(1)
    stopwords=[x.strip('\n') for x in stopwords]
    return stopwords

def readModel():
    with open('nbmodel.txt', 'rb') as handle:
        model = pickle.loads(handle.read())
    return model

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

def NBtest():
    model=readModel()
    output= open("nboutput.txt","w")
    for root, dirs, files in os.walk("op_spam_train"):
        if 'fold1' in root:
            for file in files:
                if file.endswith('.txt') and file !='README.txt' :
                    document=readFile(root,file)
                    score1=score2=score3=score4=0
                    for word in document:
                        if word in model:
                            score1+=math.log(model[word][0])
                            score2+=math.log(model[word][1])
                            score3+=math.log(model[word][2])
                            score4+=math.log(model[word][3])
                    if score3> score4:
                        output.write('deceptive ')
                    else:
                        output.write('truthful ')    
                    if score1> score2:
                        output.write('negative ')
                    else:
                        output.write('positive ')
                    filename=root+'\\'+file
                    output.write(filename)
                    output.write('\n')
    output.close()
    return 

NBtest()