import torch
import torch.nn as nn

# 1. 创建一个随机输入张量（模拟单张灰度图）
batch_size = 1
in_channels = 1   # 灰度图
height = 5
width = 5
x = torch.randn(batch_size, in_channels, height, width)  
print(x)

# 2. 定义一个 Conv2d 层
conv = nn.Conv2d(
    in_channels=1,      # 输入通道数（与上面一致）
    out_channels=6,     # 输出通道数（卷积核个数）
    kernel_size=5,      # 卷积核大小 5x5
    padding=2           # 填充2，保持输出尺寸不变（对于 5x5 核，padding=2 可保持宽高不变）
)

# 3. 将输入送入卷积层，得到输出
out = conv(x)

# 4. 查看输入和输出的形状

print("输入形状:", x.shape)   # torch.Size([1, 1, 28, 28])
print("输出形状:", out.shape) # torch.Size([1, 6, 28, 28])

# 5. 查看输出张量的一部分数值（默认是随机初始化的权重，所以输出也是随机的）
# print("输出张量:\n", out)  # 打印第一个样本、第一个输出通道、左上角 5x5 区域


pool = nn.MaxPool2d(kernel_size=2, stride=2)
out = pool(out)

print(out)