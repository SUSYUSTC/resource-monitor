# Resource Monitor

<p align="center">
  <!-- PyPI -->
  <a href="https://pypi.org/project/mathtranslate/">
    <img src="https://img.shields.io/pypi/v/mathtranslate.svg?logo=pypi"/>
  </a>
  <!-- License -->
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/license-Apache%202.0-yellow.svg?logo=apache"/>
  </a>

This is a repo to moniter the resource usages of your python codes like TensorBoard and WanDB. 

# Usage

```
from monitor import ResourceMonitor

with ResourceMonitor(interval=0.1, GPU=False, save_path=None):
   # your code here
```
<img src="https://github.com/SUSYUSTC/resource-monitor/blob/main/fig/resource.png" width="1000">
