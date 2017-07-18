# -*- coding: utf-8 -*-
import requests
import json
import os

def remove_atinfo(instr):
    newwords = []
    words = instr.split(" ")
    for word in words:
        if(not word.startswith('@')):
            newwords.append(word)
    return " ".join(newwords)
    
def find_between(in_string, first, last):
    try:
        start = in_string.index( first ) + len( first )
        end = in_string.index( last, start )
        return in_string[start:end]
    except ValueError:
        return ""
    
def get_remote_response(content, host = '127.0.0.1', port = 32727):
    url = 'http://127.0.0.1:' + str(port) + '/'
    r = requests.get(url, dict(
        custword=content))
    try:
        result_json = json.loads(r.content.decode("utf-8"))
        print (result_json['response'])
        return result_json['response']
    except ValueError:
        return ""
    
def read_file_intostr(filename, needstrip = False, myEncoding = "utf-8"):
    if(not os.path.exists(filename)):
        print("cannot open " + filename + " ...", 3)
        return None
    with open(filename, 'r', encoding=myEncoding) as myfile:
        if(needstrip):
            data = myfile.read().replace('\n', '')
        else:
            data = myfile.read()
    return data
   
def write_append_file(str, filename, newline = False, myEncoding = "utf-8"):
    with open(filename, 'a+', encoding = myEncoding) as f:
        f.write(str)
        if(newline):
            f.write("\n")
    return True
    
def write_new_file(str, filename, newline = False, myEncoding = "utf-8"):
    with open(filename, 'w+', encoding = myEncoding) as f:
        f.write(str)
        if(newline):
            f.write("\n")
    return True
   
if __name__=='__main__':
    #rs = remove_atinfo('123 @test 321 oogcasfas')
    #print (rs)
    print ("all task done~")

    #print (r.content.decode("utf-8"))