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

## 添加小车并查看车载相机

下面用 Webots 自带的 `Khepera4` 作示例。这是一辆带前视相机的双轮差速小车。首次添加时，Webots 会从官方模型库下载资源。[Khepera IV 模型说明](https://github.com/cyberbotics/webots/blob/R2025a/docs/guide/khepera4.md)

1. 打开赛道后暂停仿真。在左侧场景树选中最后一个顶层节点 `VenueClutter`，点击 **Add（+）**，选择 **PROTO nodes (Webots Projects) → robots → k-team → khepera4 → Khepera4**。
2. 展开 `Khepera4`。把 `translation` 设为 `2.93 0.23 0`，把 `rotation` 设为 `0 0 1 3.14159`。这样小车会放在底部起点虚线右侧，车头朝左。`translation` 的单位为米，`rotation` 最后一项的单位为弧度。
3. 使用模型默认的 `khepera4` 控制器，点运行。车载相机会自动开始采样，3D 窗口中会出现带紫色边框的原始相机画面。示例控制器会驱动小车移动，查看起点画面时可以短暂运行后暂停。
4. 如果预览被关闭，在场景树选中小车，再通过 **Robot → Camera Devices** 显示 `camera`。双击预览可以独立开窗。要保存加车后的地图，可以在原 `worlds/` 目录下另存一个 `.wbt` 文件。[Webots 相机预览说明](https://github.com/cyberbotics/webots/blob/R2025a/docs/reference/camera.md#overlay-image)

已有 Webots 车模时，可以把它的 `.proto` 和引用的网格、贴图一起放入本地 `protos/`，保留资源的相对路径，再从场景树导入。自己搭建简模时，将车体外观放进 `Robot`，再在其 `children` 里添加 `Camera`，设置相对位置、角度和分辨率。相机采样由该小车的控制器启用。[Webots Camera 参考](https://github.com/cyberbotics/webots/blob/R2025a/docs/reference/camera.md)
