from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from urllib.parse import urlparse
import tensorflow as tf
import seq2seq_model
import os
import numpy as np

import jieba

port = 9999

class TestClassA1():
    def __init__(self):
        self.value = 1
        
    def get_value(self):
        return self.value

class Chatbot():
    def __init__(self, ckppath, train_encode_vocabulary, train_decode_vocabulary):
        print ("load vocabulary...")
        self.vocab_en, _, vocabulary_encode_size = self._read_vocabulary(train_encode_vocabulary)
        _, self.vocab_de, vocabulary_decode_size = self._read_vocabulary(train_decode_vocabulary)
        #vocabulary_encode_size = 218436
        #vocabulary_decode_size = 257986
         
        self.buckets = [(5, 10), (10, 15), (20, 25), (40, 50)]
        layer_size = 768  # 每层大小
        num_layers = 5   # 层数
        batch_size =  1
        
        self.model = seq2seq_model.Seq2SeqModel(source_vocab_size=vocabulary_encode_size, target_vocab_size=vocabulary_decode_size,
                                   buckets=self.buckets, size=layer_size, num_layers=num_layers, max_gradient_norm= 5.0,
                                   batch_size=batch_size, learning_rate=0.5, learning_rate_decay_factor=0.99, forward_only=True, use_lstm=False)       
        self.model.batch_size = 1
        
        print ("start to inst tensorflow session...")
        self.sess = tf.Session()
        ckpt = tf.train.get_checkpoint_state(ckppath)
        if ckpt != None:
            print("Load ckpt from " + ckpt.model_checkpoint_path)
            self.model.saver.restore(self.sess, ckpt.model_checkpoint_path)
        print ("tensorflow module loading completed.")
        
    def _read_vocabulary(self, input_file, my_encoding = "utf-8"):
        tmp_vocab = []
        with open(input_file, "r", encoding=my_encoding) as f:
            readlines_result = f.readlines()
            tmp_vocab.extend(readlines_result)
        tmp_vocab = [line.strip() for line in tmp_vocab]
        vocab = dict([(x, y) for (y, x) in enumerate(tmp_vocab)])
        return vocab, tmp_vocab, len(readlines_result)
        
    def get_respon(self, input_string, debug = True):
        PAD_ID = 0
        GO_ID = 1
        EOS_ID = 2
        UNK_ID = 3
        
        input_string_vec = []
        #cut word.
        cut_word = jieba.lcut(input_string)
        #for words in input_string.strip():
        for words in cut_word:
            input_string_vec.append(self.vocab_en.get(words, UNK_ID))
        bucket_id_list = [b for b in range(len(self.buckets)) if self.buckets[b][0] > len(input_string_vec)]
        if(len(bucket_id_list) < 1):
            bucket_id_list = [3] #fix if bucket_id empty...
        bucket_id = min(bucket_id_list)
        print ("[DEBUG]bucket_id:" + str(bucket_id))
        encoder_inputs, decoder_inputs, target_weights = self.model.get_batch({bucket_id: [(input_string_vec, [])]}, bucket_id)
        _, _, output_logits = self.model.step(self.sess, encoder_inputs, decoder_inputs, target_weights, bucket_id, True)
        outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]
        if EOS_ID in outputs:
            outputs = outputs[:outputs.index(EOS_ID)]
        outputs_fixed = []
        #remove string occured repeatly.
        last_put_word = ""
        for single_el in outputs:
            if(not single_el == last_put_word):
                outputs_fixed.append(single_el)
                last_put_word = single_el
        final_out_list = [tf.compat.as_str(self.vocab_de[output]) for output in outputs_fixed]
        if(debug):
            print " / ".join(final_out_list)
        response = "".join(final_out_list)
        return response
        
class MyhandlerAoi(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            query = urlparse(self.path).query
            qc_splited = query.split("&")
            #installize query_components
            query_components = dict()
            for qc in qc_splited:
                rs = qc.split("=")
                if(len(rs) == 2):
                    query_components[rs[0]] = rs[1]
            if(rs["custword"]):
                result_content = bot.get_respon(rs["custword"])
            else:
                result_content = "input error..."
            self.send_response(200)
            
            self.send_header('Content-type','text/html')
            self.end_headers()
            
            self.wfile.write(result_content.encode("utf-8"))
            print (query_components)
            return
        except Exception as ex:
            #print (ex)
            raise ex

    def do_GET(self):
        print ("got a request...")
        try:
            query = urlparse(self.path).query
            qc_splited = query.split("&")
            #installize query_components
            query_components = dict()
            for qc in qc_splited:
                rs = qc.split("=")
                if(len(rs) == 2):
                    query_components[rs[0]] = rs[1]
            if("custword" in query_components):
                
                #result_content = "中文测试"
                #print (query_components["custword"])
                myinput = urllib.parse.unquote(query_components["custword"])
                result_content = bot.get_respon(myinput)
                print (myinput)
            else:
                result_content = "input error..."
            print (result_content)
            self.send_response(200)
            self.send_header('Content-type','text/html; charset=utf-8')
            self.end_headers()
            #self.wfile.write(bytes("<!DOCTYPE html><head><meta charset=\"utf-8\"></head><body><h1>Device Static Content</h1></body>", "utf-8"))
            self.wfile.write("{\"response\":\"".encode("utf-8"))
            self.wfile.write(result_content.encode("utf-8"))
            self.wfile.write("\"}".encode("utf-8"))
            #self.wfile.write("</body>".encode("utf-8"))
            print (query_components)
            return
        except Exception as ex:
            #print (ex)
            raise ex

def run(port, server_class=HTTPServer, handler_class=MyhandlerAoi):
    try:
        global var1 
        var1 = TestClassA1()
        #use bot~~
        global bot
        bot = Chatbot('data/chatbot_models/', 'data/chatbot_models/train_encode_vocabulary', 'data/chatbot_models/train_decode_vocabulary')
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print ("prepare http server on port:" + str(port))
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()
    
if __name__=='__main__':
    run(port)