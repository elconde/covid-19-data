# covid-19-data
> Scripts for reading the COVID-19 data available from the New York Times


# Prerequisites

- Anaconda
- Git

# Installation

1. Clone this repository with Git
2. `git submodule update --init` will fetch the New York Times data
3. From an Anaconda prompt:

```
conda create --name covid-19-data python=3.7 pandas matplotlib=3.1.3 basemap pillow
conda activate covid-19-data
```


# Animated Map
In order to show the animated map of U.S. county cases follow the instructions in the cb_2018 folder.

![png_to_gif.gif](png_to_gif.gif)