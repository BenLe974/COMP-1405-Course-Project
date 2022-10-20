import parse_functions
import os_functions
import os
import webdev
import searchdata

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
    for i in queue:
        ref = parse_functions.reference_gen(i)
        for j in ref:
            if j in queue:
                continue
            else:
                queue.append(j)
    
    unique = []
    while len(queue) > 0:
        url = queue.pop()
        title = parse_functions.find_title(url)
        contents = parse_functions.page_contents(url)
        filepath = os.path.join("search_results",title)
        os_functions.directory_gen(filepath)
        os_functions.file_gen(filepath,"page_address.txt",url)
        for key in contents:
            os_functions.file_gen(filepath,key + ".txt",contents[key])
            if key not in unique:
                unique.append(key)
        references = parse_functions.reference_gen(url)
        
        for link in references:
            if not os.path.exists(os.path.join(filepath,"outgoing_links.txt")):
                os_functions.file_gen(filepath,"outgoing_links.txt",link)
            else:
                filein = open(os.path.join(filepath,"outgoing_links.txt"),"a")
                filein.write(link + "\n")
                filein.close()
        length = 0
        for key in contents:
            length += contents[key]
        os_functions.file_gen(filepath,"doc_length.txt",length)
        totalpages += 1
    

    titles = os.listdir("search_results")
    for name in titles:
        filepath = os.path.join("search_results",name)
        os_functions.file_gen(filepath,"tfidf.txt","")
        clear = open(os.path.join(filepath,"tfidf.txt"),"w")
        clear.close()
        for word in unique:
            fileopen = open(os.path.join(filepath,"tfidf.txt"),"a")
            page = open(os.path.join(filepath,"page_address.txt"),"r")
            fileopen.write(str(searchdata.get_tf_idf(page.read().strip(),word))+"\n")
            page.close()
            fileopen.close()

    os_functions.file_gen("search_results","words_found.txt",unique[0])
    found = open(os.path.join("search_results","words_found.txt"),"a")
    for i in range(1,len(unique)-1):
        found.write(unique[i] + "\n")
    found.close()
    return totalpages

print(crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))
