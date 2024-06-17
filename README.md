## versiyon 0.1 

## bir sonraki güncelleme 
bir sonraki güncelleme de cüzdan şeklinde yapmayı düşünüyorum şuanda ödeme yapanları ayrı ayrı tutmuyor data da no sql ile sadece anlık ödeme yapma işlevi var ek özelik isteklerinizi ütfen iletin destek için [telegram](t.me/yaaniyakup)

# Telegram Papara kişisel hesap için  Ödeme alma  Botu

Bu, Kişisel Papara  hesabı üzerinden yapılan ödemeleri belirli ödeme bilgilerini kontrol ederek doğrulayan bir Telegram botudur. Bot, kullanıcılara ödeme yaparken kullanmaları için benzersiz bir açıklama sağlar ve bu açıklamayı içeren e-posta içeriğini kontrol ederek ödemeyi doğrular.

## Özellikler

- Her ödeme isteği için benzersiz bir açıklama oluşturur.
- Gelen Papara e-postalarını kontrol ederek ödemeleri doğrular.
- Kullanıcılara Telegram üzerinden gerçek zamanlı ödeme onayı sağlar.

## Gereksinimler

- Python 3.7+
- BotFather'dan alınmış bir Telegram bot tokeni.
- IMAP erişimi etkinleştirilmiş bir Gmail hesabı.
- Gmail için uygulamaya özel bir şifre.

## Kurulum

1. Depoyu klonlayın:

    ```sh
    git clone https://github.com/yaaniyakup/papara.git
    cd papara
    ```

2. Gerekli Python paketlerini yükleyin:

    ```sh
    pip install -r requirements.txt
    ```

3. `papara_payment_bot.py` ve `email_checker.py` dosyasındaki yapılandırma bilgilerini güncelleyin:

    ```python
    # papara_payment_bot.py
    TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'
    # email_checker.py
    EMAIL_USER = 'your_email@gmail.com'
    EMAIL_PASS = 'your_application_specific_password'
    IMAP_SERVER = 'imap.gmail.com'
    
    ```

4. Gmail hesabınızda IMAP erişiminin etkinleştirildiğinden emin olun ve iki faktörlü kimlik doğrulama etkinse uygulamaya özel bir şifre oluşturun.

## Kullanım

1. Botu çalıştırın:

    ```sh
    python papara_payment_bot.py
    ```

2. Bot ile Telegram üzerinden etkileşime geçin:

    - `/start` komutunu kullanarak botu başlatın.
    - `/pay` komutunu kullanarak ödeme bilgisi isteyin.
    - `/confirm` komutunu kullanarak ödemeyi onaylayın.

## Dosya Açıklamaları

- `papara_payment_bot.py`: Telegram komutlarını ve ödeme doğrulamasını yöneten ana bot betiği.
- `email_checker.py`: Gelen e-postaları ödeme doğrulaması için kontrol eden betik.

## Telegram Komutları

- `/start`: Botu başlatır ve hoş geldiniz mesajı gönderir.
- `/pay`: Benzersiz bir ödeme açıklaması oluşturur ve ödeme talimatlarını gönderir.
- `/confirm`: Ödeme doğrulamasını kontrol eder ve kullanıcıyı bilgilendirir.

## Detaylı İş Akışı

1. **/start Komutu**:
    - Bot kullanıcıyı karşılar ve ödeme yapma talimatlarını verir.
2. **/pay Komutu**:
    - Bot benzersiz bir açıklama oluşturur ve kullanıcıya Papara hesap bilgilerini ve benzersiz açıklamayı gönderir.
3. **/confirm Komutu**:
    - Bot gelen e-postaları kullanıcının açıklamasıyla kontrol eder. Eşleşen bir e-posta bulunursa, bot ödemeyi onaylar.

## Örnek E-posta Yapısı

Ödemeleri doğrularken bot, aşağıdaki yapıya sahip e-postaları kontrol eder:

- **Gönderen**: Papara <bilgi@papara.com>
- **Konu**: "Hesabına" veya "hesabında" kelimelerini içeren.
- **Gövde**: Kullanıcıya verilen benzersiz açıklamayı içeren.

## Notlar

- E-posta kimlik bilgilerinizi güvende tuttuğunuzdan emin olun.
- Hassas bilgileri üretim ortamında çevresel değişkenler veya güvenli bir kasada saklayın.

## Katkıda Bulunma
bana destek olmak için repo ya yıldız verin 
küçük bir destek için papara : 1087365760

1. Depoyu forklayın.
2. Yeni bir dal oluşturun (`git checkout -b feature-branch`).
3. Değişikliklerinizi yapın.
4. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik ekle'`).
5. Dala push edin (`git push origin feature-branch`).
6. Yeni bir Pull Request oluşturun.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasına bakın.

