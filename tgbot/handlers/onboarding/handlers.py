import datetime

from django.utils import timezone
from telegram import ParseMode, Update, InlineQueryResultPhoto, InputMediaPhoto
from telegram.ext import CallbackContext

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User
from tgbot.handlers.onboarding.keyboards import (
    make_keyboard_for_start_command,
    make_keyboard_for_categorias,
    make_keyboard_for_anime,
    make_keyboard_for_ayuda
)
from catalogo.models import Category, Anime


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_sticker(static_text.start_sticker)
    update.message.reply_text(text=text,
                              reply_markup=make_keyboard_for_start_command())


def secret_level(update: Update, context: CallbackContext) -> None:
    # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )


#Catalogo
def catalogo(update: Update, context: CallbackContext):
    categorias = Category.objects.all()
    if categorias:
        text = "categorias:"
        update.message.reply_sticker(static_text.catalogo_sticker)
        update.message.reply_text(text=text, reply_markup=make_keyboard_for_categorias(categorias))
    else:
        update.message.reply_sticker(static_text.catalogo_sticker)
        update.message.reply_text(text='No hay Catalogo aun')

#Ayuda
def ayuda(update: Update, context: CallbackContext):
    update.message.reply_text(text=static_text.ayuda_text, reply_markup=make_keyboard_for_ayuda())

#Noticias
def noticias(update, context):
    update.message.reply_text(text='No hay Noticias aun')

def anime(update, context, kword):
    category_id = Category.objects.get(name=kword).id
    animes = Anime.objects.filter(category=category_id)
    text = 'Animes:'
    update.message.reply_text(text, reply_markup=make_keyboard_for_anime(animes))

def anime_detail(update: Update, context: CallbackContext, name):
    anime = Anime.objects.get(name=name)
    text= f'Nombre: {anime.name}\nG??nero: {anime.genero}\nCap??tulos: {anime.capitulos}\nCompa????a: {anime.compania}\nFecha: {anime.date}\nDescripci??n:\n{anime.descripcion}'
    update.message.reply_photo(anime.imagen, text, parse_mode=ParseMode.HTML)

def text_filtro(update: Update, context: CallbackContext):
    text = update.message.text
    categorias = Category.objects.all()
    lista_categorias = [categoria.name for categoria in categorias]

    if text in lista_categorias:
        anime(update, context, text)
        return
    animes = Anime.objects.all()
    lista_animes = [anime.name for anime in animes]

    if text in lista_animes:
        anime_detail(update, context, text)

def faq(update: Update, context: CallbackContext):
    update.message.reply_text(static_text.faq_text)

def log(update: Update, context: CallbackContext):
    update.message.reply_text(static_text.log_text)
