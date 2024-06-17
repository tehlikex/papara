import logging
import time
import warnings
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from email_checker import check_email_for_payment  # email_checker.py'deki fonksiyonu içe aktarın

# Uyarı mesajını bastırma
warnings.filterwarnings("ignore", category=UserWarning, module='telegram')

# Telegram Bot API tokeninizi buraya ekleyin
TELEGRAM_BOT_TOKEN = 'telegram bot tokeniniz'

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ödeme bilgilerini saklamak için basit bir yapı
user_payments = {}

# Benzersiz açıklama oluşturma
def generate_unique_description(user_id):
    return f"payment_{user_id}_{int(time.time())}"

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_markdown_v2(
        fr'Hoş geldiniz {user.mention_markdown_v2()}\! Papara ile ödeme yapmak için /pay komutunu kullanabilirsiniz\.',
    )

# /pay komutu
async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    description = generate_unique_description(user.id)
    user_payments[user.id] = description

    papara_account_info = "1234567890"  # Papara hesap numaranızı buraya ekleyin
    await update.message.reply_text(
        f'Lütfen Papara hesabınıza ödeme yapın. Açıklama: {description}\n'
        f'Hesap Numarası: {papara_account_info}\n'
        'Ödeme yaptıktan sonra onaylamak için /confirm komutunu kullanabilirsiniz.',
        reply_markup=ReplyKeyboardRemove()
    )

# /confirm komutu
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.id in user_payments:
        description = user_payments[user.id]
        await update.message.reply_text('Ödemenizi kontrol ediyoruz, lütfen bekleyin...')
        
        if check_email_for_payment(description):
            await update.message.reply_text('Ödemeniz başarıyla alındı! Teşekkür ederiz.')
            del user_payments[user.id]
        else:
            await update.message.reply_text('Henüz ödeme alınmadı. Lütfen tekrar kontrol edin.')
    else:
        await update.message.reply_text('Ödeme açıklamanız bulunamadı. Lütfen önce /pay komutunu kullanarak ödeme yapın.')

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Komut işleyicileri
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pay", pay))
    application.add_handler(CommandHandler("confirm", confirm))

    # Botu başlatma
    application.run_polling()

if __name__ == '__main__':
    main()
