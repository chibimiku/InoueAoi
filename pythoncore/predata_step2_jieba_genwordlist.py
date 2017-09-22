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

dir_name = 'data/'

encoding_in_filename = dir_name + 'train.enc'
encoding_vocab_filename = dir_name + 'train_encode_vocabulary'
encoding_cut_out_filename = dir_name + 'train_cut.enc'
encoding_cut_out_fixed_filename = dir_name + 'train_cut_fixed.enc'
encoding_vec_filename = dir_name + 'train_encode.vec'

decoding_in_filename = dir_name + 'train.dec'
decoding_vocab_filename = dir_name + 'train_decode_vocabulary'
decoding_cut_out_filename = dir_name + 'train_cut.dec'
decoding_cut_out_fixed_filename = dir_name + 'train_cut_fixed.dec'
decoding_vec_filename = dir_name + 'train_decode.vec'

test_encoding_in_filename = dir_name + 'test.enc'
test_encoding_vocab_filename = dir_name + 'test_encode_vocabulary'
test_encoding_cut_out_filename = dir_name + 'test_cut.enc'
test_encoding_vec_filename = dir_name + 'test_encode.vec'

test_decoding_in_filename = dir_name + 'test.dec'
test_decoding_vocab_filename = dir_name + 'test_decode_vocabulary'
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


#给字典按value排序，返回的是list
def sort_by_value(d, insert_max = 0, in_reverse=True):
    print ("insert_max:" + str(insert_max))
    #return sorted(d.items(), lambda x, y: cmp(x[1], y[1]), reverse=in_reverse)
    list_t = sorted(d.items(), key=lambda item:item[1], reverse=in_reverse)
    return_list = []
    insert_count = 0
    for row in list_t:
        if(insert_max > 0 and insert_count > insert_max):
            break
        return_list.append(row[0])
        insert_count = insert_count + 1
    return return_list

# 用jieba lib进行分词，产生分词过后拿空格分割开的训练集
# offical site:https://github.com/fxsjy/jieba

#在分割的同时提取所有的词输出词表
def gen_cut_file_jieba(inputfile, cut_outputfile, vocabulary_outfile, start_header, appendword = '', vocal_size = 100000):
    print ("going to cut file...")
    print ("vocal size:" + str(vocal_size))
    #vocabulary = [] #词典换成dict
    #vocal_size：按出现次数最多取最高频的x词
    
    vocabulary = {}
    outfileobj = open(cut_outputfile, 'w+', encoding = 'utf-8')
    '''
    #先输入头部的几个tag
    #dict无序，这里弃用
    for word in start_header:
        #vocabulary.append(word)
        vocabulary[word] = 1
    '''
    print ("goting to read input file " + inputfile)
    #读取原始文件
    progress_line = 0 
    with open(inputfile, "r", encoding = "utf8") as f:
        for line in f:
            if(progress_line % 10000 == 0):
                print ("proc for " + str(progress_line) + " line(s)...")
                print ("vocabulary size: " + str(len(vocabulary)))
            seg_list = jieba.lcut(line.strip(), cut_all=False) #lcut直接拿list
            #输出文件
            outfileobj.write(" ".join(seg_list))
            outfileobj.write("\n")
            #维护词表
            for single_seg in seg_list:
                #if(not single_seg in vocabulary):
                if(not single_seg in vocabulary):
                    #vocabulary.append(single_seg)
                    vocabulary[single_seg] = 1
                else:
                    vocabulary[single_seg] = vocabulary[single_seg] + 1
            progress_line = progress_line + 1
    vocabulary_sorted = sort_by_value(vocabulary, vocal_size, in_reverse=True) #排序，这一步会比较费劲
    #注意后面用 vocabulary_sorted 已经是list了
        
    #支持通过appendword追加3500个常用汉字
    if (not appendword == "" ):
        print ("going to open appendfile:" + str(appendword))
        with open(appendword, 'r', encoding = "utf8") as apf:
            for line in apf:
                #vocabulary.append(line.strip())
                if(not line.strip() in vocabulary_sorted):
                    #vocabulary[line.strip()] = 1
                    vocabulary_sorted.append(line.strip())
    print ("output vocabulary to file:" + vocabulary_outfile)
    #输出词表
    vocabulary_fileobj = open(vocabulary_outfile, 'w+', encoding = 'utf-8')
    #在这里输出头部那几个固定的词
    for word in start_header:
        vocabulary_fileobj.write(word)
        vocabulary_fileobj.write("\n")
    for word in vocabulary_sorted:
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
    
def data_ap(cuted_data_path, vocab_path, output_path):
    vocab = {}
    #先加载词表成dict
    with open(vocab_path, 'r' , encoding="utf8") as fp:
        for line in fp:
            vocab[line.strip()] = 1
    print ("loaded " + str(len(vocab)) + " word(s)")
    
    word_count_cutted = 0
    word_count_not_cutted = 0
    with open(cuted_data_path, 'r', encoding="utf8" ) as fp:
        with open(output_path, 'w+' , encoding="utf8") as wfp:
            for line in fp:
                wordlist = line.strip().split(' ')
                new_wordlist = []
                for word in wordlist:
                    if(word in vocab):
                        word_count_not_cutted = word_count_not_cutted + 1
                        new_wordlist.append(word)
                    else:
                        word_count_cutted =  word_count_cutted + 1
                        for ss_char in word:
                            new_wordlist.append(ss_char)
                wfp.write(" ".join(new_wordlist))
                wfp.write("\n")
    print ("not cut word: " + str(word_count_not_cutted))
    print ("cut word: " + str(word_count_cutted))

#抓紧了开车
gen_cut_file_jieba(encoding_in_filename, encoding_cut_out_filename, encoding_vocab_filename, START_VOCABULART, appendword)
gen_cut_file_jieba(decoding_in_filename, decoding_cut_out_filename, decoding_vocab_filename, START_VOCABULART, appendword)
gen_cut_file_jieba(test_encoding_in_filename, test_encoding_cut_out_filename, test_encoding_vocab_filename, START_VOCABULART, appendword)
gen_cut_file_jieba(test_decoding_in_filename, test_decoding_cut_out_filename, test_decoding_vocab_filename, START_VOCABULART, appendword)

#依照新的词表，对已经cut过的文件里，无法从vocab找到的"词"再次分解成字。
data_ap(encoding_cut_out_filename, encoding_vocab_filename, encoding_cut_out_fixed_filename)
data_ap(decoding_cut_out_filename, decoding_vocab_filename, decoding_cut_out_fixed_filename)


#在上述步骤都完成之后，依词表将分词结果(_cut的输出)转化为向量
data_utils.data_to_token_ids(encoding_cut_out_fixed_filename, encoding_vec_filename, encoding_vocab_filename)
data_utils.data_to_token_ids(decoding_cut_out_fixed_filename, decoding_vec_filename, decoding_vocab_filename)
data_utils.data_to_token_ids(test_encoding_cut_out_filename, test_encoding_vec_filename, test_encoding_vocab_filename)
data_utils.data_to_token_ids(test_decoding_cut_out_filename, test_decoding_vec_filename, test_decoding_vocab_filename)