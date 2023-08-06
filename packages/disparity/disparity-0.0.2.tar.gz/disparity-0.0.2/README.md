```python
# default_exp disparity
```

# Disparity


```python
# export
import numba
import numpy as np

from camera_calib.utils import *
```


```python
import re
from pathlib import Path
import matplotlib.pyplot as plt

import torch
```

# Utilities


```python
def _parse_name(name_img):
    match = re.match(r'''SERIAL_(?P<serial>.*)_
                         DATETIME_(?P<date>.*)_
                         CAM_(?P<cam>.*)_
                         FRAMEID_(?P<frameid>.*)_
                         COUNTER_(?P<counter>.*).png''', 
                     name_img, 
                     re.VERBOSE)
    return match.groupdict()
```


```python
def _get_imgs(dir_imgs):
    imgs = []
    for file_img in dir_imgs.glob('*.png'):
        dict_group = _parse_name(file_img.name)
        img = api.File16bitImg(file_img)
        img.idx_cam = int(dict_group['cam'])-1
        img.idx_cb  = int(dict_group['counter'])-1
        imgs.append(img)
    return imgs
```


```python
def _print_imgs(imgs): 
    for img in imgs: print(f'{img.name} - cam: {img.idx_cam} - cb: {img.idx_cb}')
```

# Compute disparity map

First, we need to calibrate, then rectify, and then we can compute disparity maps.

## Calibrate


```python
import camera_calib.api as api
```


```python
imgs = _get_imgs(Path('data/calib'))
_print_imgs(imgs)
```

    SERIAL_19061245_DATETIME_2020-08-16-16:58:39-927381_CAM_1_FRAMEID_0_COUNTER_1 - cam: 0 - cb: 0
    SERIAL_16276941_DATETIME_2020-08-16-16:58:53-756240_CAM_2_FRAMEID_0_COUNTER_2 - cam: 1 - cb: 1
    SERIAL_16276941_DATETIME_2020-08-16-16:58:39-927424_CAM_2_FRAMEID_0_COUNTER_1 - cam: 1 - cb: 0
    SERIAL_16276941_DATETIME_2020-08-16-16:59:05-367688_CAM_2_FRAMEID_0_COUNTER_3 - cam: 1 - cb: 2
    SERIAL_19061245_DATETIME_2020-08-16-16:59:59-403047_CAM_1_FRAMEID_0_COUNTER_4 - cam: 0 - cb: 3
    SERIAL_16276941_DATETIME_2020-08-16-17:00:14-283298_CAM_2_FRAMEID_0_COUNTER_5 - cam: 1 - cb: 4
    SERIAL_19061245_DATETIME_2020-08-16-16:58:53-756222_CAM_1_FRAMEID_0_COUNTER_2 - cam: 0 - cb: 1
    SERIAL_16276941_DATETIME_2020-08-16-16:59:59-403092_CAM_2_FRAMEID_0_COUNTER_4 - cam: 1 - cb: 3
    SERIAL_19061245_DATETIME_2020-08-16-16:59:05-367645_CAM_1_FRAMEID_0_COUNTER_3 - cam: 0 - cb: 2
    SERIAL_19061245_DATETIME_2020-08-16-17:00:14-283252_CAM_1_FRAMEID_0_COUNTER_5 - cam: 0 - cb: 4



```python
h_cb = 50.8
w_cb = 50.8
h_f = 42.672
w_f = 42.672
num_c_h = 16
num_c_w = 16
spacing_c = 2.032
cb_geom = api.CbGeom(h_cb, w_cb,
                     api.CpCSRGrid(num_c_h, num_c_w, spacing_c),
                     api.FmCFPGrid(h_f, w_f))
```


```python
file_model = Path('models/dot_vision_checker.pth')
detector = api.DotVisionCheckerDLDetector(file_model)
```


```python
refiner = api.OpenCVCheckerRefiner(hw_min=5, hw_max=15, cutoff_it=20, cutoff_norm=1e-3)
```


