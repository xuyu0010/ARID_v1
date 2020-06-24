import os
import numpy as np
import cv2

def histogram_equalization(init_path, init_dirname):
    os.mkdir('clips_v1_GIC_HE')
    init_dir_path = os.path.join(init_path, init_dirname)
    new_dir_path = os.path.join(init_path, 'clips_v1_GIC_HE')

    for dirname in os.listdir(init_dir_path):
        if '.' in dirname or dirname == 'list_cvt_v1':
            continue
        init_class_path = os.path.join(init_dir_path, dirname)
        new_class_path = os.path.join(new_dir_path, dirname)
        os.mkdir(new_class_path)

        for file in os.listdir(init_class_path):
            if '.' in dirname or dirname == 'list_cvt_v1' or '.avi' not in file:
                continue
            
            init_clip_path = os.path.join(init_class_path, file)
            new_clip_path = os.path.join(new_class_path, file)

            cap = cv2.VideoCapture(init_clip_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
                    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            new_cap = cv2.VideoWriter(new_clip_path, cv2.VideoWriter_fourcc('X', '2', '6', '4'), fps, size)

            while(True):
                ret, frame = cap.read()
                if ret == True:
                    cache_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)
                    channels=cv2.split(cache_frame)
                    cv2.equalizeHist(channels[0], channels[0])
                    cv2.merge(channels, cache_frame)
                    frame = cv2.cvtColor(cache_frame, cv2.COLOR_YCrCb2BGR)
                    new_cap.write(frame)
                else:
                    print("Completed the processing of %s" %(file))
                    break

            cv2.destroyAllWindows()
            cap.release
            new_cap.release

if __name__ == '__main__':
    histogram_equalization(init_path=os.getcwd(), init_dirname="clips_v1_GIC")