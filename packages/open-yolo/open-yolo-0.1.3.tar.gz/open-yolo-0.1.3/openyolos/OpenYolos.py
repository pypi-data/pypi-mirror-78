import time
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn

from models.datasets import LoadImages, letterbox
from models.experimental import attempt_load
from models.general import (check_img_size, non_max_suppression, scale_coords, xyxy2xywh, plot_one_box)
from models.torch_utils import select_device, time_synchronized


class OpenYolos:
    def __init__(self, model_path='../weights/yolov5x.pt'):
        self.model, self.image_size, self.device = self.load_model(model_path)
        pass

    def load_model(self, model_path, image_size=640):
        device = select_device('')
        model = attempt_load(model_path, map_location=device)  # load FP32 model
        image_size = check_img_size(image_size, s=model.stride.max())  # check img_size

        if device.type != 'cpu':
            model.half()  # to FP16

        img = torch.zeros((1, 3, image_size, image_size), device=device)  # init img
        _ = model(img.half() if device.type != 'cpu' else img) if device.type != 'cpu' else None

        return model, image_size, device

    def train(self):
        pass

    def predict(self, image):
        img = letterbox(image, new_shape=self.image_size)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.device.type != 'cpu' else img.float()  # uint8 to fp16/32
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        with torch.no_grad():
            pred = self.model(img, augment=False)[0]
        pred = non_max_suppression(pred, 0.4, 0.5)
        res = []
        for i, det in enumerate(pred):
            if det is not None and len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], image.shape).round()
                for x1, y1, x2, y2, conf, cls in det.numpy():
                    res.append(dict(type=int(cls), x1=x1, y1=y1, x2=x2, y2=y2, confidence=conf))
                    plot_one_box([x1, y1, x2, y2], image, label=str(int(cls)))
        cv2.imwrite("1.png", image)
        return res

    def inference(self, source='inference/images', out='inference/output'):
        save_img = True
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadImages(source, img_size=self.image_size)

        names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

        t0 = time.time()
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(self.device)
            img = img.half() if self.device.type != 'cpu' else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            t1 = time_synchronized()

            with torch.no_grad():
                pred = self.model(img, augment=False)[0]

            # Apply NMS
            conf_thres = 0.4
            iou_thres = 0.5
            pred = non_max_suppression(pred, conf_thres, iou_thres)
            t2 = time_synchronized()

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                p, s, im0 = path, '', im0s
                save_path = str(Path(out) / Path(p).name)
                txt_path = str(Path(out) / Path(p).stem) + ('_%g' % dataset.frame if dataset.mode == 'video' else '')
                s += '%gx%g ' % img.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if det is not None and len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += '%g %ss, ' % (n, names[int(c)])  # add to string

                    # Write results
                    save_txt = True
                    for *xyxy, conf, cls in det:
                        if save_txt:  # Write to file
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                            with open(txt_path + '.txt', 'a') as f:
                                f.write(('%g ' * 5 + '\n') % (cls, *xywh))  # label format

                        if save_img:  # Add bbox to image
                            label = '%s %.2f' % (names[int(cls)], conf)
                            plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)

                # Print time (inference + NMS)
                print('%sDone. (%.3fs)' % (s, t2 - t1))
                if save_img:
                    if dataset.mode == 'images':
                        cv2.imwrite(save_path, im0)
        print('Done. (%.3fs)' % (time.time() - t0))


if __name__ == '__main__':
    de = OpenYolos()
    # de.inference()
    img = cv2.imread("bus.jpg")
    res = de.predict(img)
    print(res)