```python
calib = api.multi_calib(imgs, cb_geom, detector, refiner)
```

    Refining control points for: SERIAL_19061245_DATETIME_2020-08-16-16:58:39-927381_CAM_1_FRAMEID_0_COUNTER_1...
    Refining control points for: SERIAL_19061245_DATETIME_2020-08-16-16:59:59-403047_CAM_1_FRAMEID_0_COUNTER_4...
    Refining control points for: SERIAL_19061245_DATETIME_2020-08-16-16:58:53-756222_CAM_1_FRAMEID_0_COUNTER_2...
    Refining control points for: SERIAL_19061245_DATETIME_2020-08-16-16:59:05-367645_CAM_1_FRAMEID_0_COUNTER_3...
    Refining control points for: SERIAL_19061245_DATETIME_2020-08-16-17:00:14-283252_CAM_1_FRAMEID_0_COUNTER_5...
    Refining single parameters...
     - Iteration: 000 - Norm:    0.05166 - Loss:   40.43536
     - Iteration: 001 - Norm:    0.05871 - Loss:   27.05900
     - Iteration: 002 - Norm:    0.10641 - Loss:   16.14479
     - Iteration: 003 - Norm:    0.52404 - Loss:    9.86104
     - Iteration: 004 - Norm:    0.70472 - Loss:    5.50705
     - Iteration: 005 - Norm:    0.15078 - Loss:    5.39712
     - Iteration: 006 - Norm:    0.02470 - Loss:    5.38315
     - Iteration: 007 - Norm:    0.01638 - Loss:    5.37218
     - Iteration: 008 - Norm:    0.00468 - Loss:    5.37189
     - Iteration: 009 - Norm:    0.13333 - Loss:    5.36454
     - Iteration: 010 - Norm:    0.00423 - Loss:    5.36439
     - Iteration: 011 - Norm:   28.76676 - Loss:    3.86312
     - Iteration: 012 - Norm:   17.23997 - Loss:    3.17776
     - Iteration: 013 - Norm:    0.00853 - Loss:    3.17776
     - Iteration: 014 - Norm:    0.00000 - Loss:    3.17776
    Refining control points for: SERIAL_16276941_DATETIME_2020-08-16-16:58:53-756240_CAM_2_FRAMEID_0_COUNTER_2...
    Refining control points for: SERIAL_16276941_DATETIME_2020-08-16-16:58:39-927424_CAM_2_FRAMEID_0_COUNTER_1...
    Refining control points for: SERIAL_16276941_DATETIME_2020-08-16-16:59:05-367688_CAM_2_FRAMEID_0_COUNTER_3...
    Refining control points for: SERIAL_16276941_DATETIME_2020-08-16-17:00:14-283298_CAM_2_FRAMEID_0_COUNTER_5...
    Refining control points for: SERIAL_16276941_DATETIME_2020-08-16-16:59:59-403092_CAM_2_FRAMEID_0_COUNTER_4...
    Refining single parameters...
     - Iteration: 000 - Norm:    0.04648 - Loss:   33.60078
     - Iteration: 001 - Norm:    0.03970 - Loss:   26.93946
     - Iteration: 002 - Norm:    0.04580 - Loss:   24.62314
     - Iteration: 003 - Norm:    0.14923 - Loss:   21.53392
     - Iteration: 004 - Norm:    0.48321 - Loss:   13.00884
     - Iteration: 005 - Norm:    0.00873 - Loss:   12.83886
     - Iteration: 006 - Norm:    0.65804 - Loss:    8.40447
     - Iteration: 007 - Norm:    0.10469 - Loss:    8.11526
     - Iteration: 008 - Norm:    0.09923 - Loss:    8.02833
     - Iteration: 009 - Norm:    0.09764 - Loss:    7.97387
     - Iteration: 010 - Norm:    0.18271 - Loss:    7.92175
     - Iteration: 011 - Norm:    9.62275 - Loss:    7.45953
     - Iteration: 012 - Norm:   37.67393 - Loss:    5.66647
     - Iteration: 013 - Norm:    1.13521 - Loss:    5.66112
     - Iteration: 014 - Norm:    0.01024 - Loss:    5.66107
     - Iteration: 015 - Norm:  142.51304 - Loss:    3.52503
     - Iteration: 016 - Norm:    0.29318 - Loss:    3.52483
     - Iteration: 017 - Norm:    0.00000 - Loss:    3.52483
    Refining multi parameters...
     - Iteration: 000 - Norm:    0.00633 - Loss:  365.50887
     - Iteration: 001 - Norm:    0.03670 - Loss:  251.90410
     - Iteration: 002 - Norm:    0.03891 - Loss:  191.50267
     - Iteration: 003 - Norm:    0.03330 - Loss:  169.51325
     - Iteration: 004 - Norm:    0.14800 - Loss:  115.86002
     - Iteration: 005 - Norm:    0.03182 - Loss:   99.71262
     - Iteration: 006 - Norm:    0.09812 - Loss:   78.23173
     - Iteration: 007 - Norm:    0.12045 - Loss:   50.32390
     - Iteration: 008 - Norm:    0.02356 - Loss:   45.52809
     - Iteration: 009 - Norm:    0.00880 - Loss:   44.19760
     - Iteration: 010 - Norm:    0.03753 - Loss:   40.63650
     - Iteration: 011 - Norm:    0.03345 - Loss:   37.87511
     - Iteration: 012 - Norm:    0.01658 - Loss:   36.71647
     - Iteration: 013 - Norm:    0.02828 - Loss:   34.62113
     - Iteration: 014 - Norm:    0.05827 - Loss:   30.72548
     - Iteration: 015 - Norm:    0.00558 - Loss:   30.46024
     - Iteration: 016 - Norm:    0.00377 - Loss:   30.32508
     - Iteration: 017 - Norm:    0.01700 - Loss:   29.78092
     - Iteration: 018 - Norm:    0.00733 - Loss:   29.58850
     - Iteration: 019 - Norm:    0.16740 - Loss:   25.31908
     - Iteration: 020 - Norm:    0.02405 - Loss:   24.72751
     - Iteration: 021 - Norm:    0.00133 - Loss:   24.69757
     - Iteration: 022 - Norm:    0.00339 - Loss:   24.62627
     - Iteration: 023 - Norm:    0.00355 - Loss:   24.59673
     - Iteration: 024 - Norm:    0.04353 - Loss:   24.94890
     - Iteration: 025 - Norm:    0.04560 - Loss:   24.23809
     - Iteration: 026 - Norm:    0.04802 - Loss:   24.02517
     - Iteration: 027 - Norm:    0.00035 - Loss:   24.02463
     - Iteration: 028 - Norm:    0.00095 - Loss:   24.02313
     - Iteration: 029 - Norm:    0.07848 - Loss:   23.82852
     - Iteration: 030 - Norm:    0.06296 - Loss:   23.67669
     - Iteration: 031 - Norm:    0.00122 - Loss:   23.67818
     - Iteration: 032 - Norm:    0.01764 - Loss:   23.65771
     - Iteration: 033 - Norm:    0.53306 - Loss:   23.11532
     - Iteration: 034 - Norm:    0.00389 - Loss:   23.11467
     - Iteration: 035 - Norm:    0.00026 - Loss:   23.11465
     - Iteration: 036 - Norm:    0.00855 - Loss:   23.11144
     - Iteration: 037 - Norm:    0.04346 - Loss:   23.09543
     - Iteration: 038 - Norm:    0.00329 - Loss:   23.09395
     - Iteration: 039 - Norm:    0.00014 - Loss:   23.09395
     - Iteration: 040 - Norm:    0.00550 - Loss:   23.09309
     - Iteration: 041 - Norm:    0.11960 - Loss:   23.05538
     - Iteration: 042 - Norm:    0.21922 - Loss:   22.99648
     - Iteration: 043 - Norm:    0.00130 - Loss:   22.99645
     - Iteration: 044 - Norm:    0.00077 - Loss:   22.99642
     - Iteration: 045 - Norm:    0.04483 - Loss:   22.98557
     - Iteration: 046 - Norm:    7.57304 - Loss:   21.17649
     - Iteration: 047 - Norm:   10.45625 - Loss:   18.59859
     - Iteration: 048 - Norm:    0.76570 - Loss:   18.39438
     - Iteration: 049 - Norm:    0.01591 - Loss:   18.39388
     - Iteration: 050 - Norm:    0.01743 - Loss:   18.39040
     - Iteration: 051 - Norm:    4.64610 - Loss:   17.20502
     - Iteration: 052 - Norm:    2.02334 - Loss:   16.86937
     - Iteration: 053 - Norm:    0.00002 - Loss:   16.86937
     - Iteration: 054 - Norm:    0.02372 - Loss:   16.86879
     - Iteration: 055 - Norm:    2.26827 - Loss:   16.59826
     - Iteration: 056 - Norm:   29.46264 - Loss:   13.48704
     - Iteration: 057 - Norm:    2.88659 - Loss:   13.25918
     - Iteration: 058 - Norm:    0.04408 - Loss:   13.25897
     - Iteration: 059 - Norm:    0.00140 - Loss:   13.25896
     - Iteration: 060 - Norm:    0.00002 - Loss:   13.25896
     - Iteration: 061 - Norm:    0.00000 - Loss:   13.25896



