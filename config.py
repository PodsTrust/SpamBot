API_TOKEN = '5861812609:AAEJoa8ERuYSncaYi_a2bbDpD4uSgm1bEEA'


main_menu_ua = ["📱Отримати завдання", "💰 Баланс","ℹ️ Інструкція з роботу", "🆘 Підтримка"]
main_menu_ru = ["📱Получить задание", "💰 Баланс","ℹ️ Инструкция по боту", "🆘 Поддержка"]
main_menu_en = ["📱Get Task", "💰 Balance","ℹ️ Bot Instructions", "🆘 Support"]

MODERATION_GROUP_ID = -710855932
WITHDRAW_GROUP_ID = -656034669

MIN_WITHDRAW = 10

ADMINS = [917522531,2011705567,5613131644]

#BUTTONS

withdraw = ["💳 Вивід","💳 Вывод","💳 Withdraw"]
spam = ["Розсилка","Рассылка","Spam"]
complaints = ["Скарги","Жалобы","Complaints"]
done = ["✅ Виконав","✅ Выполнил","✅ Done"]
cancel = ["❌ Скасувати виконання","❌ Отменить выполнение","❌ Cancel task"]


# TEXTS

select_language = """Вибери мову спілкування

Выбери язык

Choose your language"""


welcome_message = ["""Привіт""","""Привет""","""Welcome"""]

instructions = ["""⚫️Привіт, я тобі розповім як заробляти за допомогою цього бота 

1.тобі потрібно натиснути отримати завдання 
Після чого тобі випаде список людей (список видає по 10-20 чоловік) яким потрібно буде відправити повідомлення (повідомлення тобі буде видано)

2. після того як ти їм написав тобі потрібно зробити запис екрану де буде видно останні 20 повідомлень, обов'язково врахуй що тобі потрібно буде зняти не кожне окреме листування а останні повідомлення в твоїх чатах.

3. після того як ти відправиш модератору на перевірку, протягом 2-10м тобі зараховуватися на баланс гроші.

4. Щоб вивести гроші натисни на баланс, після чого на виведення, далі просто потрібно вказати номер Карти.
Протягом 10м очікуй зарахування коштів.

⚫️ПРАЙС
1 повідомлення = 2грн 
1 скарга = 4грн
Мінімальна сума виведення 10грн 

вдалої роботи ::)""","""⚫️Привет, я тебе расскажу как зарабатывать с помощью этого бота 

1.тебе нужно нажать получить задание 
После чего тебе выпадет список людей(список выдаёт по 10-20 человек) которым нужно будет отправить сообщение(сообщение тебе будет выдано)

2.после того как ты им написал тебе нужно сделать запись экрана где будет видно последние 20 сообщений,обязательно учти что тебе нужно будет заснять не каждую отдельную переписку а последние сообщения в твоих чатах.

3.после того как ты отправишь модератору на проверку, в течении 2-10м тебе зачисляться на баланс деньги.

4. Чтобы вывести деньги нажми на баланс, после чего на вывод, дальше просто нужно указать номер Карты.
В течении 10м ожидай зачисления средств.

⚫️ПРАЙС
1 сообщения = 2грн 
1 жалоба = 4грн
Минимальная сумма вывода 10грн 

удачной работы ::)""","""⚫️Hi, I will tell you how to earn with this bot 

1.You need to click get the job 
After that you will fall out a list of people (the list gives out 10-20 people) who need to send a message (the message you will be given)

2.After you write them you need to make a record of the screen, which will be visible to the last 20 messages, be sure to note that you will need to shoot not every individual correspondence and the last message in your chats.

3.After you send the moderator to verify, within 2-10m you enroll in the balance of money.

4. To withdraw money, click on the balance, then to withdraw, then you just need to specify the number of the card.
Within 10 m, expect the enrollment of funds.

⚫️ PRICE
1 message = 2rn 
1 complaint = 4grn
The minimum withdrawal amount of 10grn 

Good luck ::)"""]


