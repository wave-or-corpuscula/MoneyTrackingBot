import logging

from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic

from tgbot.states import MainMenuStates, MoneyTrackerStates

from tgbot.utils import Database, ScreenManager

from tgbot.handlers.users.money_tracker.settings import show_spending_types_list_for_edit

from tgbot.misc.callback_data.navigation import NavigationActions, NavigationCbData
from tgbot.keyboards.money_tracker.edit_spending_types_kb import EditSpendingTypeActions, EditSpendingTypeCbData
from tgbot.keyboards.money_tracker.settings_menu_kb import MTSettingsMenuActions, MTSettingsMenuCbData
from tgbot.keyboards.money_tracker.spending_types_kb import SpendingTypesCbData


edit_spending_types_router = Router(name=__name__)

# Выход в меню настроек
@edit_spending_types_router.callback_query(
	NavigationCbData.filter(F.navigation == NavigationActions.back),
	StateFilter(MoneyTrackerStates.spending_types_edit_list)
)
async def cancel_editing_spending_types(callback: types.CallbackQuery, state: FSMContext):
	await state.set_state(MoneyTrackerStates.choosing_setting)
	await callback.message.edit_text(**ScreenManager.SETTINGS_MENU.as_kwargs())

# Выбран тип трат для изменения
@edit_spending_types_router.callback_query(
	SpendingTypesCbData.filter(),
	StateFilter(MoneyTrackerStates.spending_types_edit_list)
)
async def choosed_spending_type_for_edit(callback: types.CallbackQuery, state: FSMContext, callback_data: SpendingTypesCbData):
	await state.update_data({"update_type_id": callback_data.type_id})
	await state.set_state(MoneyTrackerStates.spending_type_edit_choosed)
	await callback.message.edit_text(**ScreenManager.EDITING_SPENDING_TYPE.as_kwargs(user_id=callback.from_user.id, 
																					 type_id=callback_data.type_id))

# Удаление типа трат
@edit_spending_types_router.callback_query(
	EditSpendingTypeCbData.filter(F.action == EditSpendingTypeActions.delete),
	StateFilter(MoneyTrackerStates.spending_type_edit_choosed)
)
async def delete_spending_type(callback: types.CallbackQuery, state: FSMContext, db: Database):
	state_data = await state.get_data()
	type_id = state_data.get("update_type_id")
	db.delete_spending_type(type_id)
	await state.set_state(MoneyTrackerStates.choosing_setting)
	await callback.message.edit_text(**ScreenManager.SPENDING_TYPE_DELETED.as_kwargs())


# Изменение названия типа трат
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

# Ввод нового названия типа трат
@edit_spending_types_router.message(
	StateFilter(MoneyTrackerStates.spending_type_edit_enter_new)
)
async def enter_new_spending_type_name(message: types.Message, state: FSMContext, db: Database, bot: Bot):
	state_data = await state.get_data()
	type_id = state_data.get("update_type_id")
	if len(message.text) > 64:
		raise Exception("Type name is too big")
	db.update_spending_type(type_id, message.text)
	await state.set_state(MoneyTrackerStates.choosing_setting)
	state_data = await state.get_data()
	message_id : int = state_data.get("message_id")
	await bot.edit_message_text(
		chat_id=message.chat.id,
		message_id=message_id,
		**ScreenManager.SPENDING_TYPE_NAME_EDITED.as_kwargs()
	)
	await message.delete()

# Добавление нового типа трат
@edit_spending_types_router.callback_query(
	EditSpendingTypeCbData.filter(F.action == EditSpendingTypeActions.new),
	StateFilter(MoneyTrackerStates.spending_types_edit_list)
)
async def add_new_spending_type(callback: types.CallbackQuery, state: FSMContext):
	await state.set_data({"message_id": callback.message.message_id})
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

# Ввод нового типа трат
@edit_spending_types_router.message(
	StateFilter(MoneyTrackerStates.spending_type_enter_new)
)
async def enter_new_spending_type(message: types.Message, state: FSMContext, db: Database, bot: Bot):
	if len(message.text) > 64:
		raise Exception("Type name is too big")
	db.add_spending_type(message.from_user.id, type_name=message.text)
	await state.set_state(MoneyTrackerStates.choosing_setting)
	state_data = await state.get_data()
	message_id : int = state_data.get("message_id")
	await bot.edit_message_text(
		chat_id=message.chat.id,
		message_id=message_id,
		**ScreenManager.NEW_SPENDING_TYPE_ADDED.as_kwargs()
	)
	await message.delete()

# Отмена редактирования выбранного типа
@edit_spending_types_router.callback_query(
        NavigationCbData.filter(F.navigation == NavigationActions.back),
        StateFilter(MoneyTrackerStates.spending_type_edit_choosed)
)
async def cancel_editing_spending_type(callback: types.CallbackQuery, state: FSMContext):
    await show_spending_types_list_for_edit(callback, state)


# TODO: Сделать максимальное количество категорий
# TODO: Сделать обработку невалидного (слишком длинного) ввода пользователя