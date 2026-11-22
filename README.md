# 椰椰杯 Webots 赛道仿真环境

这是在 Webots R2025a 中验证的椰椰杯赛道环境。场地按 4 m × 4 m 放样，白色通道按实拍比例设为 360 mm，两侧黑边各宽 50 mm。场景包含起终点虚线、墙体和场外标线、消防箱、黑色银脚沙发，以及离地 3.6 m 的灯管。

## 下载安装 Webots

1. 打开 [Webots R2025a 官方发布页](https://github.com/cyberbotics/webots/releases/tag/R2025a)。
2. Windows 64 位用户下载并运行 [Webots R2025a 安装包](https://github.com/cyberbotics/webots/releases/download/R2025a/webots-R2025a_setup.exe)。macOS 和 Linux 用户在同一发布页选择对应系统的安装包。
3. 安装完成后启动 Webots。

## 下载并打开地图

1. 在本仓库页面点击 **Code → Download ZIP**，下载并解压整个压缩包。
2. 在 Webots 中选择 **File → Open World…**，打开解压目录里的 [worlds/yeyebei_venue.wbt](worlds/yeyebei_venue.wbt)。
3. 保留解压后的目录结构，Webots 会自动从 worlds/textures/ 读取赛道贴图，从 protos/ 加载场边物品和灯光模型。
