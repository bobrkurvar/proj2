from typing import Any
from bot.utils.game_sea_battle_util import get_field
GAMES_BTN_LEXICON: dict[str, str] = {
    'rps': 'Камень ножницы бумага',
    'btn_2': 'Угадай число',
    'sea_battle': 'Морской бой',
}

#ROCK PAPER SCISSORS - КАМЕНЬ НОЖНИЦЫ БУМАГА
RPS_GAME_LEXICON: dict[str, str] = {
    'R': 'Камень - ⛰️',

    'P': 'Бумага - 📄',

    'S': 'Ножницы - ✂️'

}

RPS_ANSWER_LEXICON_MSG: dict[str, str] = {
    "result_msg": 'Ваш ход - {}\n\nМой ход - {}\n\n',
    "player win": 'Вы победили 🏆🏆🏆\n',
    'bot win': 'Вы проиграли 🏳️🏳️🏳️\n',
    'draw': 'Ничья ❔❔❔',
    'repeat_msg': 'Играем дальше? ✅✅✅ ❌❌❌',
}

RPS_ANSWER_LEXICON_BTN = {
    'yes': 'yes - ✅✅✅',
    'no': 'no - ❌❌❌'
}

def get_sea_battle_field_lexicon(fld: list[list[int]], h: int = 8) -> dict[str, str]:
    map_for_cell = {1: '🚢', 0: '', 2: '🌊', 3: '💥'}
    keys = []
    values = []
    for i in range(h):
        for j in range(h):
            keys.append(f'{i}{j}')
            values.append(map_for_cell[fld[i][j]])
    res = dict(zip(keys, values))
    print(res)
    return res
get_sea_battle_field_lexicon(get_field())