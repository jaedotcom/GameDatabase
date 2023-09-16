import os.path
from functools import wraps
from flask import Blueprint, render_template, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from password_validator import PasswordValidator
import games.authentication.services as services
from games.adapters.memoryRepository import MemoryRepository

# Configure Blueprint
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    featured_genres = MemoryRepository().get_genres()

    username_not_unique = None
    registration_success = False

    if form.validate_on_submit():
        # Successful POST -- the username & password have passed validation checking
        # Use the service layer to attempt to add the new user
        try:
            services.add_user(form.username.data, form.password.data, MemoryRepository())
            registration_success = True
            print(registration_success)
            # Success, redirect the user to the login page
            return redirect(url_for("authentication_bp.login"))
        except services.NameNotUniqueException:
            username_not_unique = "Username is already taken. Please try again."

    # For a GET or failed POST request, return the Registration web page
    return render_template(
        'authentication/credentials.html',
        title="Sign Up | CS235 Game Library",
        form_title="Sign Up",
        handler_url=url_for("authentication_bp.register"),
        username_error_message=username_not_unique,
        password_error_message=None,
        form=form,
        featured_genres=featured_genres,
        registration_success=registration_success,
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_not_recognised = None
    password_does_not_match_username = None
    featured_genres = MemoryRepository().get_genres()

    if form.validate_on_submit():
        # Successful POST, so the username and password have passed validation checks
        # Use the service layer to look up the user
        try:
            user = services.get_user(form.username.data, MemoryRepository())


            # Authenticate user
            services.authenticate_user(user['username'], form.password.data, MemoryRepository())

            # Initialize the session and redirect the user to the home page
            session.clear()
            session['username'] = user['username']

            return redirect(url_for("profile_bp.profile"))

        except services.UnknownUserException:
            # Username does not exist
            username_not_recognized = "Username not recognized. Please try again or sign up."

        except services.AuthenticationException:
            # Incorrect Password
            password_does_not_match_username = "Incorrect password. Please try again."

    return render_template(
        'authentication/credentials.html',
        title="Log In | CS235 Game Library",
        form_title="Log In",
        form=form,
        handler_url=url_for("authentication_bp.login"),
        featured_genres=featured_genres,
        username_error_message=username_not_recognised,
        password_error_message=password_does_not_match_username,
    )


@authentication_blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for("home_bp.home"))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "username" not in session:
            return redirect(url_for("authentication_bp.login"))
        return view(**kwargs)

    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = "Password must be at least 8 characters long and contain an uppercase character, lowercase " \
                      "character, and a digit from 0-9."
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message="Username is required"),
        Length(min=3, max=50, message="Username must be between 3 and 50 characters long.")
    ])
    password = PasswordField("Password", [
        DataRequired(message="Password is required"),
        PasswordValid(),
        EqualTo('password_confirmation', message='Passwords must match')
    ])
    password_confirmation = PasswordField("Confirm password", [
        DataRequired(message="Password confirmation required"),
    ])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField('Username', [
        DataRequired()
    ])
    password = PasswordField('Password', [
        DataRequired()
    ])
    submit = SubmitField("Login")
