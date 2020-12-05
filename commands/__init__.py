from subtitle import (
    BASE_URL,
    get_lang,
    search_sub
)

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Support Group', url='https://t.me/linux_repo'),
                    InlineKeyboardButton('Developer', url='https://t.me/AbirHasan2005')
                ],
                [
                    InlineKeyboardButton('Telegram Bots Updates Channel', url='https://t.me/Discovery_Updates'),
                ]
            ]
        )
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi, *{update.effective_user.first_name}*!\n\nI am **Subtitles Search Bot**. I can provide you movie subtitles.\n\n——→ Just Send me Movie Name with Release Year. \n\n**Example:** `Extraction 2020`", parse_mode="Markdown", reply_markup=reply_markup)

def searching(update: Update, context: CallbackContext):
    if update.message.via_bot != None:
        return

    search_message = context.bot.send_message(chat_id=update.effective_chat.id, text="Searching your subtitle file")
    sub_name = update.effective_message.text
    full_index, title, keyword = search_sub(sub_name)
    inline_keyboard = []
    if len(full_index) == 0:
        context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=search_message.message_id, text="No results found")
        return
    
    index = full_index[:15]
    for i in index:
        subtitle = title[i-1]
        key = keyword[i-1]
        inline_keyboard.append([InlineKeyboardButton(subtitle, callback_data=f"{key}")])

    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=search_message.message_id, text=f"Got the following results for your query *{sub_name}*. Select the preffered type from the below options", parse_mode="Markdown", reply_markup=reply_markup)
