from sklearn.cluster import DBSCAN
import numpy as np
from mexc_api.spot import Spot
import time
import utils
import pandas as pd


def clusterize(data):

    # Преобразуем данные в формат для кластеризации
    data_reshaped = np.array(data).reshape(-1, 1)

    # Кластеризация
    dbscan = DBSCAN(eps=0.5, min_samples=2)
    clusters = dbscan.fit_predict(data_reshaped)

    # Проверяем количество уникальных кластеров
    unique_clusters = np.unique(clusters)

    if len(unique_clusters) > 1:
        print(f"Найдены плотные группы: {unique_clusters[unique_clusters != -1]}")
    else:
        print("Плотные группы отсутствуют.")
    return clusters


spot = Spot("", "")

print("time delta:", utils.get_server_time_delta(spot), "s")

trades = spot.market.trades('MCNUSDT', 400)
# for i in range(10):
#     print(f"{trades[i]['quoteQty']} at {utils.format_timestamp(trades[i]['time'])}")
# print()

df = pd.DataFrame(trades)
df = df.groupby('quoteQty', as_index=False).sum()
print(df.head())

# clusters = clusterize(df['quoteQty'])
# print("Clusters output:\n", clusters)
