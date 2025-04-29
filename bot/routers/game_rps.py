from aiogram import Router, F
from aiogram.types import  CallbackQuery
from bot.keyboards.core_keyboards import get_inline_keyboard_for_rps, get_inline_keyboard_answer_rps
from bot.lexicon.core_lexicon import RPS_ANSWER_LEXICON
from bot.utils import game_rps_util

router = Router()

#rps - Rock paper scissors(Камень ножницы бумага)

@router.callback_query((F.data == 'Камень ножницы бумага') | F.data.lower().startswith('yes'))
async def process_rps_game(callback: CallbackQuery):
    await callback.message.answer(text="Ваш ход", reply_markup=get_inline_keyboard_for_rps())
    await callback.answer()
    await callback.message.delete()

@router.callback_query(F.data.in_({'Камень - ⛰️'}))
async def process_rock(callback: CallbackQuery):
    result = game_rps_util.win_or_lose('R')
    await callback.message.answer(text=RPS_ANSWER_LEXICON['result_msg'].format('Камень - ⛰️', result[0]) + RPS_ANSWER_LEXICON[result[1]],
                                  reply_markup=get_inline_keyboard_answer_rps())
    await callback.answer()
    await callback.message.delete()

@router.callback_query(F.data.in_({'Бумага - 📄'}))
async def process_paper(callback: CallbackQuery):
    result = game_rps_util.win_or_lose('P')
    await callback.message.answer(text=RPS_ANSWER_LEXICON['result_msg'].format('Бумага - 📄', result[0]) + RPS_ANSWER_LEXICON[result[1]],
                                  reply_markup=get_inline_keyboard_answer_rps())
    await callback.answer()
    await callback.message.delete()

@router.callback_query(F.data.in_({'Ножницы - ✂️'}))
async def process_scissors(callback: CallbackQuery):
    result = game_rps_util.win_or_lose('S')
    await callback.message.answer(text=RPS_ANSWER_LEXICON['result_msg'].format('Ножницы - ✂️', result[0]) + RPS_ANSWER_LEXICON[result[1]],
                                  reply_markup=get_inline_keyboard_answer_rps())
    await callback.answer()
    await callback.message.delete()

@router.callback_query(F.data.lower().startswith('no'))
async def process_no_repeat(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

