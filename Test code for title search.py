import webdev
url = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"
contents = webdev.read_url(url)

#title finder
split1 = contents.split("<title>")
split2 = split1[1].split("</title>")
title = split2[0]

#body finder
split1 = contents.split("<p>")
split2 = split1[1].split("</p>")
body = split2[0].split()

#finding the base url to which we can add references onto
baseurl = ""
for i in range(1,len(url)-1):
    if url[-i] == "/":
        baseurl = url[0:-i]
        break

#reference link finder
ref = split2[1].split()
reference = []
for i in range(len(ref)-1):
    if ref[i] == "<a":
        reference.append(ref[i+1])
ref.clear()
for i in range(len(reference)-1):
    split = reference[i].split("=")
    href = split[1].split(">")[0]
    ref.append(baseurl+href.strip('"').strip("."))








