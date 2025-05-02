# from aiogram import Router, F
# from aiogram.types import CallbackQuery
# from bot.keyboards.core_keyboards import get_inline_kb
# from bot.lexicon.games_lexicon import get_sea_battle_field_lexicon
# from bot.filters.callback_factory import CallbackFactorySeaBattle
# from copy import deepcopy
#
# router = Router()
# fld = get_field()
# @router.callback_query(F.data == 'sea_battle')
# async def process_game_start(callback: CallbackQuery):
#     lex = get_sea_battle_field_lexicon(fld)
#     keyboard = get_inline_kb(**lex, width=8)
#     await callback.message.answer(text="Ваш ход", reply_markup=keyboard)
#     await callback.answer()
#     await callback.message.delete()
#
# @router.callback_query(CallbackFactorySeaBattle.filter())
# async def process_shot(callback: CallbackQuery):
#     x = int(callback.data.split(':')[1])
#     y = int(callback.data.split(':')[0])
#     fld[x][y] = 3
#     lex =
#     keyboard = get_inline_kb(**SEA_BATTLE_LEXICON, width=8)
#     await callback.message.answer(text="Ваш ход", reply_markup=keyboard)
#     await callback.answer()
#     await callback.message.delete()