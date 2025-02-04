# Copyright (c) OpenMMLab. All rights reserved.
import os.path as osp

import mmcv
import numpy as np
from PIL import Image

from .builder import DATASETS
from .custom import CustomDataset


@DATASETS.register_module()
class AI2ThorDataset(CustomDataset):
    """AI2ThorDataset dataset.

    In segmentation map annotation for ADE20K, 0 stands for background, which
    is not included in 120 categories. ``reduce_zero_label`` is fixed to True.
    The ``img_suffix`` is fixed to '.jpg' and ``seg_map_suffix`` is fixed to
    '.png'.
    """
    CLASSES = (
       'floor', 'alarmclock', 'apple', 'armchair', 'baseballbat', 'basketball', 'bathtub', 'bathtubbasin',
       'bed', 'blinds', 'book', 'boots', 'bowl', 'box', 'bread', 'butterknife', 'cabinet', 'candle', 'cart', 'cd', 
       'cellphone', 'chair', 'cloth', 'coffeemachine', 'countertop', 'creditcard', 'cup', 'curtains', 'desk', 'desklamp', 
       'dishsponge', 'drawer', 'dresser', 'egg', 'floorlamp', 'footstool', 'fork', 'fridge', 'garbagecan', 'glassbottle', 
       'handtowel', 'handtowelholder', 'houseplant', 'kettle', 'keychain', 'knife', 'ladle', 'laptop', 'laundryhamper', 
       'laundryhamperlid', 'lettuce', 'lightswitch', 'microwave', 'mirror', 'mug', 'newspaper', 'ottoman', 'painting', 'pan', 
       'papertowel', 'papertowelroll', 'pen', 'pencil', 'peppershaker', 'pillow', 'plate', 'plunger', 'poster', 'pot', 'potato', 
       'remotecontrol', 'safe', 'saltshaker', 'scrubbrush', 'shelf', 'showerdoor', 'showerglass', 'sink', 'sinkbasin', 'soapbar', 
       'soapbottle', 'sofa', 'spatula', 'spoon', 'spraybottle', 'statue', 'stoveburner', 'stoveknob', 'diningtable', 'coffeetable', 
       'sidetable', 'teddybear', 'television', 'tennisracket', 'tissuebox', 'toaster', 'toilet', 'toiletpaper', 'toiletpaperhanger', 
       'toiletpaperroll', 'tomato', 'towel', 'towelholder', 'tvstand', 'vase', 'watch', 'wateringcan', 'window', 'winebottle', 
       'applesliced', 'showercurtain', 'tomatosliced', 'lettucesliced', 'lamp', 'showerhead', 'eggcracked', 'breadsliced', 'potatosliced', 
       'faucet')

    PALETTE = [[120, 120, 120], [180, 120, 120], [6, 230, 230], [80, 50, 50],
               [4, 200, 3], [120, 120, 80], [140, 140, 140], [204, 5, 255],
               [230, 230, 230], [4, 250, 7], [224, 5, 255], [235, 255, 7],
               [150, 5, 61], [120, 120, 70], [8, 255, 51], [255, 6, 82],
               [143, 255, 140], [204, 255, 4], [255, 51, 7], [204, 70, 3],
               [0, 102, 200], [61, 230, 250], [255, 6, 51], [11, 102, 255],
               [255, 7, 71], [255, 9, 224], [9, 7, 230], [220, 220, 220],
               [255, 9, 92], [112, 9, 255], [8, 255, 214], [7, 255, 224],
               [255, 184, 6], [10, 255, 71], [255, 41, 10], [7, 255, 255],
               [224, 255, 8], [102, 8, 255], [255, 61, 6], [255, 194, 7],
               [255, 122, 8], [0, 255, 20], [255, 8, 41], [255, 5, 153],
               [6, 51, 255], [235, 12, 255], [160, 150, 20], [0, 163, 255],
               [140, 140, 140], [250, 10, 15], [20, 255, 0], [31, 255, 0],
               [255, 31, 0], [255, 224, 0], [153, 255, 0], [0, 0, 255],
               [255, 71, 0], [0, 235, 255], [0, 173, 255], [31, 0, 255],
               [11, 200, 200], [255, 82, 0], [0, 255, 245], [0, 61, 255],
               [0, 255, 112], [0, 255, 133], [255, 0, 0], [255, 163, 0],
               [255, 102, 0], [194, 255, 0], [0, 143, 255], [51, 255, 0],
               [0, 82, 255], [0, 255, 41], [0, 255, 173], [10, 0, 255],
               [173, 255, 0], [0, 255, 153], [255, 92, 0], [255, 0, 255],
               [255, 0, 245], [255, 0, 102], [255, 173, 0], [255, 0, 20],
               [255, 184, 184], [0, 31, 255], [0, 255, 61], [0, 71, 255],
               [255, 0, 204], [0, 255, 194], [0, 255, 82], [0, 10, 255],
               [0, 112, 255], [51, 0, 255], [0, 194, 255], [0, 122, 255],
               [0, 255, 163], [255, 153, 0], [0, 255, 10], [255, 112, 0],
               [143, 255, 0], [82, 0, 255], [163, 255, 0], [255, 235, 0],
               [8, 184, 170], [133, 0, 255], [0, 255, 92], [184, 0, 255],
               [255, 0, 31], [0, 184, 255], [0, 214, 255], [255, 0, 112],
               [92, 255, 0], [0, 224, 255], [112, 224, 255], [70, 184, 160],
               [163, 0, 255], [153, 0, 255], [71, 255, 0], [255, 0, 163],
               [255, 204, 0], [255, 0, 143], [0, 255, 235], [133, 255, 0],
               [255, 0, 235], [245, 0, 255], [255, 0, 122], [255, 245, 0],
               #[10, 190, 212], [214, 255, 0], [0, 204, 255], [20, 0, 255],
               #[255, 255, 0], [0, 153, 255], [0, 41, 255], [0, 255, 204],
               #[41, 0, 255], [41, 255, 0], [173, 0, 255], [0, 245, 255],
               #[71, 0, 255], [122, 0, 255], [0, 255, 184], [0, 92, 255],
               #[184, 255, 0], [0, 133, 255], [255, 214, 0], [25, 194, 194],
               [102, 255, 0], [92, 0, 255]]
    
    def __init__(self, **kwargs):
        super(AI2ThorDataset, self).__init__(
            img_suffix='.jpeg',
            seg_map_suffix='_mask_processed_gray.png',
            reduce_zero_label=True,
            **kwargs)

    def results2img(self, results, imgfile_prefix, to_label_id, indices=None):
        """Write the segmentation results to images.

        Args:
            results (list[list | tuple | ndarray]): Testing results of the
                dataset.
            imgfile_prefix (str): The filename prefix of the png files.
                If the prefix is "somepath/xxx",
                the png files will be named "somepath/xxx.png".
            to_label_id (bool): whether convert output to label_id for
                submission.
            indices (list[int], optional): Indices of input results, if not
                set, all the indices of the dataset will be used.
                Default: None.

        Returns:
            list[str: str]: result txt files which contains corresponding
            semantic segmentation images.
        """
        
        if indices is None:
            indices = list(range(len(self)))

        mmcv.mkdir_or_exist(imgfile_prefix)
        result_files = []
        for result, idx in zip(results, indices):

            filename = self.img_infos[idx]['filename']
            basename = osp.splitext(osp.basename(filename))[0]

            png_filename = osp.join(imgfile_prefix, f'{basename}.png')

            # The  index range of official requirement is from 0 to 150.
            # But the index range of output is from 0 to 149.
            # That is because we set reduce_zero_label=True.
            result = result + 1

            output = Image.fromarray(result.astype(np.uint8))
            output.save(png_filename)
            result_files.append(png_filename)

        return result_files

    def format_results(self,
                       results,
                       imgfile_prefix,
                       to_label_id=True,
                       indices=None):
        """Format the results into dir (standard format for ade20k evaluation).

        Args:
            results (list): Testing results of the dataset.
            imgfile_prefix (str | None): The prefix of images files. It
                includes the file path and the prefix of filename, e.g.,
                "a/b/prefix".
            to_label_id (bool): whether convert output to label_id for
                submission. Default: False
            indices (list[int], optional): Indices of input results, if not
                set, all the indices of the dataset will be used.
                Default: None.

        Returns:
            tuple: (result_files, tmp_dir), result_files is a list containing
               the image paths, tmp_dir is the temporal directory created
                for saving json/png files when img_prefix is not specified.
        """

        if indices is None:
            indices = list(range(len(self)))

        assert isinstance(results, list), 'results must be a list.'
        assert isinstance(indices, list), 'indices must be a list.'

        result_files = self.results2img(results, imgfile_prefix, to_label_id,
                                        indices)
        return result_files
