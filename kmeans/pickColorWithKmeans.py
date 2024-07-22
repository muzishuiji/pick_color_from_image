# 找出一张图的物种主要颜色
# 使用kmeans聚类算法
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import utils
import cv2

# 
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Path to the image")
ap.add_argument('-c', '--clusters', required=True, type=int,help='# of clusters')
args = vars(ap.parse_args())

# 加载图像并将其从BGR转换为RGB，以便我们可以使用matplotlib显示它
image = cv2.imread(args["image"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 显示图片
plt.figure()
plt.axis('off')
plt.imshow(image)

# 将图像调整为一个像素列表
image = image.reshape((image.shape[0] * image.shape[1], 3))

# 聚类像素强度
clt = KMeans(n_clusters=args["clusters"])
clt.fit(image)

# 构建一个聚类直方图，然后创建一个代表每种颜色标记的像素数量的图形
hist = utils.centroid_histogram(clt)
bar = utils.plot_colors(hist, clt.cluster_centers_)

# show our color bart
plt.figure()
plt.axis('off')
plt.imshow(bar)
plt.show()

