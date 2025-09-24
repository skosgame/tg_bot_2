"""
Главный файл телеграм-бота для мотивации предпринимателей.
"""
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config.settings import BOT_TOKEN
from bot.handlers import (
    start_command,
    handle_message,
    handle_impressive_button,
    error_handler
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Основная функция для запуска бота.
    """
    # Проверяем наличие токена
    if not BOT_TOKEN:
        logger.error('BOT_TOKEN не найден! Создайте файл .env и добавьте токен бота.')
        return
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler('start', start_command))
    
    # Добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Добавляем обработчик callback-запросов (кнопки)
    application.add_handler(CallbackQueryHandler(handle_impressive_button, pattern='impressive'))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    logger.info('Запуск бота...')
    application.run_polling(allowed_updates=['message', 'callback_query'])


if __name__ == '__main__':
    main()