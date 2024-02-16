from sklearn.metrics import silhouette_score

from clustering import X, labels

# Предположим, что X - это матрица признаков комментариев после TF-IDF векторизации,
# а labels - метки кластеров, полученные после кластеризации.

score = silhouette_score(X, labels, metric='euclidean')

print(f"Силуэтный коэффициент: {score}")
