// Initialize Telegram WebApp
const tgApp = window.Telegram.WebApp;
let userLanguage = tgApp.initDataUnsafe?.user?.language_code || 'en';
let userData = null;
let userDogs = [];
let currentGame = null;
let telegramId = null;

// Available language codes
const supportedLanguages = ['en', 'tr', 'ru', 'ar'];
if (!supportedLanguages.includes(userLanguage)) {
    userLanguage = 'en';
}

// Translations
const translations = {
    // English is the default, other languages will be loaded
    en: {
        loading: "Loading...",
        dogsTitle: "Your Dogs",
        gamesTitle: "Mini Games",
        shopTitle: "Dog Shop",
        noDogs: "No dogs yet",
        buyFirstDog: "Visit the shop to buy your first dog!",
        gamesLeft: "games left today",
        dogsCount: "Dogs",
        upgradeBtn: "Upgrade",
        battleBtn: "Battle",
        miningBtn: "Collect Mining Rewards",
        watchAdBtn: "Watch Ad",
        guessGame: "Guess Number",
        clickGame: "Fast Clicks",
        lootGame: "Loot Box",
        quizGame: "Dog Quiz",
        upgradeSuccess: "Dog upgraded successfully!",
        upgradeFailed: "Not enough DOGTEA to upgrade",
        battleStart: "Battle started!",
        battleWin: "You won the battle!",
        battleLose: "You lost the battle.",
        miningSuccess: "Mining rewards collected!",
        adWatched: "Thanks for watching the ad!",
        gameOver: "Game Over",
        playAgain: "Play Again",
        correct: "Correct!",
        wrong: "Wrong!",
        timeUp: "Time's up!",
        playBtn: "Play",
        closeBtn: "Close",
        submitBtn: "Submit",
        confirmBtn: "Confirm",
        cancelBtn: "Cancel",
        buyFor: "Buy for",
    },
    // Other languages will be populated at runtime
};

// Document ready
document.addEventListener('DOMContentLoaded', function() {
    // Expand Telegram WebApp to full size
    tgApp.expand();
    
    // Initialize the app
    initializeApp();
    
    // Set up tab navigation
    setupTabNavigation();
    
    // Setup game buttons
    setupGameButtons();
    
    // Setup UI interactions
    setupUIInteractions();
});

// Initialize the app
function initializeApp() {
    if (tgApp.initDataUnsafe && tgApp.initDataUnsafe.user) {
        telegramId = tgApp.initDataUnsafe.user.id;
        userLanguage = tgApp.initDataUnsafe.user.language_code || 'en';
        
        // Load user data
        loadUserData(telegramId).then(() => {
            // Once data is loaded, show the main content
            document.getElementById('loadingScreen').classList.add('d-none');
            document.getElementById('mainContent').classList.remove('d-none');
            
            // Update the UI with user data
            updateUserInterface();
        });
    } else {
        // Testing mode - use demo data
        telegramId = 123456789;
        
        // Load demo data
        loadDemoData().then(() => {
            document.getElementById('loadingScreen').classList.add('d-none');
            document.getElementById('mainContent').classList.remove('d-none');
            updateUserInterface();
        });
    }
    
    // Set RTL for Arabic
    if (userLanguage === 'ar') {
        document.documentElement.setAttribute('dir', 'rtl');
    } else {
        document.documentElement.setAttribute('dir', 'ltr');
    }
}

// Load user data from the API
async function loadUserData(telegramId) {
    try {
        // Load user info
        const userResponse = await fetch('/api/user_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ telegram_id: telegramId })
        });
        
        if (!userResponse.ok) {
            throw new Error('Failed to load user data');
        }
        
        userData = await userResponse.json();
        
        // Load dog info
        const dogResponse = await fetch('/api/dog_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ telegram_id: telegramId })
        });
        
        if (!dogResponse.ok) {
            throw new Error('Failed to load dog data');
        }
        
        const dogData = await dogResponse.json();
        userDogs = dogData.dogs;
        
    } catch (error) {
        console.error('Error loading data:', error);
        // Show error message
        document.getElementById('loadingScreen').innerHTML = `
            <div class="alert alert-danger" role="alert">
                Failed to load data. Please try again.
            </div>
            <button class="btn btn-primary mt-3" onclick="window.location.reload()">
                Retry
            </button>
        `;
    }
}

// For testing - load demo data
function loadDemoData() {
    return new Promise((resolve) => {
        setTimeout(() => {
            userData = {
                username: "DogLover",
                xp: 245,
                level: 3,
                dogtea_balance: 125.5,
                games_played_today: 1,
                games_left_today: 1
            };
            
            userDogs = [
                {
                    id: 1,
                    name: "Rex",
                    breed: "Labrador",
                    level: 2,
                    strength: 15,
                    mining_power: 1.5,
                    upgrade_cost: 15
                },
                {
                    id: 2,
                    name: "Luna",
                    breed: "Husky",
                    level: 3,
                    strength: 18,
                    mining_power: 2.2,
                    upgrade_cost: 25
                }
            ];
            
            resolve();
        }, 1000);
    });
}

