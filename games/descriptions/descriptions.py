from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from better_profanity import profanity
from games.authentication.authentication import login_required
from games.domainmodel.model import User, Review
from games.games import services as game_services
from games.games.services import get_game_by_id
from games.profile import services as profile_services
from games.adapters import repository as repo
from games.home import services as sv
from games.reviews.reviews import ProfanityFree

descriptions_blueprint = Blueprint('descriptions_bp', __name__)


@descriptions_blueprint.route('/gameDescription', methods=['GET'])
def descriptions():
    global current_game_dict
    current_game = request.args.get('current_game')
    game_id = request.args.get('current_game_id')
    try:
        current_game_dict = eval(current_game)
    except SyntaxError:
        all_games = game_services.get_games(repo.repo_instance)
        for game in all_games:
            if game.get('game_id') == int(game_id):
                current_game_dict = game
    all_genres = sv.get_genres(repo.repo_instance)
    # Create an instance of CommentForm
    form = CommentForm()

    return render_template('browse/gameDescription.html', games=current_game_dict, all_genres=all_genres, form=form)


@descriptions_blueprint.route('/gameDescription/review', methods=['GET', 'POST'])
@login_required
def submit_review():
    current_game = request.args.get('current_game')
    print(current_game)
    game_id = request.args.get('game_id')
    print(game_id)

    username = session.get('username')
    password = session.get('password')
    user = User(username=username, password=password)

    if current_game is None:
        all_games = game_services.get_games(repo.repo_instance)
        for game in all_games:
            if game.get('game_id') == int(game_id):
                current_game = game

    form = CommentForm()
    if form.validate_on_submit():
        if current_game_dict:
            try:
                comment = form.comment.data
                rating = int(form.rating.data)
                game_review = Review(user=user, game=current_game, rating=rating, comment=comment)
                current_game.reviews.append(game_review)

                return redirect(url_for('browse/DescriptionReview.html', review=game_review, games=current_game, game_id=game_id))

            except ValueError:
                pass

    return render_template(
        'browse/gameDescription.html',
        games=current_game,
        form=form,
        game_id=game_id,
    )


@descriptions_blueprint.route('/gameDescription/<int:game_id>', methods=['GET'])
def search_game_description():
    game_id = request.args.get('current_game_id')
    game = game_services.get_game_by_id(game_id, repo.repo_instance)
    # game = request.args.get('current_game')
    if game is None:
        pass

    all_genres = sv.get_genres(repo.repo_instance)

    form = CommentForm()

    return render_template('browse/gameDescription.html', games=game, all_genres=all_genres, form=form)


@descriptions_blueprint.route('/gameDescription/withReviews', methods=['GET'])
def descriptions_with_reviews():
    global current_game_dict
    current_game = request.args.get('current_game')
    game_id = request.args.get('current_game_id')
    try:
        current_game_dict = eval(current_game)
    except SyntaxError:
        all_games = game_services.get_games(repo.repo_instance)
        for game in all_games:
            if game.get('game_id') == int(game_id):
                current_game_dict = game
    all_genres = sv.get_genres(repo.repo_instance)

    # Create an instance of CommentForm
    form = CommentForm()
    review = repo.get_reviews_by_game_id(int(game_id))
    return render_template('browse/gameDescription.html', reviews=review, games=current_game_dict,
                           all_genres=all_genres, form=form)


@descriptions_blueprint.route('/gameDescription/favourite', methods=['GET', 'POST'])
@login_required
def favourite():
    current_game = request.args.get('current_game')
    game_id = request.args.get('current_game_id')

    try:
        current_game_dict = eval(current_game)
    except SyntaxError:
        all_games = game_services.get_games(repo.repo_instance)
        for game in all_games:
            if game.get('game_id') == int(game_id):
                current_game_dict = game

    user = session.get('username')
    if user:
        current_user = profile_services.get_user(user, repo.repo_instance)

        if current_user:
            game1 = repo.repo_instance.get_game_by_id(current_game_dict['game_id'])

            if game1:
                profile_services.add_to_favourites(current_user, game1)

    all_genres = sv.get_genres(repo.repo_instance)

    # Create an instance of CommentForm
    form = CommentForm()

    return render_template('browse/gameDescription.html', games=current_game_dict, all_genres=all_genres, form=form)


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = TextAreaField('Rating', [
        DataRequired(),
        NumberRange(min=1, max=5, message='Rating must be between 1 and 5')
    ])
    game_id = HiddenField("game id")
    submit = SubmitField('Submit')