```python
api.plot_residuals(calib);
```


![png](README_files/README_17_0.png)



```python
api.plot_extrinsics(calib);
```


![png](README_files/README_18_0.png)



```python
api.save(calib, 'data/calib/calib.pth')
```

Freeze above and just load


```python
calib = api.load('data/calib/calib.pth')
```

## Rectify


```python
from image_rect import image_rect
```


```python
imgs = _get_imgs(Path('data/scene1'))
_print_imgs(imgs)
```

    SERIAL_19061245_DATETIME_2020-08-16-17:05:28-278345_CAM_1_FRAMEID_0_COUNTER_1 - cam: 0 - cb: 0
    SERIAL_16276941_DATETIME_2020-08-16-17:05:28-278389_CAM_2_FRAMEID_0_COUNTER_1 - cam: 1 - cb: 0



```python
[img1] = [img for img in imgs if img.idx_cam == 0]
[img2] = [img for img in imgs if img.idx_cam == 1]
img1.name, img2.name
```




    ('SERIAL_19061245_DATETIME_2020-08-16-17:05:28-278345_CAM_1_FRAMEID_0_COUNTER_1',
     'SERIAL_16276941_DATETIME_2020-08-16-17:05:28-278389_CAM_2_FRAMEID_0_COUNTER_1')




