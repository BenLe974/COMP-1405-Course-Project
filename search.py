import searchdata
import os
import math
import time

def search(phrase,boost):
    if boost == "True" or boost == "False":
        query = phrase.split()
        tfidf = {}
        crawl = open("words_found.txt","r")
        titles = os.listdir("search_results")
        keys = crawl.read().strip().split()
        for title in titles:
            tfidf[title] = {}
            pageweights = open(os.path.join("search_results",title,"tfidf.txt"),"r")
            values = pageweights.read().strip().split()
            n=0
            for key in keys:
                tfidf[title][key] = values[n]
                n +=1
        qvector = {}
        for word in query:
            tf = query.count(word)/len(query)
            idf = searchdata.get_idf(word)
            qvector[word] = math.log2(1+tf)*idf
        cosine = []
        denq = 0
        for searchword in qvector:
            denq += qvector[searchword]*qvector[searchword]
        for title in titles:
            filein = open(os.path.join("search_results",title,"page_address.txt"),"r")
            address = filein.read().strip()
            filein.close()
            num = 0
            dend = 0
            for searchword in qvector:
                if searchword in tfidf[title]:
                    num += float(qvector[searchword])*float(tfidf[title][searchword])
                    dend += float(tfidf[title][searchword])*float(tfidf[title][searchword])
            if num == 0:
                cosine.append(str(0) + " " +address)
            else:
                cosine.append(str(num/(math.sqrt(denq)*math.sqrt(dend))) + " " + address)
        sortedcosine = []
        while len(cosine) > 0:
            largest = cosine[0]
            for i in range(len(cosine)):
                if cosine[i] > largest:
                    largest = cosine[i]
            sortedcosine.append(largest)
            cosine.remove(largest)
        return sortedcosine[0:9]
    else:
        return print("you have not put in a proper value for boost")

start = time.time()
print(search("apple peach apricot","True"))
end = time.time()
print(end-start)