# encoding=utf-8

#offical site:https://github.com/fxsjy/jieba

import jieba
import jieba.posseg as pseg
import jieba.analyse
#read letter file

vocabulary_size=200000

encoding_in_filename = 'train.enc'
encoding_out_filename = 'train_encode_vocabulary'
decoding_in_filename = 'train.dec'
decoding_out_filename = 'train_decode_vocabulary'

#outfileobj = open(outfilename, 'w+', encoding = 'utf-8')


#移除标点符号？

def gen_vocabulary_file_jieba(inputfile, outputfile, vocabulary_size):    
    content = open(inputfile, 'rb').read()
    tags = jieba.analyse.extract_tags(content, topK=vocabulary_size)
    #print(",".join(tags))
    with open(outputfile, "w", encoding = "utf8") as ff:
        for word in tags:
            ff.write(word + "\n")
    
gen_vocabulary_file_jieba(encoding_in_filename,encoding_out_filename, vocabulary_size)
gen_vocabulary_file_jieba(decoding_in_filename,decoding_out_filename, vocabulary_size)
print ("tasks done!")