from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from better_profanity import profanity
from games.authentication.authentication import login_required
from games.domainmodel.model import User, Review
from games.games import services as game_services
from games.profile import services as profile_services
from games.adapters import repository as repo
from games.home import services as sv
from games.descriptions import services as description_services

descriptions_blueprint = Blueprint('descriptions_bp', __name__)


@descriptions_blueprint.route('/gameDescription', methods=['GET'])
def descriptions():
    global current_game_dict
    current_game = request.args.get('current_game')
    game_id = request.args.get('current_game_id')
    current_game_type = description_services.get_game(repo.repo_instance, int(game_id))
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

    return render_template('browse/gameDescription.html',
                           games=current_game_dict,
                           all_genres=all_genres,
                           form=form,
                           reviews=current_game_type.reviews)


@descriptions_blueprint.route('/gameDescription/review', methods=['GET', 'POST'])
@login_required
def submit_review():  #### after submit button
    print("description/submit_review")
    current_game_str = request.args.get('current_game')
    current_game = None
    game_id = int(request.args.get('game_id'))

    username = session.get('username')
    password = session.get('password')
    user = User(username=username, password=password)

    if current_game is None:
        current_game = description_services.get_game(repo.repo_instance, game_id)
        all_games = game_services.get_games(repo.repo_instance)

    form = CommentForm()
    if form.validate_on_submit():
        try:
            comment = form.comment.data
            rating = int(form.rating.data)
            game_review = Review(user=user, game=current_game, rating=rating, comment=comment)
            current_game.reviews.append(game_review)
            description_services.add_review_to_database(repo.repo_instance, game_review)

        except ValueError:
            pass

    return render_template(
        'browse/gameDescription.html',
        games=current_game_dict,
        form=form,
        game_id=game_id,
        reviews=current_game.reviews
    )


@descriptions_blueprint.route('/gameDescription/<int:game_id>', methods=['GET'])
def search_game_description():
    print("description search_game_description")
    game_id = request.args.get('current_game_id')
    game = game_services.get_game_by_id(game_id, repo.repo_instance)
    # game = request.args.get('current_game')
    if game is None:
        pass

    all_genres = sv.get_genres(repo.repo_instance)

    form = CommentForm()

    return render_template('browse/gameDescription.html', games=game, all_genres=all_genres, form=form)


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


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message="Comment must be at least 4 characters long."),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = DecimalField('Rating', [
        DataRequired(),
        NumberRange(min=1, max=5, message='Rating must be between 1 and 5')
    ])
    game_id = HiddenField("game id")
    submit = SubmitField('Submit')
