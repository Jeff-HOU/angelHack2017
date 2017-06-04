# sample usage: python3 json2markdown.py https://hotmelon-655ec.firebaseio.com/.json Writing_your_PhD_thesis_in_LaTeX2e-Krishna_Kumar md.md
import urllib.request, json, sys
from firebase import firebase
import subprocess

link = sys.argv[1] # json url
file = sys.argv[3] # output file path
name = sys.argv[2] # which article to convert

firebase = firebase.FirebaseApplication('https://hotmelon-655ec.firebaseio.com', None)
tmp_ppt = name+'-ppt'
ppt = '/'+name+'-ppt'

'''
put_content = ''
put_cmd = ['curl', '-X', 'PUT', '-d', put_content, 'https://hotmelon-655ec.firebaseio.com/ppt_test/'+slideCount+'/'+elementCount+'.json']

curl_content = '{"title":"'+"title"+'""}'
curl_cmd = 'curl -X PUT -d '+ curl_content + 'https://hotmelon-655ec.firebaseio.com/ppt_test/'+slideCount+'/'+elementCount+'.json'
'''
with urllib.request.urlopen(link) as url:
    # load json, set basic vars
    slideCount = 1
    elementCount = 0
    data = json.loads(url.read().decode())
    f = open(file, 'w+')
    f.close()
    f = open(file, 'a')
    f.write('---\n\n')
    sd = data[name]
    bgcolor = data["style"]["backgroundColor"]
    color = data["style"]["color"]
    colorPic = "https://hotmelon.tech/color/"
    
    # clear the corresponding PPT folder, set dome basic elements and bgColor
    firebase.put('/', tmp_ppt, data = '')
    firebase.put(ppt+'/'+str(slideCount), "bg", data = bgcolor)
    firebase.put(ppt+'/'+str(slideCount), "color", data = color)
    slideCount += 1
    f.write("![]("+colorPic+bgcolor+".png"+"){.background}\n\n")

    # set title
    f.write("# "+'<span style="color: '+color+'">'+sd["title"]+'</span>'+"\n\n")
    firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"title", data = sd["title"])
    elementCount += 1
    
    # set subtitle
    f.write("## "+'<span style="color: '+color+'">'+sd["subtitle"]+'</span>'+"\n\n")
    firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"subtitle", data = sd["subtitle"])
    elementCount += 1
    
    # set authors
    #atr = ', '.join(sd["authors"])
    #f.write('<span style="color: grey">Authors: '+atr+"</span>\n\n")
    
    # set notes
    f.write('<!--'+'\n')
    f.write(sd["abstract"]+"\n")
    f.write('-->'+'\n\n')
    
    # create new page, set bgColor
    f.write('---\n\n')
    slideCount += 1
    elementCount = 0
    f.write("![]("+colorPic+bgcolor+".png"+"){.background}\n\n")

    cptr = sd["chapters"]
    for i, _ in enumerate(cptr):
        scptr = cptr[i]
        f.write("# "+'<span style="color: '+color+'">'+scptr["title"]+'</span>'+"{.big}"+"\n\n")
        firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"title", data = scptr["title"])
        elementCount += 1
        
        f.write("---\n\n")
        slideCount += 1
        elementCount = 0
        f.write("![]("+colorPic+bgcolor+".png"+"){.background}\n\n")

        sec = scptr["sections"]
        for j, _ in enumerate(sec):
            ssec = sec[j]
            noFignoKwdId = 1
            try:
                if not ssec["figures"] == "":
                    noFignoKwdId = 0
                    for k, val in enumerate(ssec["figures"]):
                        # set title
                        f.write("# "+'<span style="color: '+color+'">'+ssec["title"]+'</span>'+"\n\n")
                        firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"title", data = ssec["title"])
                        elementCount += 1
                        
                        # convert and put figures
                        fig = ssec["figures"][k]
                        f.write("![]("+fig+")"+"\n\n")
                        firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"figure", data = fig)
                        elementCount += 1
                        
                        # create new page, set bgColor
                        f.write("---\n\n")
                        slideCount += 1
                        elementCount = 0
                        f.write("![]("+colorPic+bgcolor+".png"+"){.background}\n\n")

            except:
                print("", end='')
            try:
                if not ssec["keywords"] == "":
                    noFignoKwdId = 0
                    f.write("# "+'<span style="color: '+color+'">'+ssec["title"]+'</span>'+"\n\n")
                    firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"title", data = ssec["title"])
                    elementCount += 1
                    keyword = []
                    for k, val in enumerate(ssec["keywords"]):
                        f.write("* "+'<span style="color: '+color+'">'+val+'</span>'+"\n\n")
                        keyword.append(val)
                        
                        # if index of keywords and reach 10n, create a new page and continue.
                        if (k % 10 == 0 and k > 0):
                            f.write("---\n\n")
                            firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"keyword", data = ', '.join(keyword))
                            keyword = []
                            slideCount += 1
                            elementCount = 0
                            f.write("![]("+colorPic+bgcolor+".png"+"){.background}\n\n")
                            
                            # if the last index is a 10n, do not create a new title for it.
                            if not k == len(ssec["keywords"]) - 1:
                                f.write("# "+'<span style="color: '+color+'">'+ssec["title"]+'</span>'+"\n\n")
                                firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"title", data = ssec["title"])
                                elementCount += 1
                        tmp = k # used to keep track of k.
                    if not tmp % 10 == 0:
                        f.write("---\n\n")
                        slideCount += 1
                        elementCount = 0
                        f.write("![]("+colorPic+bgcolor+".png"+"){.background}\n\n")
                        
            except:
                print("", end='')
            if noFignoKwdId:
                # if there is no figure ot keyword, display only section title
                f.write("# "+'<span style="color: '+color+'">'+ssec["title"]+'</span>'+"{.big}\n\n")
                firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"title", data = ssec["title"])
                elementCount += 1
                f.write("---\n\n")
                slideCount += 1
                elementCount = 0
                f.write("![]("+colorPic+bgcolor+".png"+"){.background}\n\n")

    f.close()
