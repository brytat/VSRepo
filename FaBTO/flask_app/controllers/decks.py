
from flask import url_for, render_template, redirect, request, session

from flask_app import app
from flask_app.models.deck import Deck
from flask_app.models.user import User

from flask_app.controllers.users import render_decks_page

@app.route('/deck/create', methods=['POST'])
def create_deck():
    if request.form['user_id'] not in session:
        flash("You are not able to make decks for another user.")
        return redirect(url_for('render_decks_page', user_id=request.form['user_id']))
    data = {
        "deck_hero":request.form['deck_hero'],
        "format":request.form['format'],
        "deck_comp_level":request.form['deck_comp_level'],
        "description":request.form['description'],
        "user_id":request.form["user_id"]
    }
    print(data)
    Deck.create_deck(data)
    return redirect(url_for('render_decks_page', user_id=session['user_id']))

@app.route('/deck/edit/<int:deck_id>')
def render_edit_deck(deck_id):
    if 'user_id' not in session:
        return redirect('/')
    pageName = "Edit Deck"
    data = {
        'deck_id': deck_id
    }
    data1 = {
        "user_id": session['user_id']
    }
    deck = Deck.get_one(data)
    deck = deck[0]
    user = User.get_one(data1)
    return render_template('editDeck.html', user=user, deck=deck, pageName=pageName)

@app.route('/deck/update/<int:deck_id>', methods=['POST'])
def process_update_deck(deck_id):
    if session['user_id'] not in session:
        return redirect('/')
    data = {
        'deck_hero': request.form['deck_hero'],
        'format': request.form['format'],
        'deck_comp_level': request.form['deck_comp_level'],
        'description': request.form['description'],
        'deck_id': deck_id,
    }
    print(data)
    Deck.update_deck(data)
    return redirect(url_for('render_decks_page', user_id=session['user_id']))

@app.route('/deck/delete/<int:deck_id>')
def delete_deck(deck_id):
    if session['user_id'] not in session:
        return redirect('/')
    data = {
        'deck_id': deck_id
    }
    Deck.delete_deck(data)
    return redirect(url_for('render_decks_page', user_id=session['user_id']))