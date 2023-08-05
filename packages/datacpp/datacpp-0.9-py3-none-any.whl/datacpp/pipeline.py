import datacpp.libdatacpp as data
import numpy as np
import time
class pipeline:
    def __init__(self,batch_size,file_name,label_name,image_dir,label_dir,label_type,\
        label_postfix=".xml",image_type=".jpg",out_h=640,out_w=640,shuffle=True,\
        que_size=10,thread_num=4,heatmap=True,out_flag=False):
        self.batch_size=batch_size
        self.file_name=file_name
        self.label_name=label_name
        self.image_dir=image_dir
        self.label_dir=label_dir
        self.label_type=label_type
        self.label_postfix=label_postfix
        self.image_type=image_type
        self.out_h=out_h
        self.out_w=out_w
        self.shuffle=shuffle
        self.thread_num=thread_num
        self.heatmap=heatmap
        self.out_flag=out_flag

    def producer(self,epoch): 
        self.batch_data=data.args_init(self.batch_size,self.out_h,self.out_w,self.image_dir,\
            self.label_dir,self.file_name,self.label_name,self.image_type,self.label_type,self.label_postfix,\
                self.heatmap, self.shuffle,self.thread_num,self.out_flag)
        data.start_producer(self.batch_data,epoch)
        batch_size = self.batch_data.get_batch_size()
        epoch_size = self.batch_data.get_epoch_size()
        return int(epoch_size/batch_size)
    def consumer(self,):
        batch=data.next_batch_detection()
        return [batch.images,batch.box_labels]