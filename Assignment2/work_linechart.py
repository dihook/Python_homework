import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from ucimlrepo import fetch_ucirepo
import numpy as np

# 获取网上的数据
daily_demand_forecasting_orders = fetch_ucirepo(id=409)
X = daily_demand_forecasting_orders.data.features

# 第1到第5周的数据
X = X[X['Week of the month'].isin([1, 2, 3, 4, 5])]

# 三种订单 列表
order_types = ['Order type A', 'Order type B', 'Order type C']

# 颜色
colors = ['tab:blue', 'tab:orange', 'tab:green']    #tab_blue wrong spelling

# 按周统计每种订单类型的总数
order_counts = X.groupby('Week of the month')[order_types].sum().reset_index()

# 曲线动画数据
x = order_counts['Week of the month']
y_data = [order_counts[otype] for otype in order_types]

x_smooth = np.linspace(x.min(), x.max(), 100) # more smooth points
y_smooth = [np.interp(x_smooth, x, y) for y in y_data]

# 爱心形状函数
def heart_shape(t):
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    return x, y

t = np.linspace(0, 2 * np.pi, 200)
heart_x, heart_y = heart_shape(t)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5)) # Adjusted size 

# Left line chart animation
ax1.set_title('Weekly Order Types Line Animation')
ax1.set_xlabel('Week of the Month (1-5)')
ax1.set_ylabel('Order Quantity')
lines = [ax1.plot([], [], label=otype, lw=2, color=colors[i])[0] for i, otype in enumerate(order_types)]

ax1.set_xlim(1, 5)
ax1.set_ylim(0, order_counts[order_types].values.max() * 1.1)
ax1.legend()

# Right heart animation
ax2.set_title('Order Type Heart Beat')
ax2.axis('off')
hearts = [ax2.plot([], [], color=colors[i], lw=5, alpha=0.8)[0] for i in range(3)]

# All hearts share the same center
center = (0, 0)
ax2.set_xlim(-12, 12)
ax2.set_ylim(-12, 12)

# 归一化订单数量用于缩放，改为全局最大值
global_max = max([y.max() for y in y_smooth])

# 动画初始化
def init():
    for line in lines:
        line.set_data([], [])
    for heart in hearts:
        heart.set_data([], [])
    return lines + hearts

# 动画帧
def animate(i):
    # 折线
    for idx, line in enumerate(lines):
        line.set_data(x_smooth[:i+1], y_smooth[idx][:i+1])
    # 爱心
    for idx, heart in enumerate(hearts):
        scale = 0.25 + 0.25 * y_smooth[idx][i] / global_max  # 0.25~0.5缩放，按全局最大值
        cx, cy = center
        heart.set_data(heart_x * scale + cx, heart_y * scale + cy)
    return lines + hearts

# loop
ani = FuncAnimation(fig, animate, init_func=init, frames=len(x_smooth), interval=50, blit=True)
plt.tight_layout()
plt.show()
