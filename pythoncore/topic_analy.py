# -*- coding: utf-8 -*-
# auto operator for weibo.

import jieba
import jieba.analyse

import data_utils

#把原始topic文件切分成关键词->topic
def split_topic(in_file, out_file):
    line_count = 0

    with open(in_file, 'r', encoding="utf8") as fp:
        with open(out_file, 'w+', encoding="utf8") as wfp:
            for line in fp:
                try:
                    line_count = line_count + 1
                    m_data = line.split("\t")
                    split_rs = jieba.analyse.extract_tags(m_data[1], topK=5)
                    #print (split_rs)
                    keyword_string = ",".join(split_rs)
                    final_string = m_data[0] + "\t" + keyword_string
                    wfp.write(final_string.strip() + "\n")
                    
                    if(line_count > 0 and line_count % 10000 == 0):
                        print ("run for " + str(line_count) + " line(s)")
                except e:
                    pass

#把上一步获得的文件切分两部分，方便后面交给data_utils.data_to_token_ids去处理
def split_2row(in_file, out_file1, out_file2):
    line_count = 0

    with open(in_file, 'r', encoding="utf8") as fp:
        with open(out_file1, 'w+', encoding="utf8") as wfp1:
            with open(out_file2, 'w+', encoding="utf8") as wfp2:
                for line in fp:
                    try:
                        m_data = line.split("\t")
                        to_data = m_data[1].split(",")
                        if(not m_data):
                            continue
                        if(not to_data):
                            continue
                        wfp1.write(m_data[0].strip() + "\n")
                        wfp2.write(" ".join(to_data).strip() + "\n")
                        if(line_count > 0 and line_count % 10000 == 0):
                            print ("run for " + str(line_count) + " line(s)")
                    except:
                        pass

def do_word2vec():
    my_len = 15000000
    data_utils.create_vocabulary('data/topic/topic_index.vocal', 'data/topic/topic_index.txt', my_len)
    data_utils.data_to_token_ids('data/topic/topic_index.txt', 'data/topic/topic_index.vec', 'data/topic/topic_index.vocal')
    
    data_utils.create_vocabulary('data/topic/topic_group.vocal', 'data/topic/topic_group.txt', my_len)
    data_utils.data_to_token_ids('data/topic/topic_group.txt', 'data/topic/topic_group.vec', 'data/topic/topic_group.vocal')
                        
#split_topic('data/zhihu_topic_output', 'data/topic_output.txt')
#split_2row('data/topic/topic_output.txt', 'data/topic/topic_index.txt', 'data/topic/topic_group.txt')
do_word2vec()