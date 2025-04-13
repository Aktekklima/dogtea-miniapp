texts = {
    # General
    'welcome': 'Welcome to DogTea Mining Bot, {name}! 🐕\n\nStart mining DOGTEA tokens with your virtual dogs. Buy, upgrade, and battle with your dogs to earn more tokens!\n\nUse the menu below to get started:',
    'help_text': '🐕 *DogTea Mining Bot Commands* 🐕\n\n/start - Start the bot and see main menu\n/profile - View your profile and stats\n/dogs - View your dogs and their stats\n/shop - Buy new dogs with TON\n/daily - Check your daily game limits\n/play - Play mini-games to earn DOGTEA\n/language - Change language\n/referral - Get your referral link\n/webapp - Open the DogTea WebApp',
    
    # Buttons
    'play_button': '🎮 Play',
    'dogs_button': '🐕 My Dogs',
    'shop_button': '🛒 Shop',
    'language_button': '🌍 Language',
    'webapp_button': '🎮 Open WebApp',
    'open_webapp': '🎮 Open WebApp',
    'webapp_text': 'Open the DogTea Mining WebApp:',
    'upgrade_button': 'Upgrade',
    'battle_button': 'Battle',
    'watch_ad_button': '📺 Watch Ad',
    'back_button': '◀️ Back',
    'confirm_button': '✅ Confirm',
    'cancel_button': '❌ Cancel',
    'attack_button': '⚔️ Attack',
    'special_button': '🔥 Special',
    'defend_button': '🛡️ Defend',
    
    # Profile
    'profile_text': '👤 *Your Profile*\n\nUsername: {username}\nLevel: {level}\nXP: {xp}/{xp_next}\nDOGTEA Balance: {dogtea}\nDogs: {dogs}\nGames left today: {games_left}',
    
    # Dogs
    'no_dogs_message': 'You don\'t have any dogs yet! Visit the shop to buy your first dog.',
    'dogs_list_header': '🐕 *Your Dogs* 🐕',
    'dog_stats': 'Level: {level}\nStrength: {strength}\nMining Power: {mining_power}\nUpgrade Cost: {upgrade_cost} DOGTEA',
    'invalid_dog': 'Invalid dog selection or the dog doesn\'t belong to you.',
    'dog_upgraded': '🐕 *Dog Upgraded!* 🐕\n\nYour dog {name} has been upgraded to level {level}!\n\nNew stats:\nStrength: {strength}\nMining Power: {mining_power}\n\nYour remaining balance: {balance} DOGTEA',
    'upgrade_failed': 'Failed to upgrade your dog. Please try again later.',
    
    # Shop
    'shop_header': '🛒 *Dog Shop* 🛒\n\nBuy new dogs to increase your mining power and earn more DOGTEA tokens!',
    'dog_price': 'Price: {price} TON',
    'confirm_purchase': 'Are you sure you want to buy a {breed} dog for {price} TON?',
    'purchase_successful': '🎉 Congratulations! You purchased a {breed} dog named {name}!\n\nUse /dogs to see your new companion.',
    'payment_error': 'There was an error processing your payment. Please try again later.',
    'dog_purchase_title': '{breed} Dog',
    'dog_purchase_description': 'Purchase a {breed} dog for {price} TON',
    
    # Games
    'available_games': '🎮 *Available Games* 🎮\n\nYou have {games_left} games left today. Choose a game to play:',
    'no_games_left': 'You have no games left to play today. You can watch an ad to get an extra game.',
    'ad_watched': 'Thanks for watching the ad! You got an extra game. You now have {games_left} games left today.',
    'no_more_ads': 'You have already watched the maximum number of ads today. Come back tomorrow for more games!',
    'daily_message': '📅 *Daily Status* 📅\n\nYou have {games_left} regular games left today.\nYou have {ad_games_left} ad games left today.',
    'game_expired': 'This game has expired. Please start a new game.',
    'game_cancelled': 'Game cancelled.',
    'game_reward': '🎁 *Reward* 🎁\n\nYou earned {reward_amount} DOGTEA tokens!\n\nNew balance: {new_balance} DOGTEA',
    'level_up': '🎉 *Level Up!* 🎉\n\nCongratulations! You reached level {new_level}!',
    
    # Guess Game
    'guess_game_button': '🔢 Guess Number',
    'guess_game_start': '🔢 *Guess the Number* 🔢\n\nI\'m thinking of a number between 1 and 100. Can you guess it?\n\nYou have {max_attempts} attempts.',
    'guess_game_prompt': 'Select a range:\n\nAttempts: {attempts}/{max_attempts}',
    'guess_game_select_number': 'Select a number between {start} and {end}:\n\nAttempts: {attempts}/{max_attempts}',
    'guess_game_continue': 'Your guess: {guess}\n{hint}\n\nAttempts: {attempts}/{max_attempts}',
    'guess_game_win': '🎉 Correct! The number was {target}.\nYou guessed it in {attempts} attempts!',
    'guess_game_lose': '❌ Game over! The number was {target}.',
    'guess_higher': 'Try higher!',
    'guess_lower': 'Try lower!',
    
    # Click Game
    'click_game_button': '👆 Fast Clicks',
    'click_game_start': '👆 *Fast Clicking Game* 👆\n\nClick the button as many times as possible in {duration} seconds!',
    'click_game_progress': 'Clicks: {clicks}\nTime remaining: {remaining:.1f}s',
    'click_game_end': '⏱️ Time\'s up!\n\nYou made {clicks} clicks in {duration} seconds!',
    'clicks': 'clicks',
    
    # Loot Box
    'loot_box_button': '🎁 Loot Box',
    'loot_box_prompt': '🎁 *Loot Box* 🎁\n\nChoose one of the boxes to reveal your prize!',
    'loot_box_result': 'You opened box #{box_number} and found {reward} DOGTEA tokens!',
    'loot_box_already_opened': 'This box has already been opened!',
    
    # Quiz Game
    'quiz_game_button': '❓ Dog Quiz',
    'quiz_game_question': '❓ *Dog Quiz* ❓\n\n{question}\n\nYou have {time_limit} seconds to answer!',
    'quiz_correct_answer': '✅ Correct answer: {option}\n\nYou answered in {time:.1f} seconds and earned a time bonus of {time_bonus:.1f} DOGTEA!',
    'quiz_wrong_answer': '❌ Wrong answer!\n\nYou selected: {selected}\nCorrect answer: {correct}',
    'quiz_too_slow': '⏱️ Too slow! You ran out of time.',
    
    # Battle System
    'battle_start': '⚔️ *Dog Battle* ⚔️\n\nYour {dog_name} ({dog_breed}, Level {dog_level}) is facing {opponent_name} ({opponent_breed}, Level {opponent_level})!\n\nChoose your action:',
    'battle_continue': '⚔️ *Battle - Turn {turn}* ⚔️\n\n{user_dog} (HP: {user_hp}) vs {opponent_dog} (HP: {opponent_hp})\n\nChoose your next action:',
    'battle_attack_result': '{dog_name} attacks for {damage} damage! (Opponent HP: {opponent_hp})',
    'battle_special_success': '{dog_name} uses a special attack for {damage} damage! (Opponent HP: {opponent_hp})',
    'battle_special_miss': '{dog_name} tried a special attack but missed!',
    'battle_defend_result': '{dog_name} defends and recovers {heal} HP! (HP: {user_hp})',
    'battle_win': '🎉 *Victory!* 🎉\n\nYour {dog_name} defeated {opponent_name}!\n\nYou earned {reward} DOGTEA tokens!',
    'battle_lose': '😢 *Defeat* 😢\n\nYour {dog_name} was defeated by {opponent_name}.\nBetter luck next time!',
    'battle_log': '*Battle Log:*',
    'battle_expired': 'This battle has ended or expired.',
    
    # Language
    'language_selection': '🌐 *Language Selection* 🌐\n\nSelect your preferred language:',
    'language_changed': '✅ Language changed successfully!',
    
    # Referral
    'referral_message': '👥 *Refer Friends* 👥\n\nShare this link with your friends and earn DOGTEA tokens when they join:\n\n{referral_link}',
    
    # Errors
    'insufficient_funds': 'You don\'t have enough DOGTEA tokens. Required: {required}, Your balance: {balance}',
}