```python
rect = image_rect.rectify(calib)
```


```python
with torch.no_grad():
    arr1_r = image_rect.rect_img(img1, rect)
    arr2_r = image_rect.rect_img(img2, rect)
```


```python
_, axs = plt.subplots(1, 2, figsize=(20,15))
axs[0].imshow(arr1_r, cmap='gray')
axs[1].imshow(arr2_r, cmap='gray')
```




    <matplotlib.image.AxesImage at 0x7fa3e6d66fd0>




![png](README_files/README_28_1.png)


## Disparity

Do initial resize to make processing faster; also note that I'm doing the rest in numba/numpy since a lot of nested for loops are involved.

NOTE: numba does not yet support classes with inheritance, so I've used functions as first class citizens for now


```python
arr1, arr2 = [imresize(torch2np(arr), shape(arr)/4) for arr in [arr1_r, arr2_r]]
```


```python
_, axs = plt.subplots(1, 2, figsize=(10,10))
for arr, ax in zip([arr1, arr2], axs): ax.imshow(arr)
```


![png](README_files/README_32_0.png)


### Basic block matching

sum of absolute difference is a common loss function for disparity maps


```python
# export
@numba.jit(nopython=True)
def SAD(arr1, arr2):
    l = 0
    for i in range(arr1.shape[0]):
        for j in range(arr2.shape[1]):
            l += abs(arr1[i,j] - arr2[i,j])
    return l
```

`rect_loss_p` will compute the loss for a single point and store the losses in a buffer


```python
# export
@numba.jit(nopython=True)
def rect_loss_p(arr1, arr2, x, y, hw, min_disp, max_disp, loss, buf_loss):
    h_arr, w_arr = arr1.shape[0], arr1.shape[1]

    l_t, t_t, r_t, b_t = max(x-hw, 0), max(y-hw, 0), min(x+hw, w_arr-1), min(y+hw, h_arr-1)
    h_t, w_t = b_t-t_t+1, r_t-l_t+1
    for j in range(max(-l_t, min_disp), min(w_arr-r_t, max_disp+1)):
        buf_loss[j-min_disp] = loss(arr1[t_t:t_t+h_t, l_t:l_t+w_t], arr2[t_t:t_t+h_t, j+l_t:j+l_t+w_t])
```

`argmin_int` is the integer argument minimum; `int` suffix is only used to distinguish between subpixel minimum, which is used later.


```python
# export
@numba.jit(nopython=True)
def argmin_int(arr): return np.argmin(arr)
```

Test out getting the loss for an example point


```python
def _debug_rect_loss_p(x, y):
    buf_loss = np.full(max_disp-min_disp+1, np.inf)
    rect_loss_p(arr1, arr2, x, y, hw, min_disp, max_disp, loss, buf_loss)
    disp = argmin(buf_loss) + min_disp
    _, axs = plt.subplots(1, 2, figsize=(10,10))
    axs[0].imshow(arr1)
    axs[0].plot(x, y, 'rs')
    axs[1].imshow(arr2)
    axs[1].plot(x+disp, y, 'rs')
```


```python
hw = 15
min_disp = -15
max_disp =  15
loss = SAD
argmin = argmin_int
_debug_rect_loss_p(x=60, y=75)
```


![png](README_files/README_42_0.png)


`rect_loss_l` will compute the loss for an entire line. Note that an initial disparity map guess can also be input; if this is the case, then the disparity range will be centered around this disparity value instead of zero.