// Update the user interface with loaded data
function updateUserInterface() {
    // Update profile section
    document.getElementById('username').textContent = userData.username;
    document.getElementById('userLevel').textContent = userData.level;
    document.getElementById('userXp').textContent = userData.xp;
    document.getElementById('dogteaBalance').textContent = userData.dogtea_balance.toFixed(1);
    document.getElementById('gamesLeft').textContent = `${userData.games_left_today} games left today`;
    
    // Calculate XP progress to next level
    const xpForNextLevel = (userData.level + 1) * 100;
    const currentLevelXp = userData.level * 100;
    const xpProgress = ((userData.xp - currentLevelXp) / (xpForNextLevel - currentLevelXp)) * 100;
    document.getElementById('xpProgress').style.width = `${xpProgress}%`;
    
    // Update dogs section
    updateDogsSection();
    
    // Update games section
    document.getElementById('gamesBadge').textContent = `${userData.games_left_today} games left`;
    
    // Disable game buttons if no games left
    const gameButtons = document.querySelectorAll('#gamesSection .btn-primary');
    if (userData.games_left_today <= 0) {
        gameButtons.forEach(btn => {
            btn.disabled = true;
            btn.classList.add('disabled');
        });
    } else {
        gameButtons.forEach(btn => {
            btn.disabled = false;
            btn.classList.remove('disabled');
        });
    }
    
    // Update watch ad button
    const watchAdBtn = document.getElementById('watchAdBtn');
    if (userData.ad_games_used >= 2) {
        watchAdBtn.disabled = true;
        watchAdBtn.classList.add('disabled');
    } else {
        watchAdBtn.disabled = false;
        watchAdBtn.classList.remove('disabled');
    }
}

// Update the dogs section
function updateDogsSection() {
    const dogsListEl = document.getElementById('dogsList');
    const dogCountEl = document.getElementById('dogCount');
    
    // Update dog count
    dogCountEl.textContent = `${userDogs.length} Dogs`;
    
    // Clear current dogs list
    dogsListEl.innerHTML = '';
    
    if (userDogs.length === 0) {
        // Show placeholder if no dogs
        dogsListEl.innerHTML = `
            <div class="col">
                <div class="card h-100 placeholder-card">
                    <div class="card-body text-center d-flex flex-column justify-content-center">
                        <p class="fs-5 text-muted mb-0">No dogs yet</p>
                        <p class="text-muted">Visit the shop to buy your first dog!</p>
                    </div>
                </div>
            </div>
        `;
        return;
    }
    
    // Add each dog to the list
    userDogs.forEach(dog => {
        const dogCard = createDogCard(dog);
        dogsListEl.appendChild(dogCard);
    });
}

// Create a dog card element
function createDogCard(dog) {
    // Clone the template
    const template = document.getElementById('dogCardTemplate');
    const dogCard = template.content.cloneNode(true);
    
    // Get dog icon based on breed
    const breedIcon = getBreedIcon(dog.breed);
    dogCard.querySelector('.dog-icon-use').setAttribute('href', `/static/assets/dog_icons.svg#${breedIcon}`);
    
    // Set dog details
    dogCard.querySelector('.dog-name').textContent = dog.name;
    dogCard.querySelector('.dog-breed').textContent = dog.breed;
    dogCard.querySelector('.dog-level').textContent = `Level ${dog.level}`;
    dogCard.querySelector('.dog-strength').textContent = dog.strength;
    dogCard.querySelector('.dog-mining').textContent = dog.mining_power.toFixed(1);
    dogCard.querySelector('.upgrade-cost').textContent = `${dog.upgrade_cost.toFixed(1)} DOGTEA`;
    
    // Set up buttons
    const upgradeBtn = dogCard.querySelector('.upgrade-btn');
    upgradeBtn.dataset.dogId = dog.id;
    upgradeBtn.addEventListener('click', () => handleDogUpgrade(dog));
    
    const battleBtn = dogCard.querySelector('.battle-btn');
    battleBtn.dataset.dogId = dog.id;
    battleBtn.addEventListener('click', () => handleDogBattle(dog));
    
    return dogCard;
}

// Get the icon ID based on dog breed
function getBreedIcon(breed) {
    const breedMap = {
        'Labrador': 'labrador',
        'German Shepherd': 'german-shepherd',
        'Bulldog': 'bulldog',
        'Golden Retriever': 'golden-retriever',
        'Siberian Husky': 'husky',
        'Poodle': 'poodle',
        'Corgi': 'corgi',
        'Pug': 'pug',
        'Beagle': 'beagle',
        'Chihuahua': 'chihuahua'
    };
    
    return breedMap[breed] || 'dog-main';
}

// Setup tab navigation
function setupTabNavigation() {
    const dogsTab = document.getElementById('dogsTab');
    const gamesTab = document.getElementById('gamesTab');
    const shopTab = document.getElementById('shopTab');
    
    const dogsSection = document.getElementById('dogsSection');
    const gamesSection = document.getElementById('gamesSection');
    const shopSection = document.getElementById('shopSection');
    
    dogsTab.addEventListener('click', function() {
        // Update active tab
        dogsTab.classList.add('active');
        gamesTab.classList.remove('active');
        shopTab.classList.remove('active');
        
        // Show/hide sections
        dogsSection.classList.remove('d-none');
        gamesSection.classList.add('d-none');
        shopSection.classList.add('d-none');
    });
    
    gamesTab.addEventListener('click', function() {
        // Update active tab
        dogsTab.classList.remove('active');
        gamesTab.classList.add('active');
        shopTab.classList.remove('active');
        
        // Show/hide sections
        dogsSection.classList.add('d-none');
        gamesSection.classList.remove('d-none');
        shopSection.classList.add('d-none');
    });
    
    shopTab.addEventListener('click', function() {
        // Update active tab
        dogsTab.classList.remove('active');
        gamesTab.classList.remove('active');
        shopTab.classList.add('active');
        
        // Show/hide sections
        dogsSection.classList.add('d-none');
        gamesSection.classList.add('d-none');
        shopSection.classList.remove('d-none');
    });
}

// Setup game buttons
function setupGameButtons() {
    document.getElementById('guessGameBtn').addEventListener('click', () => startGuessGame());
    document.getElementById('clickGameBtn').addEventListener('click', () => startClickGame());
    document.getElementById('lootBoxBtn').addEventListener('click', () => startLootBoxGame());
    document.getElementById('quizGameBtn').addEventListener('click', () => startQuizGame());
    document.getElementById('closeGameBtn').addEventListener('click', () => closeGameOverlay());
}

