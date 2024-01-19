import cv2
import re
from matplotlib import pyplot

import numpy as np

class ImageWrapper:
    def __init__(self, img_path: str) -> None:
        self.img_path = img_path
    
    def load(self) -> None:
        pass
    
    def shape(self) -> tuple:
        pass
    
    def width(self) -> float:
        pass
    
    def height(self) -> float:
        pass
    
    def raw(self):
        pass
    
    def printformat(self):
        pass
    
    def annotate(self, boxes, labels):
        pass
    
    def imshow(self, plt: pyplot) -> None:
        pass

class CVImageWrapper(ImageWrapper):
    def __init__(
        self, img_path: str, 
        bbox_color = (36,255,12),
        bbox_thickness: int = 3,
        label_pos: int = -10,
        font_scale: float = 0.6,
        font_type=cv2.FONT_HERSHEY_SIMPLEX,
        label_color = (36,255,12),
        ) -> None:
        super().__init__(img_path)
        self.load()
        self.label_pos = label_pos
        self.font_scale = font_scale
        self.font_type = font_type
        self.bbox_thickness = bbox_thickness
        self.bbox_color = bbox_color
        self.label_color = label_color
    
    def load(self):
        self.raw_img = cv2.imread(self.img_path, cv2.IMREAD_ANYCOLOR)
        
    def shape(self) -> tuple:
        return self.raw_img.shape
    
    def width(self) -> int:
        return self.raw_img.shape[1]
    
    def height(self) -> int:
        return self.raw_img.shape[0]
    
    def depth(self) -> int:
        return self.raw_img.shape[2]
    
    def raw(self):
        return self.raw_img
    
    def printformat(self):
        return cv2.cvtColor(self.raw_img, cv2.COLOR_BGR2RGB)
    
    def _resolve_label_color(self, label, label_colors):
        if label_colors is None:
            return self.label_color
        
        return label_colors[label]
    
    def _resolve_bbox_color(self, bbox_index, labels, bbox_colors):
        if bbox_colors is None or labels is None:
            return self.bbox_color
        
        return bbox_colors[labels[bbox_index]]
    
    def annotate(self, boxes, labels=None, suppress_labels=False, bbox_colors=None, label_colors=None):
        img = self.raw_img
        for i, box in enumerate(boxes):
            img = cv2.rectangle(
                img,
                (int(box[0]), int(box[1])),
                (int(box[0]+box[2]), int(box[1]+box[3])),
                color=self._resolve_bbox_color(i, labels, bbox_colors),
                thickness=self.bbox_thickness
            )
            if not suppress_labels and labels is not None and len(labels) > i:
                img = cv2.putText(
                    img,
                    labels[i],
                    (int(box[0]), int(box[1]+self.label_pos)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=self.font_scale,
                    color=self._resolve_label_color(labels[i], label_colors),
                    thickness=2
                )
        return img
    
    def add_title(self, title):
        img = cv2.putText(
            self.raw_img,
            title,
            (self.width()/2-len(title)*2, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=self.font_scale,
            color=self.label_color,
            thickness=2
        )
        return img
    
    def denormalize_bboxes(self, bboxes : np.array):
        width, height = (self.width(), self.height())
        x_min = ((bboxes[:, 0] - bboxes[:, 2] / 2) * width).astype(int)
        y_min = ((bboxes[:, 1] - bboxes[:, 3] / 2) * height).astype(int)
        x_max = ((bboxes[:, 0] + bboxes[:, 2] / 2) * width).astype(int)
        y_max = ((bboxes[:, 1] + bboxes[:, 3] / 2) * height).astype(int)
        return np.column_stack((x_min, y_min, x_max - x_min, y_max - y_min))
    
    def normalize_bboxes(self, bboxes : np.array):
        x_min, x_max = bboxes[:, 0], bboxes[:, 0] + bboxes[:, 2]
        y_min, y_max = bboxes[:, 1], bboxes[:, 1] + bboxes[:, 3]
        
        x_c = (x_min + x_max) / 2 / self.width()
        y_c = (y_min + y_max) / 2 / self.height()
        
        w = (x_max - x_min) / self.width()
        h = (y_max - y_min) / self.height()
        
        return np.column_stack((x_c, y_c, w, h))
    
    def imshow(self, plt: pyplot) -> None:
        plt.imshow(self.printformat(), cmap = plt.cm.Spectral)
        plt.axis('off')
        plt.show(block=True)

import os
from pathlib import Path

class FileIterator:
    def __init__(self, dir, extensions=[]) -> None:
        self.dir = dir
        self.files = []
        
        for f in os.listdir(self.dir):
            if Path(f).suffix in extensions:
                self.files.append(f)
    
    def __len__(self):
        return len(self.files)
    
    def __getitem__(self, i):
        if i < len(self.files):
            return str(Path(self.dir) / self.files[i])
        else:
            raise IndexError('{} is out of {}'.format(i, len(self.files)))
    
    # def __iter__(self):
    #     self.current = 0
    #     return self
    
    # def __next__(self):
    #     self.current += 1
    #     if self.current < len(self.img_names):
    #         return self.current
    #     raise StopIteration

class ImageIterator(FileIterator):
    def __init__(self, dir, extensions=['.jpg', '.jpeg']) -> None:
        super(ImageIterator, self).__init__(dir, extensions)
        
class AnnFileReader:
    def __init__(self, ann_path) -> None:
        self.ann_path = ann_path
    
    def _read_all_lines(self) -> list:
        f = open(self.ann_path, "r")
        lines = f.readlines()
        f.close()
        return lines
    
    def _tokenize(self, line) -> np.array:
        tokens = re.split('\s+', line.strip())
        tokens = [int(t) for t in tokens]
        return np.array(tokens)
            
    def read(self):
        lines = self._read_all_lines()
        if len(lines) == 0:
            return np.array([])
        
        line_tokens = []
        for line in lines:
            tokens = re.split('\s+', line.strip())
            tokens = [float(t) for t in tokens]
            line_tokens.append(tokens)
            
        return np.array(line_tokens)

class AnnFileWriter:
    def __init__(self, ann_path, overwrite=True) -> None:
        self.ann_path = ann_path
        self.overwrite = True
    
    def _to_lines(self, bboxes: np.array) -> list:
        lines = []
        for bbox in bboxes:
            lines.append(' '.join([str(int(bbox[0]))]+[str(x) for x in bbox[1:]])+'\n')
        return lines
    
    def write(self, bboxes : np.array) -> None:
        ann_f = open(self.ann_path, "w" if self.overwrite else "a")
        ann_f.writelines(self._to_lines(bboxes))
        ann_f.close()
