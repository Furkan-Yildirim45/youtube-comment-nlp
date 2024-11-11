import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import EarlyStopping
from sklearn.metrics import classification_report
import json
import os

class NeuralNetworkModel:
    def __init__(self, input_shape, num_classes=3):
        self.model = self._build_model(input_shape, num_classes)

    def _build_model(self, input_shape, num_classes):
        model = Sequential([
            Dense(512, activation='relu', input_shape=(input_shape,)),
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
        # Klasörün varlığını kontrol et, yoksa oluştur
        if not os.path.exists(os.path.dirname(model_path)):
            os.makedirs(os.path.dirname(model_path))

        self.model.save(model_path)
        print(f"Model '{model_path}' dosyasına kaydedildi.")

    def save_metrics(self, y_test, y_pred, report_path='models/neural_network/model_metrics.json'):
        # Klasörün varlığını kontrol et, yoksa oluştur
        if not os.path.exists(os.path.dirname(report_path)):
            os.makedirs(os.path.dirname(report_path))

        # Sınıflandırma raporunu oluştur
        report = classification_report(y_test, y_pred, target_names=['Pozitif', 'Negatif', 'Nötr'])
        print(report)

        # JSON formatında raporu kaydet
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=4)
        print(f"Model metrikleri '{report_path}' dosyasına kaydedildi.")
