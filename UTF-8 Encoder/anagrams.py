import sys

def main():
    text1=str(sys.argv[1])
    text=list(text1)
    text.sort(cmp=None, key=None, reverse=False)
    anagram(text,0)
    printlist.sort(cmp=None, key=None, reverse=False)
   # print printlist
    for x in printlist:
        f.write(x+'\n')
    
def anagram(text,index):
    if index == len(text)-1:
        str1 = ''.join(text)
        #print str1
        printlist.append(str1)
    for x in range(index,len(text)):
        temp=text[index]
        text[index]=text[x]
        text[x]=temp
        anagram(text,index+1)
        temp=text[index]
        text[index]=text[x]
        text[x]=temp
    return
f = open('anagram_out.txt','w')
printlist = []
main()