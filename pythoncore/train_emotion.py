import tensorflow as tf
import jieba
import jieba.analyse
from tensorflow.examples.tutorials.mnist import input_data
import common_utils
import data_utils
import random
import numpy as np

#这里放一系列的句子分析器用来提取句子的属性，例如分析句子情感成分。

#定义测试数据
test_sentence = ['今天去哪里吃比较好？', '这个东西真是讨厌极了。', '这个东西真可恶！', '数字罪大恶极，你是怎么看这东西的？', '这个是什么东西，看不明白。', '不要哭，没事的。']

def get_felling(sentence, model_path = 'data/models/emotion/'):
    #先载入模型
 
    #获取topwords
    topwords = jieba.analyse.extract_tags(sentence)
    print (topwords)

def train_feeling():
    #训练模型
    #《TensorFlow实践》第3章 tensorflow第一步
    vec_filename = 'data/emotion/sentence_vec.txt'
    emotion_vec = 'data/emotion/emotion_vec.txt'
    
    #设置默认模型目录
    default_module_dir = 'data/models/emotion/'

    #用典型的softmax regression模型来尝试推断这句话包含的情绪.
    #我们假定有6种基本情绪，愤怒、恐惧、惊讶、厌恶、快乐和悲伤，约定在标注时把这6个情绪编码为0-5
    
    sess = tf.InteractiveSession()
    #每句话假设长度为140字，定义输入长度就这样.后面的None表示不限制输入长度
    in_sentence = tf.placeholder(tf.float32, [None, 140])
    
    #初始化这两个变量保存weights和biases(这个情绪的偏移倾向)
    weight = tf.Variable(tf.zeros([140, 6]))
    biases = tf.Variable(tf.zeros([6]))
    
    #接下来用tf实现softmax regression算法
    #y = softmax(Wx + b)
    y = tf.nn.softmax(tf.matmul(in_sentence, weight) + biases)
    y_ = tf.placeholder(tf.float32, [None, 6])
    
    #reduce_xx系列是对tensor某一个维度上的数据进行运算求值，第一个参数input_tensor是输入的tensor，第二个参数reduction_indices是指在哪个维度上求值
    #reduce_mean是求平均值
    #cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
        
    '''
    minimize(
        loss,
        global_step=None,
        var_list=None,
        gate_gradients=GATE_OP,
        aggregation_method=None,
        colocate_gradients_with_ops=False,
        name=None,
        grad_loss=None
    )
    '''
    global_step = tf.Variable(0, name='global_step', trainable=False)
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy, global_step = global_step)
    
    sess = tf.InteractiveSession()
    #initialize_all_variables已被弃用
    
    #先检测以前是否存在固有的模型来恢复前一次训练
    
    saver = tf.train.Saver(max_to_keep = 2)
    ckpt = tf.train.get_checkpoint_state(default_module_dir)
    if ckpt != None:
        print ("checkpoint detected in " + default_module_dir)
        saver.restore(sess, ckpt.model_checkpoint_path)
    else:
        print ("checkpoint not found... start from first step.")
        tf.global_variables_initializer().run()
    
    #开始训练
    #在那之前要先弄一波数据，把数据转化为真实向量
    
    #从几个文件里load数据
    x_base = get_token_ids_from_file(vec_filename, 140)
    y__base = get_token_ids_from_file(emotion_vec, 6)
    
    
    max_step = 5
    for i in range(max_step):
        #每次随机取200个进行训练
        if(i > 0 and i % 500 == 0):
            print ("run for step:" +str(i))
        batch_xs, batch_ys = get_train_simples(200, x_base, y__base)
        sess.run(train_step, feed_dict={in_sentence: batch_xs, y_: batch_ys})
    
    print ("emotion training completed, step: " + str(max_step) + ", total step:" + str(global_step.eval()))
    #保存模型
    save_path = saver.save(sess, default_module_dir + "save_test.ckpt", global_step = global_step.eval())
    
    #验证模型？
    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    
    #最终输出验证模型的结果
    eval_xs, eval_ys = get_train_simples(5, x_base, y__base) #再从训练集里拿5个出来
    print ("test data accracy %g"%accuracy.eval(feed_dict={in_sentence: eval_xs, y_:eval_ys}))

#恢复模型
def recover_feeling(checkpoint):
    #设置变量
    in_sentence = tf.placeholder(tf.float32, [None, 140])
    
    weight = tf.Variable(tf.zeros([140, 6]))
    biases = tf.Variable(tf.zeros([6]))
    global_step = tf.Variable(0, name='global_step', trainable=False)

    #y = softmax(Wx + b)
    y = tf.nn.softmax(tf.matmul(in_sentence, weight) + biases)
    y_ = tf.placeholder(tf.float32, [None, 6])
    sess = tf.InteractiveSession()
    
    #恢复模型.
    saver = tf.train.Saver()
    saver.restore(sess, checkpoint)
    
    #读取模型完毕，加载词表
    vocab, tmp_vocab = read_vocabulary('data/emotion/vocabulary.txt')
    
    #把一些句子转化为vec的array
    vec_list1 = convert_sentence_to_vec_list('你今天感觉怎么样', vocab, 140)
    vec_list2 = convert_sentence_to_vec_list('高兴啊', vocab, 140)
    vec_list_final = [np.array(vec_list1), np.array(vec_list2)]
    print (vec_list_final)
    
    #交给sess进行检查
    data = np.array(vec_list_final)
    result = sess.run(y, feed_dict={in_sentence: data})
    print (result)

