import random
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'super_secret_akq_key'  # Needed for session management

# --- GAME CONSTANTS ---
CARDS = ['A', 'K', 'Q']
CARD_VALUES = {'A': 3, 'K': 2, 'Q': 1}

# --- AI LOGIC ---
def get_computer_move(computer_card, action_history, current_role):
    """
    Simple AI Strategy for AKQ Game.
    """
    # If Computer is Player 1
    if current_role == 'Player 1':
        if len(action_history) == 0:  # Opening move
            # Bet strongly with Ace (Value), Bet sometimes with Queen (Bluff), Check King
            if computer_card == 'A': return 'Check' if random.random() > 0.9 else 'Bet'
            if computer_card == 'Q': return 'Bet' if random.random() > 0.7 else 'Check'
            else : return 'Check'
        
        # Inside get_computer_move, under Player 1 Logic
        if action_history[-1] == 'Bet': 
            if computer_card == 'A': return 'Call'  # Always call with Ace
            if computer_card == 'Q': return 'Fold'

            # Handling the King
            if computer_card == 'K':
                # Fold 60% of the time, Call 40% of the time
                # Here we are putting slightly more emphasis on fold as we are only playing one round poker 
                # So we can't actually estimate about the frequency of the other player bluffing thus it is always safe to lose less money. 
                # If the other player had Ace and we will call then definitely we are bound to loose more money.
                return 'Call' if random.random() > 0.6 else 'Fold'

    # If Computer is Player 2
    if current_role == 'Player 2':
        last_move = action_history[-1]
        
        if last_move == 'Check': # Player 1 checked
            # Bet with Ace, Check with King, Bluff Bet small % with Queen
            if computer_card == 'A': return 'Bet'
            if computer_card == 'Q': return 'Bet' if random.random() > 0.7 else 'Check'
            return 'Bet' if random.random() > 0.8 else 'Check'
            
        if last_move == 'Bet': # Player 1 bet
            # Call with Ace
            if computer_card == 'A': return 'Call'
            # Here we are putting slightly more emphasis on fold as we are only playing one round poker 
            # So we can't actually estimate about the frequency of the other player bluffing thus it is always safe to lose less money. 
            # If the other player had Ace and we will call then definitely we are bound to loose more money.
            if computer_card == 'K': return 'Call' if random.random() > 0.6 else 'Fold' 
            return 'Fold'
    
    return 'Check' # Fallback

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/toss_coin', methods=['POST'])
def toss_coin():
    """
    Handles the initial coin toss to determine Player 1 vs Player 2.
    """
    user_choice = request.json.get('choice') # 'H' or 'T'
    toss_result = random.choice(['H', 'T'])
    
    user_won_toss = (user_choice == toss_result)
    
    # Setup Game State
    deck = CARDS.copy()
    random.shuffle(deck)
    
    session['user_card'] = deck.pop()
    session['comp_card'] = deck.pop()
    session['user_role'] = 'Player 1' if user_won_toss else 'Player 2'
    session['comp_role'] = 'Player 2' if user_won_toss else 'Player 1'
    session['pot'] = 2.0  # Ante $1 each
    session['history'] = []
    session['game_over'] = False
    
    return jsonify({
        'toss_result': toss_result,
        'user_won_toss': user_won_toss,
        'user_role': session['user_role'],
        'user_card': session['user_card'],
        # We do NOT send comp_card yet
    })

@app.route('/game_step', methods=['POST'])
def game_step():
    """
    Handles a single turn of the game.
    """
    user_action = request.json.get('action') # 'Bet', 'Check', 'Call', 'Fold', or None (start)
    
    response = {}
    history = session.get('history', [])
    user_role = session.get('user_role')
    comp_role = session.get('comp_role')
    
    # 1. Handle User Action (if any)
    if user_action:
        history.append(user_action)
        if user_action == 'Bet':
            session['pot'] += 1
        elif user_action == 'Call':
            session['pot'] += 1
            return finish_game(history, reason="Showdown")
        elif user_action == 'Fold':
            return finish_game(history, winner="Computer", reason="You Folded")

    # 2. Check if User checked and it was P2's turn to end game (Check-Check)
    if len(history) == 2 and history == ['Check', 'Check']:
         return finish_game(history, reason="Showdown")

    # 3. Computer's Turn?
    # Logic: It's computer turn if:
    # - History is empty and Comp is P1
    # - Last move was 'Check' and Comp is P2
    # - Last move was 'Bet' and Comp is P2 (needs to call/fold)
    # - Last move was 'Bet' and Comp is P1 (P2 bet, P1 must act)
    
    is_comp_turn = False
    if len(history) == 0 and comp_role == 'Player 1': is_comp_turn = True
    elif len(history) > 0:
        last_actor = 'User' if len(history) % 2 != 0 else 'Computer' 
        # If User started (P1), len=1 (User acted), now Comp (P2) turn.
        # Wait, if User is P1, they act at index 0. Next is index 1 (Comp).
        if user_role == 'Player 1':
            if len(history) % 2 != 0: is_comp_turn = True
        else: # User is P2
            if len(history) % 2 == 0: is_comp_turn = True

    if is_comp_turn:
        comp_move = get_computer_move(session['comp_card'], history, comp_role)
        history.append(comp_move)
        session['history'] = history
        
        response['comp_move'] = comp_move
        
        if comp_move == 'Bet':
            session['pot'] += 1
            response['message'] = "Computer Bets $1. Your action?"
            response['options'] = ['Call', 'Fold']
        elif comp_move == 'Check':
            if len(history) == 2 and history[0] == 'Check': # Check-Check
                return finish_game(history, reason="Showdown")
            response['message'] = "Computer Checks. Your action?"
            response['options'] = ['Check', 'Bet'] if len(history)==1 else ['Check', 'Bet'] # Logic for P2
        elif comp_move == 'Call':
            session['pot'] += 1
            return finish_game(history, reason="Showdown")
        elif comp_move == 'Fold':
            return finish_game(history, winner="User", reason="Computer Folded")
            
    else:
        # It's User's turn to start (User is P1, empty history)
        if len(history) == 0 and user_role == 'Player 1':
            response['message'] = "You are Player 1. Action?"
            response['options'] = ['Check', 'Bet']
    
    response['pot'] = session['pot']
    return jsonify(response)

def finish_game(history, winner=None, reason=""):
    """
    Calculates results and formats the final response.
    """
    user_card = session['user_card']
    comp_card = session['comp_card']
    pot = session['pot']
    
    if winner is None: # Showdown
        user_val = CARD_VALUES[user_card]
        comp_val = CARD_VALUES[comp_card]
        if user_val > comp_val:
            winner = "User"
            reason = f"Showdown: {user_card} beats {comp_card}"
        else:
            winner = "Computer"
            reason = f"Showdown: {comp_card} beats {user_card}"
            
    money_msg = ""
    if winner == "User":
        money_msg = f"You won ${pot}" # Simplified net
    else:
        money_msg = f"Computer won ${pot} (You lost)"

    return jsonify({
        'game_over': True,
        'winner': winner,
        'reason': reason,
        'money_msg': money_msg,
        'pot': pot,
        'comp_card': comp_card, # Reveal computer card
        'history': history
    })

if __name__ == '__main__':
    app.run(debug=True)