// Setup other UI interactions
function setupUIInteractions() {
    // Mining button
    document.getElementById('miningBtn').addEventListener('click', collectMiningRewards);
    
    // Watch ad button
    document.getElementById('watchAdBtn').addEventListener('click', watchAd);
    
    // Shop buy buttons
    const buyButtons = document.querySelectorAll('#shopSection button[data-breed]');
    buyButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const breed = btn.dataset.breed;
            const price = btn.dataset.price;
            buyDog(breed, price);
        });
    });
}

// Handle dog upgrade
function handleDogUpgrade(dog) {
    // Check if user has enough DOGTEA
    if (userData.dogtea_balance < dog.upgrade_cost) {
        // Show error
        tgApp.showPopup({
            title: "Insufficient funds",
            message: `You need ${dog.upgrade_cost.toFixed(1)} DOGTEA to upgrade ${dog.name}.`,
            buttons: [{type: "ok"}]
        });
        return;
    }
    
    // Show confirmation
    tgApp.showPopup({
        title: "Upgrade Dog",
        message: `Are you sure you want to upgrade ${dog.name} for ${dog.upgrade_cost.toFixed(1)} DOGTEA?`,
        buttons: [
            {
                id: "confirm",
                type: "ok",
                text: "Confirm"
            },
            {
                id: "cancel",
                type: "cancel",
                text: "Cancel"
            }
        ]
    }, function(buttonId) {
        if (buttonId === "confirm") {
            // Simulate upgrade success
            // In a real app, this would make an API call
            simulateDogUpgrade(dog);
        }
    });
}

// Simulate dog upgrade (in real app, would call API)
function simulateDogUpgrade(dog) {
    // Update user balance
    userData.dogtea_balance -= dog.upgrade_cost;
    
    // Update dog
    const dogIndex = userDogs.findIndex(d => d.id === dog.id);
    if (dogIndex !== -1) {
        userDogs[dogIndex].level += 1;
        userDogs[dogIndex].strength += 5;
        userDogs[dogIndex].mining_power += 0.5;
        userDogs[dogIndex].upgrade_cost *= 1.5;
    }
    
    // Update UI
    updateUserInterface();
    
    // Show success message
    tgApp.showPopup({
        title: "Upgrade Successful",
        message: `${dog.name} has been upgraded to level ${dog.level + 1}!`,
        buttons: [{type: "ok"}]
    });
}

// Handle dog battle
function handleDogBattle(dog) {
    openGameOverlay("Battle Mode");
    
    // Clone battle template
    const template = document.getElementById('battleTemplate');
    const battleUI = template.content.cloneNode(true);
    
    // Set up battle UI
    const yourDogIcon = battleUI.querySelector('#yourDogIcon');
    yourDogIcon.setAttribute('href', `/static/assets/dog_icons.svg#${getBreedIcon(dog.breed)}`);
    
    battleUI.querySelector('#yourDogName').textContent = `${dog.name} (Lvl ${dog.level})`;
    
    // Create opponent
    const opponentLevel = Math.max(1, Math.min(5, dog.level + Math.floor(Math.random() * 3) - 1));
    const opponentBreeds = ['Labrador', 'German Shepherd', 'Bulldog', 'Golden Retriever', 'Husky'];
    const opponentBreed = opponentBreeds[Math.floor(Math.random() * opponentBreeds.length)];
    const opponentName = ['Max', 'Rocky', 'Luna', 'Buddy', 'Charlie'][Math.floor(Math.random() * 5)];
    
    const opponentDogIcon = battleUI.querySelector('#opponentDogIcon');
    opponentDogIcon.setAttribute('href', `/static/assets/dog_icons.svg#${getBreedIcon(opponentBreed)}`);
    
    battleUI.querySelector('#opponentDogName').textContent = `${opponentName} (Lvl ${opponentLevel})`;
    
    // Set up battle state
    const battleState = {
        yourDog: {
            name: dog.name,
            level: dog.level,
            strength: dog.strength,
            hp: 100
        },
        opponentDog: {
            name: opponentName,
            level: opponentLevel,
            strength: 10 + (opponentLevel * 5),
            hp: 100
        },
        turn: 1
    };
    
    // Add battle UI to game content
    const gameContent = document.getElementById('gameContent');
    gameContent.innerHTML = '';
    gameContent.appendChild(battleUI);
    
    // Set up battle buttons
    document.getElementById('attackBtn').addEventListener('click', () => battleAction(battleState, 'attack'));
    document.getElementById('specialBtn').addEventListener('click', () => battleAction(battleState, 'special'));
    document.getElementById('defendBtn').addEventListener('click', () => battleAction(battleState, 'defend'));
}

