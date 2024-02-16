from api import comments
from preprocess_natasha import preprocess_text_natasha
from preproccess_nltk import preprocess_text_nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize

# Предобработка комментариев
preprocessed_comments = [preprocess_text_natasha(comment) for comment in comments] 
#preprocess_text_nltk
#preprocess_text_natasha


# Векторизация текста
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(preprocessed_comments)
X_normalized = normalize(X)

# Кластеризация
k = 5  # Предполагаемое количество кластеров
model = KMeans(n_clusters=k, random_state=42)
model.fit(X_normalized)

# Получение меток кластеров
labels = model.labels_

# Анализ результатов
for i in range(k):
    cluster = [comments[j] for j in range(len(comments)) if labels[j] == i]
    print(f"Кластер {i+1}:")
    for comment in cluster[:5]:  # Вывод первых 5 комментариев каждого кластера
        print(comment)
    print("\n")