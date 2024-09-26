from aiogram import types


class Multitool:

    @staticmethod
    def feature_in_process_text(data : types.Message | types.CallbackQuery):
        if isinstance(data, types.CallbackQuery):
            html_text = data.message.html_text
        else:
            html_text = data.html_text
        text = [
            "<u>Функция в разработке</u>\n",
            html_text,
        ]
        return "\n".join(text)