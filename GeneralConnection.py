#!/usr/bin/python
import requests
import sys, getopt

def main(argv):

    url = ""
    outputfile = ""
    request = ""
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["url=","ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('usage : python test.py -u <Graph_URL> -o <outputfile>')
            sys.exit()
        elif opt in ("-u", "--url"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    r= requests.post('http://legivoc.org/sparql_form', auth=('salbouze@tracksens.com', 'LouiseALB*'), params = {'xml':'1','query': request1, 'db':'at.rdf'})
    my_request = " "
    print(r)
    print(r.status_code)
    print(r.text)

    return

if __name__== "__main__":

    main(sys.argv[1:])
    print("The end")
