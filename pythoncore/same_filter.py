# encoding=utf-8

#对两个文件处理，过滤掉在file1里的重复项，同时file2对应行也干掉.

def do_filter_two(file1_path, file2_path, file1_outpath, file2_outpath):
    history_in = {} #弄个dict用来放历史索引
    
    drop_count = 0
    total_line = 0
    
    wfp1 = open(file1_outpath, 'w+', encoding = "utf8")
    wfp2 = open(file2_outpath, 'w+', encoding = "utf8")
    
    with open(file1_path, 'r' , encoding="utf8") as fp1:
        with open(file2_path, 'r' , encoding="utf8") as fp2:
            for line1 in fp1:
                total_line = total_line + 1
                if(total_line % 50000 == 0):
                    print ("run for " + str(total_line) + " line(s)...")
                l2 = fp2.readline().strip()
                l1 = line1.strip()
                if(l1 in history_in):
                    drop_count = drop_count + 1
                    continue
                history_in[l1] = 1
                wfp1.write(l1)
                wfp1.write("\n")
                wfp2.write(l2)
                wfp2.write("\n")
                
    #关闭wfp1和wfp2
    wfp1.close()
    wfp2.close()
    
    print ("drop line:" + str(drop_count))
    print ("total line:" + str(total_line))
    

#do_filter_two('data/train.enc', 'data/train.dec', 'data/train_filtered.enc', 'data/train_filtered.dec')
do_filter_two('data/shot.enc', 'data/shot.dec', '/tmp/train_filtered.enc', '/tmp/train_filtered.dec')