texts = {
    # General
    'welcome_message': 'Добро пожаловать в DogTea Mining Bot, {}! 🐕\n\nНачните майнить токены DOGTEA со своими виртуальными собаками. Покупайте, улучшайте и участвуйте в боях со своими собаками, чтобы заработать больше токенов!\n\nИспользуйте меню ниже, чтобы начать:',
    'help_message': '🐕 *Команды DogTea Mining Bot* 🐕\n\n/start - Запустить бота и увидеть главное меню\n/profile - Просмотреть свой профиль и статистику\n/dogs - Просмотреть своих собак и их статистику\n/shop - Купить новых собак за TON\n/daily - Проверить дневные лимиты игр\n/play - Играть в мини-игры, чтобы заработать DOGTEA\n/language - Изменить язык\n/referral - Получить свою реферальную ссылку\n/webapp - Открыть DogTea WebApp',
    
    # Buttons
    'play_button': '🎮 Играть',
    'my_dogs_button': '🐕 Мои собаки',
    'shop_button': '🛒 Магазин',
    'upgrade_button': 'Улучшить',
    'battle_button': 'Бой',
    'watch_ad_button': '📺 Смотреть рекламу',
    'back_button': '◀️ Назад',
    'confirm_button': '✅ Подтвердить',
    'cancel_button': '❌ Отмена',
    'attack_button': '⚔️ Атака',
    'special_button': '🔥 Особая',
    'defend_button': '🛡️ Защита',
    
    # Profile
    'profile_message': '👤 *Ваш профиль*\n\nИмя пользователя: {username}\nУровень: {level}\nXP: {xp}/{next_level_xp}\nБаланс DOGTEA: {dogtea_balance}\nСобак: {dogs_count}\nОсталось игр сегодня: {games_left}',
    
    # Dogs
    'no_dogs_message': 'У вас еще нет собак! Посетите магазин, чтобы купить свою первую собаку.',
    'dogs_list_header': '🐕 *Ваши собаки* 🐕',
    'dog_stats': 'Уровень: {level}\nСила: {strength}\nМощность майнинга: {mining_power}\nСтоимость улучшения: {upgrade_cost} DOGTEA',
    'invalid_dog': 'Недействительный выбор собаки или собака вам не принадлежит.',
    'dog_upgraded': '🐕 *Собака улучшена!* 🐕\n\nВаша собака {name} была улучшена до уровня {level}!\n\nНовые характеристики:\nСила: {strength}\nМощность майнинга: {mining_power}\n\nВаш оставшийся баланс: {balance} DOGTEA',
    'upgrade_failed': 'Не удалось улучшить вашу собаку. Пожалуйста, попробуйте позже.',
    
    # Shop
    'shop_header': '🛒 *Магазин собак* 🛒\n\nПокупайте новых собак, чтобы увеличить свою мощность майнинга и зарабатывать больше токенов DOGTEA!',
    'dog_price': 'Цена: {price} TON',
    'confirm_purchase': 'Вы уверены, что хотите купить собаку породы {breed} за {price} TON?',
    'purchase_successful': '🎉 Поздравляем! Вы приобрели собаку породы {breed} по имени {name}!\n\nИспользуйте /dogs, чтобы увидеть своего нового питомца.',
    'payment_error': 'Произошла ошибка при обработке вашего платежа. Пожалуйста, попробуйте позже.',
    'dog_purchase_title': 'Собака {breed}',
    'dog_purchase_description': 'Приобрести собаку породы {breed} за {price} TON',
    
    # Games
    'available_games': '🎮 *Доступные игры* 🎮\n\nУ вас осталось {games_left} игр сегодня. Выберите игру:',
    'no_games_left': 'У вас не осталось игр на сегодня. Вы можете посмотреть рекламу, чтобы получить дополнительную игру.',
    'ad_watched': 'Спасибо за просмотр рекламы! Вы получили дополнительную игру. Теперь у вас осталось {games_left} игр сегодня.',
    'no_more_ads': 'Вы уже посмотрели максимальное количество рекламы сегодня. Возвращайтесь завтра для большего количества игр!',
    'daily_message': '📅 *Ежедневный статус* 📅\n\nУ вас осталось {games_left} обычных игр сегодня.\nУ вас осталось {ad_games_left} рекламных игр сегодня.',
    'game_expired': 'Эта игра истекла. Пожалуйста, начните новую игру.',
    'game_cancelled': 'Игра отменена.',
    'game_reward': '🎁 *Награда* 🎁\n\nВы заработали {reward_amount} токенов DOGTEA!\n\nНовый баланс: {new_balance} DOGTEA',
    'level_up': '🎉 *Повышение уровня!* 🎉\n\nПоздравляем! Вы достигли уровня {new_level}!',
    
    # Guess Game
    'guess_game_button': '🔢 Угадай число',
    'guess_game_start': '🔢 *Угадай число* 🔢\n\nЯ загадал число от 1 до 100. Сможете ли вы его угадать?\n\nУ вас есть {max_attempts} попыток.',
    'guess_game_prompt': 'Выберите диапазон:\n\nПопытки: {attempts}/{max_attempts}',
    'guess_game_select_number': 'Выберите число от {start} до {end}:\n\nПопытки: {attempts}/{max_attempts}',
    'guess_game_continue': 'Ваша догадка: {guess}\n{hint}\n\nПопытки: {attempts}/{max_attempts}',
    'guess_game_win': '🎉 Верно! Число было {target}.\nВы угадали за {attempts} попыток!',
    'guess_game_lose': '❌ Игра окончена! Число было {target}.',
    'guess_higher': 'Попробуйте больше!',
    'guess_lower': 'Попробуйте меньше!',
    
    # Click Game
    'click_game_button': '👆 Быстрые клики',
    'click_game_start': '👆 *Игра быстрых кликов* 👆\n\nКликайте по кнопке как можно больше раз за {duration} секунд!',
    'click_game_progress': 'Клики: {clicks}\nОсталось времени: {remaining:.1f}с',
    'click_game_end': '⏱️ Время вышло!\n\nВы сделали {clicks} кликов за {duration} секунд!',
    'clicks': 'кликов',
    
    # Loot Box
    'loot_box_button': '🎁 Сундук с сокровищами',
    'loot_box_prompt': '🎁 *Сундук с сокровищами* 🎁\n\nВыберите один из сундуков, чтобы узнать свой приз!',
    'loot_box_result': 'Вы открыли сундук #{box_number} и нашли {reward} токенов DOGTEA!',
    'loot_box_already_opened': 'Этот сундук уже был открыт!',
    
    # Quiz Game
    'quiz_game_button': '❓ Викторина о собаках',
    'quiz_game_question': '❓ *Викторина о собаках* ❓\n\n{question}\n\nУ вас есть {time_limit} секунд, чтобы ответить!',
    'quiz_correct_answer': '✅ Правильный ответ: {option}\n\nВы ответили за {time:.1f} секунд и заработали временной бонус в размере {time_bonus:.1f} DOGTEA!',
    'quiz_wrong_answer': '❌ Неправильный ответ!\n\nВы выбрали: {selected}\nПравильный ответ: {correct}',
    'quiz_too_slow': '⏱️ Слишком медленно! У вас закончилось время.',
    
    # Battle System
    'battle_start': '⚔️ *Битва собак* ⚔️\n\nВаша {dog_name} ({dog_breed}, Уровень {dog_level}) против {opponent_name} ({opponent_breed}, Уровень {opponent_level})!\n\nВыберите свое действие:',
    'battle_continue': '⚔️ *Битва - Ход {turn}* ⚔️\n\n{user_dog} (HP: {user_hp}) против {opponent_dog} (HP: {opponent_hp})\n\nВыберите свое следующее действие:',
    'battle_attack_result': '{dog_name} атакует на {damage} урона! (HP оппонента: {opponent_hp})',
    'battle_special_success': '{dog_name} использует особую атаку на {damage} урона! (HP оппонента: {opponent_hp})',
    'battle_special_miss': '{dog_name} попытался использовать особую атаку, но промахнулся!',
    'battle_defend_result': '{dog_name} защищается и восстанавливает {heal} HP! (HP: {user_hp})',
    'battle_win': '🎉 *Победа!* 🎉\n\nВаша {dog_name} победила {opponent_name}!\n\nВы заработали {reward} токенов DOGTEA!',
    'battle_lose': '😢 *Поражение* 😢\n\nВаша {dog_name} была побеждена {opponent_name}.\nУдачи в следующий раз!',
    'battle_log': '*Журнал битвы:*',
    'battle_expired': 'Эта битва закончилась или истекла.',
    
    # Language
    'language_selection': '🌐 *Выбор языка* 🌐\n\nВыберите предпочитаемый язык:',
    'language_changed': '✅ Язык успешно изменен!',
    
    # Referral
    'referral_message': '👥 *Пригласите друзей* 👥\n\nПоделитесь этой ссылкой с друзьями и зарабатывайте токены DOGTEA, когда они присоединятся:\n\n{referral_link}',
    
    # Errors
    'insufficient_funds': 'У вас недостаточно токенов DOGTEA. Требуется: {required}, Ваш баланс: {balance}',
}
