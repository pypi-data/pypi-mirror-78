# 鲁棒, 可复用的多 realsense 控制库

## 特性
- [x] 对 realsense 良好的鲁棒性
    - 能解决常见错误
    - 支持拔了 USB 再插, 程序接着运作
- [x] 易用的配置接口
    - 基于重写类的方法(override method)来实现接口
    - 由于 realsense 配置项本身的复杂性, 很难做到更加简洁
- [x] 支持多进程处理多个 realsense
    - 在低端赛扬 CPU 上, 时延能降低 50%
- [x] 可复用
- [ ] 系统级重启 USB (还未实现)

## 使用方式

Demo:
```
python multi_realsense_manager/multi_realsense_manager.py
```
使用说明见 ["multi_realsense_manager/multi_realsense_manager.py"](multi_realsense_manager/multi_realsense_manager.py#L248-301) 代码里的注释
