import nltk
from services.comment_service import CommentService

def main():
    dosya_adi = "CampusX-translated_comments"
    yorum_servisi = CommentService(f'./datasets/{dosya_adi}.csv')
    
    # Tek seferde tüm işlemleri gerçekleştir
    yorum_servisi.process_all_steps(dosya_adi)

if __name__ == "__main__":
    main()



#şuanda githuba push etmedim çok fazla veri seti var onları bi temizlemek lazım tek veri setinde halletsem yeterlidir.
