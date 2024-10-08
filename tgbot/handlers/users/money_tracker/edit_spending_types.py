import logging

from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic
from aiogram.enums.content_type import ContentType

from tgbot.config import Config

from tgbot.states import MoneyTrackerStates

from tgbot.utils import Database, ScreenManager

from tgbot.handlers.users.money_tracker.settings import show_spending_types_list_for_edit

from tgbot.filters import MaxSpendingTypesAmountFilter, ValidateTypeNameFilter

from tgbot.misc.callback_data.navigation import NavigationActions, NavigationCbData
from tgbot.keyboards.money_tracker.edit_spending_types_kb import EditSpendingTypeActions, EditSpendingTypeCbData
from tgbot.keyboards.money_tracker.spending_types_kb import SpendingTypesCbData


edit_spending_types_router = Router(name=__name__)

# --- Выход в меню настроек --- #

@edit_spending_types_router.callback_query(
	NavigationCbData.filter(F.navigation == NavigationActions.back),
	StateFilter(MoneyTrackerStates.spending_types_edit_list)
)
async def cancel_editing_spending_types(callback: types.CallbackQuery, state: FSMContext):
	await state.set_state(MoneyTrackerStates.choosing_setting)
	await callback.message.edit_text(**ScreenManager.SETTINGS_MENU.as_kwargs())

# --- Выход в меню настроек --- #


# --- Выбран тип трат для изменения --- #

@edit_spending_types_router.callback_query(
	SpendingTypesCbData.filter(),
	StateFilter(MoneyTrackerStates.spending_types_edit_list)
)
async def choosed_spending_type_for_edit(callback: types.CallbackQuery, state: FSMContext, callback_data: SpendingTypesCbData):
	await state.update_data({"update_type_id": callback_data.type_id})
	await state.set_state(MoneyTrackerStates.spending_type_edit_choosed)
	await callback.message.edit_text(**ScreenManager.EDITING_SPENDING_TYPE.as_kwargs(user_id=callback.from_user.id, 
																					 type_id=callback_data.type_id))

# --- Выбран тип трат для изменения --- #


# --- Отмена редактирования выбранного типа --- #

@edit_spending_types_router.callback_query(
        NavigationCbData.filter(F.navigation == NavigationActions.back),
        StateFilter(MoneyTrackerStates.spending_type_edit_choosed)
)
async def cancel_editing_spending_type(callback: types.CallbackQuery, state: FSMContext):
    await show_spending_types_list_for_edit(callback, state)

# --- Отмена редактирования выбранного типа --- #


# --- Удаление типа трат --- #

# Сообщение о подтверждении удаления
@edit_spending_types_router.callback_query(
	EditSpendingTypeCbData.filter(F.action == EditSpendingTypeActions.delete),
	StateFilter(MoneyTrackerStates.spending_type_edit_choosed)
)
async def confirm_deleting_spending_type(callback: types.CallbackQuery, state: FSMContext):
	await state.set_state(MoneyTrackerStates.spending_type_deleting_confirm)
	await callback.message.edit_text(**ScreenManager.CONFIRM_DELETING_SPENDING_TYPE.as_kwargs())

# Удаление типа
@edit_spending_types_router.callback_query(
	EditSpendingTypeCbData.filter(F.action == EditSpendingTypeActions.delete),
	StateFilter(MoneyTrackerStates.spending_type_deleting_confirm)
)
async def delete_spending_type(callback: types.CallbackQuery, state: FSMContext, db: Database):
	state_data = await state.get_data()
	type_id = state_data.get("update_type_id")
	db.delete_spending_type(type_id)
	await state.set_state(MoneyTrackerStates.spending_types_edit_list)
	await callback.message.edit_text(**ScreenManager.SPENDING_TYPE_DELETED.as_kwargs(user_id=callback.from_user.id))

# Отмена удаления
@edit_spending_types_router.callback_query(
	NavigationCbData.filter(F.navigation == NavigationActions.back),
	StateFilter(MoneyTrackerStates.spending_type_deleting_confirm)
)
async def delete_spending_type(callback: types.CallbackQuery, state: FSMContext):
	state_data = await state.get_data()
	type_id = state_data.get("update_type_id")
	await state.set_state(MoneyTrackerStates.spending_type_edit_choosed)
	await callback.message.edit_text(**ScreenManager.EDITING_SPENDING_TYPE.as_kwargs(user_id=callback.from_user.id, 
																					 type_id=type_id))

# --- Удаление типа трат --- #


# --- Изменение названия типа трат --- #

@edit_spending_types_router.callback_query(
	EditSpendingTypeCbData.filter(F.action == EditSpendingTypeActions.edit),
	StateFilter(MoneyTrackerStates.spending_type_edit_choosed)
)
async def edit_spending_type_name(callback: types.CallbackQuery, state: FSMContext):
	await state.update_data({"message_id": callback.message.message_id})
	await state.set_state(MoneyTrackerStates.spending_type_edit_enter_new)
	await callback.message.edit_text(**ScreenManager.EDIT_SPENDING_TYPE_NAME.as_kwargs())


