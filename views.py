import flask

from flask.views import MethodView

from flask_login import (
    login_required,
    current_user,
)

from werkzeug.exceptions import BadRequest

from database import db

from models import (
    User,
    Photo,
)

from exceptions import (
    CoreException,
    LoginException,
)

import forms


class UserRegistrationView(MethodView):
    def get(self):
        form = forms.RegistrationForm()

        return flask.render_template(
            template_name_or_list='registration.html',
            form=form,
        )

    def post(self):
        form = forms.RegistrationForm()

        if form.validate_on_submit():
            form.save()

        return flask.render_template(
            template_name_or_list='registration.html',
            form=form,
        )


class UserLoginView(MethodView):
    def get(self):
        form = forms.LoginForm()

        return flask.render_template(
            template_name_or_list='login.html',
            form=form,
        )

    def post(self):
        form = forms.LoginForm()

        if form.validate_on_submit():
            try:
                form.login()

            except LoginException as exception:
                flask.flash(message=str(exception))

        return flask.render_template(
            template_name_or_list='login.html',
            form=form,
        )


class UploadPhotoView(MethodView):
    decorators = [
        login_required,
    ]

    def get(self):
        form = forms.PhotoForm()

        return flask.render_template(
            template_name_or_list='upload_photo.html',
            form=form,
        )

    def post(self):
        form = forms.PhotoForm()

        if form.validate_on_submit():
            photo = form.save()

            photo_link = photo.photo_link()
            response = flask.redirect(location=photo_link)

            return response

        return flask.render_template(
            template_name_or_list='upload_photo.html',
            form=form,
        )


class ViewFile(MethodView):
    def get(self, file_name):
        uploads_directory = str(flask.current_app.config['UPLOADS_DIRECTORY'])

        return flask.send_from_directory(uploads_directory, file_name)


class UserProfileView(MethodView):
    def get(self, user_id):
        user = User.query.get(user_id)

        if user is None:
            return 'User not found!', 404

        return flask.render_template(
            template_name_or_list='profile_photos.html',
            photos=user.photos,
        )


class PhotoDetailView(MethodView):
    def get(self, photo_id):
        photo = Photo.query.get(photo_id)

        if photo is None:
            return 'Photo not found', 404

        return flask.render_template(
            template_name_or_list='photo_detail.html',
            photo=photo,
        )


class AddLikeView(MethodView):
    decorators = [
        login_required,
    ]

    def post(self, photo_id):
        photo = Photo.query.get(photo_id)

        if photo is None:
            return 'Photo not found', 404

        try:
            like = photo.add_like(from_user=current_user)

        except CoreException as exception:
            raise BadRequest(description=str(exception)) from exception

        db.session.add(like)
        db.session.commit()

        return 'ok'


class AddCommentView(MethodView):
    decorators = [
        login_required,
    ]

    def post(self, photo_id):
        photo = Photo.query.get(photo_id)

        if photo is None:
            return 'Photo not found', 404

        comment = photo.add_comment(
            from_user=current_user,
            content=flask.request.form['content'],
        )

        db.session.add(comment)
        db.session.commit()

        return 'ok'
