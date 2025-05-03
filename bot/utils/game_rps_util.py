from random import choice
from bot.lexicon.core_lexicon import RPS_GAME_LEXICON

cases_for_player = ['R','S', 'P']

draw_cases = [(i,j) for i in cases_for_player for j in cases_for_player if i == j]
res_cases = [(i,j) for i in cases_for_player for j in cases_for_player if i != j]
win_cases = [ i for i in res_cases if (i[0] == 'R' and i[1] == 'S')
                  or (i[0] == 'S' and i[1] == 'P') or (i[0] == 'P' and i[1] == 'R') ]

def win_or_lose(player: str) -> list[str]:
    bot = choice(cases_for_player)
    res = [RPS_GAME_LEXICON[bot]]
    if (bot, player) in draw_cases:
        res.append("draw")
    elif (bot, player) in win_cases:
        res.append("bot win")
    else:
        res.append("player win")
    return res

if __name__ == '__main__':
    while win_or_lose('R') != 'player win':
        print(win_or_lose('R'))
    else: print("player win")