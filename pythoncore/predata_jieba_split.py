# encoding=utf-8
import jieba

#用jieba再把数据分割成空格流

def gen_vocabulary_file_jieba(inputfile, outputfile):
    outfileobj = open(outputfile, 'w+', encoding = 'utf-8')
    with open(inputfile, encoding="utf-8") as f:
        for line in f:
            seg_list = jieba.cut(line.strip(), cut_all=False)
            outfileobj.write(" ".join(seg_list) + "\n")
            
gen_vocabulary_file_jieba('train.enc', 'train_cut.enc')
gen_vocabulary_file_jieba('train.dec', 'train_cut.dec')