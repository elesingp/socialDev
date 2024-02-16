from sklearn.metrics import silhouette_score

from clustering import X, labels

score = silhouette_score(X, labels, metric='euclidean')

print(f"Силуэтный коэффициент: {score}")