```python
# export
@numba.jit(nopython=True)
def rect_loss_l(arr1, arr2, y, hw, r_disp, loss, arr_disp_init=None):
    h_arr, w_arr = arr1.shape[0], arr1.shape[1]

    buf_loss = np.full((w_arr, r_disp[1]-r_disp[0]+1), np.inf)
    for i in range(w_arr):
        disp_init = 0 if arr_disp_init is None else arr_disp_init[y, i]
        min_disp, max_disp = [disp + disp_init for disp in r_disp]
        rect_loss_p(arr1, arr2, i, y, hw, min_disp, max_disp, loss, buf_loss[i, :])
    return buf_loss
```


```python
def _debug_rect_loss_l(y):
    buf_loss = rect_loss_l(arr1, arr2, y, hw, r_disp, loss)
    _, ax = plt.subplots(1, 1, figsize=(10,10))
    ax.imshow(buf_loss.T)
    return buf_loss
```


```python
r_disp = (-15, 15)
```


```python
_debug_rect_loss_l(60);
```


![png](README_files/README_47_0.png)


Note in the above (transposed) loss buffer, the `argmin` will be done column-wise, which could be a problem near column ~125 since there are two minima there.

`min_path_int` will compute the path from left to right of transposed loss buffer using the minimum value in each column.


```python
# export
@numba.jit(nopython=True)
def min_path_int(arr_loss, buf_path):
    for i in range(len(arr_loss)):
        buf_path[i] = argmin_int(arr_loss[i, :])
```

`rect_match_arr` will compute a disparity map. It takes an input `min_path` function which, when given a loss buffer, will compute the best path across it; this will make more sense when we use dynamic programming. `arr_disp_init` is an initial guess for the disparity map; this will make more sense when we do the image pyramids. 

Note that this seems to be the level where multi-threading makes sense; it's not too fine grained where overhead will slow things down and it's not too grainular such that a single thread can cause a long delay.


```python
# export
@numba.jit(nopython=True, parallel=True)
def rect_match_arr(arr1, arr2, hw, r_disp, loss, min_path, arr_disp_init=None):
    h_arr, w_arr = arr1.shape[0], arr1.shape[1]
    
    arr_disp = np.empty((h_arr, w_arr))
    for i in numba.prange(h_arr):
        buf_loss = rect_loss_l(arr1, arr2, i, hw, r_disp, loss, arr_disp_init)
        min_path(buf_loss, arr_disp[i,:]) # range offset and initial disparity need to be applied after
        arr_disp[i,:] += r_disp[0]                                       
        if arr_disp_init is not None: arr_disp[i,:] += arr_disp_init[i,:]
    return arr_disp
```


```python
arr_disp = rect_match_arr(arr1, arr2, hw, r_disp, loss, min_path_int)
```

Do it again so numba will compile and run faster.


```python
arr_disp = rect_match_arr(arr1, arr2, hw, r_disp, loss, min_path_int)
```

~200 ms is not bad. This could be realtime-ish performance for this image resolution.


```python
_, axs = plt.subplots(1, 2, figsize=(15,10))
axs[0].imshow(arr_disp, vmin=min_disp, vmax=max_disp)
axs[1].imshow(arr1)
axs[1].imshow(arr_disp, vmin=min_disp, vmax=max_disp, alpha=0.5)
```




    <matplotlib.image.AxesImage at 0x7fa3deccce50>




![png](README_files/README_57_1.png)


As to be expected this doesn't look great; lets debug some problem areas


```python
_debug_rect_loss_p(125, 60)
```


![png](README_files/README_59_0.png)


There is confusion with similar patterns. Note the found point on the right image is 3 stripes other rather than 2 on the left image.


```python
_debug_rect_loss_p(125, 25)
```


![png](README_files/README_61_0.png)


Glare causes an issue; note the point on the right image is aligned to the glare instead of where it should be


```python
_debug_rect_loss_p(45, 100)
```


![png](README_files/README_63_0.png)


This is actually wrong since the left part of the object is not visible to the right camera. It's more aligned to the side of the object rather than its actual location.


```python
_debug_rect_loss_p(60, 125)
```


![png](README_files/README_65_0.png)


This might be due to the fact that sub images are not normalized (mean subtracted and divided by std-dev) before being compared.

### Subpixel block matching

`argmin_sub` uses a single newton's iteration to find the root of the derivate (i.e. the minima). The update is the first derivative divided by the second derivative at the integer minimum location.


