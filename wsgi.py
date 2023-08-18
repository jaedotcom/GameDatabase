"""App entry point."""
from games import create_app
from flask import Flask, render_template
import csv

app = create_app()

@app.route('/')
def show_home():
    games = []
    with open('games.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            games.append(row)
    return render_template('home.html', games=games)

@app.route('/gameDescription')
def show_gameDescription():
    return render_template('gameDescription.html')



if __name__ == "__main__":
    app.run(host='localhost', port=5000, threaded=False)
