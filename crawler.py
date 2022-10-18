import parse_functions
import os_functions
import os

def crawl(seed): #seed is url that you start from
    
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
        os_functions.directory_gen(os.path.join("search_results",title))
        for key in contents:
            os_functions.file_gen(os.path.join("search_results",title),key,contents[key])
        totalpages += 1
    return totalpages

print(crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))
