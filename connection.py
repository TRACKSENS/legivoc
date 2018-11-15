import requests
import time
import re
import os

EMPTY_RETURN = """<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    xmlns:legivoc="http://legivoc.org/namespaces/2014/legivoc#"
    xmlns:skosxl="http://www.w3.org/2008/05/skos-xl#"
    xmlns:dct="http://purl.org/dc/terms/"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
</rdf:RDF>"""

def connection(limit, nbrOfReq, fileName):


    request1 = """  PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
                    PREFIX skosxl:<http://www.w3.org/2008/05/skos-xl#>
                    
                   CONSTRUCT {
                      ?s ?p ?o .
                   }
                    WHERE {
                       ?s ?p ?o .
                    }
                    ORDER BY ?s ?p ?o 
                    """

    request1 = request1 + " LIMIT " + str(limit) + " OFFSET " + str(nbrOfReq*limit)

    time.sleep(1)

    r= requests.post('http://legivoc.org/sparql_form', auth=('salbouze@tracksens.com', 'LouiseALB*'), params = {'xml':'1','query': request1, 'db':fileName})

    return r.text.strip()

if __name__== "__main__":

    text = " "
    limit = 10000
    nbrOfReq = 0
    globalText = ""
    endOfFile = False

    print("START")

    if not os.path.exists("./results"):
        os.mkdir("./results")

    #File_list = ["at", "be", "de", "dk", "es", "eu", "fi", "fr", "gr", "lt", "mt", "nl", "si", "uk", "ch"]
    File_list = ["ch" , "si", "eu" ]

    for elt in enumerate(File_list):
        fileName = elt[1] + ".rdf"
        first = True
        if not os.path.exists("./results/" + elt[1]):
            os.mkdir("./results/" + elt[1])
        nbrOfReq = 0

        while len(text)>650 or first :
            text = connection(limit, nbrOfReq, fileName)

            with open("./results/"+elt[1] + "/"+elt[1]+"_"+str(nbrOfReq)+".xml", "a", encoding="utf-8") as myLexic:
                myLexic.write(text)

            nbrOfReq += 1

            if not first:
                a = re.compile("<rdf:RDF.*?>", re.DOTALL)
                tmp = re.sub(a, "", text)
                tmp = re.sub("</rdf:RDF>", "", tmp)
                globalText += tmp
            else:
                globalText += text
                globalText = re.sub("</rdf:RDF>", "", globalText)
                first = False

        globalText += "\n</rdf:RDF>"

        with open("./results/"+elt[1] + "/all"+ elt[1] +".xml", "a", encoding="utf-8") as myLexic:
            myLexic.write(globalText)

        globalText = ""

    print("END")
