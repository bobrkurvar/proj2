
START_LEXICON: dict[str, str] = {
    'start_msg': '''Выбирайте что хотите из списка что вы видите ниже:\n\nКамень ножницы бумага - для игры в одноимённую игру\n\nУгадай число - для игры в одноимённую игру''',
}

GAMES_BTN_LEXICON: dict[str, str] = {
    'rps': 'Камень ножницы бумага',
    'btn_2': 'Угадай число',

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