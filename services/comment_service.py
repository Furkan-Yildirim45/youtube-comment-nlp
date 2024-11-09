# main.py
import time
import nltk
import pandas as pd
import re
from googletrans import Translator
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('punkt')      # Genel tokenizasyon veritabanı
nltk.download('punkt_tab')  # Cümle tokenizasyonu için gerekli kaynak
nltk.download('stopwords')  # Stopwords veritabanı
nltk.download('vader_lexicon')

class CommentService:
    def __init__(self, csv_dosyasi):
        self.data = pd.read_csv(csv_dosyasi, engine="python")
        self.translator = Translator() # Türkçe stopword'leri al
        self.stop_words = set(stopwords.words('turkish')) # Stemming işlemi için stemmer
        self.stemmer = PorterStemmer()

    def correct_comment(self, yazi):
        if isinstance(yazi, str):
            yazi = re.sub(r"[^a-zA-ZçÇğĞıİöÖşŞüÜ\s]", "", yazi)
            yazi = yazi.lower()
        else:
            yazi = ""
        return yazi

    def translate_tr(self, yazi, index, retries=3, delay=5):
        if yazi:
            for attempt in range(retries):
                try:
                    translated = self.translator.translate(yazi, dest='tr')
                    print(f"[{index}] Çeviri başarılı: '{yazi}' -> '{translated.text}'")
                    return translated.text
                except Exception as e:
                    print(f"[{index}] Çeviri hatası: {e}, yeniden deniyorum... (Deneme {attempt + 1}/{retries})")
                    print("error :e".format(e))
                    time.sleep(delay)
            print(f"[{index}] Tüm denemeler başarısız oldu: '{yazi}'")
            return yazi
        return ""

    def tokenize_comments(self):
        # CSV'de mevcut olan sütun adını doğru yazdığınızdan emin olun
        if 'snippet_topLevelComment_snippet_textDisplay' in self.data.columns:
            # Her yorum üzerinde direkt işlem yaparak tokenize işlemi
            self.data['yorum_tokenize'] = self.data['snippet_topLevelComment_snippet_textDisplay'].apply(
                lambda yorum: word_tokenize(yorum) if isinstance(yorum, str) else []
            )
            print("Tokenizasyon işlemi tamamlandı.")
        else:
            print("Hata: 'snippet_topLevelComment_snippet_textDisplay' sütunu bulunamadı.")

    # Stopword'leri çıkarma
    def remove_stopwords(self, tokens):
        return [word for word in tokens if word not in self.stop_words]

    # Kelimeleri köklerine indirgeme (Stemming)
    def stem_words(self, tokens):
        return [self.stemmer.stem(word) for word in tokens]

    # Bir yorum üzerinde stopword çıkarma ve stemming işlemi
    def process_single_comment(self, tokens):
        # Stopword'leri çıkar
        tokens_no_stopwords = self.remove_stopwords(tokens)
        # Stemming yap
        tokens_stemmed = self.stem_words(tokens_no_stopwords)
        # Tokenları birleştirip string olarak dndüör
        return " ".join(tokens_stemmed)

    def save_to_csv(self, dosya_adi, columns):
        self.data[columns].to_csv(dosya_adi, index=False, encoding='utf-8-sig')
        print(f"Veriler '{dosya_adi}' dosyasına kaydedildi.")

    def analyze_sentiment(self,dosya_adi):
        #Yorumların duygusal analizini yapar ve sonuçları 'Duygu' sütununa ekler.
        sia = SentimentIntensityAnalyzer()
        df = pd.read_csv('datasets/processed/{0}.csv'.format(dosya_adi))

        def get_sentiment(yorum):
            # Yorumun duygu skorlarını hesapla
            if isinstance(yorum, str):
                scores = sia.polarity_scores(yorum)
                if scores['compound'] >= 0.05:
                    return "Pozitif"
                elif scores['compound'] <= -0.05:
                    return "Negatif"
                else:
                    return "Nötr"
            return "Bilinmiyor"
        
        # Yeni bir duygu kolonu ekleyin
        df['Duygu'] = df['yorum_islenmis'].apply(get_sentiment)
        print(df.head())
        print("Duygu analizi tamamlandı.")

def process_all_steps(self, dosya_adi):
        # Yorumları temizle
        self.data['yorum_temiz'] = self.data['snippet_topLevelComment_snippet_textDisplay'].apply(self.correct_comment)
        
        # Yorumları çevir
        for index, yazi in enumerate(self.data['yorum_temiz']):
            self.data.at[index, 'snippet_topLevelComment_snippet_textDisplay'] = self.translate_tr(yazi, index)
            if index % 100 == 0:
                print(f"[{index}] Çeviri işlemi devam ediyor...")

        # Gereksiz geçici sütunları kaldır
        self.data.drop(columns=['yorum_temiz'], inplace=True)
        self.save_to_csv(f'./datasets/{dosya_adi}_translated.csv', ['snippet_topLevelComment_snippet_textDisplay'])

        # Tokenizasyon
        self.tokenize_comments()
        self.save_to_csv(f'./datasets/tokenized/{dosya_adi}_tokenized.csv', ['yorum_tokenize'])

        # Stopword'leri çıkarma ve stemming
        self.data['yorum_no_stopwords'] = self.data['yorum_tokenize'].apply(self.remove_stopwords)
        self.data['yorum_stemmed'] = self.data['yorum_no_stopwords'].apply(self.stem_words)
        self.data['yorum_islenmis'] = self.data['yorum_stemmed'].apply(lambda tokens: " ".join(tokens))
        self.save_to_csv(f'./datasets/processed/{dosya_adi}_processed.csv', ['yorum_islenmis'])

        # Duygu analizi
        self.analyze_sentiment(f'{dosya_adi}_processed')
