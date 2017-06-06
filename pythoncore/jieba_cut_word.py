# encoding=utf-8

import jieba
# 用jieba lib进行分词

def gen_cut_file_jieba(inputfile, outputfile):
    outfileobj = open(outputfile, 'w+', encoding = 'utf-8')
    with open(inputfile, "r", encoding = "utf8") as f:
        for line in f:
            seg_list = jieba.cut(line.strip(), cut_all=False)
            outfileobj.write(" ".join(seg_list))
            outfileobj.write("\n")
            
gen_cut_file_jieba('test.enc', 'test_cut.enc')
gen_cut_file_jieba('test.dec', 'test_cut.dec')