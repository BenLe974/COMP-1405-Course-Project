import parse_functions
import os_functions
import os
import webdev
import searchdata
import matmult
import math

def crawl(seed): #seed is url that you start from
    if webdev.read_url(seed) == "":
        return print("This is not a valid URL")
        
    if os_functions.directory_check("search_results") == False:
        os_functions.directory_gen("search_results")
    
    directories = os.listdir("search_results")
    for i in directories:
        os_functions.directory_delete(os.path.join("search_results",i))
    os_functions.file_delete("search_results","words_found.txt")
    totalpages = 0
    queue = parse_functions.reference_gen(seed)
    queue.append(seed)
  
                
    
    unique = []
    for i in queue:
        url = i
        title = parse_functions.find_title(url)
        contents = parse_functions.page_contents(url)
        filepath = os.path.join("search_results",title)
        os_functions.directory_gen(filepath)
        os_functions.file_gen(filepath,"page_address.txt",url)
        length = 0
        for key in contents:
            length += contents[key]
        os_functions.file_gen(filepath,"doc_length.txt",length)
        for key in contents:
            os_functions.file_gen(filepath,key + ".txt",contents[key]/length)
            if key not in unique:
                unique.append(key)
        references = parse_functions.reference_gen(url)
        
        filein = open(os.path.join(filepath,"outgoing_links.txt"),"w")
        for link in references:  
            filein.write(link + "\n")
            if link not in queue:
                queue.append(link)
        filein.close()
        totalpages += 1
   

    found = open("words_found.txt","w")
    idfs = open("idf.txt","w")
    for i in range(len(unique)):
        found.write(unique[i] + "\n")
        idfs.write(str(searchdata.get_idf(unique[i]))+"\n")
    found.close()
    idfs.close()
    
   
    titles = os.listdir("search_results")
    filein = open("idf.txt","r")
    idfs = filein.read().strip().split()
    filein.close()
    for name in titles:
        filepath = os.path.join("search_results",name)
        fileopen = open(os.path.join(filepath,"tfidf.txt"),"w")
        
        for word in unique:
            if os.path.exists(os.path.join(filepath, word + ".txt")):
                page = open(os.path.join(filepath, word + ".txt"),"r")
                tf = float(page.read().strip())
                page.close()
            else:
                tf = 0
            fileopen.write(str(math.log2(1+ tf)*float(idfs[unique.index(word)]))+"\n")  
            
        fileopen.close()
   
    
    
    probmatrix = []
    index = 0
    alpha = 0.1
    for title in titles:
        address = open(os.path.join("search_results",title,"page_address.txt"),"r")
        link = address.read().strip()
        address.close()
        row = []
        count = 0
        for i in titles:
            outgoing = open(os.path.join("search_results",i,"outgoing_links.txt"),"r")
            if link in outgoing.read().strip().split():
                row.append(1)
                count += 1
            else:
                row.append(0)
        for i in range(totalpages):
            row[i] = (row[i]/count)*(1-alpha)+(alpha/totalpages)

        probmatrix.append(row)
        outgoing.close()
        index +=1
    t = [1/totalpages] * totalpages
    tprime = matmult.mult_matrix(t,probmatrix)
    euclidist = float(matmult.euclidean_dist(t,tprime))
    while euclidist > 0.0001:
        t = tprime
        tprime = matmult.mult_matrix(t,probmatrix)
        euclidist = float(matmult.euclidean_dist(t,tprime))
    t = tprime

    for i in range(totalpages):
        os_functions.file_gen(os.path.join("search_results",titles[i]),"page_rank.txt",t[i])
    return totalpages