```python
# export
@numba.jit(nopython=True)
def argmin_sub(arr):
    idx_min = argmin_int(arr)
    if 1 <= idx_min <= len(arr)-2:
        delta_idx = ((arr[idx_min+1]-arr[idx_min-1])/2)/(arr[idx_min+1]-2*arr[idx_min]+arr[idx_min-1])
        if np.isnan(delta_idx): delta_idx =  0
        if delta_idx < -1:      delta_idx = -1
        if delta_idx >  1:      delta_idx =  1
        idx_min = idx_min - delta_idx
    return idx_min
```


```python
# export
@numba.jit(nopython=True)
def min_path_sub(arr_loss, buf_path):
    for i in range(len(arr_loss)):
        buf_path[i] = argmin_sub(arr_loss[i, :])
```


```python
arr_disp = rect_match_arr(arr1, arr2, hw, r_disp, loss, min_path_sub)
```


```python
arr_disp = rect_match_arr(arr1, arr2, hw, r_disp, loss, min_path_sub)
```

Again, around ~200 ms, the subpixel stuff doesn't add much overhead


```python
_, axs = plt.subplots(1, 2, figsize=(15,10))
axs[0].imshow(arr_disp, vmin=-15, vmax=15)
axs[1].imshow(arr1)
axs[1].imshow(arr_disp, vmin=-15, vmax=15, alpha=0.5)
```




    <matplotlib.image.AxesImage at 0x7fa3de329a10>




![png](README_files/README_74_1.png)


Looks smoother near the center of the object.

### Dynamic programming

The goal of dynamic programming is to find the shortest path from left to right in the following array:


```python
arr_loss = _debug_rect_loss_l(75)
```


![png](README_files/README_78_0.png)


But with an added smoothness contraint. This will be in the form of a penalty for going "up" and "down" and also a max change between neighboring columns. The hope is that, in the above, the path taken will not skip down near the ~125 column, but will instead continue smoothly above it, because doing so would incur a pentalty.


```python
# export
@numba.jit(nopython=True)
def _min_path_int_dp(arr_loss, buf_path, r_disp, max_change, penality_disp):
    buf_route     = np.zeros(arr_loss.shape)
    buf_move      = np.empty((2*max_change+1, r_disp[1]-r_disp[0]+1))
    buf_loss_prev = arr_loss[-1].copy() # Going backwards, this is initial optimal loss
    for i in range(len(arr_loss)-2, -1, -1):
        # Get loss of each move
        buf_move[:] = np.inf
        for j in range(-max_change, max_change+1):
            idx_minl, idx_maxl = max( j,0), min(arr_loss.shape[1]+j,arr_loss.shape[1])
            idx_minm, idx_maxm = max(-j,0), min(arr_loss.shape[1]-j,arr_loss.shape[1])
            buf_move[j+max_change, idx_minm:idx_maxm] = buf_loss_prev[idx_minl:idx_maxl] + abs(j)*penality_disp
        # Get optimal move and store it
        for j in range(buf_move.shape[1]):
            idx_min = np.argmin(buf_move[:,j])
            buf_route[i,j] = idx_min - max_change
            buf_loss_prev[j] = arr_loss[i,j] + buf_move[idx_min, j] # total loss = loss + optimal move
    # Gather path
    buf_path[0] = np.argmin(buf_loss_prev)
    for i in range(1, len(buf_route)):
        buf_path[i] = buf_path[i-1] + buf_route[i-1, int(buf_path[i-1])]
```

Numba does not support lambdas yet, so use factory function as per documentation


```python
# export
def make_min_path_int_dp(r_disp, max_change, penalty_disp):
    @numba.jit(nopython=True)
    def min_path(arr_loss, buf_path):
        return _min_path_int_dp(arr_loss, buf_path, r_disp, max_change, penalty_disp)
    return min_path
```


```python
max_change = 3
penalty_disp = 2
```


```python
min_path_int_dp = make_min_path_int_dp(r_disp, max_change, penalty_disp)
```


```python
def _debug_min_path(min_path):
    buf_path = np.empty(arr_loss.shape[0])
    min_path(arr_loss, buf_path)
    _, ax = plt.subplots(1,1,figsize=(10,10))
    ax.imshow(arr_loss.T)
    plt.plot(buf_path, '-r')
```


```python
_debug_min_path(min_path_int)
```


![png](README_files/README_86_0.png)



```python
_debug_min_path(min_path_int_dp)
```


![png](README_files/README_87_0.png)


Dynamic programming punishes the jump near 125 and prevents it from happening... cool


```python
arr_disp = rect_match_arr(arr1, arr2, hw, r_disp, loss, min_path_int_dp)
```


