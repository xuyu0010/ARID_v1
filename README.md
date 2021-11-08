# Framework for Action Recognition and Action Recognition in the Dark

This repository contains the framework for Action Recognition in the Dark.

## Prerequisites

This code is based on PyTorch, you may need to install the following packages:
```
PyTorch >= 0.4 (perfer 1.2 and above)
opencv-python (pip install)
PILLOW (pip install) (optional for optical flow)
scikit-video (optional for optical flow)
```

## Training

Train with initialization from pre-trained models:
```
python train_arid11.py --network <Network Name> --is-dark
```
There are a number of parameters that can be further tuned. We recommend a batch size of 16 per GPU.
We provide several networks that can be utilized, and can be found in the ```/network``` folder, change the ```--network``` parameter to toggle through the networks

## Testing

Evaluate the trained model:
```
cd test
python evaluate_video.py
```
If models with optical flow is used, the following command is used instead:
```
cd test
python evaluate_flow.py
```

## Other Information

<!-- - To download our dataset, click on [this link](https://xuyu0010.github.io/arid.html) -->
- To download the dataset, please write to xuyu0014@e.ntu.edu.sg for the download link. Thank you! [__Update!__]
- To view our paper, go to [this arxiv link](http://arxiv.org/abs/2006.03876)
- If you find our paper useful, please cite our paper:
```
@article{xu2020arid,
  title={ARID: A New Dataset for Recognizing Action in the Dark},
  author={Xu, Yuecong and Yang, Jianfei and Cao, Haozhi and Mao, Kezhi and Yin, Jianxiong and See, Simon},
  journal={arXiv preprint arXiv:2006.03876},
  year={2020}
}
```
- Our code base is adapted from [Multi-Fiber Network for Video Recognition](https://github.com/cypw/PyTorch-MFNet), we would like to thank the authors for providing the code base.
- You may contact me through xuyu0014@e.ntu.edu.sg
- This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
