// Global State
let userRole = "";

async function tossCoin(choice) {
    const res = await fetch('/toss_coin', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ choice: choice })
    });
    const data = await res.json();

    // UI Updates for Coin Toss
    const resultText = document.getElementById('coin-result');
    resultText.innerHTML = `Coin landed on <b>${data.toss_result}</b>. <br> 
                            You are ${data.user_won_toss ? "<b>Player 1 (Act First)</b>" : "<b>Player 2 (Act Second)</b>"}`;
    
    // Transition to Game
    setTimeout(() => {
        document.getElementById('coin-section').classList.add('hidden');
        document.getElementById('game-section').classList.remove('hidden');
        setupGameUI(data);
    }, 2000);
}

function setupGameUI(data) {
    userRole = data.user_role;
    document.getElementById('player-role-display').innerText = userRole;
    document.getElementById('user-card-val').innerText = data.user_card;
    
    // If User is Player 1, they act immediately.
    // If User is Player 2, we need to ask server for Computer's first move.
    
    processGameStep(null); // Initialize game loop
}

async function processGameStep(userAction) {
    // Disable buttons while processing
    const btnArea = document.getElementById('action-buttons');
    btnArea.innerHTML = ''; 

    const res = await fetch('/game_step', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ action: userAction })
    });
    const data = await res.json();

    // Update Pot
    if(data.pot) document.getElementById('pot-amount').innerText = data.pot;

    // Check for Game Over
    if (data.game_over) {
        endGame(data);
        return;
    }

    // Show Computer Move if happened
    if (data.comp_move) {
        const compBubble = document.getElementById('comp-action');
        compBubble.innerText = `Computer chooses: ${data.comp_move}`;
        compBubble.style.animation = "none";
        compBubble.offsetHeight; /* trigger reflow */
        compBubble.style.animation = "popIn 0.3s";
    }

    // Update Message and Buttons for User
    if (data.message) {
        document.getElementById('game-message').innerText = data.message;
        
        btnArea.classList.remove('hidden');
        data.options.forEach(opt => {
            const btn = document.createElement('button');
            btn.innerText = opt;
            btn.onclick = () => processGameStep(opt);
            btnArea.appendChild(btn);
        });
    } else {
        document.getElementById('game-message').innerText = "Waiting for computer...";
        // If no message/options, likely recursing or waiting (shouldn't happen in this sync logic often)
    }
}

function endGame(data) {
    // Reveal Computer Card
    const compCardVis = document.getElementById('comp-card-vis');
    compCardVis.classList.remove('back');
    compCardVis.classList.add('front');
    compCardVis.innerHTML = `<span class="card-text">${data.comp_card}</span>`;

    // Show Overlay after brief delay
    setTimeout(() => {
        const overlay = document.getElementById('result-overlay');
        overlay.classList.remove('hidden');
        
        document.getElementById('winner-text').innerText = data.winner === "User" ? "YOU WON!" : "YOU LOST!";
        document.getElementById('reason-text').innerText = data.reason;
        document.getElementById('money-text').innerText = data.money_msg;
        
        // Dynamic color
        document.querySelector('.result-box').style.borderTop = 
            `10px solid ${data.winner === "User" ? "#2ecc71" : "#e74c3c"}`;
    }, 1000);
}