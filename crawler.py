import parse_functions
import os_functions
import os
import webdev

def crawl(seed): #seed is url that you start from
    if webdev.read_url(seed) == "":
        return print("This is not a valid URL")
        
    if os_functions.directory_check("search_results") == False:
        os_functions.directory_gen("search_results")
    
    directories = os.listdir("search_results")
    for i in directories:
        os_functions.directory_delete(os.path.join("search_results",i))
    
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
    
    while len(queue) > 0:
        url = queue.pop()
        title = parse_functions.find_title(url)
        contents = parse_functions.page_contents(url)
        filepath = os.path.join("search_results",title)
        os_functions.directory_gen(filepath)
        os_functions.file_gen(filepath,"page_address.txt",url)
        for key in contents:
            os_functions.file_gen(filepath,key + ".txt",contents[key])
        references = parse_functions.reference_gen(url)
        
        for link in references:
            if not os.path.exists(os.path.join(filepath,"outgoing_links.txt")):
                os_functions.file_gen(filepath,"outgoing_links.txt",link)
            else:
                filein = open(os.path.join(filepath,"outgoing_links.txt"),"a")
                filein.write(link + "\n")
                filein.close()
        totalpages += 1
    return totalpages

print(crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))
