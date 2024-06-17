import logging
import time
import warnings
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from email_checker import check_email_for_payment
from database import init_db, get_balance, update_balance

# Uyarı mesajını bastırma
warnings.filterwarnings("ignore", category=UserWarning, module='telegram')

# Yapılandırma bilgileri
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Veritabanını başlatma
init_db()

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

    await update.message.reply_text(
        f'Lütfen Papara hesabınıza ödeme yapın. Açıklama: {description}\n'
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
            update_balance(user.id, 100)  # Ödeme tutarını buraya ekleyin
            del user_payments[user.id]
        else:
            await update.message.reply_text('Henüz ödeme alınmadı. Lütfen tekrar kontrol edin.')
    else:
        await update.message.reply_text('Ödeme açıklamanız bulunamadı. Lütfen önce /pay komutunu kullanarak ödeme yapın.')

# /balance komutu
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    balance = get_balance(user.id)
    if balance is not None:
        await update.message.reply_text(f'Bakiyeniz: {balance} TL')
    else:
        await update.message.reply_text('Bakiyeniz bulunmamaktadır.')

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Komut işleyicileri
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pay", pay))
    application.add_handler(CommandHandler("confirm", confirm))
    application.add_handler(CommandHandler("balance", balance))

    # Botu başlatma
    application.run_polling()

if __name__ == '__main__':
    main()
