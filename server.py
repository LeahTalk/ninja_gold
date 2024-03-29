from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)  
app.secret_key = 'keep it secret, keep it safe'
import random
from datetime import datetime

@app.route('/')
def index():
  if ('gold_amount' not in session) or ('activities' not in session) or ('user_moves' not in session):
    session['gold_amount'] = 0
    session['activities'] = []
    session['user_moves'] = 0
  if session['gold_amount'] >= 300:    
    return render_template('index.html', reset_display = 'inline-block', gold_button_display = "none",
              remaining_moves = "You win!!! You are a Ninja(gambling) master!")
  if session['user_moves'] == 15 or session['gold_amount'] < 0:
    return render_template('index.html', reset_display = 'inline-block', gold_button_display = "none",
              remaining_moves = "You lose!!! You will never be a true ninja....")
  return render_template('index.html', reset_display = 'none', gold_button_display = "inline-block",
   remaining_moves = "Make 300 gold in 15 moves or less! You have " + str(15 - session['user_moves']) + " moves remaining.")

@app.route('/process_money', methods = ['POST'])
def result():
  session['user_moves'] += 1
  dateTimeObj = datetime.now()
  dateStr = str(dateTimeObj.year) + '/' + str(dateTimeObj.month) + '/' + str(dateTimeObj.day)
  timeStr = dateTimeObj.strftime("%I:%M %p")
  action_type = request.form['place']
  if action_type == 'farm':
    gold_earned = random.randint(10, 20)
    session['activities'].append([f"Earned {gold_earned} gold from the farm! ({dateStr} {timeStr})", 'green'])
    session['gold_amount'] += gold_earned
  elif action_type == 'cave':
    gold_earned = random.randint(5, 10)
    session['activities'].append([f"Earned {gold_earned} gold from the cave! ({dateStr} {timeStr})", 'green'])
    session['gold_amount'] += gold_earned
  elif action_type == 'house':
    gold_earned = random.randint(2, 5)
    session['activities'].append([f"Earned {gold_earned} gold from the house! ({dateStr} {timeStr})", 'green'])
    session['gold_amount'] += gold_earned
  else:
    gold_amount = random.randint(0, 50)
    num_sign = random.randint(0,1)
    if gold_amount == 0:
      session['activities'].append([f"Went even at the casino. ({dateStr} {timeStr})", 'black'])
    elif num_sign == 0:
      session['activities'].append([f"Earned {gold_amount} gold from the casino! ({dateStr} {timeStr})", 'green'])
      session['gold_amount'] += gold_amount
    else:
      session['activities'].append([f"Lost {gold_amount} gold at the casino! ({dateStr} {timeStr})", 'red'])
      session['gold_amount'] -= gold_amount
  return redirect('/')

@app.route('/reset')
def reset():
  session.clear()
  return redirect('/')

if __name__=="__main__":   # Ensure this file is being run directly and not from a different module
    app.run(debug=True)    # Run the app in debug mode.
