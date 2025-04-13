texts = {
    # General
    'welcome': 'DogTea Mining Bot\'a Hoşgeldin, {name}! 🐕\n\nSanal köpeklerinle DOGTEA token madenciliği yap. Köpekleri satın al, geliştir ve savaştırarak daha fazla token kazan!\n\nBaşlamak için aşağıdaki menüyü kullan:',
    'help_text': '🐕 *DogTea Mining Bot Komutları* 🐕\n\n/start - Botu başlat ve ana menüyü gör\n/profile - Profilini ve istatistiklerini görüntüle\n/dogs - Köpeklerini ve istatistiklerini görüntüle\n/shop - TON ile yeni köpekler satın al\n/daily - Günlük oyun limitlerini kontrol et\n/play - DOGTEA kazanmak için mini oyunlar oyna\n/language - Dil değiştir\n/referral - Referans bağlantını al\n/webapp - DogTea WebApp\'i aç',
    
    # Buttons
    'play_button': '🎮 Oyna',
    'dogs_button': '🐕 Köpeklerim',
    'shop_button': '🛒 Mağaza',
    'language_button': '🌍 Dil',
    'webapp_button': '🎮 WebApp\'i Aç',
    'open_webapp': '🎮 WebApp\'i Aç',
    'webapp_text': 'DogTea Mining WebApp\'i aç:',
    'upgrade_button': 'Yükselt',
    'battle_button': 'Savaş',
    'watch_ad_button': '📺 Reklam İzle',
    'back_button': '◀️ Geri',
    'confirm_button': '✅ Onayla',
    'cancel_button': '❌ İptal',
    'attack_button': '⚔️ Saldır',
    'special_button': '🔥 Özel',
    'defend_button': '🛡️ Savun',
    
    # Profile
    'profile_text': '👤 *Profil Bilgilerin*\n\nKullanıcı Adı: {username}\nSeviye: {level}\nXP: {xp}/{xp_next}\nDOGTEA Bakiye: {dogtea}\nKöpekler: {dogs}\nBugün kalan oyunlar: {games_left}',
    
    # Dogs
    'no_dogs_message': 'Henüz hiç köpeğin yok! İlk köpeğini satın almak için mağazayı ziyaret et.',
    'dogs_list_header': '🐕 *Köpeklerin* 🐕',
    'dog_stats': 'Seviye: {level}\nGüç: {strength}\nMadencilik Gücü: {mining_power}\nYükseltme Maliyeti: {upgrade_cost} DOGTEA',
    'invalid_dog': 'Geçersiz köpek seçimi veya köpek size ait değil.',
    'dog_upgraded': '🐕 *Köpek Yükseltildi!* 🐕\n\nKöpeğin {name} seviye {level}\'e yükseltildi!\n\nYeni istatistikler:\nGüç: {strength}\nMadencilik Gücü: {mining_power}\n\nKalan bakiyen: {balance} DOGTEA',
    'upgrade_failed': 'Köpeğin yükseltilmesi başarısız oldu. Lütfen daha sonra tekrar dene.',
    
    # Shop
    'shop_header': '🛒 *Köpek Mağazası* 🛒\n\nMadencilik gücünü artırmak ve daha fazla DOGTEA token kazanmak için yeni köpekler satın al!',
    'dog_price': 'Fiyat: {price} TON',
    'confirm_purchase': '{price} TON karşılığında bir {breed} köpeği satın almak istediğine emin misin?',
    'purchase_successful': '🎉 Tebrikler! {name} adında bir {breed} köpeği satın aldın!\n\nYeni dostunu görmek için /dogs komutunu kullan.',
    'payment_error': 'Ödemeniz işlenirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.',
    'dog_purchase_title': '{breed} Köpeği',
    'dog_purchase_description': '{price} TON karşılığında bir {breed} köpeği satın al',
    
    # Games
    'available_games': '🎮 *Mevcut Oyunlar* 🎮\n\nBugün {games_left} oyun hakkın kaldı. Oynamak için bir oyun seç:',
    'no_games_left': 'Bugün oynayacak oyun hakkın kalmadı. Ekstra bir oyun için reklam izleyebilirsin.',
    'ad_watched': 'Reklamı izlediğin için teşekkürler! Ekstra bir oyun hakkı kazandın. Şimdi {games_left} oyun hakkın var.',
    'no_more_ads': 'Bugün için maksimum reklam izleme sayısına ulaştın. Daha fazla oyun için yarın tekrar gel!',
    'daily_message': '📅 *Günlük Durum* 📅\n\nBugün {games_left} normal oyun hakkın kaldı.\nBugün {ad_games_left} reklam oyun hakkın kaldı.',
    'game_expired': 'Bu oyun süresi doldu. Lütfen yeni bir oyun başlat.',
    'game_cancelled': 'Oyun iptal edildi.',
    'game_reward': '🎁 *Ödül* 🎁\n\n{reward_amount} DOGTEA token kazandın!\n\nYeni bakiye: {new_balance} DOGTEA',
    'level_up': '🎉 *Seviye Atladın!* 🎉\n\nTebrikler! Seviye {new_level}\'e ulaştın!',
    
    # Guess Game
    'guess_game_button': '🔢 Sayı Tahmin Et',
    'guess_game_start': '🔢 *Sayıyı Tahmin Et* 🔢\n\n1 ile 100 arasında bir sayı düşünüyorum. Tahmin edebilir misin?\n\n{max_attempts} deneme hakkın var.',
    'guess_game_prompt': 'Bir aralık seç:\n\nDenemeler: {attempts}/{max_attempts}',
    'guess_game_select_number': '{start} ile {end} arasında bir sayı seç:\n\nDenemeler: {attempts}/{max_attempts}',
    'guess_game_continue': 'Tahminin: {guess}\n{hint}\n\nDenemeler: {attempts}/{max_attempts}',
    'guess_game_win': '🎉 Doğru! Sayı {target} idi.\n{attempts} denemede bildin!',
    'guess_game_lose': '❌ Oyun bitti! Sayı {target} idi.',
    'guess_higher': 'Daha yüksek bir sayı dene!',
    'guess_lower': 'Daha düşük bir sayı dene!',
    
    # Click Game
    'click_game_button': '👆 Hızlı Tıklama',
    'click_game_start': '👆 *Hızlı Tıklama Oyunu* 👆\n\n{duration} saniye içinde düğmeye mümkün olduğunca çok tıkla!',
    'click_game_progress': 'Tıklamalar: {clicks}\nKalan süre: {remaining:.1f}sn',
    'click_game_end': '⏱️ Süre doldu!\n\n{duration} saniyede {clicks} tıklama yaptın!',
    'clicks': 'tıklama',
    
    # Loot Box
    'loot_box_button': '🎁 Hazine Kutusu',
    'loot_box_prompt': '🎁 *Hazine Kutusu* 🎁\n\nÖdülünü görmek için kutulardan birini seç!',
    'loot_box_result': '#{box_number} numaralı kutuyu açtın ve {reward} DOGTEA token buldun!',
    'loot_box_already_opened': 'Bu kutu zaten açıldı!',
    
    # Quiz Game
    'quiz_game_button': '❓ Köpek Bilgi Yarışması',
    'quiz_game_question': '❓ *Köpek Bilgi Yarışması* ❓\n\n{question}\n\nCevaplamak için {time_limit} saniyen var!',
    'quiz_correct_answer': '✅ Doğru cevap: {option}\n\n{time:.1f} saniyede cevapladın ve {time_bonus:.1f} DOGTEA zaman bonusu kazandın!',
    'quiz_wrong_answer': '❌ Yanlış cevap!\n\nSeçtiğin: {selected}\nDoğru cevap: {correct}',
    'quiz_too_slow': '⏱️ Çok yavaş! Süren doldu.',
    
    # Battle System
    'battle_start': '⚔️ *Köpek Savaşı* ⚔️\n\n{dog_name} ({dog_breed}, Seviye {dog_level}) ile {opponent_name} ({opponent_breed}, Seviye {opponent_level}) karşı karşıya!\n\nHamleni seç:',
    'battle_continue': '⚔️ *Savaş - Tur {turn}* ⚔️\n\n{user_dog} (HP: {user_hp}) vs {opponent_dog} (HP: {opponent_hp})\n\nBir sonraki hamleni seç:',
    'battle_attack_result': '{dog_name} {damage} hasar veriyor! (Rakip HP: {opponent_hp})',
    'battle_special_success': '{dog_name} özel saldırı ile {damage} hasar veriyor! (Rakip HP: {opponent_hp})',
    'battle_special_miss': '{dog_name} özel saldırı denedi ama ıskaladı!',
    'battle_defend_result': '{dog_name} savunma yapıyor ve {heal} HP kazanıyor! (HP: {user_hp})',
    'battle_win': '🎉 *Zafer!* 🎉\n\n{dog_name}, {opponent_name}\'i yendi!\n\n{reward} DOGTEA token kazandın!',
    'battle_lose': '😢 *Yenilgi* 😢\n\n{dog_name}, {opponent_name} tarafından yenildi.\nBir dahaki sefere daha iyi şanslar!',
    'battle_log': '*Savaş Kaydı:*',
    'battle_expired': 'Bu savaş sona erdi veya süresi doldu.',
    
    # Language
    'language_selection': '🌐 *Dil Seçimi* 🌐\n\nTercih ettiğin dili seç:',
    'language_changed': '✅ Dil başarıyla değiştirildi!',
    
    # Referral
    'referral_message': '👥 *Arkadaşlarını Davet Et* 👥\n\nBu bağlantıyı arkadaşlarınla paylaş ve katıldıklarında DOGTEA token kazan:\n\n{referral_link}',
    
    # Errors
    'insufficient_funds': 'Yeterli DOGTEA tokenin yok. Gerekli: {required}, Bakiyen: {balance}',
}
