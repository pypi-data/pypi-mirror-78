
![medium_logo](https://raw.githubusercontent.com/rediscovery-io/remo-python/master/img/remo_normal.png)

# Remo: images and annotations management for Computer Vision


Remo is a web-application for managing and visualising images and annotations.

It was developed for data scientists, engineers and ML researchers to facilitate
the exploration, sharing and management of datasets and annotations for Computer Vision.

Use Remo to:

- **visualise and inspect** datasets, annotations and predictions
- **search and organise images** by classes or tags
- **visualise statistics** like # objects per class
- **quickly annotate** your images

Remo can be called from code or used as a standalone application.

It runs on Windows, Linux and Mac, and it can be embed in Jupyter Notebook or Google Colab.

Under the hood, Remo it's written using Python and React.JS, and relies on a PostgreSQL database to store metadata.

- - -

## Python commands
Here is an example of using the Python library to:

- crate a dataset
- upload annotations
- visualise statistics on annotations
- search for specific images

Simple workflow:

``` python
import remo

# create dataset
my_dataset = remo.create_dataset(name = 'open images test',
                            urls = ["https://s-3.s3-eu-west-1.amazonaws.com/open-images.zip"],
                            annotation_task="Object detection")

# list existing datasets                
remo.list_datasets()

# browse the dataset
my_dataset.view()

my_dataset.list_images()

# view stats
my_dataset.view_annotation_statistics()

# annotate
my_dataset.view_annotate()



```

---

## Installation
Remo is compatible with **Python 3.6+** and runs on **Linux, macOS and Windows**. The latest remo releases are available over <a href="https://pypi.org/project/remo/" target="_blank">pip</a>.

On a fresh Ubuntu machine, you may be needed to install gcc and python3-dev packages.

### 1. Pip install
You can install remo using `pip`.

``` bash
pip install remo
```

### 2. Initialise
To complete the installation, run:

```
python -m remo_app init
```

This will download some additional packages and create a folder .remo in your home directory. By default, this is the location where Remo looks for its configuration file, **remo.json**.


### 3. Optional: separate python library

When installing remo, you also automatically install the remo-python library.
Optionally, you can install the python library in a separate Python 3.5+ environment and use it to interface with remo app.

``` bash
# First activate your Python work environment
pip install remo-sdk
```

---
## Launch remo

To launch the web app, run from command line:

``` bash
python -m remo_app
```

Remo will be served by default in its own Electron app. But you can also access it through your browser or embed it in a Jupyter Notebook.


![](https://remo.ai/docs/img/remo_preview.PNG)

---
## Command Line Interface

You can use remo from your command line, doing `python -m remo_app` and using the following options:


```bash
  (no command)          - start server and open the default frontend
  no-browser            - start server

  init [options]        - initialize settings and download additional packages
  Options:
    --colab             - specify installation on Google Colab
    --remo-home <dir>   - set custom remo home dir location.
                          Default location: ~/.remo,
                          on Colab default location: /gdrive/My Drive/RemoApp

  kill                  - kill running remo instances
  open                  - open the Electron app
  remove-dataset        - delete datasets
  delete                - delete all the datasets and metadata
  backup                - create database backup

  --version             - show remo version
  --help                - show help info
```

---
## Support

In case you need support or want to give us some precious feedback, you can get in touch with us on <a href="https://discuss.remo.ai" target="_blank"> our forum</a>.

For any other query, you can also to write to us at  `#!css hello AT remo DOT ai`
