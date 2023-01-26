from telegram import ReplyKeyboardMarkup, KeyboardButton

# from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
from tgbot.handlers.onboarding import static_text


def make_keyboard_for_start_command() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(static_text.noticias_button)
        ],
        [
            KeyboardButton(static_text.catalogo_button),
            KeyboardButton(static_text.ayuda_button)
        ]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def make_keyboard_for_categorias(categorias) -> ReplyKeyboardMarkup:
    lista_buttons = []
    for category in categorias:
        lista_row = []
        button = KeyboardButton(f'{category.name}')
        lista_row.append(button)
        lista_buttons.append(lista_row)
    button_back = KeyboardButton(static_text.volver_menu_button)
    lista_buttons.append([button_back])
    return ReplyKeyboardMarkup(lista_buttons, resize_keyboard=True)

def make_keyboard_for_anime(animes) -> ReplyKeyboardMarkup:
    lista_buttons = []
    for anime in animes:
        lista_row = []
        button = KeyboardButton(f'{anime.name}')
        lista_row.append(button)
        lista_buttons.append(lista_row)
    button_back = KeyboardButton(static_text.volver_button)
    lista_buttons.append([button_back])
    return ReplyKeyboardMarkup(lista_buttons, resize_keyboard=True)

def make_keyboard_for_ayuda() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(static_text.faq_buttons), KeyboardButton(static_text.log_button)],
        [KeyboardButton(static_text.volver_menu_button)]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)