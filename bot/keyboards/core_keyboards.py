from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from bot.lexicon.core_lexicon import GAMES_BTN_LEXICON, RPS_GAME_LEXICON, RPS_ANSWER_LEXICON
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_keyboard_for_start_game() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = [KeyboardButton(text=GAMES_BTN_LEXICON['btn_1']),
                                                    KeyboardButton(text=GAMES_BTN_LEXICON['btn_2'])]

    kb_builder.row(*buttons, width=1)
    choice_game_keyboard = kb_builder.as_markup(resize_keyboard=True)
    return choice_game_keyboard

#rps - Rock paper scissors(Камень ножницы бумага)

def get_keyboard_for_game_rps() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = [KeyboardButton(text=RPS_GAME_LEXICON['R']),
                                              KeyboardButton(text=RPS_GAME_LEXICON['P']), KeyboardButton(text=RPS_GAME_LEXICON['S'])]

    kb_builder.row(*buttons, width=1)
    game_rps_keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)
    return game_rps_keyboard

def get_inline_keyboard_for_start() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text=GAMES_BTN_LEXICON['btn_1'],
                                                                       callback_data=GAMES_BTN_LEXICON['btn_1']),
                                                  InlineKeyboardButton(text=GAMES_BTN_LEXICON['btn_2'],
                                                           callback_data=GAMES_BTN_LEXICON['btn_2'])]
    kb_builder.row(*buttons, width=1)

    keyboard = kb_builder.as_markup()
    return keyboard

def get_inline_keyboard_for_rps() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text=RPS_GAME_LEXICON['R'], callback_data=RPS_GAME_LEXICON['R']),
                                     InlineKeyboardButton(text=RPS_GAME_LEXICON['P'], callback_data=RPS_GAME_LEXICON['P']),
                                     InlineKeyboardButton(text=RPS_GAME_LEXICON['S'], callback_data=RPS_GAME_LEXICON['S'])]

    kb_builder.row(*buttons, width=1)
    keyboard = kb_builder.as_markup(resize_keyboard=True)
    return keyboard

def get_inline_keyboard_answer_rps():
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text=RPS_ANSWER_LEXICON['no'], callback_data=RPS_ANSWER_LEXICON['no']),
                                     InlineKeyboardButton(text=RPS_ANSWER_LEXICON['yes'], callback_data=RPS_ANSWER_LEXICON['yes'])]

    kb_builder.row(*buttons, width=1)
    keyboard = kb_builder.as_markup(resize_keyboard=True)
    return keyboard