# -*- coding: utf-8 -*-
import requests
import json

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
    
def get_remote_response(content, host = '127.0.0.1', port = 9999):
    url = 'http://127.0.0.1:9999/'
    r = requests.get(url, dict(
        custword=content))
    result_json = json.loads(r.content.decode("utf-8"))
    print (result_json['response'])
    return result_json['response']
    
if __name__=='__main__':
    #rs = remove_atinfo('123 @test 321 oogcasfas')
    #print (rs)
    print ("all task done~")

    #print (r.content.decode("utf-8"))