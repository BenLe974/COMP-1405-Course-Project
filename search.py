import searchdata
import os
import math
import crawler

def search(phrase,boost):
    if boost == True or boost == False:
        query = phrase.split()
        tfidf = {}
        crawl = open("words_found.txt","r")
        titles = os.listdir("search_results")
        keys = crawl.read().strip().split()
        crawl.close()
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
            elif boost == True:
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

def search_menu():
    choice = ""
    seed = input("Please provide a seed link to start the crawl at: ")
    print("Please wait for the crawl to finish")
    pagecount = crawler.crawl(seed)
    print("The crawl visited " + str(pagecount) + " pages")
    while choice != "q":
        print("")
        print("")
        print("1. Get outgoing links for the link entered.")
        print("2. Get incoming links for the link entered.")
        print("3. Get the page rank for the link entered.")
        print("4. Get the idf value for the word entered.")
        print("5. Get the tf value for the word entered in the document.")
        print("6. Get the tfidf value for the word entered in the document.")
        print("7. Do a search on the cached documents.")
        choice = input("Please choose an option from the list. Enter q to quit: ")
        if choice == "1":
            link = input("Please input the link you would like to find the outgoing links for: ")
            print("")
            print(searchdata.get_outgoing_links(link))
        elif choice == "2":
            link = input("Please input the link you would like to find the incoming links for: ")
            print("")
            print(searchdata.get_incoming_links(link))
        elif choice == "3":
            link = input("Please input the link you would like to find the page rank for: ")
            print("")
            print(searchdata.get_page_rank(link))
        elif choice == "4":
            word = input("Please input the word you would like to find the idf value for: ")
            print("")
            print(searchdata.get_idf(word))
        elif choice == "5":
            word = input("Please input the word you would like to find the tf value for: ")
            link = input("Please input the link you would like to find the tf value for the given word: ")
            print("")
            print(searchdata.get_tf(link,word))
        elif choice == "6":
            word = input("Please input the word you would like to find the tfidf value for: ")
            link = input("Please input the link you would like to find the tfidf value for the given word: ")
            print("")
            print(searchdata.get_tf_idf(link,word))
        elif choice == "7":
            phrase = input("Please input your search query, with every word separated by spaces: ")
            boost = input("Would you like to boost the search with page rank values? Enter T to boost or F to not: ")
            if boost == "F":
                print("")
                print("Here are the top ten links for your search query")
                print(search(phrase,False))
            elif boost == "T":
                print("")
                print("Here are the top ten links for your search query")
                print(search(phrase,True))
            else:
                print("That's not a valid boost option")

#search_menu()
