texts = {
    # General
    'welcome_message': 'مرحبًا بك في روبوت DogTea للتعدين، {}! 🐕\n\nابدأ في تعدين رموز DOGTEA مع كلابك الافتراضية. اشترِ وطوّر وحارب بكلابك لكسب المزيد من الرموز!\n\nاستخدم القائمة أدناه للبدء:',
    'help_message': '🐕 *أوامر روبوت DogTea للتعدين* 🐕\n\n/start - ابدأ الروبوت وشاهد القائمة الرئيسية\n/profile - عرض ملفك الشخصي والإحصائيات\n/dogs - عرض كلابك وإحصائياتها\n/shop - شراء كلاب جديدة باستخدام TON\n/daily - تحقق من حدود الألعاب اليومية\n/play - العب الألعاب المصغرة لكسب DOGTEA\n/language - تغيير اللغة\n/referral - احصل على رابط الإحالة الخاص بك\n/webapp - افتح تطبيق DogTea',
    
    # Buttons
    'play_button': '🎮 العب',
    'my_dogs_button': '🐕 كلابي',
    'shop_button': '🛒 المتجر',
    'upgrade_button': 'ترقية',
    'battle_button': 'معركة',
    'watch_ad_button': '📺 مشاهدة الإعلان',
    'back_button': '◀️ رجوع',
    'confirm_button': '✅ تأكيد',
    'cancel_button': '❌ إلغاء',
    'attack_button': '⚔️ هجوم',
    'special_button': '🔥 خاص',
    'defend_button': '🛡️ دفاع',
    
    # Profile
    'profile_message': '👤 *ملفك الشخصي*\n\nاسم المستخدم: {username}\nالمستوى: {level}\nالخبرة: {xp}/{next_level_xp}\nرصيد DOGTEA: {dogtea_balance}\nالكلاب: {dogs_count}\nالألعاب المتبقية اليوم: {games_left}',
    
    # Dogs
    'no_dogs_message': 'ليس لديك أي كلاب بعد! قم بزيارة المتجر لشراء كلبك الأول.',
    'dogs_list_header': '🐕 *كلابك* 🐕',
    'dog_stats': 'المستوى: {level}\nالقوة: {strength}\nقوة التعدين: {mining_power}\nتكلفة الترقية: {upgrade_cost} DOGTEA',
    'invalid_dog': 'اختيار كلب غير صالح أو الكلب لا ينتمي إليك.',
    'dog_upgraded': '🐕 *تمت ترقية الكلب!* 🐕\n\nتمت ترقية كلبك {name} إلى المستوى {level}!\n\nالإحصائيات الجديدة:\nالقوة: {strength}\nقوة التعدين: {mining_power}\n\nرصيدك المتبقي: {balance} DOGTEA',
    'upgrade_failed': 'فشلت ترقية كلبك. يرجى المحاولة مرة أخرى لاحقًا.',
    
    # Shop
    'shop_header': '🛒 *متجر الكلاب* 🛒\n\nاشترِ كلابًا جديدة لزيادة قوة التعدين وكسب المزيد من رموز DOGTEA!',
    'dog_price': 'السعر: {price} TON',
    'confirm_purchase': 'هل أنت متأكد من رغبتك في شراء كلب {breed} مقابل {price} TON؟',
    'purchase_successful': '🎉 تهانينا! لقد اشتريت كلب {breed} باسم {name}!\n\nاستخدم /dogs لرؤية رفيقك الجديد.',
    'payment_error': 'حدث خطأ أثناء معالجة دفعتك. يرجى المحاولة مرة أخرى لاحقًا.',
    'dog_purchase_title': 'كلب {breed}',
    'dog_purchase_description': 'شراء كلب {breed} مقابل {price} TON',
    
    # Games
    'available_games': '🎮 *الألعاب المتاحة* 🎮\n\nلديك {games_left} ألعاب متبقية اليوم. اختر لعبة للعب:',
    'no_games_left': 'ليس لديك ألعاب متبقية للعب اليوم. يمكنك مشاهدة إعلان للحصول على لعبة إضافية.',
    'ad_watched': 'شكرًا لمشاهدة الإعلان! لقد حصلت على لعبة إضافية. لديك الآن {games_left} ألعاب متبقية اليوم.',
    'no_more_ads': 'لقد شاهدت بالفعل الحد الأقصى من الإعلانات اليوم. عد غدًا للمزيد من الألعاب!',
    'daily_message': '📅 *الحالة اليومية* 📅\n\nلديك {games_left} ألعاب عادية متبقية اليوم.\nلديك {ad_games_left} ألعاب إعلانية متبقية اليوم.',
    'game_expired': 'انتهت صلاحية هذه اللعبة. يرجى بدء لعبة جديدة.',
    'game_cancelled': 'تم إلغاء اللعبة.',
    'game_reward': '🎁 *المكافأة* 🎁\n\nلقد ربحت {reward_amount} رمز DOGTEA!\n\nالرصيد الجديد: {new_balance} DOGTEA',
    'level_up': '🎉 *ارتقاء المستوى!* 🎉\n\nتهانينا! لقد وصلت إلى المستوى {new_level}!',
    
    # Guess Game
    'guess_game_button': '🔢 خمن الرقم',
    'guess_game_start': '🔢 *خمن الرقم* 🔢\n\nأفكر في رقم بين 1 و 100. هل يمكنك تخمينه؟\n\nلديك {max_attempts} محاولات.',
    'guess_game_prompt': 'اختر نطاقًا:\n\nالمحاولات: {attempts}/{max_attempts}',
    'guess_game_select_number': 'اختر رقمًا بين {start} و {end}:\n\nالمحاولات: {attempts}/{max_attempts}',
    'guess_game_continue': 'تخمينك: {guess}\n{hint}\n\nالمحاولات: {attempts}/{max_attempts}',
    'guess_game_win': '🎉 صحيح! كان الرقم {target}.\nلقد خمنته في {attempts} محاولات!',
    'guess_game_lose': '❌ انتهت اللعبة! كان الرقم {target}.',
    'guess_higher': 'جرب رقمًا أعلى!',
    'guess_lower': 'جرب رقمًا أقل!',
    
    # Click Game
    'click_game_button': '👆 نقرات سريعة',
    'click_game_start': '👆 *لعبة النقر السريع* 👆\n\nانقر على الزر أكبر عدد ممكن من المرات في {duration} ثانية!',
    'click_game_progress': 'النقرات: {clicks}\nالوقت المتبقي: {remaining:.1f}ث',
    'click_game_end': '⏱️ انتهى الوقت!\n\nلقد قمت بـ {clicks} نقرة في {duration} ثانية!',
    'clicks': 'نقرات',
    
    # Loot Box
    'loot_box_button': '🎁 صندوق الكنز',
    'loot_box_prompt': '🎁 *صندوق الكنز* 🎁\n\nاختر أحد الصناديق للكشف عن جائزتك!',
    'loot_box_result': 'لقد فتحت الصندوق #{box_number} ووجدت {reward} رمز DOGTEA!',
    'loot_box_already_opened': 'تم فتح هذا الصندوق بالفعل!',
    
    # Quiz Game
    'quiz_game_button': '❓ اختبار معلومات الكلاب',
    'quiz_game_question': '❓ *اختبار معلومات الكلاب* ❓\n\n{question}\n\nلديك {time_limit} ثانية للإجابة!',
    'quiz_correct_answer': '✅ الإجابة الصحيحة: {option}\n\nلقد أجبت في {time:.1f} ثانية وحصلت على مكافأة وقت قدرها {time_bonus:.1f} DOGTEA!',
    'quiz_wrong_answer': '❌ إجابة خاطئة!\n\nلقد اخترت: {selected}\nالإجابة الصحيحة: {correct}',
    'quiz_too_slow': '⏱️ بطيء جدًا! لقد نفد وقتك.',
    
    # Battle System
    'battle_start': '⚔️ *معركة الكلاب* ⚔️\n\n{dog_name} ({dog_breed}، المستوى {dog_level}) يواجه {opponent_name} ({opponent_breed}، المستوى {opponent_level})!\n\nاختر إجراءك:',
    'battle_continue': '⚔️ *المعركة - الجولة {turn}* ⚔️\n\n{user_dog} (الصحة: {user_hp}) ضد {opponent_dog} (الصحة: {opponent_hp})\n\nاختر إجراءك التالي:',
    'battle_attack_result': '{dog_name} يهاجم بـ {damage} ضرر! (صحة الخصم: {opponent_hp})',
    'battle_special_success': '{dog_name} يستخدم هجومًا خاصًا بـ {damage} ضرر! (صحة الخصم: {opponent_hp})',
    'battle_special_miss': '{dog_name} حاول هجومًا خاصًا لكنه أخطأ!',
    'battle_defend_result': '{dog_name} يدافع ويستعيد {heal} نقطة صحة! (الصحة: {user_hp})',
    'battle_win': '🎉 *النصر!* 🎉\n\n{dog_name} هزم {opponent_name}!\n\nلقد ربحت {reward} رمز DOGTEA!',
    'battle_lose': '😢 *الهزيمة* 😢\n\nتم هزيمة {dog_name} بواسطة {opponent_name}.\nحظًا أوفر في المرة القادمة!',
    'battle_log': '*سجل المعركة:*',
    'battle_expired': 'انتهت هذه المعركة أو انتهت صلاحيتها.',
    
    # Language
    'language_selection': '🌐 *اختيار اللغة* 🌐\n\nاختر لغتك المفضلة:',
    'language_changed': '✅ تم تغيير اللغة بنجاح!',
    
    # Referral
    'referral_message': '👥 *دعوة الأصدقاء* 👥\n\nشارك هذا الرابط مع أصدقائك واكسب رموز DOGTEA عندما ينضمون:\n\n{referral_link}',
    
    # Errors
    'insufficient_funds': 'ليس لديك ما يكفي من رموز DOGTEA. المطلوب: {required}، رصيدك: {balance}',
}