# Отмена изменения названия типа трат
@edit_spending_types_router.callback_query(
	NavigationCbData.filter(F.navigation == NavigationActions.back),
	StateFilter(MoneyTrackerStates.spending_type_edit_enter_new)
)
async def cancel_edit_spending_type_name(callback: types.CallbackQuery, state: FSMContext):
	state_data = await state.get_data()
	type_id = state_data.get("update_type_id")
	await state.set_state(MoneyTrackerStates.spending_type_edit_choosed)
	await callback.message.edit_text(**ScreenManager.EDITING_SPENDING_TYPE.as_kwargs(user_id=callback.from_user.id, 
																					 type_id=type_id))


# Валидация ввода нового названия типа трат
@edit_spending_types_router.message(
	F.content_type == ContentType.TEXT,
	ValidateTypeNameFilter(),
	StateFilter(MoneyTrackerStates.spending_type_edit_enter_new)
)
async def enter_invalid_new_spending_type_name(message: types.Message, state: FSMContext, bot: Bot, config: Config):
	state_data = await state.get_data()
	message_id : int = state_data.get("message_id")
	try:
		await bot.edit_message_text(
			chat_id=message.chat.id,
			message_id=message_id,
			**ScreenManager.ENTER_INVALID_SPENDING_TYPE.as_kwargs(max_len=config.bot_settings.max_spending_type_len))
	except:
		pass
	await message.delete()


# Ввод нового названия типа трат
@edit_spending_types_router.message(
	F.content_type == ContentType.TEXT,
	StateFilter(MoneyTrackerStates.spending_type_edit_enter_new)
)
async def enter_new_spending_type_name(message: types.Message, state: FSMContext, db: Database, bot: Bot):
	state_data = await state.get_data()
	type_id = state_data.get("update_type_id")
	db.update_spending_type(type_id, message.text)
	await state.set_state(MoneyTrackerStates.spending_types_edit_list)
	state_data = await state.get_data()
	message_id : int = state_data.get("message_id")
	await bot.edit_message_text(
		chat_id=message.chat.id,
		message_id=message_id,
		**ScreenManager.SPENDING_TYPE_NAME_EDITED.as_kwargs(user_id=message.from_user.id)
	)
	await message.delete()

# --- Изменение названия типа трат --- #


# --- Добавление нового типа трат --- #

# Проверка на максимальное число типов трат
@edit_spending_types_router.callback_query(
	EditSpendingTypeCbData.filter(F.action == EditSpendingTypeActions.new),
	MaxSpendingTypesAmountFilter(),
	StateFilter(MoneyTrackerStates.spending_types_edit_list)
)
async def max_spending_types_amount(callback: types.CallbackQuery, config: Config):
	await callback.answer(**ScreenManager.MAX_SPENDING_TYPES_ALERT.as_kwargs(max_types=config.bot_settings.max_spending_types_amount), show_alert=True)


@edit_spending_types_router.callback_query(
	EditSpendingTypeCbData.filter(F.action == EditSpendingTypeActions.new),
	StateFilter(MoneyTrackerStates.spending_types_edit_list)
)
async def add_new_spending_type(callback: types.CallbackQuery, state: FSMContext):
	await state.update_data({"message_id": callback.message.message_id})
	await state.set_state(MoneyTrackerStates.spending_type_enter_new)
	await callback.message.edit_text(**ScreenManager.ENTER_NEW_SPENDING_TYPE.as_kwargs())

# Отмена добавления нового типа трат
@edit_spending_types_router.callback_query(
	NavigationCbData.filter(F.navigation == NavigationActions.back),
	StateFilter(MoneyTrackerStates.spending_type_enter_new)
)
async def cancel_enter_new_spending_type(callback: types.CallbackQuery, state: FSMContext):
	await state.set_state(MoneyTrackerStates.spending_types_edit_list)
	await callback.message.edit_text(**ScreenManager.SETTINGS_EDIT_SPENDING_TYPES_LIST.as_kwargs(user_id=callback.from_user.id))

# Валидация ввода нового типа трат
@edit_spending_types_router.message(
	F.content_type == ContentType.TEXT,
	ValidateTypeNameFilter(),
	StateFilter(MoneyTrackerStates.spending_type_enter_new)
)
async def enter_invalid_new_spending_type(message: types.Message, state: FSMContext, bot: Bot, config: Config):
	await enter_invalid_new_spending_type_name(message, state, bot, config)

# Ввод нового типа трат
@edit_spending_types_router.message(
	F.content_type == ContentType.TEXT,
	StateFilter(MoneyTrackerStates.spending_type_enter_new)
)
async def enter_new_spending_type(message: types.Message, state: FSMContext, db: Database, bot: Bot):
	db.add_spending_type(message.from_user.id, type_name=message.text)
	await state.set_state(MoneyTrackerStates.spending_types_edit_list)
	state_data = await state.get_data()
	message_id : int = state_data.get("message_id")
	await bot.edit_message_text(
		chat_id=message.chat.id,
		message_id=message_id,
		**ScreenManager.NEW_SPENDING_TYPE_ADDED.as_kwargs(user_id=message.from_user.id)
	)
	await message.delete()

# --- Добавление нового типа трат --- #