// Handle battle action
function battleAction(battleState, action) {
    const battleLog = document.getElementById('battleLog');
    let damage = 0;
    let message = '';
    
    // Player's turn
    switch (action) {
        case 'attack':
            // Regular attack
            damage = calculateDamage(battleState.yourDog.strength, 'attack');
            battleState.opponentDog.hp -= damage;
            message = `${battleState.yourDog.name} attacks for ${damage} damage!`;
            break;
            
        case 'special':
            // Special attack - more damage but can miss
            if (Math.random() < 0.7) {
                damage = calculateDamage(battleState.yourDog.strength, 'special');
                battleState.opponentDog.hp -= damage;
                message = `${battleState.yourDog.name} uses a special attack for ${damage} damage!`;
            } else {
                message = `${battleState.yourDog.name} tried a special attack but missed!`;
            }
            break;
            
        case 'defend':
            // Defend - recover some HP
            const healAmount = Math.floor(Math.random() * 11) + 5; // 5-15 HP
            battleState.yourDog.hp = Math.min(100, battleState.yourDog.hp + healAmount);
            message = `${battleState.yourDog.name} defends and recovers ${healAmount} HP!`;
            break;
    }
    
    // Add message to battle log
    addBattleLogMessage(message);
    
    // Update HP bars
    updateBattleHP(battleState);
    
    // Check if opponent is defeated
    if (battleState.opponentDog.hp <= 0) {
        endBattle(battleState, true);
        return;
    }
    
    // Opponent's turn (after a short delay)
    setTimeout(() => {
        // Simple AI - random action
        const opponentActions = ['attack', 'attack', 'special', 'defend']; // More weight on attack
        const opponentAction = opponentActions[Math.floor(Math.random() * opponentActions.length)];
        
        switch (opponentAction) {
            case 'attack':
                damage = calculateDamage(battleState.opponentDog.strength, 'attack');
                battleState.yourDog.hp -= damage;
                message = `${battleState.opponentDog.name} attacks for ${damage} damage!`;
                break;
                
            case 'special':
                if (Math.random() < 0.7) {
                    damage = calculateDamage(battleState.opponentDog.strength, 'special');
                    battleState.yourDog.hp -= damage;
                    message = `${battleState.opponentDog.name} uses a special attack for ${damage} damage!`;
                } else {
                    message = `${battleState.opponentDog.name} tried a special attack but missed!`;
                }
                break;
                
            case 'defend':
                const healAmount = Math.floor(Math.random() * 11) + 5; // 5-15 HP
                battleState.opponentDog.hp = Math.min(100, battleState.opponentDog.hp + healAmount);
                message = `${battleState.opponentDog.name} defends and recovers ${healAmount} HP!`;
                break;
        }
        
        // Add message to battle log
        addBattleLogMessage(message);
        
        // Update HP bars
        updateBattleHP(battleState);
        
        // Check if player is defeated
        if (battleState.yourDog.hp <= 0) {
            endBattle(battleState, false);
            return;
        }
        
        // Increment turn
        battleState.turn++;
    }, 1000);
}

// Calculate damage for battle
function calculateDamage(strength, attackType) {
    const baseDamage = Math.floor(strength / 2);
    
    if (attackType === 'attack') {
        // Regular attack: base damage +/- 20%
        const variation = baseDamage * ((Math.random() * 0.4) - 0.2);
        return Math.max(1, Math.round(baseDamage + variation));
    } else if (attackType === 'special') {
        // Special attack: 1.5x base damage +/- 30%
        const specialDamage = baseDamage * 1.5;
        const variation = specialDamage * ((Math.random() * 0.6) - 0.3);
        return Math.max(1, Math.round(specialDamage + variation));
    }
    
    return baseDamage;
}

// Add message to battle log
function addBattleLogMessage(message) {
    const battleLog = document.getElementById('battleLog');
    const messageEl = document.createElement('p');
    messageEl.className = 'battle-message';
    messageEl.textContent = message;
    battleLog.appendChild(messageEl);
    battleLog.scrollTop = battleLog.scrollHeight;
}

// Update battle HP bars
function updateBattleHP(battleState) {
    // Cap HP at 0
    battleState.yourDog.hp = Math.max(0, battleState.yourDog.hp);
    battleState.opponentDog.hp = Math.max(0, battleState.opponentDog.hp);
    
    // Update HP bars
    document.getElementById('yourDogHP').style.width = `${battleState.yourDog.hp}%`;
    document.getElementById('opponentDogHP').style.width = `${battleState.opponentDog.hp}%`;
    
    // Change color based on HP
    if (battleState.yourDog.hp < 30) {
        document.getElementById('yourDogHP').classList.remove('bg-success');
        document.getElementById('yourDogHP').classList.add('bg-danger');
    }
    
    if (battleState.opponentDog.hp < 30) {
        document.getElementById('opponentDogHP').classList.remove('bg-danger');
        document.getElementById('opponentDogHP').classList.add('bg-warning');
    }
}

// End battle
function endBattle(battleState, isWinner) {
    // Disable battle buttons
    document.getElementById('attackBtn').disabled = true;
    document.getElementById('specialBtn').disabled = true;
    document.getElementById('defendBtn').disabled = true;
    
    if (isWinner) {
        // Calculate reward
        const baseReward = 5;
        const levelMultiplier = 1.2;
        const reward = baseReward * (Math.pow(levelMultiplier, battleState.opponentDog.level - 1));
        const roundedReward = Math.round(reward * 10) / 10;
        
        // Add reward to user balance
        userData.dogtea_balance += roundedReward;
        
        // Add message to battle log
        addBattleLogMessage(`You won the battle and earned ${roundedReward.toFixed(1)} DOGTEA!`);
        
        // Update UI
        updateUserInterface();
    } else {
        // Add message to battle log
        addBattleLogMessage(`You lost the battle.`);
    }
    
    // Add close button
    const battleActions = document.getElementById('battleActions');
    battleActions.innerHTML = `
        <button class="btn btn-primary w-100" id="closeBattleBtn">
            Close
        </button>
    `;
    
    document.getElementById('closeBattleBtn').addEventListener('click', closeGameOverlay);
}

