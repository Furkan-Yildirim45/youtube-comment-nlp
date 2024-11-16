import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import EarlyStopping
from sklearn.metrics import classification_report
import json
import os
from tensorflow.keras.preprocessing.text import Tokenizer  # Burada tensorflow.keras kullanıyoruz
from tensorflow.keras.preprocessing.sequence import pad_sequences  # Burada tensorflow.keras kullanıyoruz

class NeuralNetworkModel:
    def __init__(self, input_shape=None, num_classes=3, model_path=None):
        if model_path is not None:
            self.model = self.load_model(model_path)
        else:
            self.model = self._build_model(input_shape, num_classes)
        self.tokenizer = Tokenizer()  # Tokenizer'ı başlatıyoruz

    def _build_model(self, input_shape, num_classes):
        model = Sequential([
            Dense(512, activation='relu', input_shape=(input_shape,)),  # input_shape burada (100,) olmalı
            Dropout(0.5),
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(num_classes, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model


    def train(self, X_train, y_train, epochs=20, batch_size=32, validation_split=0.2):
        early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
        history = self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,
                                 validation_split=validation_split, callbacks=[early_stopping])
        return history

    def evaluate(self, X_test, y_test):
        if X_test is None or y_test is None:
            raise ValueError("X_test veya y_test verisi geçerli değil!")
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test)
        print(f"Test doğruluğu: {test_accuracy}")
        return test_loss, test_accuracy

    def save_model(self, model_path='models/neural_network/model.keras'):
        if not os.path.exists(os.path.dirname(model_path)):
            os.makedirs(os.path.dirname(model_path))
        self.model.save(model_path)
        print(f"Model '{model_path}' dosyasına kaydedildi.")

    def save_metrics(self, y_test, y_pred, report_path='models/neural_network/model_metrics.json'):
        if not os.path.exists(os.path.dirname(report_path)):
            os.makedirs(os.path.dirname(report_path))
        report = classification_report(y_test, y_pred, target_names=['Pozitif', 'Negatif', 'Nötr'])
        print(report)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=4)
        print(f"Model metrikleri '{report_path}' dosyasına kaydedildi.")

    def load_model(self, model_path):
        from keras.models import load_model
        self.model = load_model(model_path)
        print(f"Model '{model_path}' başarıyla yüklendi.")
        return self.model

    def preprocess_text(self, text):
        # Metni sayısal verilere dönüştür ve modelin beklediği uzunluğa indir
        self.tokenizer.fit_on_texts([text])  # Tokenizer'ı metinle eğit
        sequence = self.tokenizer.texts_to_sequences([text])  # Metni sayısal verilere dönüştür
        padded_sequence = pad_sequences(sequence, maxlen=4)  # Maksimum uzunluk 4 olacak şekilde padding uygula
        return padded_sequence

    def predict_sentiment(self, text):
        if self.model is None:
            raise ValueError("Model yüklenmedi. Lütfen önce bir model yükleyin.")
        
        # Metni sayısal verilere dönüştür
        processed_text = self.preprocess_text(text)
        predictions = self.model.predict(processed_text)  # Sayısal veriyi modele gönder

        # Tahmin edilen sınıfı döndür
        class_index = np.argmax(predictions, axis=-1)[0]
        class_names = ['Pozitif', 'Negatif', 'Nötr']  # Sınıf isimleri
        return class_names[class_index]


if __name__ == "__main__":
    # Modeli yükleyin veya oluşturun
    model_path = "./models/neural_network/model.keras"
    nn_model = NeuralNetworkModel(model_path=model_path)  # Mevcut model yoksa input_shape belirlenmeli

    # Yeni bir yorum sınıflandırmak
    comment = "Bu video gerçekten çok faydalıydı!"
    result = nn_model.predict_sentiment(comment)
    print(f"Yorumun duygu durumu: {result}")

