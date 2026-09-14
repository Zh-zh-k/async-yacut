import asyncio

from flask import flash, redirect, render_template

from yacut import app, db
from yacut.disk import upload_files
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id

DUPLICATED_SHORT_ID_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()

    if form.validate_on_submit():
        custom_id = form.custom_id.data

        if custom_id:
            if custom_id == 'files' or URLMap.query.filter_by(
                short=custom_id
            ).first():
                flash(DUPLICATED_SHORT_ID_MESSAGE)
                return render_template('index.html', form=form)

            short_id = custom_id
        else:
            short_id = get_unique_short_id()

        url_map = URLMap(
            original=form.original_link.data,
            short=short_id
        )
        db.session.add(url_map)
        db.session.commit()

        short_link = f'http://localhost/{short_id}'

        return render_template(
            'index.html',
            form=form,
            short_link=short_link
        )

    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    form = FileUploadForm()
    uploaded_files = []

    if form.validate_on_submit():
        files_data = [
            (file.filename, file.read())
            for file in form.files.data
        ]

        upload_results = asyncio.run(
            upload_files(files_data)
        )

        for filename, download_link in upload_results:
            short_id = get_unique_short_id()

            url_map = URLMap(
                original=download_link,
                short=short_id
            )

            db.session.add(url_map)

            uploaded_files.append({
                'filename': filename,
                'short_link': f'http://localhost/{short_id}'
            })

        db.session.commit()

    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files
    )
