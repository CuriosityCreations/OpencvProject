# OpencvProject
Human tracking

##Dependencies
```sudo apt-get install build-essential cmake git pkg-config```

```sudo apt-get install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev```

```sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev```

```sudo apt-get install libgtk2.0-dev```

```sudo apt-get install libatlas-base-dev gfortran```

```sudo apt-get install python3-cairocffi```

## virtualenv and virtualenvwrapper
 Create entirely separate and independent Python environments

```sudo pip3 install virtualenv virtualenvwrapper```

```export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.5```

```export WORKON_HOME=$HOME/.virtualenvs```

```source /usr/local/bin/virtualenvwrapper.sh```

```source ~/.bashrc```

```mkvirtualenv cv```

```workon cv```

## Install python3 and Numpy on virtualenv
```sudo apt-get install python3```

```pip3 install numpy```

##Install OpenCV 3.0
```cd ~```

```git clone https://github.com/Itseez/opencv.git```

```git clone https://github.com/Itseez/opencv_contrib.git```

```cd ~/opencv```

```mkdir build```

```cd build```

```cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=OFF \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D BUILD_EXAMPLES=ON ..```

```cmake -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules ~/opencv```

```make -j4```

```sudo make install```

```sudo ldconfig```

```cd ~/.virtualenvs/cv/lib/python3.5/site-packages/```

```ln -s /usr/local/lib/python3.5/site-packages/cv2.cpython-35m-arm-linux-gnueabihf.so  cv2.so```

###Python Path

import sys

print(sys.path)
