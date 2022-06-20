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

## NumPy

```python
import numpy as np                        # matrix manipulations
from numpy.testing import assert_allclose # compare numpy arrays
from numpy.linalg import norm             # normalize numpy vectors
np.set_printoptions(precision=1)
np.set_printoptions(suppress=True)
```

## Embed Video

```python
from ipywidgets import Video
Video.from_file("Megamind.mp4")
```

## OpenCV

```python
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