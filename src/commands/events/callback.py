from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == 'canceled_tribunal' or
                       F.data == 'ended_tribunal' or
                       F.data == 'confirm' or
                       F.data == 'unconfirm')
async def callback_no_answer(callback: CallbackQuery) -> None:
    await callback.answer()
