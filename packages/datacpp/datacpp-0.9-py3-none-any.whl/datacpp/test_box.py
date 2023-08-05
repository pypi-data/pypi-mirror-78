import datacpp.dataloader as dataloader
import datacpp.libdatacpp as datacpp
import numpy as np
import cv2
import time

if __name__=="__main__":
    label_type=datacpp.LABEL_TYPE.DETECTION
    batch_size=32
    file_name="/home/wls/datasets/VOC/VOCdevkit/VOC2012/ImageSets/Main/train.txt"
    label_name="/home/wls/datasets/VOC/VOCdevkit/class.txt"
    image_dir="/home/wls/datasets/VOC/VOCdevkit/VOC2012/JPEGImages/"
    label_dir="/home/wls/datasets/VOC/VOCdevkit/VOC2012/Annotations/"
    batch=dataloader.data_batch(file_name,label_name,image_dir,label_dir,batch_size,label_type)
    epoch=300
    epoch_batch=batch.init_batch(epoch)
    for i in range(epoch*epoch_batch):
        start=time.time()
        batch_data=batch.next_batch()
        if batch_data is None:
            continue
        images=batch_data[0]
        labels=batch_data[1]
        for i in range(len(images)):
            height,width,_=images[i].shape
            images[i]*=0.2
            images[i]+=0.4
            images[i]*=255
            print("image:",images[i].astype(np.uint8))
            for j in range(len(labels[i])):
                box=labels[i][j]
                for t in range(4):
                    if t%2==0:
                        box[t]=int(box[t]*width)
                    else:
                        box[t]=int(box[t]*height)
                cv2.rectangle(images[i],(box[0],box[1]),(box[2],box[3]),(255,0,0),thickness=1)
                cv2.putText(images[i],str(box[4]),(box[0],box[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0))
            cv2.imshow("images:",images[i].astype(np.uint8))
            cv2.waitKey(0)