balance = ["""ID: {}
💵Баланс: {} UAH""","""ID: {}
💵Баланс: {} UAH""","""ID: {}
💵Balance: {} UAH"""]


select_category = ["Вибери категорію завдань 👇","Выбери категорию заданий 👇","Choose a task category 👇"]

you_have_not_complete_task = ["""У тебе є невиконане завдання""", """У тебя есть невыполненное задание""","""You have an unfinished task"""]
not_tasks = ["""На даний момент немає завдань.""", """В данный момент нету заданий.""","""There are no tasks at the moment."""]

spam_rep = ["Прийшли кожному з вище ☝️ представлених цей текст 👇","Пришли каждому из выше ☝️ представленных этот текст 👇","Send each of the above ☝️ presented this text 👇"]

after_done = [f"Після виконання жми 👇",f"После выполнения жми 👇",f"After done, press 👇"]

go_to_channel = ["Зайди на канал ☝️, натисни на три точки і вибери заблокувати канал. У списку вибери інше","Зайди на  канал ☝️,нажми на три точки и выбери заблокировать канал.В списке выбери другое","Go to the channel ☝️, click on the three dots and choose to block the channel. In the list, select another"]

screen_recording = ["‼️ ВАЖЛИВО! Увімкніть запис екрана і записуйте всі кроки, щоб перевірити завдання","‼️ ВАЖНО!!! Включите запись екрана и записывайте все шаги, для проверки задания","‼️ IMPORTANT!!! Turn on screen recording and record all steps to check the task"]

completing_canceled = ["Виконання завдання скасовано","Выполнение задания отменено","Task canceled"]

result1 = ["Прийшли результат виконання завдання у вигляді скріншота. Якщо потрібно прикріпити повідомлення для адміністратора, залиш підпис до фотографії","Пришли результат выполнения задания в виде скриншота. Если нужно прикрепить сообщение для администратора, оставь подпись к фотографии","Sent the result of the task in the form of a screenshot. If you need to attach a message for the administrator, leave a caption to the photo"]

result2 = ["Прийшли результат виконання завдання у вигляді ведопису екрана. Якщо потрібно прикріпити повідомлення для адміністратора, залиш підпис до відео","Пришли результат выполнения задания в виде ведеозаписи екрана. Если нужно прикрепить сообщение для администратора, оставь подпись к видео","We received the result of the task in the form of a video recording of the screen. If you need to attach a message for the administrator, leave a caption to the video"]

task_already_completed = ["Це завдання вже виконане!","Это задание уже выполнено!","This mission has already been completed!"]
task_in_moderation = ["Це завдання на модерації!","Это задание на модерации!","This is a moderation task!"]
task_completed = ["✅ Завдання прийняте. Тобі нараховано {}","✅ Задание принято. Тебе начислено {}","✅ Task accepted. You have received {}"]
task_canceled = [f"❌ Завдання відхилено.",f"❌ Задание отклонено.",f"❌ Task rejected."]
withdraw_completed = [f"✅ Висновок надіслано на твою карту",f"✅ Вывод отправлен на твою карту",f"✅ Withdrawal sent to your card"]
withdraw_canceled = [f"❌ Відмовлено у виведенні",f"❌ Отказано в выводе",f"❌ Withdrawal denied"]
min_withdraw = [f"Мінімальна сума для виведення {MIN_WITHDRAW} UAH",f"Минимальная сумма для вывода {MIN_WITHDRAW} UAH",f"Minimum withdrawal amount {MIN_WITHDRAW} UAH"]

to_moder = [f"""Результат надіслано на модерацію""",f"""Результат отправлен на модерацию""",f"""Result sent for moderation"""]
enter_card = ["Введи номер картки для виведення","Введи номер карты для вывода","Enter card number to withdraw"]
card_not_valid = [f"""Неправильний номер картки""",f"""Неверный номер карты""",f"""Invalid card number"""]
withraw_app_send = [f"""Заявку на виведення подано""", f"""Заявка на вывод подана""",f"""Withdrawal request submitted"""]
