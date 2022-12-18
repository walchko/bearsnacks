# Jupyter Notebooks

- [Computer Vision](https://nbviewer.jupyter.org/github/walchko/bearsnacks/blob/main/computer-vision/index.ipynb)
- [Multiped](https://nbviewer.jupyter.org/github/walchko/bearsnacks/blob/main/multiped/index.ipynb)
- [Navigation and Mapping](https://nbviewer.jupyter.org/github/walchko/bearsnacks/blob/main/navigation-and-mapping/index.ipynb)
- [Machine Learning](https://nbviewer.jupyter.org/github/walchko/bearsnacks/blob/main/machine-learning/index.ipynb)
- [Python](python/index.ipynb)
- [Space](space/index.ipynb)
- [Engineering Toolbox](engineering-toolbox/index.ipynb)
- [Drones](drones/index.ipynb)
- [Data Science](data-science/index.ipynb)

# Python Notes

## Creating Virtual Environments (venv)

```bash
python -m venv <folder_location>
```

## Github Workflow

```python
name: CheckPackage
on: [push]

jobs:
    build:
        runs-on: ubuntu-latest
        strategy:
          max-parallel: 5
          fail-fast: true
          matrix:
            python-version: ["3.8", "3.9", "3.10", "3.11"]
        steps:
            - uses: actions/checkout@main
            - name: Setup Python ${{ matrix.python-version }}
              uses: actions/setup-python@main
              with:
                python-version: ${{ matrix.python-version }}
            - name: Install packages
              run: |
                echo "Installing dependencies"
                python3 -m venv .venv
                source .venv/bin/activate
                pip install -U pip setuptools wheel poetry pytest
                poetry install
                pytest tests/
```

## Switching Venv

When you have setup multiple `venv`'s, add the following to your `bashrc`/`zshrc` profile and you can easily change between them with `changevenv <new_venv>`. All of my virtual environments are located in my home directory at `$HOME/venvs`, which is why you see `DIR="$HOME/venvs/$1"` bellow.

```bash
function changevenv () {
    if [ $# -eq 0 ]; then
        echo "\n!! Please select a new venv: changevenv py\n"
        return
    fi

    DIR="$HOME/venvs/$1"
    if [ -d "$DIR" ]; then
        if typeset -f deactivate > /dev/null ; then
            deactivate
        fi

        . "$DIR/bin/activate"

        echo "\n>> SUCCESS! Changed to venv $1\n"
    else
        echo "\n!! Sorry, $1 doesn't exist, choose a new venv\n"
    fi
}
```

# Jupyter Lab


## Reload Imports

```python
# reload library
%load_ext autoreload
%autoreload 2
```

## JupyterTollBox (`jtb`)

```python
from jtb import getCodeUrl, getCodeFile, getCodeImport

import bob
getCodeImport(bob)      # will show everthing
getCodeImport(bob.func) # show just function func

getCodeFile("path/to/file")

getCodeUrl("github.com/user/repo/file.py")
```

## NumPy

```python
import numpy as np                        # matrix manipulations
from numpy.testing import assert_allclose # compare numpy arrays
from numpy.linalg import norm             # normalize numpy vectors
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
```

## Matplotlib

```python
plt.axis("off")  # turn off axis labels on images
plt.ticklabel_format(style='plain') # to prevent scientific notation
```

```python
from matplotlib import animation
import matplotlib
from IPython.display import display, HTML

def plot_sequence_images(image_array):
    ''' Display images sequence as an animation in jupyter notebook
    
    Args:
        image_array(numpy.ndarray): image_array.shape equal to (num_images, height, width, num_channels)
    '''
    dpi = 72.0
    xpixels, ypixels = image_array[0].shape[:2]
    fig = plt.figure(figsize=(ypixels/dpi, xpixels/dpi), dpi=dpi)
    im = plt.figimage(image_array[0])

    def animate(i):
        im.set_array(image_array[i])
        return (im,)

    # animation.embed_limit needs to be increased if video is too big
    matplotlib.rcParams['animation.embed_limit'] = 40e6
    anim = animation.FuncAnimation(fig, animate, frames=len(image_array), interval=50, repeat_delay=1, repeat=False)
    display(HTML(anim.to_html5_video()))
```

## Embed Video

```python
from ipywidgets import Video
Video.from_file("Megamind.mp4")
```

## OpenCV

```python
bgr2rgb = lambda im: cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
rgb2bgr = lambda im: cv2.cvtColor(im, cv2.COLOR_RGB2BGR)

hsv2bgr = lambda im: cv2.cvtColor(im, cv2.COLOR_HSV2BGR)
bgr2hsv = lambda im: cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

bgr2gray = lambda im: cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
gray2bgr = lambda im: cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)

rgb2gray = lambda im: cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
gray2rgb = lambda im: cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)

# simple function to save a video
import platform
def videoWrite(frames, fname='out.mp4'):
    frame_height, frame_width, _ = frames[0].shape
    
    # pick a good encoder for the current OS
    sys = platform.system()
    if sys in ['Darwin']:  # this is on macOS
        fourcc = "mp4v" # 'avc1' - old?
    else:  # this is for Windoze
        fourcc = 'mjpg'
        
    out = cv2.VideoWriter(
        fname,
        cv2.VideoWriter_fourcc(*fourcc), 
        30, 
        (frame_width,frame_height))
    for frame in frames:
        out.write(frame)
    out.release()
```
