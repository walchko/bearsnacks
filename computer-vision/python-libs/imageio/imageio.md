---
title: ImageIO
date: 8 Nov 2020
---

ImageIO uses Pillow with a simple interface to read/write images. It
is also able to work with video using `ffmpeg`.

```python
#!/usr/bin/env python3
import imageio
from glob import glob

def save(imgFiles, fname, fps=30):
    writer = imageio.get_writer(fname, fps=fps)
    sz = len(imgFiles)
    for i, imgf in enumerate(imgFiles):
        im = imageio.imread(imgf)
        # writer.append_data(im[:, :, 1])
        writer.append_data(im)
        if i%100 == 0:
            print(f">> Frame {i}/{sz}")
    writer.close()
    
imgfiles = sorted(glob("./data/*.png"))
save(imgfiles, "test.mp4")
```
