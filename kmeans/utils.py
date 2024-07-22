import numpy as np
import cv2

def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins = numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype('float')
    hist /= hist.sum()
    return hist

def plot_colors(hist, centroids):
    # 初始化条形图，表示每种颜色的相对频率
    bar = np.zeros((50, 300, 3), dtype="unit8")
    startX = 0
    # 循环遍历每个聚类的百分比和每个聚类的颜色
    for(percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0, int(endX), 50), color.astype("uint8").tolist(), -1)
        startX = endX
    return bar