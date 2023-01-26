"""
    Telegram event handlers
"""
from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
    InlineQueryHandler
)

from dtb.settings import DEBUG
from tgbot.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST
from tgbot.handlers.broadcast_message.static_text import broadcast_command
from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON

from tgbot.handlers.utils import files, error
from tgbot.handlers.admin import handlers as admin_handlers
from tgbot.handlers.location import handlers as location_handlers
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.broadcast_message import handlers as broadcast_handlers
from tgbot.handlers.inline import handlers as inline_handlers
from tgbot.main import bot
from tgbot.handlers.onboarding.static_text import (
    ayuda_button,
    noticias_button,
    volver_menu_button,
    volver_button,
    catalogo_button,
    faq_buttons,
    log_button)

def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    # onboarding
    dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))

    # admin commands
    dp.add_handler(CommandHandler("admin", admin_handlers.admin))
    dp.add_handler(CommandHandler("stats", admin_handlers.stats))
    dp.add_handler(CommandHandler('export_users', admin_handlers.export_users))

    # location
    dp.add_handler(CommandHandler("ask_location", location_handlers.ask_for_location))
    dp.add_handler(MessageHandler(Filters.location, location_handlers.location_handler))

    #regex
    dp.add_handler(MessageHandler(Filters.regex(fr'{catalogo_button}'), onboarding_handlers.catalogo))
    dp.add_handler(MessageHandler(Filters.regex(fr'{ayuda_button}'), onboarding_handlers.ayuda))
    dp.add_handler(MessageHandler(Filters.regex(fr'{noticias_button}'), onboarding_handlers.noticias))
    dp.add_handler(MessageHandler(Filters.regex(fr'{faq_buttons}'), onboarding_handlers.faq))
    dp.add_handler(MessageHandler(Filters.regex(fr'{log_button}'), onboarding_handlers.log))
    dp.add_handler(MessageHandler(Filters.regex(fr'{volver_menu_button}'), onboarding_handlers.command_start))
    dp.add_handler(MessageHandler(Filters.regex(fr'{volver_button}'), onboarding_handlers.catalogo))


    # secret level
    dp.add_handler(CallbackQueryHandler(onboarding_handlers.secret_level, pattern=f"^{SECRET_LEVEL_BUTTON}"))

    # broadcast message
    dp.add_handler(
        MessageHandler(Filters.regex(rf'^{broadcast_command}(/s)?.*'), broadcast_handlers.broadcast_command_with_message)
    )
    dp.add_handler(
        CallbackQueryHandler(broadcast_handlers.broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}")
    )

    # files
    dp.add_handler(MessageHandler(
        Filters.animation | Filters.photo  | Filters.video | Filters.video_note | Filters.document | Filters.sticker, files.show_file_id,
    ))
    #regex especiales
    dp.add_handler(MessageHandler(Filters.text, onboarding_handlers.text_filtro))
    dp.add_handler(InlineQueryHandler(inline_handlers.inline_query))

    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(
    #     Filters.document, <function_handler>,
    # ))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(
    #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,
    # ))

    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
