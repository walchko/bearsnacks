---
title: Image Serialization Using Base64 Encoding
date: 2 Nov 2019
---

```python
import base64
import numpy as np

# create a fake image: img.size = 307200
img = np.random.randint(256, size=(1, 480, 640), dtype=np.uint8)

# encode image, len(image_string) = 409600
image = base64.b64encode(img)
image_string = image.decode("utf-8")
```
