import jieba

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