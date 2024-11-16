import sys
import os

# models klasörünü modül yolu olarak ekleyin
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

from neurel_network_model import NeuralNetworkModel  # Artık buradan import edilebilir
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris  # Örnek veri kümesi, kendi verinizi kullanabilirsiniz

class TrainNeuralNetwork:
    def __init__(self, file_name):
        """Başlatıcı metod: Dosya adını alır ve veri setini yükler."""
        self.file_name = file_name
        self.X_train, self.X_test, self.y_train, self.y_test = self.load_data()

    def load_data(self):
        """Veriyi yükler ve eğitim ve test setlerine böler, dosya yoksa oluşturur."""
        # 'file_name' kullanarak dosya adlarını oluştur
        X_path = f"datasets/processed/{self.file_name}_X_data.pkl"
        y_path = f"datasets/processed/{self.file_name}_y_labels.pkl"
        X_test_path = f"datasets/processed/{self.file_name}_X_test.pkl"
        y_test_path = f"datasets/processed/{self.file_name}_y_test.pkl"

        # Eğer dosyalar yoksa, veriyi yükleyip bölüp kaydedin
        if not os.path.exists(X_path) or not os.path.exists(y_path) or not os.path.exists(X_test_path) or not os.path.exists(y_test_path):
            print("Dosyalar bulunamadı, veri yükleniyor ve kaydediliyor...")
            # Veriyi yükleyin (örnek olarak Iris veri kümesi kullanılıyor)
            data = load_iris()  # Burada kendi veri kümenizi yükleyebilirsiniz
            X = data.data
            y = data.target

            # Veriyi eğitim ve test setlerine ayırın
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Veriyi pickle ile kaydedin
            os.makedirs(os.path.dirname(X_path), exist_ok=True)  # Dosya yolunu oluşturun
            joblib.dump(X_train, X_path)
            joblib.dump(y_train, y_path)
            joblib.dump(X_test, X_test_path)
            joblib.dump(y_test, y_test_path)
            print(f"Veri kaydedildi: {X_path}, {y_path}, {X_test_path}, {y_test_path}")
        else:
            print("Dosyalar bulundu, yükleniyor...")
            # Dosyaları yükleyin
            X_train = joblib.load(X_path)
            y_train = joblib.load(y_path)
            X_test = joblib.load(X_test_path)
            y_test = joblib.load(y_test_path)

        return X_train, X_test, y_train, y_test

    def train_and_evaluate(self):
        """Modeli eğitir, değerlendirir ve kaydeder."""
        input_shape = self.X_train.shape[1]
        model = NeuralNetworkModel(input_shape=input_shape)

        # Modeli eğit
        history = model.train(self.X_train, self.y_train)

        # Modeli değerlendir
        if self.X_test is None or self.y_test is None:
            print("Test verileri eksik!")
            return  # Test verisi yoksa işlem yapma

        test_loss, test_accuracy = model.evaluate(self.X_test, self.y_test)

        # Tahminleri al ve sınıflandırma raporunu oluştur
        y_pred = np.argmax(model.model.predict(self.X_test), axis=1)  # Y_pred doğru alınmalı
        model.save_metrics(self.y_test, y_pred)

        # Modeli kaydet
        model.save_model()

if __name__ == "__main__":
    file_name = "CampusX-official_comments_processed"  # Burada dosya adını belirliyoruz
    trainer = TrainNeuralNetwork(file_name=file_name)  # Dosya adı parametre olarak veriliyor
    trainer.train_and_evaluate()
