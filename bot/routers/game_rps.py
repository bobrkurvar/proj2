from aiogram import Router, F
from aiogram.types import  CallbackQuery
from bot.keyboards.core_keyboards import get_inline_kb
from bot.lexicon.core_lexicon import RPS_GAME_LEXICON, RPS_ANSWER_LEXICON_MSG, RPS_ANSWER_LEXICON_BTN
from bot.utils import game_rps_util

router = Router()

#rps - Rock paper scissors(Камень ножницы бумага)


@router.callback_query((F.data == 'rps') | F.data.lower().startswith('yes'))
async def process_rps_game(callback: CallbackQuery):
    keyboard = get_inline_kb(**RPS_GAME_LEXICON)
    await callback.message.answer(text="Ваш ход", reply_markup=keyboard)
    await callback.answer()
    await callback.message.delete()

@router.callback_query(F.data.in_({'R', 'P', 'S'}))
async def process_rps(callback: CallbackQuery):
    keyboard = get_inline_kb(**RPS_ANSWER_LEXICON_BTN)
    result = game_rps_util.win_or_lose(callback.data)
    await callback.message.answer(text=RPS_ANSWER_LEXICON_MSG['result_msg'].format(RPS_GAME_LEXICON[callback.data], result[0])
                                       + RPS_ANSWER_LEXICON_MSG[result[1]],
                                  reply_markup=keyboard)
    await callback.answer()
    await callback.message.delete()

@router.callback_query(F.data.lower().startswith('no'))
async def process_no_repeat(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

