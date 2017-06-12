# encoding=utf-8
#用jieba分词器分词 
#https://github.com/fxsjy/jieba
import jieba

#根据同义词生成一系列对话用于强化训练

#首先加载同义词，直接弄到内存里面去
synword_filename = "data/synword_test.txt"
synword_dict = {}

originalqa_filename = "data/data_ori.txt"

#从文件加载两两对应的同义词
with open(synword_filename, 'r', encoding="utf-8") as fp:
    for line in fp:
        words = line.split(" ")
        if(len(words) < 2):
            continue 
            
        if(words[0] in synword_dict):
            print (words[0])
            if(not words[1] in synword_dict[words[0]]):
                synword_dict[words[0]].append(words[1].strip())
        else:
            synword_dict[words[0]] = [words[1].strip()]

'''
--->file
大家 大伙儿
大家 米娜桑
星星 星辰

-->out
{'星星': ['星辰'], '大家': ['大伙儿', '米娜桑']}
'''

print (synword_dict)

#读取句子，根据分词结果，依次找每个词的同义词进行拼接
with open(originalqa_filename, 'r', encoding="utf-8") as fp:
    linecount = 0 #这个地方计数一下，看看速度怎么样
    for line in fp:
        seg_list = jieba.lcut(line.strip(), cut_all=False)
        print (seg_list)
        #enumerate的方式循环（PEP279）
        for index, singleword in enumerate(seg_list):
            if(singleword in synword_dict):
                #如果有的话就循环输出把这个词替换成所有的同义词
                for replaceword in synword_dict[singleword]:
                    front = ''.join(seg_list[:index])
                    behind = ''.join(seg_list[index+1:])
                    #测试环境先输出到标准输出
                    outputline = front + replaceword + behind
                    print(outputline)
            linecount = linecount + 1