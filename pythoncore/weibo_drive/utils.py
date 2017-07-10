# -*- coding: utf-8 -*-

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
    
if __name__=='__main__':
    #rs = remove_atinfo('123 @test 321 oogcasfas')
    #print (rs)
    print ("all task done~")
    url = 'http://127.0.0.1:9999/'
    r = requests.get(url, dict(
        custword='你好'))
    print(r.json)