// Collect mining rewards
function collectMiningRewards() {
    if (userDogs.length === 0) {
        tgApp.showPopup({
            title: "No Dogs",
            message: "You need to buy at least one dog to collect mining rewards.",
            buttons: [{type: "ok"}]
        });
        return;
    }
    
    // Calculate mining reward based on dogs
    let totalMining = 0;
    
    userDogs.forEach(dog => {
        // Base mining rate for dog's level
        const baseRate = [0, 0.5, 1.0, 1.5, 2.0, 3.0][dog.level] || 0.5;
        
        // Apply dog's mining power
        const miningReward = baseRate * dog.mining_power;
        totalMining += miningReward;
    });
    
    // Round to one decimal
    totalMining = Math.round(totalMining * 10) / 10;
    
    // Add to user balance
    userData.dogtea_balance += totalMining;
    
    // Update UI
    updateUserInterface();
    
    // Show success message
    tgApp.showPopup({
        title: "Mining Rewards",
        message: `You collected ${totalMining.toFixed(1)} DOGTEA from your dogs!`,
        buttons: [{type: "ok"}]
    });
}

// Watch ad for extra game
function watchAd() {
    // Simulate watching an ad
    tgApp.showPopup({
        title: "Watch Ad",
        message: "Would you like to watch an ad to get an extra game?",
        buttons: [
            {
                id: "watch",
                type: "ok",
                text: "Watch Ad"
            },
            {
                id: "cancel",
                type: "cancel",
                text: "Cancel"
            }
        ]
    }, function(buttonId) {
        if (buttonId === "watch") {
            // Simulate ad completion
            setTimeout(() => {
                // Increase games left
                userData.games_left_today += 1;
                userData.ad_games_used = (userData.ad_games_used || 0) + 1;
                
                // Update UI
                updateUserInterface();
                
                // Show success message
                tgApp.showPopup({
                    title: "Ad Completed",
                    message: "Thanks for watching! You got an extra game.",
                    buttons: [{type: "ok"}]
                });
            }, 1500);
        }
    });
}

// Buy a dog
function buyDog(breed, price) {
    // In a real app, this would integrate with TON payments
    tgApp.showPopup({
        title: "Buy Dog",
        message: `Would you like to buy a ${breed} dog for ${price} TON?`,
        buttons: [
            {
                id: "buy",
                type: "ok",
                text: "Buy"
            },
            {
                id: "cancel",
                type: "cancel",
                text: "Cancel"
            }
        ]
    }, function(buttonId) {
        if (buttonId === "buy") {
            // Simulate successful purchase
            simulateDogPurchase(breed);
        }
    });
}

// Simulate dog purchase (in real app, would use TON payment API)
function simulateDogPurchase(breed) {
    // Generate a random name
    const dogNames = ["Buddy", "Max", "Charlie", "Rocky", "Cooper", "Duke", "Bear", "Teddy", "Tucker", "Winston"];
    const name = dogNames[Math.floor(Math.random() * dogNames.length)];
    
    // Create new dog
    const newDog = {
        id: userDogs.length + 1,
        name: name,
        breed: breed,
        level: 1,
        strength: 10,
        mining_power: 1.0,
        upgrade_cost: 1.0
    };
    
    // Add to user's dogs
    userDogs.push(newDog);
    
    // Update UI
    updateUserInterface();
    
    // Show success message
    tgApp.showPopup({
        title: "Purchase Successful",
        message: `You purchased a ${breed} dog named ${name}!`,
        buttons: [{type: "ok"}]
    });
    
    // Switch to dogs tab
    document.getElementById('dogsTab').click();
}

// Open game overlay
function openGameOverlay(title) {
    document.getElementById('gameTitle').textContent = title;
    document.getElementById('gameContent').innerHTML = '';
    document.getElementById('gameOverlay').classList.remove('d-none');
}

// Close game overlay
function closeGameOverlay() {
    document.getElementById('gameOverlay').classList.add('d-none');
    currentGame = null;
}

// Start guess number game
function startGuessGame() {
    if (userData.games_left_today <= 0) {
        tgApp.showPopup({
            title: "No Games Left",
            message: "You have no games left today. Watch an ad or come back tomorrow.",
            buttons: [{type: "ok"}]
        });
        return;
    }
    
    openGameOverlay("Guess the Number");
    
    // Reduce available games
    userData.games_left_today -= 1;
    updateUserInterface();
    
    // Set up game state
    currentGame = {
        type: 'guess',
        target: Math.floor(Math.random() * 100) + 1,
        attempts: 0,
        maxAttempts: 5
    };
    
    // Create game UI
    const gameContent = document.getElementById('gameContent');
    gameContent.innerHTML = `
        <p class="mb-3">I'm thinking of a number between 1 and 100. Can you guess it?</p>
        <p class="mb-3">You have <span id="attemptsLeft">${currentGame.maxAttempts}</span> attempts left.</p>
        <div id="guessResult" class="alert alert-info d-none mb-3"></div>
        
        <div class="mb-3">
            <label for="guessInput" class="form-label">Your guess:</label>
            <div class="input-group">
                <input type="number" class="form-control" id="guessInput" min="1" max="100" placeholder="Enter a number">
                <button class="btn btn-primary" id="submitGuessBtn">Guess</button>
            </div>
        </div>
        
        <div class="number-grid mb-3">
            ${generateNumberButtons()}
        </div>
    `;
    
    // Set up event listeners
    document.getElementById('submitGuessBtn').addEventListener('click', processGuess);
    document.getElementById('guessInput').addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            processGuess();
        }
    });
    
    // Set up number buttons
    const numberButtons = document.querySelectorAll('.number-btn');
    numberButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            document.getElementById('guessInput').value = this.textContent;
        });
    });
}

// Generate number buttons for guess game
function generateNumberButtons() {
    let buttons = '';
    for (let i = 1; i <= 10; i++) {
        buttons += `<button class="btn btn-outline-secondary number-btn">${i}</button>`;
    }
    return buttons;
}

