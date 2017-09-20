# encoding=utf-8

#jieba 分词
#https://github.com/fxsjy/jieba

import jieba
import jieba.analyse
#data_utils from tensorflow modules
#https://github.com/tensorflow/models/blob/master/tutorials/rnn/translate/
import data_utils

#修改一下，让jieba在分割时同时提取全部的词表，防止UNK太多。

#设置常量

dir_name = 'data/corpus/new_170919/'

encoding_in_filename = dir_name + 'train.enc'
encoding_out_filename = dir_name + 'train_encode_vocabulary'
encoding_cut_out_filename = dir_name + 'train_cut.enc'
encoding_vec_filename = dir_name + 'train_encode.vec'

decoding_in_filename = dir_name + 'train.dec'
decoding_out_filename = dir_name + 'train_decode_vocabulary'
decoding_cut_out_filename = dir_name + 'train_cut.dec'
decoding_vec_filename = dir_name + 'train_decode.vec'

test_encoding_in_filename = dir_name + 'test.enc'
test_encoding_out_filename = dir_name + 'test_encode_vocabulary'
test_encoding_cut_out_filename = dir_name + 'test_cut.enc'
test_encoding_vec_filename = dir_name + 'test_encode.vec'

test_decoding_in_filename = dir_name + 'test.dec'
test_decoding_out_filename = dir_name + 'test_decode_vocabulary'
test_decoding_cut_out_filename = dir_name + 'test_cut.dec'
test_decoding_vec_filename = dir_name + 'test_decode.vec'

appendword = 'data/chinese_char_3k5.txt' #3500个常用汉字

###
# 特殊标记，用来填充标记对话
PAD = "__PAD__"
GO = "__GO__"
EOS = "__EOS__"  # 对话结束
UNK = "__UNK__"  # 标记未出现在词汇表中的字符
START_VOCABULART = [PAD, GO, EOS, UNK]
PAD_ID = 0
GO_ID = 1
EOS_ID = 2
UNK_ID = 3


# 用jieba lib进行分词，产生分词过后拿空格分割开的训练集
# offical site:https://github.com/fxsjy/jieba

#在分割的同时提取所有的词输出词表
def gen_cut_file_jieba(inputfile, cut_outputfile, vocabulary_outfile, start_header, appendword = ''):
    print ("going to cut file...")
    vocabulary = []
    outfileobj = open(cut_outputfile, 'w+', encoding = 'utf-8')
    #先输入头部的几个tag
    for word in start_header:
        vocabulary.append(word)
    print ("goting to read input file " + inputfile)
    #读取原始文件
    progress_line = 0 
    with open(inputfile, "r", encoding = "utf8") as f:
        for line in f:
            if(progress_line % 2500 == 0):
                print ("proc for " + str(progress_line) + " line(s)...")
                print ("vocabulary size: " + str(len(vocabulary)))
            seg_list = jieba.lcut(line.strip(), cut_all=False) #lcut直接拿list
            #输出文件
            outfileobj.write(" ".join(seg_list))
            outfileobj.write("\n")
            #维护词表
            for single_seg in seg_list:
                if(not single_seg in vocabulary):
                    vocabulary.append(single_seg)
            progress_line = progress_line + 1
    #通过appendword追加3500个常用汉字.
    if (not appendword == "" ):
        print ("going to open appendfile:" + str(appendword))
        with open(appendword, 'r', encoding = "utf8") as apf:
            for line in apf:
                vocabulary.append(line.strip())
    print ("output vocabulary to file:" + vocabulary_outfile)
    #输出词表
    vocabulary_fileobj = open(vocabulary_outfile, 'w+', encoding = 'utf-8')
    for word in vocabulary:
        vocabulary_fileobj.write(word)
        vocabulary_fileobj.write("\n")
            
# 提取topx的词，一次生成整个儿词表
# 恩这个已经不再用了…
def gen_vocabulary_file_jieba(inputfile, outputfile, start_header, vocabulary_size, appendword = ''):
    vocabulary_count = 0
    content = open(inputfile, 'rb').read()
    tags = jieba.analyse.extract_tags(content, topK=vocabulary_size)
    with open(outputfile, "w", encoding = "utf8") as ff:
        #先输入头部的几个tag
        for word in START_VOCABULART:
            ff.write(word + "\n")
            vocabulary_count = vocabulary_count + 1
        #通过appendword追加3500个常用汉字.
        if (not appendword == "" ):
            print ("going to open appendfile:" + str(appendword))
            with open(appendword, 'r', encoding = "utf8") as apf:
                for line in apf:
                    ff.write(line.strip() + "\n")
                    vocabulary_count = vocabulary_count + 1
        #再输入词
        for word in tags:
            ff.write(word + "\n")
            vocabulary_count = vocabulary_count + 1
    print ("outputfile " + outputfile + " with " + str(vocabulary_count) + " line(s)...")
    return True

#抓紧了开车
gen_cut_file_jieba(encoding_in_filename, encoding_cut_out_filename, encoding_out_filename, START_VOCABULART, appendword)
gen_cut_file_jieba(decoding_in_filename, decoding_cut_out_filename, decoding_out_filename, START_VOCABULART, appendword)
gen_cut_file_jieba(test_encoding_in_filename, test_encoding_cut_out_filename, test_encoding_out_filename, START_VOCABULART, appendword)
gen_cut_file_jieba(test_decoding_in_filename, test_decoding_cut_out_filename, test_decoding_out_filename, START_VOCABULART, appendword)


#在上述步骤都完成之后，依词表将分词结果(_cut的输出)转化为向量
data_utils.data_to_token_ids(encoding_cut_out_filename, encoding_vec_filename, encoding_out_filename)
data_utils.data_to_token_ids(decoding_cut_out_filename, decoding_vec_filename, decoding_out_filename)
data_utils.data_to_token_ids(test_encoding_cut_out_filename, test_encoding_vec_filename, test_encoding_out_filename)
data_utils.data_to_token_ids(test_decoding_cut_out_filename, test_decoding_vec_filename, test_decoding_out_filename)
