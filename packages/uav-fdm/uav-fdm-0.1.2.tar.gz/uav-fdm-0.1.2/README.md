
# uav_fdm 无人机动力学模型

## 概述

本项目将matlab代码生成的三自由度飞行动力学模型C++类通过SWIG进行包装，并通过distutils发布python平台接口。

## 编译安装

本地编译

```bash
python setup.py build_ext --inplace
```

安装编译

```bash
python setup.py install --user
```

## 使用

```python
import uav_fdm

lat0 = 23
lon0 = 110
alt0 = 100
v_n0 = 20
v_e0 = 0
hdot0 = 0

uav1 = uav_fdm.uav_fdm(lat0,lon0,alt0,v_n0, v_e0, hdot0)

deltaT = 1
vg_c = 20
hdot_c = 0
psidot_c = 0.1 # loiter

for True:
    [lat,lon,alt,v_n,v_e,v_d] = uav1.update(deltaT, vg_c, hdot_c, psidot_c)
```
