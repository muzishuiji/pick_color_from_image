import numpy as np
import time
from sklearn.cluster import KMeans
from PIL import Image

def extract_colors(image_path, num_colors):
    start_time = time.time()
    # 读取图片
    image = Image.open(image_path)
    # 转换为RGB数组
    pixels = np.array(image.resize((100, 100)))
    pixels = pixels.reshape(-1, 3)
    
    # 应用K-means聚类
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    
    # 获取聚类中心作为主题色
    colors = kmeans.cluster_centers_
    end_time = time.time()
    execute_time = (end_time - start_time) * 1000
    print(f"execute_time: {execute_time}", colors)
    return colors.astype(int)

# 使用示例
colors = extract_colors("./images/cover1.jpg", 5)
print(colors)