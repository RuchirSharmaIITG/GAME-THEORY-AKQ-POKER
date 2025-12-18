# AKQ Poker: Game Theory Simulation

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Framework-Flask-green?style=flat&logo=flask)
![Game Theory](https://img.shields.io/badge/Project-Game_Theory-orange?style=flat)

A web-based implementation of **AKQ Poker** (also known as Ace-King-Queen or Kuhn Poker), developed to demonstrate **Nash Equilibrium** and **Asymmetric Information** in a zero-sum game environment.

This project simulates a "Heads-Up" match between a human player and an algorithmic opponent that uses mixed strategies to bluff, trap, and value-bet.

---

## 📸 Live Demo & Screenshots

<h2>[Link to Live Site: https://game-theory-akq-poker.onrender.com/]</h2>

<img width="1919" height="902" alt="image" src="https://github.com/user-attachments/assets/adfc279c-51e4-46b5-8c12-036f69c7ba72" />
<h3><p align="center"><b>After choosing Heads(H)</b></p></h3>
<img width="1919" height="906" alt="image" src="https://github.com/user-attachments/assets/ceb23907-18f0-438f-909c-89804aebe0fb" />
<h3><p align="center"><b>GAME BEGINS!!!</b></p></h3>
<img width="1919" height="907" alt="image" src="https://github.com/user-attachments/assets/e95a08d7-5495-49a1-914c-89be54a99451" />
<h3><p align="center"><b>After choosing Call</b></p></h3>
<img width="1919" height="901" alt="image" src="https://github.com/user-attachments/assets/c6af3d3a-e264-4238-852a-3ccc67258a63" />





---

## 📜 The Rules of the Game

AKQ Poker is a simplified version of Hold'em, distilled down to the pure mathematics of bluffing and calling.

1.  **The Deck:** Contains only 3 cards: **Ace (A)**, **King (K)**, **Queen (Q)**.
    * Rank: `Ace > King > Queen`.
2.  **The Ante:** Both players put **$1** into the pot to start ($2 Total).
3.  **The Deal:** Each player receives **one private card**. The third card is discarded unseen.
4.  **The Action:**
    * **Player 1** acts first (Check or Bet $1).
    * **Player 2** responds (Check, Call, or Fold).
5.  **The Showdown:** If neither player folds, the higher card wins the pot.

---

## 🤖 AI Behavior & Strategy

The computer opponent does not play randomly, nor does it play perfectly predictable "static" moves. Instead, it implements a **Mixed Strategy** derived from Game Theory analysis to remain unexploitable.

The AI behaves differently depending on the card it holds:

### ♠️ With an Ace (The "Value" Hand)
* **Behavior:** **Aggressive & Confident.**
* **Strategy:** The AI knows it cannot lose. It primarily bets to force you to pay to see the showdown. However, it will occasionally check (trap) to induce you into bluffing, punishing you for being too aggressive.

### ♣️ With a King (The "Defensive" Hand)
* **Behavior:** **Cautious & Reactive.**
* **Strategy:** The King beats a Queen but loses to an Ace. The AI rarely initiates betting with this hand, preferring to keep the pot small (Checking). When facing a bet, it acts as a **"Bluff Catcher"**—sometimes calling to catch you lying, and sometimes folding to play it safe.

### ♥️ With a Queen (The "Bluff" Hand)
* **Behavior:** **Deceptive & Tricky.**
* **Strategy:** The AI knows it has the worst hand. It cannot win at a showdown. Therefore, it will frequently **Bluff** (represent an Ace) to try and scare you into folding a King. If the bluff fails, it accepts the loss, but the threat of the bluff keeps the game balanced.

---

## 🏗️ Technical Implementation

The project is built using a simple client-server architecture:

* **Backend (Game Logic):**
    * Written in **Python** using **Flask**.
    * Handles state management (whose turn it is, pot size, winner calculation).
    * Implements the decision-making algorithm (`get_computer_move`) which uses weighted randomization to simulate "human-like" unpredictability.
* **Frontend (Interface):**
    * **HTML/CSS:** Custom-styled to resemble a casino table with card flip animations.
    * **JavaScript:** Handles asynchronous `fetch` requests to the Python backend to update the game state without reloading the page.

---

## ⚙️ Installation & Run Locally

If you want to run this simulation on your own machine:

1.  **Clone the repository**
    ```bash
    git clone https://github.com/RuchirSharmaIITG/GAME-THEORY-AKQ-POKER.git
    cd akq-poker-project
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Flask server**
    ```bash
    python app.py
    ```

4.  **Play**
    Open your web browser and go to: `http://127.0.0.1:5000`

---

## 👥 Credits & Reference

**Project Team:**
* Shreyansh Kumar
* Ruchir Sharma
* Shourya Agarwal

**Based on:**
* *Game Theory - AKQ Poker (Technical Analysis, 2025)*
