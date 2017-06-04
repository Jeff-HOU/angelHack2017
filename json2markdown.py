# sample usage: python3 json2markdown.py https://hotmelon-655ec.firebaseio.com/.json Writing_your_PhD_thesis_in_LaTeX2e-Krishna_Kumar md.md
import urllib.request, json, sys
from firebase import firebase
import subprocess

link = sys.argv[1] # json url
file = sys.argv[3] # output file path
name = sys.argv[2] # which article to convert

firebase = firebase.FirebaseApplication('https://hotmelon-655ec.firebaseio.com', None)
ppt = '/ppt'

'''
put_content = ''
put_cmd = ['curl', '-X', 'PUT', '-d', put_content, 'https://hotmelon-655ec.firebaseio.com/ppt_test/'+slideCount+'/'+elementCount+'.json']

curl_content = '{"title":"'+"title"+'""}'
curl_cmd = 'curl -X PUT -d '+ curl_content + 'https://hotmelon-655ec.firebaseio.com/ppt_test/'+slideCount+'/'+elementCount+'.json'
'''
with urllib.request.urlopen(link) as url:
    slideCount = 1
    elementCount = 0
    element = []
    #data_element = json.dumps({})
    keyword = []

    data = json.loads(url.read().decode())
    f = open(file, 'w+')
    f.close()
    f = open(file, 'a')
    f.write('---\n\n')
    sd = data[name] # maybe this is also an input?
    bgcolor = data["style"]["backgroundColor"]
    color = data["style"]["color"]
    colorPic = "https://34.208.199.223/color/"
    firebase.put('/', 'ppt', data = '')
    firebase.put(ppt+'/'+str(slideCount), "bg", data = bgcolor)
    firebase.put(ppt+'/'+str(slideCount), "color", data = color)
    slideCount += 1

    f.write("![]("+colorPic+bgcolor+".png"+"){.background}\n\n")
    #element.append({str(elementCount)+"bg" : bgcolor})

    
    #elementCount += 1
    f.write("# "+'<span style="color: '+color+'">'+sd["title"]+'</span>'+"\n\n")
    #element.append({str(elementCount)+"title" : sd["title"]})
    firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"title", data = sd["title"])
    elementCount += 1

    '''
    put_content = '{"title":"'+sd["title"]+'""}'
    print (put_content)
    put_cmd = ['curl', '-X', 'PUT', '-d', put_content, 'https://hotmelon-655ec.firebaseio.com/ppt_test/0.json']
    try:
        output = subprocess.check_output(put_cmd, stderr=subprocess.STDOUT)
        retcode = 0
    except subprocess.CalledProcessError, e:
        retcode = e.returncode
        output = e.output
    elementCount += 1
    
    fh = os.popen(curl_cmd, 'r')
    data = fh.read()
    fh.close()
    '''

    f.write("## "+'<span style="color: '+color+'">'+sd["subtitle"]+'</span>'+"\n\n")
    #element.append({str(elementCount)+"subtitle": sd["subtitle"]})
    firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"subtitle", data = sd["subtitle"])
    elementCount += 1
    #atr = ', '.join(sd["authors"])
    #f.write('<span style="color: grey">Authors: '+atr+"</span>\n\n")
    f.write('<!--'+'\n')
    f.write(sd["abstract"]+"\n")
    f.write('-->'+'\n\n')
    f.write('---\n\n')
    #print (element)
    #json_element = json.dumps(element)
    #firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"bg", data = {{json_element}})
    slideCount += 1
    elementCount = 0
    f.write("![]("+colorPic+bgcolor+".png"+"){.background}\n\n")
    #firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"bg", data = bgcolor)
    #elementCount += 1
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
        #firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"bg", data = bgcolor)
        #elementCount += 1
        sec = scptr["sections"]
        for j, _ in enumerate(sec):
            ssec = sec[j]
            noFignoKwdId = 1
            try:
                if not ssec["figures"] == "":
                    noFignoKwdId = 0
                    for k, val in enumerate(ssec["figures"]):
                        f.write("# "+'<span style="color: '+color+'">'+ssec["title"]+'</span>'+"\n\n")
                        firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"title", data = ssec["title"])
                        elementCount += 1
                        fig = ssec["figures"][k]
                        f.write("![]("+fig+")"+"\n\n")
                        firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"figure", data = fig)
                        elementCount += 1
                        f.write("---\n\n")
                        slideCount += 1
                        elementCount = 0
                        f.write("![]("+colorPic+bgcolor+".png"+"){.background}\n\n")
                        #firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"bg", data = bgcolor)
                        #elementCount += 1
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
                        #firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"keyword", data = val)
                        elementCount += 1
                        if (k % 10 == 0 and k > 0):
                            f.write("---\n\n")
                            firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"keyword", data = ', '.join(keyword))
                            keyword = []
                            slideCount += 1
                            elementCount = 0
                            f.write("![]("+colorPic+bgcolor+".png"+"){.background}\n\n")
                            #firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"bg", data = bgcolor)
                            #elementCount += 1
                            if not k == len(ssec["keywords"]) - 1:
                                f.write("# "+'<span style="color: '+color+'">'+ssec["title"]+'</span>'+"\n\n")
                                firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"title", data = ssec["title"])
                                elementCount += 1
                        tmp = k
                    if not k % 10 == 0:
                        f.write("---\n\n")
                        slideCount += 1
                        elementCount = 0
                        f.write("![]("+colorPic+bgcolor+".png"+"){.background}\n\n")
                        #firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"bg", data = bgcolor)
                        #elementCount += 1
                        
            except:
                print("", end='')
            if noFignoKwdId:
                f.write("# "+'<span style="color: '+color+'">'+ssec["title"]+'</span>'+"{.big}\n\n")
                firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"title", data = ssec["title"])
                elementCount += 1
                f.write("---\n\n")
                slideCount += 1
                elementCount = 0
                f.write("![]("+colorPic+bgcolor+".png"+"){.background}\n\n")
                #firebase.put(ppt+'/'+str(slideCount),str(elementCount)+"bg", data = bgcolor)
                #elementCount += 1
    f.close()