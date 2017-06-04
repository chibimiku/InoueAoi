# 前一步生成的问答文件路径
train_encode_file = 'train.enc'
train_decode_file = 'train.dec'
test_encode_file = 'test.enc'
test_decode_file = 'test.dec'
 
print('开始创建词汇表...')
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
# 参看tensorflow.models.rnn.translate.data_utils
 
vocabulary_size = 5000
# 生成词汇表文件
# 注意这里可以用第三方的来搞
def gen_vocabulary_file(input_file, output_file):
	vocabulary = {}
	with open(input_file, encoding = "utf8") as f:
		counter = 0
		for line in f:
			counter += 1
			tokens = [word for word in line.strip()]
			for word in tokens:
				if word in vocabulary:
					vocabulary[word] += 1
				else:
					vocabulary[word] = 1
		vocabulary_list = START_VOCABULART + sorted(vocabulary, key=vocabulary.get, reverse=True)
		# 取前5000个常用汉字, 应该差不多够用了(额, 好多无用字符, 最好整理一下. 我就不整理了)
		if len(vocabulary_list) > 5000:
			vocabulary_list = vocabulary_list[:5000]
		print(input_file + " 词汇表大小:", len(vocabulary_list))
		with open(output_file, "w", encoding = "utf8") as ff:
			for word in vocabulary_list:
				ff.write(word + "\n")
 
gen_vocabulary_file(train_encode_file, "train_encode_vocabulary")
gen_vocabulary_file(train_decode_file, "train_decode_vocabulary")
