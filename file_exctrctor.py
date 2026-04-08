import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.snowball import SnowballStemmer

with open('calculusfile.txt', 'r', encoding='utf-8') as fi:
    lines = fi.readlines()


stemmer = SnowballStemmer("russian")  # Используем стеммер для приведения слов к базовой форме (отсечение окончаний).

def normalize_text(text):
    # Приведение текста к нижнему регистру
    text = text.lower()
    # Удаление пунктуации и цифр
    text = re.sub(f'[{string.punctuation}0-9\\r\\t\\n]', ' ', text)

    # Стемминг
    normalized_text = ' '.join([stemmer.stem(line) for line in text.split()])
    
    return normalized_text



documents = lines
# Пример больших текстов теорем
# Применяем нормализацию с лемматизацией для каждого документа
normalized_documents = [normalize_text(doc) for doc in documents]

# Инициализируем TfidfVectorizer и обучаем на нормализованных документах
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(normalized_documents)


def get_teorems(task):
    # Создание TF-IDF векторов

    task_tfidf = vectorizer.transform([normalize_text(task)])

    # Поиск релевантных теорем по задаче
    similarities = cosine_similarity(task_tfidf, tfidf_matrix)
    print(similarities)
     # argsort тут работает возвращая индексы, которые отсортируют массив. 
    relevant_indices = [idx for idx in similarities[0].argsort() if similarities[0][idx] > 0][-5:]  # Индексы теорем с наибольшим сходством.
    
    res = "Релевантные теоремы:\n" + "\n".join([documents[index] for index in relevant_indices])
    return res