```python
arr_disp = rect_match_arr(arr1, arr2, hw, r_disp, loss, min_path_int_dp)
```

Again, ~200 ms, not bad.


```python
_, axs = plt.subplots(1, 2, figsize=(15,10))
axs[0].imshow(arr_disp, vmin=-15, vmax=15)
axs[1].imshow(arr1)
axs[1].imshow(arr_disp, vmin=-15, vmax=15, alpha=0.5)
```




    <matplotlib.image.AxesImage at 0x7fa3de4cff90>




![png](README_files/README_92_1.png)


Definitely much smoother. The glare still causes problems though.

### Sub pixel dynamic programming

I just basically replaced all `argmin`s with `argmin_sub` and also replaced indexing with `interp`. This assumes smoothness between adjacent optimal paths and im not sure if its strictly correct, but it seems to work.


```python
# export
@numba.jit(nopython=True)
def interp(arr, idx):
    if idx < 0 or idx > len(arr)-1: val = np.nan
    else:
        idx_f = np.floor(idx)
        if idx == idx_f: val = arr[int(idx_f)]
        else:            val = (idx_f+1-idx)*arr[int(idx_f)] + (idx-idx_f)*arr[int(idx_f)+1]
    return val
```


```python
arr = np.array([1,2,3])
assert_allclose(np.isnan(interp(arr, -0.5)), True)
assert_allclose(         interp(arr,  0.0),  1.0)
assert_allclose(         interp(arr,  0.5),  1.5)
assert_allclose(         interp(arr,  1.0),  2.0)
assert_allclose(         interp(arr,  1.5),  2.5)
assert_allclose(         interp(arr,  2.0),  3.0)
assert_allclose(np.isnan(interp(arr,  2.5)), True)
```


```python
# export
@numba.jit(nopython=True)
def _min_path_sub_dp(arr_loss, buf_path, r_disp, max_change, penality_disp):
    buf_route     = np.zeros(arr_loss.shape)
    buf_move      = np.empty((2*max_change+1, r_disp[1]-r_disp[0]+1))
    buf_loss_prev = arr_loss[-1].copy() # Going backwards, this is initial optimal loss
    for i in range(len(arr_loss)-2, -1, -1):
        # Get loss of each move
        buf_move[:] = np.inf
        for j in range(-max_change, max_change+1):
            idx_minl, idx_maxl = max( j,0), min(arr_loss.shape[1]+j,arr_loss.shape[1])
            idx_minm, idx_maxm = max(-j,0), min(arr_loss.shape[1]-j,arr_loss.shape[1])
            buf_move[j+max_change, idx_minm:idx_maxm] = buf_loss_prev[idx_minl:idx_maxl] + abs(j)*penality_disp
        # Get optimal move and store it
        for j in range(buf_move.shape[1]):
            idx_min = argmin_sub(buf_move[:,j])
            buf_route[i,j] = idx_min - max_change
            buf_loss_prev[j] = arr_loss[i,j] + interp(buf_move[:, j], idx_min)
    # Gather path
    buf_path[0] = argmin_sub(buf_loss_prev)
    for i in range(1, len(buf_route)):
        buf_path[i] = buf_path[i-1] + interp(buf_route[i-1, :], buf_path[i-1])
```


```python
# export
def make_min_path_sub_dp(r_disp, max_change, penalty_disp):
    @numba.jit(nopython=True)
    def min_path(arr_loss, buf_path):
        return _min_path_sub_dp(arr_loss, buf_path, r_disp, max_change, penalty_disp)
    return min_path
```


```python
min_path_sub_dp = make_min_path_sub_dp(r_disp, max_change, penalty_disp)
```


```python
_debug_min_path(min_path_sub_dp)
```


![png](README_files/README_101_0.png)


It's smooth now


```python
arr_disp = rect_match_arr(arr1, arr2, hw, r_disp, loss, min_path_sub_dp)
```


```python
arr_disp = rect_match_arr(arr1, arr2, hw, r_disp, loss, min_path_sub_dp)
```

Still ~200 ms


```python
_, axs = plt.subplots(1, 2, figsize=(15,10))
axs[0].imshow(arr_disp, vmin=-15, vmax=15)
axs[1].imshow(arr1)
axs[1].imshow(arr_disp, vmin=-15, vmax=15, alpha=0.5)
```




    <matplotlib.image.AxesImage at 0x7fa3de188850>




![png](README_files/README_106_1.png)


It's a little bit different from the integer version, but overall it looks similar and is smoother

### Image pyramid

