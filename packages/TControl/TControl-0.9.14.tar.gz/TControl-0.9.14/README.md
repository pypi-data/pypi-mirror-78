# TControl
用于自动控制系统分析的Python库。

__重要__ 

本项目有点 __不稳定__，__不要用在任何严肃的工作或商业工作中！__
## 特点
+ 支持传递函数和状态空间模型。
+ 时间响应
    + 冲动
    + 单位阶跃
    + 斜坡
    + 任何输入
+ 频率响应
    + 奈奎斯特图
    + 波特图
+ 控制系统分析
    + 可控性
    + 可观测性
    + 极点配置法
    + Lyapunov稳定性

__注意__ 
+ 针对线性时不变系统，设计了两个类：传递函数和状态空间。
+ 时间响应法和频率响应法目前只支持单输入单输出系统。

## 依赖库
+ [Python 3.7+](https://www.python.org)
+ [Numpy](https://www.numpy.org)
+ [Scipy](https://scipy.org/)
+ [Sympy](http://www.sympy.org)
+ [Matplotlib](https://matplotlib.org)
+ [nose2](https://github.com/nose-devs/nose2) (optional for test)
+ [Sphinx](http://www.sphinx-doc.org) (optional for building docs)
+ [sphinx-rtd-theme](https://github.com/rtfd/sphinx_rtd_theme) (optional sphinx theme)

## 安装
    python -m setup.py install

## 使用
    >>> import tcontrol as tc
    >>> system = tc.tf([1], [1, 1])
    >>> print(system)
      1
    -----
    s + 1
    >>> tc.tf2ss(system)
    A:     B:
      [-1.]  [1.]
    C:     D:
      [ 1.]  [0.]


## 授权
本项目受BSD 3条款许可。有关详细信息，请参见文件
[LICENSE](https://gitee.com/ljcloud/TControl/master/LICENSE).

## 预览1
![任意输入](docs/image/any_input_res.png)
## 预览2
![伯德图](docs/image/bode.png)
## 预览3
![单位脉冲响应](docs/image/impulse_res.png)
## 预览4
![奈奎斯特图](docs/image/nyquist.png)
## 预览5
![单位斜坡响应](docs/image/ramp_res.png)
## 预览6
![根轨迹图](docs/image/rlocus.png)
## 预览7
![单位阶跃响应](docs/image/step_res.png)