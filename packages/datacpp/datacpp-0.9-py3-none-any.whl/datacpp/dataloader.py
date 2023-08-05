import datacpp.pipeline as pipeline
import datacpp.libdatacpp as data

class data_batch:
    def __init__(self,file_name,label_name,image_dir,label_dir,batch_size,label_type):
        self.pipe=pipeline.pipeline(batch_size,file_name,label_name,image_dir,label_dir,label_type,heatmap=False)
    def init_batch(self,epoch):
        return self.pipe.producer(epoch)
    def next_batch(self):
        return self.pipe.consumer()