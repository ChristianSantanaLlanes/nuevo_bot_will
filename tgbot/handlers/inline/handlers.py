from telegram import Update, InlineQueryResultPhoto, InputMediaPhoto
from telegram.ext import CallbackContext

from catalogo.models import Anime

def inline_query(update: Update, context: CallbackContext):
    query = update.inline_query.query
    animes = Anime.objects.filter(name__icontains=query)
    max_result = len(animes)
    step = 10
    offset = update.inline_query.offset
    if offset == '':
        offset = 0
    else:
        offset = int(offset)
    next_offset = offset + step if offset + step < max_result else None
    results = [InlineQueryResultPhoto(anime.id,anime.imagen, anime.imagen,title=anime.name, description=anime.descripcion ,caption=f'Nombre: {anime.name}\nGénero: {anime.genero}\nCapítulos: {anime.capitulos}\nCompañía: {anime.compania}\nFecha: {anime.date}\nDescripción:\n{anime.descripcion}', input_message_content=InputMediaPhoto(anime.imagen)) for anime in animes[offset: next_offset]]
    update.inline_query.answer(results)