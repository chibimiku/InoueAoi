# encoding=utf-8

#jieba 分词
#https://github.com/fxsjy/jieba

import jieba
import jieba.analyse
#data_utils from tensorflow modules
#https://github.com/tensorflow/models/blob/master/tutorials/rnn/translate/
import data_utils

#设置常量
vocabulary_size = 200000

encoding_in_filename = 'train.enc'
encoding_out_filename = 'train_encode_vocabulary'
encoding_cut_out_filename = 'train_cut.enc'
encoding_vec_filename = 'train_encode.vec'

decoding_in_filename = 'train.dec'
decoding_out_filename = 'train_decode_vocabulary'
decoding_cut_out_filename = 'train_cut.dec'
decoding_vec_filename = 'train_decode.vec'

test_encoding_in_filename = 'test.enc'
test_encoding_out_filename = 'test_encode_vocabulary'
test_encoding_cut_out_filename = 'test_cut.enc'
test_encoding_vec_filename = 'test_encode.vec'

test_decoding_in_filename = 'test.dec'
test_decoding_out_filename = 'test_decode_vocabulary'
test_decoding_cut_out_filename = 'test_cut.dec'
test_decoding_vec_filename = 'test_decode.vec'

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

def gen_cut_file_jieba(inputfile, outputfile):
    outfileobj = open(outputfile, 'w+', encoding = 'utf-8')
    with open(inputfile, "r", encoding = "utf8") as f:
        for line in f:
            seg_list = jieba.cut(line.strip(), cut_all=False)
            outfileobj.write(" ".join(seg_list))
            outfileobj.write("\n")
            
# 提取topx的词，一次生成整个儿词表
def gen_vocabulary_file_jieba(inputfile, outputfile, start_header, vocabulary_size, appendword = ''):
    vocabulary_count = 0
    content = open(inputfile, 'rb').read()
    tags = jieba.analyse.extract_tags(content, topK = vocabulary_size)
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
gen_cut_file_jieba(encoding_in_filename, encoding_cut_out_filename)
gen_cut_file_jieba(decoding_in_filename, decoding_cut_out_filename)
gen_cut_file_jieba(test_encoding_in_filename, test_encoding_cut_out_filename)
gen_cut_file_jieba(test_decoding_in_filename, test_decoding_cut_out_filename)
gen_vocabulary_file_jieba(encoding_in_filename,encoding_out_filename, START_VOCABULART, vocabulary_size)
gen_vocabulary_file_jieba(decoding_in_filename,decoding_out_filename, START_VOCABULART, vocabulary_size)
gen_vocabulary_file_jieba(test_encoding_in_filename,test_encoding_out_filename, vocabulary_size, appendword)
gen_vocabulary_file_jieba(test_decoding_in_filename,test_decoding_out_filename, vocabulary_size, appendword)

#在上述步骤都完成之后，依词表将分词结果(_cut的输出)转化为向量
data_utils.data_to_token_ids(encoding_cut_out_filename, encoding_vec_filename, encoding_out_filename)
data_utils.data_to_token_ids(decoding_cut_out_filename, decoding_vec_filename, decoding_out_filename)
data_utils.data_to_token_ids(test_encoding_cut_out_filename, test_encoding_vec_filename, test_encoding_out_filename)
data_utils.data_to_token_ids(test_decoding_cut_out_filename, test_decoding_vec_filename, test_decoding_out_filename)