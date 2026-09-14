import asyncio

from flask import abort, flash, redirect, render_template

from yacut import app
from yacut.disk import upload_files
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import ShortIdAlreadyExistsError, URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()

    if form.validate_on_submit():
        try:
            url_map = URLMap.create(
                original=form.original_link.data,
                custom_id=form.custom_id.data
            )
        except ShortIdAlreadyExistsError as error:
            flash(str(error))
            return render_template('index.html', form=form)

        return render_template(
            'index.html',
            form=form,
            short_link=url_map.get_short_link()
        )

    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.get_by_short(short_id)

    if url_map is None:
        abort(404)

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
            url_map = URLMap.create(
                original=download_link
            )

            uploaded_files.append({
                'filename': filename,
                'short_link': url_map.get_short_link()
            })

    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files
    )