// Process a guess
function processGuess() {
    const guessInput = document.getElementById('guessInput');
    const guess = parseInt(guessInput.value);
    
    if (isNaN(guess) || guess < 1 || guess > 100) {
        // Invalid guess
        document.getElementById('guessResult').textContent = "Please enter a valid number between 1 and 100.";
        document.getElementById('guessResult').classList.remove('d-none', 'alert-success', 'alert-danger');
        document.getElementById('guessResult').classList.add('alert-warning');
        return;
    }
    
    // Increment attempts
    currentGame.attempts++;
    
    // Update attempts left
    document.getElementById('attemptsLeft').textContent = currentGame.maxAttempts - currentGame.attempts;
    
    // Check guess
    const result = document.getElementById('guessResult');
    result.classList.remove('d-none');
    
    if (guess === currentGame.target) {
        // Correct guess
        result.textContent = `Correct! The number was ${currentGame.target}.`;
        result.classList.remove('alert-info', 'alert-warning', 'alert-danger');
        result.classList.add('alert-success');
        
        // Calculate reward based on attempts
        const reward = Math.max(1, 6 - currentGame.attempts);
        
        // Add reward to balance
        userData.dogtea_balance += reward;
        updateUserInterface();
        
        // Disable input
        document.getElementById('guessInput').disabled = true;
        document.getElementById('submitGuessBtn').disabled = true;
        
        // Add play again button
        gameContent.innerHTML += `
            <div class="alert alert-success">
                You earned ${reward.toFixed(1)} DOGTEA tokens!
            </div>
            <div class="d-grid gap-2">
                <button class="btn btn-primary" id="playAgainBtn">Play Again</button>
                <button class="btn btn-secondary" id="closeGameBtn2">Close</button>
            </div>
        `;
        
        document.getElementById('playAgainBtn').addEventListener('click', () => {
            closeGameOverlay();
            startGuessGame();
        });
        
        document.getElementById('closeGameBtn2').addEventListener('click', closeGameOverlay);
        
    } else {
        // Wrong guess
        if (currentGame.attempts >= currentGame.maxAttempts) {
            // Game over
            result.textContent = `Game over! The number was ${currentGame.target}.`;
            result.classList.remove('alert-info', 'alert-warning', 'alert-success');
            result.classList.add('alert-danger');
            
            // Disable input
            document.getElementById('guessInput').disabled = true;
            document.getElementById('submitGuessBtn').disabled = true;
            
            // Add play again button
            gameContent.innerHTML += `
                <div class="d-grid gap-2">
                    <button class="btn btn-primary" id="playAgainBtn">Play Again</button>
                    <button class="btn btn-secondary" id="closeGameBtn2">Close</button>
                </div>
            `;
            
            document.getElementById('playAgainBtn').addEventListener('click', () => {
                closeGameOverlay();
                startGuessGame();
            });
            
            document.getElementById('closeGameBtn2').addEventListener('click', closeGameOverlay);
            
        } else {
            // Provide hint
            if (guess < currentGame.target) {
                result.textContent = `${guess} is too low. Try higher!`;
            } else {
                result.textContent = `${guess} is too high. Try lower!`;
            }
            result.classList.remove('alert-success', 'alert-danger');
            result.classList.add('alert-warning');
            
            // Clear input for next guess
            guessInput.value = '';
            guessInput.focus();
        }
    }
}

// Start click game
function startClickGame() {
    if (userData.games_left_today <= 0) {
        tgApp.showPopup({
            title: "No Games Left",
            message: "You have no games left today. Watch an ad or come back tomorrow.",
            buttons: [{type: "ok"}]
        });
        return;
    }
    
    openGameOverlay("Fast Clicks");
    
    // Reduce available games
    userData.games_left_today -= 1;
    updateUserInterface();
    
    // Set up game state
    currentGame = {
        type: 'click',
        clicks: 0,
        duration: 10,
        startTime: null,
        intervalId: null,
        active: false
    };
    
    // Create game UI
    const gameContent = document.getElementById('gameContent');
    gameContent.innerHTML = `
        <p class="text-center mb-3">Click the button as many times as possible in ${currentGame.duration} seconds!</p>
        
        <button class="btn btn-lg btn-primary w-100 click-button mb-3" id="clickButton">
            <span class="click-count" id="clickCount">0</span>
            <span class="click-timer" id="clickTimer">Click to start</span>
        </button>
        
        <div class="progress mb-3" role="progressbar">
            <div class="progress-bar progress-bar-striped progress-bar-animated" id="clickProgress" style="width: 100%"></div>
        </div>
    `;
    
    // Set up event listener
    const clickButton = document.getElementById('clickButton');
    
    clickButton.addEventListener('click', function() {
        if (!currentGame.active) {
            // Start the game
            startClickTimer();
            return;
        }
        
        // Increment clicks
        currentGame.clicks++;
        document.getElementById('clickCount').textContent = currentGame.clicks;
    });
}

// Start click game timer
function startClickTimer() {
    currentGame.active = true;
    currentGame.startTime = Date.now();
    
    const clickButton = document.getElementById('clickButton');
    const clickTimer = document.getElementById('clickTimer');
    const clickProgress = document.getElementById('clickProgress');
    
    clickButton.classList.add('btn-danger');
    clickButton.classList.remove('btn-primary');
    
    // Update timer every 100ms
    currentGame.intervalId = setInterval(function() {
        const elapsed = (Date.now() - currentGame.startTime) / 1000;
        const remaining = Math.max(0, currentGame.duration - elapsed);
        
        clickTimer.textContent = remaining.toFixed(1) + 's';
        clickProgress.style.width = (remaining / currentGame.duration * 100) + '%';
        
        if (remaining <= 0) {
            endClickGame();
        }
    }, 100);
}

