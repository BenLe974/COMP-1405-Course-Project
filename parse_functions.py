import webdev

def find_title(url): #title finder
    contents = webdev.read_url(url)
    split1 = contents.split("<title>")
    split2 = split1[1].split("</title>")
    title = split2[0]
    return title

def page_contents(url):
    contents = webdev.read_url(url)
    split1 = contents.split("<p>")
    split2 = split1[1].split("</p>")
    body = split2[0].split()
    bodydict = {}
    for word in body:
        if word not in bodydict:
            bodydict[word] = body.count(word)
        else:
            continue
    return bodydict

def base_address(url):#finding the base url to which we can add references onto
    baseurl = ""
    for i in range(1,len(url)-1):
        if url[-i] == "/":
            baseurl = url[0:-i]
            break
    return baseurl

def reference_gen(url):#reference link finder
    contents = webdev.read_url(url)
    split1 = contents.split("<title>")
    split2 = split1[1].split("</title>")
    ref = split2[1].split()
    reference = []
    for i in range(len(ref)-1):
        if ref[i] == "<a":
            reference.append(ref[i+1])
    ref.clear()
    base = base_address(url)
    for i in range(len(reference)):
        split = reference[i].split("=")
        href = split[1].split(">")[0]
        ref.append(base+href.strip('"').strip("."))
    return ref








