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
        crawl.close()
        for title in titles:
            tfidf[title] = {}
            #filein = open(os.path.join("search_results",title,"page_address.txt"),"r")
            #address = filein.read().strip()
            #filein.close()
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
            if idf < 0:
                continue
            else:
                qvector[word] = math.log2(1+tf)*idf
        cosine = []
        denq = 0
        for searchword in qvector:
            denq += qvector[searchword]*qvector[searchword]
        for title in titles:
            filein = open(os.path.join("search_results",title,"page_address.txt"),"r")
            address = filein.read().strip()
            filein.close()
            filein = open(os.path.join("search_results",title,"page_rank.txt"),"r")
            pagerank = float(filein.read().strip())
            filein.close()
            num = 0
            dend = 0
            for searchword in qvector:
                if searchword in tfidf[title]:
                    num += float(qvector[searchword])*float(tfidf[title][searchword])
                    dend += float(tfidf[title][searchword])*float(tfidf[title][searchword])
            if num == 0:
                cosine.append({"url": address,  "title": title,"score" :0})
            elif boost == "True":
                cosine.append({"url":address, "title": title, "score": num*pagerank/(math.sqrt(denq)*math.sqrt(dend))})
            else:
                cosine.append({"url":address, "title": title, "score": num/(math.sqrt(denq)*math.sqrt(dend))})
        sortedcosine = []
        while len(cosine) > 0:
            largest = cosine[0]
            for i in range(len(cosine)):
                if cosine[i]["score"] > largest["score"]:
                    largest = cosine[i]
            sortedcosine.append(largest)
            cosine.remove(largest)
        return sortedcosine[0:10]
    else:
        return print("you have not put in a proper value for boost")

start = time.time()
print(search("tomato peach tomato pear banana tomato peach tomato","True"))
end = time.time()
print(end-start)