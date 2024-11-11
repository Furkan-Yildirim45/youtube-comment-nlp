from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import joblib

# Veriyi yükleme ve ön işleme
def load_data():
    # İşlenmiş veriyi oku
    df = pd.read_csv('datasets/processed/CampusX-translated_comments_processed.csv')  # Duygu sütunu eklenmiş veri
    return df

# Modeli eğitme
def train_model():
    # Veriyi yükle
    df = load_data()
    
    # Eğitim ve test verisini ayıralım
    X = df['yorum_islenmis']  # İşlenmiş yorumlar (özellikler)
    y = df['Duygu']  # Duygu etiketleri (hedef değişken)

    # Eğitim ve test verisini bölelim
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Metin verisini sayısal verilere dönüştürme
    vectorizer = TfidfVectorizer(stop_words=None, max_features=5000)  # Maksimum 5000 kelime
    X_train_tfidf = vectorizer.fit_transform(X_train)  # Eğitim verisini vektörize et
    X_test_tfidf = vectorizer.transform(X_test)  # Test verisini vektörize et

    # Naive Bayes sınıflandırıcısını kullanarak model oluşturma
    model = MultinomialNB()
    model.fit(X_train_tfidf, y_train)  # Modeli eğitme

    # Modeli test etme
    y_pred = model.predict(X_test_tfidf)
    
    # Sonuçları değerlendirelim
    print("Model Performansı:")
    print("Doğruluk: ", accuracy_score(y_test, y_pred))
    print("Sınıflandırma Raporu:")
    print(classification_report(y_test, y_pred))

    # Modeli kaydetme (isteğe bağlı)
    joblib.dump(model, 'models/sentiment_model.pkl')  # Modeli kaydetme
    print("Model kaydedildi.")

if __name__ == "__main__":
    train_model()

##kod denencek claıstırılıp!
""" Model Performansı:
Doğruluk:  1.0
Sınıflandırma Raporu:
              precision    recall  f1-score   support

        Nötr       1.00      1.00      1.00         1

    accuracy                           1.00         1
   macro avg       1.00      1.00      1.00         1
weighted avg       1.00      1.00      1.00         1

Model kaydedildi. """