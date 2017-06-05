import data_utils

# 前一步生成的问答文件路径
train_encode_file = 'train.enc'
train_decode_file = 'train.dec'
test_encode_file = 'test.enc'
test_decode_file = 'test.dec'

encoding_vocabulary_filename = 'train_encode_vocabulary'
decoding_vocabulary_filename = 'train_decode_vocabulary'

data_utils.data_to_token_ids(train_encode_file, 'train_encode_many.vec', encoding_vocabulary_filename)

