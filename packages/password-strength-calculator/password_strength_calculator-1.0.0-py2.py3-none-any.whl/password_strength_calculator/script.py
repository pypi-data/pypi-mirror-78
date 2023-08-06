from nltk.corpus import words
from nltk.corpus import stopwords
wordlist = words.words()
stopwordlist = stopwords.words('english')
def ffu(x):
    y=x.lower()
    for j in stopwordlist:
        if(y==j.lower()):
            return(True)
    return(False)
wordlist.sort()
def fff(x):
    y=x.lower()
    for j in wordlist:
        if(y==j.lower()):
            return(True)
    return(False)



def score(password):    
    #password=input()
    keys=['length','unique_len','in_dictionary','special_chars','numbers','caseofletters','common_words']
    dict_score={'length':0, 'unique_len':0,'in_dictionary':0, 'special_chars':0, 'numbers':0, 'caseofletters':0,'common_words':0}
    score_coff={'length':5, 'unique_len':7,'in_dictionary':-7, 'special_chars':15, 'numbers':9, 'caseofletters':5, 'common_words':-7}
    dict_score['length']=len(password)

    if(fff(password)):
        dict_score['in_dictionary']+=len(password)
    d={}
    lo=0
    up=0
    for j in password:
        if(j not in d):
            dict_score['unique_len']+=1
            d[j]=1
        if(j.islower()):
            lo+=1
        if(j.isupper()):
            up+=1
        if(not j.isalnum()):
            dict_score['special_chars']+=1
        if(j.isnumeric()):
            dict_score['numbers']+=1
        
    dict_score['caseofletters']=min(lo,up)


    if(dict_score['in_dictionary']==0):
        i=0
        wordsss=[]
        ind=-1
        while(i<dict_score['length']):
            j=i+1
            flag=0
            while(j<=dict_score['length']):
                
                if((fff(password[i:j]) and j-i>3) or (ffu(password[i:j]) and j-i>2)):
                    if(flag==0):
                        wordsss.append(password[i:j])
                        flag=1
                    else:
                        wordsss[-1]=password[i:j]
                    
                    
                j+=1
            if(flag==1):
                i+=len(wordsss[-1])     
            else:
                i+=1 
        for t in wordsss:
            dict_score['common_words']+=len(t)
        
        
        #print(wordsss)

    score=0
    for k in keys:
        score+=dict_score[k]*score_coff[k]
    #print("score= ",score) 
    #print(dict_score)

    if(score<=50):
        ans="very weak"
    elif(score<=100):
       ans="weak"
    elif(score<=150):
        ans="neutral"
    elif(score<=200):
        ans="strong"
    else:
        ans="very strong"
    return(score,ans)


#score("iloveyou")