// End click game
function endClickGame() {
    // Clear interval
    clearInterval(currentGame.intervalId);
    
    // Calculate reward based on clicks
    // Simple formula: min 1, max 10, 1 per 10 clicks
    const reward = Math.min(10, Math.max(1, Math.floor(currentGame.clicks / 10)));
    
    // Add reward to balance
    userData.dogtea_balance += reward;
    updateUserInterface();
    
    // Update UI
    const gameContent = document.getElementById('gameContent');
    gameContent.innerHTML = `
        <div class="text-center mb-3">
            <h4>Time's up!</h4>
            <p class="fs-1">${currentGame.clicks} clicks</p>
            <div class="alert alert-success">
                You earned ${reward.toFixed(1)} DOGTEA tokens!
            </div>
        </div>
        <div class="d-grid gap-2">
            <button class="btn btn-primary" id="playAgainBtn">Play Again</button>
            <button class="btn btn-secondary" id="closeGameBtn2">Close</button>
        </div>
    `;
    
    document.getElementById('playAgainBtn').addEventListener('click', () => {
        closeGameOverlay();
        startClickGame();
    });
    
    document.getElementById('closeGameBtn2').addEventListener('click', closeGameOverlay);
    
    currentGame.active = false;
}

// Start loot box game
function startLootBoxGame() {
    if (userData.games_left_today <= 0) {
        tgApp.showPopup({
            title: "No Games Left",
            message: "You have no games left today. Watch an ad or come back tomorrow.",
            buttons: [{type: "ok"}]
        });
        return;
    }
    
    openGameOverlay("Loot Box");
    
    // Reduce available games
    userData.games_left_today -= 1;
    updateUserInterface();
    
    // Set up game state
    currentGame = {
        type: 'loot',
        boxes: [
            { id: 1, reward: Math.round((Math.random() * 9 + 1) * 10) / 10 },
            { id: 2, reward: Math.round((Math.random() * 9 + 1) * 10) / 10 },
            { id: 3, reward: Math.round((Math.random() * 9 + 1) * 10) / 10 }
        ],
        selected: null
    };
    
    // Create game UI
    const gameContent = document.getElementById('gameContent');
    gameContent.innerHTML = `
        <p class="text-center mb-3">Choose one of the boxes to reveal your prize!</p>
        
        <div class="loot-boxes">
            <div class="loot-box" data-box="1">🎁</div>
            <div class="loot-box" data-box="2">🎁</div>
            <div class="loot-box" data-box="3">🎁</div>
        </div>
        
        <div id="lootResult" class="alert d-none mb-3 text-center"></div>
    `;
    
    // Set up event listeners
    const lootBoxes = document.querySelectorAll('.loot-box');
    lootBoxes.forEach(box => {
        box.addEventListener('click', function() {
            if (currentGame.selected) return;
            
            const boxId = parseInt(this.dataset.box);
            openLootBox(boxId);
        });
    });
}

// Open a loot box
function openLootBox(boxId) {
    // Set selected box
    currentGame.selected = boxId;
    
    // Get box reward
    const box = currentGame.boxes.find(b => b.id === boxId);
    const reward = box.reward;
    
    // Add reward to balance
    userData.dogtea_balance += reward;
    updateUserInterface();
    
    // Update UI
    const lootBoxes = document.querySelectorAll('.loot-box');
    lootBoxes.forEach(boxEl => {
        const id = parseInt(boxEl.dataset.box);
        if (id === boxId) {
            boxEl.textContent = `${reward} 💰`;
            boxEl.classList.add('pulse-animation');
        } else {
            boxEl.style.opacity = '0.5';
        }
    });
    
    const lootResult = document.getElementById('lootResult');
    lootResult.textContent = `You found ${reward.toFixed(1)} DOGTEA tokens!`;
    lootResult.classList.remove('d-none');
    lootResult.classList.add('alert-success');
    
    // Add buttons
    const gameContent = document.getElementById('gameContent');
    gameContent.innerHTML += `
        <div class="d-grid gap-2">
            <button class="btn btn-primary" id="playAgainBtn">Play Again</button>
            <button class="btn btn-secondary" id="closeGameBtn2">Close</button>
        </div>
    `;
    
    document.getElementById('playAgainBtn').addEventListener('click', () => {
        closeGameOverlay();
        startLootBoxGame();
    });
    
    document.getElementById('closeGameBtn2').addEventListener('click', closeGameOverlay);
}

// Start quiz game
function startQuizGame() {
    if (userData.games_left_today <= 0) {
        tgApp.showPopup({
            title: "No Games Left",
            message: "You have no games left today. Watch an ad or come back tomorrow.",
            buttons: [{type: "ok"}]
        });
        return;
    }
    
    openGameOverlay("Dog Quiz");
    
    // Reduce available games
    userData.games_left_today -= 1;
    updateUserInterface();
    
    // Sample quiz questions
    const questions = [
        {
            question: "Which dog breed is known for having a blue-black tongue?",
            options: ["Husky", "Chow Chow", "Dalmatian", "Poodle"],
            correct: 1
        },
        {
            question: "What is the most popular dog breed in the world?",
            options: ["Labrador Retriever", "German Shepherd", "Golden Retriever", "Bulldog"],
            correct: 0
        },
        {
            question: "How many teeth does an adult dog have?",
            options: ["22", "32", "42", "52"],
            correct: 2
        },
        {
            question: "Which dog breed was originally bred to hunt lions?",
            options: ["Great Dane", "Rhodesian Ridgeback", "Mastiff", "St. Bernard"],
            correct: 1
        },
        {
            question: "What is a group of pugs called?",
            options: ["A pack", "A grumble", "A herd", "A kennel"],
            correct: 1
        }
    ];
    
    // Select random question
    const questionData = questions[Math.floor(Math.random() * questions.length)];
    
    // Set up game state
    currentGame = {
        type: 'quiz',
        question: questionData,
        timeLimit: 15,
        startTime: Date.now(),
        intervalId: null,
        answered: false
    };
    
    // Create game UI
    const gameContent = document.getElementById('gameContent');
    gameContent.innerHTML = `
        <div class="quiz-timer">
            <div class="quiz-timer-bar" style="width: 100%"></div>
        </div>
        
        <h5 class="mb-4">${questionData.question}</h5>
        
        <div class="quiz-options">
            ${questionData.options.map((option, index) => `
                <button class="btn btn-outline-primary w-100 text-start quiz-option" data-index="${index}">
                    ${['A', 'B', 'C', 'D'][index]}. ${option}
                </button>
            `).join('')}
        </div>
        
        <div id="quizResult" class="alert mt-3 d-none"></div>
    `;
    
    // Start timer
    startQuizTimer();
    
    // Set up event listeners
    const quizOptions = document.querySelectorAll('.quiz-option');
    quizOptions.forEach(option => {
        option.addEventListener('click', function() {
            if (currentGame.answered) return;
            
            const selectedIndex = parseInt(this.dataset.index);
            checkQuizAnswer(selectedIndex);
        });
    });
}

