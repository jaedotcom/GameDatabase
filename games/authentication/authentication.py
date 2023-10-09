import os.path
from functools import wraps
from flask import Blueprint, render_template, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from password_validator import PasswordValidator
import games.authentication.services as services
import games.adapters.repository as repo


# Configure Blueprint
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_not_unique = None
    registration_success = False

    if form.validate_on_submit():
        try:
            services.add_user(form.username.data, form.password.data, repo.repo_instance)
            registration_success = True
            return redirect(url_for("authentication_bp.login"))
        except services.NameNotUniqueException:
            username_not_unique = "Username is already taken. Please try again."    # This is not working#

    # For a GET or failed POST request, return the Registration web page
    return render_template(
        'authentication/credentials.html',
        title="Sign Up | CS235 Game Library",
        form_title="Sign Up",
        handler_url=url_for("authentication_bp.register"),
        username_error_message=username_not_unique,
        password_error_message=None,
        form=form,
        registration_success=registration_success,
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_not_recognised = None
    password_does_not_match_username = None

    if form.validate_on_submit():
        try:
            user = services.get_user_details(form.username.data, repo.repo_instance)


            # Authenticate user
            current_user = services.authenticate_user(user['username'], form.password.data, repo.repo_instance)
            #current_user = services.get_current_user(form.username.data, repo.repo_instance)
            current_user_name = current_user.username
            session.clear()
            session['username'] = user['username']
            session['password'] = user['password']

            return redirect(url_for("profile_bp.profile", current_user=current_user_name))

        except services.UnknownUserException:
            username_not_recognised = "Username not recognized. Please try again or sign up."

        except services.AuthenticationException:
            password_does_not_match_username = "Incorrect password. Please try again."

    return render_template(
        'authentication/credentials.html',
        title="Log In | CS235 Game Library",
        form_title="Log In",
        form=form,
        handler_url=url_for("authentication_bp.login"),
        username_error_message=username_not_recognised,  # Corrected variable name
        password_error_message=password_does_not_match_username,  # Corrected variable name
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
