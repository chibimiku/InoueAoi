# encoding=utf-8

#offical site:https://github.com/fxsjy/jieba


import jieba
import jieba.posseg as pseg
import jieba.analyse
#read letter file

filename = 'train.dec'
outfilename = 'train_out.dec'

#outfileobj = open(outfilename, 'w+', encoding = 'utf-8')


#移除标点符号？

def gen_vocabulary_file_jieba(inputfile, outputfile):
    
    '''
    with open(filename, encoding="utf-8") as f:
        for line in f:
            words = pseg.cut(line)
            for word, flag in words:
                print('%s %s' % (word, flag))
                outfileobj.write(word.strip() + ' ')
    '''
    
    content = open(inputfile, 'rb').read()
    tags = jieba.analyse.extract_tags(content, topK=10000)
    #print(",".join(tags))
    with open(outputfile, "w", encoding = "utf8") as ff:
        for word in tags:
            ff.write(word + "\n")
    
    
gen_vocabulary_file_jieba(filename,outfilename)
print ("tasks done!")