// Start quiz timer
function startQuizTimer() {
    const timerBar = document.querySelector('.quiz-timer-bar');
    
    // Update timer every 100ms
    currentGame.intervalId = setInterval(function() {
        const elapsed = (Date.now() - currentGame.startTime) / 1000;
        const remaining = Math.max(0, currentGame.timeLimit - elapsed);
        const percentage = (remaining / currentGame.timeLimit) * 100;
        
        timerBar.style.width = percentage + '%';
        
        if (remaining <= 0) {
            clearInterval(currentGame.intervalId);
            if (!currentGame.answered) {
                timeUpQuiz();
            }
        }
    }, 100);
}

// Time's up for quiz
function timeUpQuiz() {
    currentGame.answered = true;
    
    // Update UI
    const quizResult = document.getElementById('quizResult');
    quizResult.textContent = "Time's up! You didn't answer in time.";
    quizResult.classList.remove('d-none');
    quizResult.classList.add('alert-danger');
    
    // Highlight correct answer
    const quizOptions = document.querySelectorAll('.quiz-option');
    quizOptions.forEach((option, index) => {
        if (index === currentGame.question.correct) {
            option.classList.remove('btn-outline-primary');
            option.classList.add('btn-success');
        } else {
            option.classList.remove('btn-outline-primary');
            option.classList.add('btn-outline-secondary');
        }
        option.disabled = true;
    });
    
    // Add buttons
    const gameContent = document.getElementById('gameContent');
    gameContent.innerHTML += `
        <div class="d-grid gap-2 mt-3">
            <button class="btn btn-primary" id="playAgainBtn">Play Again</button>
            <button class="btn btn-secondary" id="closeGameBtn2">Close</button>
        </div>
    `;
    
    document.getElementById('playAgainBtn').addEventListener('click', () => {
        closeGameOverlay();
        startQuizGame();
    });
    
    document.getElementById('closeGameBtn2').addEventListener('click', closeGameOverlay);
}

// Check quiz answer
function checkQuizAnswer(selectedIndex) {
    clearInterval(currentGame.intervalId);
    currentGame.answered = true;
    
    // Calculate response time
    const responseTime = (Date.now() - currentGame.startTime) / 1000;
    
    // Check if answer is correct
    const isCorrect = selectedIndex === currentGame.question.correct;
    
    // Update UI
    const quizResult = document.getElementById('quizResult');
    
    if (isCorrect) {
        // Base reward
        let reward = 3;
        
        // Bonus for fast response
        const timeBonus = Math.max(0, currentGame.timeLimit - responseTime);
        const timeBonusReward = Math.min(1, timeBonus / 5);
        
        const totalReward = Math.round((reward + timeBonusReward) * 10) / 10;
        
        // Add reward to balance
        userData.dogtea_balance += totalReward;
        updateUserInterface();
        
        quizResult.innerHTML = `
            <p class="mb-1">✅ Correct! You answered in ${responseTime.toFixed(1)} seconds.</p>
            <p class="mb-0">Reward: ${reward.toFixed(1)} DOGTEA + Time bonus: ${timeBonusReward.toFixed(1)} DOGTEA</p>
        `;
        quizResult.classList.remove('d-none');
        quizResult.classList.add('alert-success');
    } else {
        quizResult.innerHTML = `
            <p class="mb-0">❌ Wrong! The correct answer was: ${currentGame.question.options[currentGame.question.correct]}</p>
        `;
        quizResult.classList.remove('d-none');
        quizResult.classList.add('alert-danger');
    }
    
    // Highlight answers
    const quizOptions = document.querySelectorAll('.quiz-option');
    quizOptions.forEach((option, index) => {
        if (index === currentGame.question.correct) {
            option.classList.remove('btn-outline-primary');
            option.classList.add('btn-success');
        } else if (index === selectedIndex && index !== currentGame.question.correct) {
            option.classList.remove('btn-outline-primary');
            option.classList.add('btn-danger');
        } else {
            option.classList.remove('btn-outline-primary');
            option.classList.add('btn-outline-secondary');
        }
        option.disabled = true;
    });
    
    // Add buttons
    const gameContent = document.getElementById('gameContent');
    gameContent.innerHTML += `
        <div class="d-grid gap-2 mt-3">
            <button class="btn btn-primary" id="playAgainBtn">Play Again</button>
            <button class="btn btn-secondary" id="closeGameBtn2">Close</button>
        </div>
    `;
    
    document.getElementById('playAgainBtn').addEventListener('click', () => {
        closeGameOverlay();
        startQuizGame();
    });
    
    document.getElementById('closeGameBtn2').addEventListener('click', closeGameOverlay);
}
