print("对话转向量...")

train_encode_vocabulary_file = 'train_encode_vocabulary'
train_decode_vocabulary_file = 'train_decode_vocabulary'

# 把对话字符串转为向量形式
def convert_to_vector(input_file, vocabulary_file, output_file):
	tmp_vocab = []
	with open(vocabulary_file, "r", encoding = "utf8") as f:
		tmp_vocab.extend(f.readlines())
	tmp_vocab = [line.strip() for line in tmp_vocab]
	vocab = dict([(x, y) for (y, x) in enumerate(tmp_vocab)])
	#{'硕': 3142, 'v': 577, 'Ｉ': 4789, '\ue796': 4515, '拖': 1333, '疤': 2201 ...}
	output_f = open(output_file, 'w', encoding = "utf8")
	with open(input_file, 'r', encoding = "utf8") as f:
		for line in f:
			line_vec = []
			for words in line.strip():
				line_vec.append(vocab.get(words, UNK_ID))
			output_f.write(" ".join([str(num) for num in line_vec]) + "\n")
	output_f.close()
 
convert_to_vector(train_encode_file, train_encode_vocabulary_file, 'train_encode.vec')
convert_to_vector(train_decode_file, train_decode_vocabulary_file, 'train_decode.vec')
 
convert_to_vector(test_encode_file, train_encode_vocabulary_file, 'test_encode.vec')
convert_to_vector(test_decode_file, train_decode_vocabulary_file, 'test_decode.vec')