Try using an image pyramid with "telescoping" search. Note that I've kept the window size the same for each level. In the most reduced image, it will use a proportionally larger window to get the overall translation correct, then in larger images, the proportionally smaller window will localize better (in theory at least).


```python
# export
def rect_match_pyr(arr1, arr2, hw, r_disp, loss, min_path, steps=3):
    if not np.all(shape(arr1) % 2**steps == 0): raise RuntimeError('Shape must be divisible by 2^steps')

    def _get_pyr(arr):
        arr_pyr = [arr]
        for idx in range(steps-1): 
            arr_pyr.append(imresize(arr_pyr[-1], shape(arr_pyr[-1])/2))
        return arr_pyr
    arr1_pyr, arr2_pyr = [_get_pyr(arr) for arr in [arr1, arr2]]

    arr_disp = None
    for idx in range(steps-1,-1,-1):
        arr1, arr2 = arr1_pyr[idx], arr2_pyr[idx]
        if arr_disp is not None:
            arr_disp = imresize(2*arr_disp, 2*shape(arr_disp)) # Remember to multiply disparities by 2
            arr_disp = np.round(arr_disp).astype(np.long)      # Must be integer
        arr_disp = rect_match_arr(arr1, arr2, hw, r_disp, loss, min_path, arr_disp)
    return arr_disp
```


```python
r_disp = (-5,5)
```


```python
arr_disp = rect_match_pyr(arr1, arr2, hw, r_disp, loss, min_path_sub)
```


```python
arr_disp = rect_match_pyr(arr1, arr2, hw, r_disp, loss, min_path_sub)
```

~100 ms, could probably optimize more but its fast


```python
_, axs = plt.subplots(1, 2, figsize=(15,10))
axs[0].imshow(arr_disp, vmin=-15, vmax=15)
axs[1].imshow(arr1)
axs[1].imshow(arr_disp, vmin=-15, vmax=15, alpha=0.5)
```




    <matplotlib.image.AxesImage at 0x7fa3d58d4f50>




![png](README_files/README_115_1.png)



```python
min_path_sub_dp = make_min_path_sub_dp(r_disp, max_change, penalty_disp)
```


```python
arr_disp = rect_match_pyr(arr1, arr2, hw, r_disp, loss, min_path_sub_dp)
```


```python
arr_disp = rect_match_pyr(arr1, arr2, hw, r_disp, loss, min_path_sub_dp)
```

~150 ms, a little slower but still pretty fast


```python
_, axs = plt.subplots(1, 2, figsize=(15,10))
axs[0].imshow(arr_disp, vmin=-15, vmax=15)
axs[1].imshow(arr1)
axs[1].imshow(arr_disp, vmin=-15, vmax=15, alpha=0.5)
```




    <matplotlib.image.AxesImage at 0x7fa3d5d3ed50>




![png](README_files/README_120_1.png)


# API

Use a class here because every time `min_path_*_dp` is instantiated it seems to make numba recompile, so cache it in a `RectMatch` object to make each call fast.


```python
# export
class RectMatch:
    def __init__(self, type_min_path, hw=15, r_disp=(-5,5), loss=SAD, steps=3, max_change=3, penalty_disp=2):
        if   type_min_path == 'int':    min_path = min_path_int
        elif type_min_path == 'sub':    min_path = min_path_sub
        elif type_min_path == 'int_dp': min_path = make_min_path_int_dp(r_disp, max_change, penalty_disp)
        elif type_min_path == 'sub_dp': min_path = make_min_path_sub_dp(r_disp, max_change, penalty_disp)
        else: raise RuntimeError(f'Unrecognized min path type: {type_min_path}')
        self.hw, self.r_disp, self.loss, self.steps, self.min_path = hw, r_disp, loss, steps, min_path
    
    def __call__(self, arr1, arr2): 
        return rect_match_pyr(arr1, arr2, self.hw, self.r_disp, self.loss, self.min_path, self.steps)
```


```python
types_min_path = ['int', 'sub', 'int_dp', 'sub_dp']
rect_matchs = [RectMatch(type_min_path) for type_min_path in types_min_path]
```


```python
_, axs = plt.subplots(2, 2, figsize=(15,10))
for ax, rect_match, type_min_path in zip(axs.ravel(), rect_matchs, types_min_path): 
    ax.imshow(rect_match(arr1, arr2), vmin=-15, vmax=15)
    ax.set_title(type_min_path)
```


![png](README_files/README_125_0.png)


# Build


```python
build_notebook()
```


    <IPython.core.display.Javascript object>


    Converted README.ipynb.



```python
convert_notebook()
```
