from kalyna_wallet_lib import generate_cusom_mnemo, get_solana_derived_wallet, get_sol_balance
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = 'KALYNA_WALLET_214_SECRET_KEY'

@app.route('/')
def index():
    if not 'words' in session:
        # session['wallet'] = "7tez6hV2Ju1FkTTuFh3TA3fFAQvrKLUB9o1PQtDzvrBt"
        return render_template('login.html')
    else:
        print(session['words'])
        words = session['words']
        address = get_solana_derived_wallet(words)[0]
        balance = get_sol_balance(address)
        wallet = {
            'address': address,
            'balance': balance
        }
        return render_template('index.html', wallet=wallet)

@app.post('/set_wallet')
def set_wallet():
        # Save the form data to the session object
        data = request.get_json()  # Get JSON data from request body
        text = data.get('text')
        print(f'Received content: {text}')
        mnemo = generate_cusom_mnemo(text)
        if not mnemo:
            return jsonify({'status':'error','message': 'text is to short'})
        session['words'] = mnemo
        return jsonify({'status':'ok','message': 'text processe successfully'})

@app.route('/logout')
def logout():
    # Clear words stored in the session object
    session.pop('words', default=None)
    return redirect('/')