def convert_sentence_to_vec_list(sentence, vocab, length):
    word_list = jieba.lcut(sentence)
    vec_list = []
    for word in word_list:
        vec_list.append(vocab.get(word, '__UNK__'))
    if(len(vec_list) < length):
        for _ in range(length - len(vec_list)):
            vec_list.append(0)
    return vec_list
        
def read_vocabulary(input_file):
    tmp_vocab = []
    with open(input_file, "r", encoding="utf-8") as f:
        tmp_vocab.extend(f.readlines())
    tmp_vocab = [line.strip() for line in tmp_vocab]
    vocab = dict([(x, y) for (y, x) in enumerate(tmp_vocab)])
    return vocab, tmp_vocab    
    
def get_token_ids_from_line(line, length, fillzero = True):   
    el_count = 0
    data_str = line.split(" ")
    data_int = []
    for my_num in data_str:
        if(el_count >= length):
            #比预期多的话直接返回
            break
        data_int.append(int(my_num))
        el_count = el_count + 1
    if(el_count < length and fillzero):
        for _ in range(length - el_count):
            data_int.append(int(0)) #剩余部分填0
    return data_int
    
def get_token_ids_from_file(filepath, length, fillzero = True):
    data = []
    with open(filepath, 'r' ,encoding = "utf8") as fp:
        for line in fp:
            data.append(get_token_ids_from_line(line,length, fillzero))
    return data

def get_train_simples(num, list1, list2):
    #verify
    if(not len(list1) == len(list2)):
        print ("ERROR these 2 list length not equal.")
        return None
    new_list1 = []
    new_list2 = []
    tmp_list = range(0, len(list1)-1) #index坐标是0
    sample_id = random.sample(tmp_list, num)
    for id in sample_id:
        #这里把里面的list也转化为np的array，从list套list转为array套array.
        new_list1.append(np.array(list1[id]))
        new_list2.append(np.array(list2[id]))
    return (np.array(new_list1), np.array(new_list2))

def test_echo_mnist_single():
    mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)
    batch_xs, batch_ys = mnist.train.next_batch(2)
    
def gen_vecfile(outfile_filename, vocabulary_filename, emotion_filename, sentence_vec_filename):
    #分别读取6种情绪的文件，注意固定顺序:愤怒、恐惧、惊讶、厌恶、快乐和悲伤
    emotion_list = ['angry', 'scary', 'surprised', 'loath', 'happy', 'sorrowful']
    #0代表填充物
    rev_vocabulary = ['__PAD__', '__UNK__']
    #弄一个6个0组组成的list，在一号emo的时候填充为[1,0,0,0,0,0].其他类同，这件事也可以在训练前读取list的时候做，可以减少储存空间（只保存1个值就行了），这里统一格式方便理解。
    ori_score_list = [0,0,0,0,0,0] 
    
    emotion_obj = open(emotion_filename, 'w+', encoding = 'utf8')
    outfileobj = open(outfile_filename, 'w+', encoding = 'utf8')
    
    progress_line = 0
    for index, emo in enumerate(emotion_list):
        progress_line_par = 0
        #copy to emo_list
        emo_list = ori_score_list[:]    
        emo_list[index] = 1 #把这个对应情绪标记设置为1
        open_filename = 'data/emotion/' + emo + '.txt'
        with open(open_filename, 'r', encoding = 'utf8') as f:
            for line in f:
                seg_list = jieba.lcut(line.strip(), cut_all=False) #lcut直接拿list            
                #输出文件
                outfileobj.write(" ".join(seg_list))
                outfileobj.write("\n")
                #维护词表
                for single_seg in seg_list:
                    if(not single_seg in rev_vocabulary):
                        rev_vocabulary.append(single_seg)
                emotion_obj.write(" ".join(convert_to_str_list(emo_list))) 
                emotion_obj.write("\n")
                progress_line_par = progress_line_par + 1
        print ("[INFO]load emotion " + emo + " for " +str(progress_line_par) + " line(s)")
    outfileobj.close()
    emotion_obj.close()
    #写入词表文件
    with open(vocabulary_filename, 'w+', encoding = 'utf8') as fp:
        for word in rev_vocabulary:
            fp.write(word)
            fp.write("\n")
    #生成词典，文字为key，token_id为value
    vocab = dict([(x, y) for (y, x) in enumerate(rev_vocabulary)])
    #依词表将分词结果转化为向量
    #data_to_token_ids(data_path, target_path, vocabulary_path,tokenizer=None, normalize_digits=True):
    #data_utils.data_to_token_ids(outfile_filename,sentence_vec_filename,vocabulary_filename)
    with open(sentence_vec_filename, 'w+', encoding = 'utf8') as sentence_vec_fp:
        with open(outfile_filename, 'r', encoding = 'utf8') as outfile_filename_fp: #打开被cut的文件
            cut_linecount = 0
            for line in outfile_filename_fp:
                word_split = line.split(' ')
                token_id_list = []
                for my_word in word_split:
                    token_id_list.append(str(vocab.get(my_word, 0)))
                sentence_vec_fp.write(" ".join(token_id_list))
                sentence_vec_fp.write("\n")
                cut_linecount = cut_linecount + 1
    print ("file " + outfile_filename + " converted to " + str(cut_linecount) + " line(s)")
    
def convert_to_str_list(in_list):
    new_list = []
    for el in in_list:
        new_list.append(str(el))
    return new_list
            
#生成数据文件，这个只用跑一次就行
#gen_vecfile('data/emotion/sentence_cut.txt', 'data/emotion/vocabulary.txt', 'data/emotion/emotion_vec.txt', 'data/emotion/sentence_vec.txt')
#test_echo_mnist_single()
train_feeling()
#recover_feeling('data/models/emotion/save_test.ckpt')