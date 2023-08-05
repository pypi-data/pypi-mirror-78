from flask import render_template, flash, redirect, url_for
from .app import app
from .token import RequestToken


@app.route('/token', methods=['GET', 'POST'])
def request_token():
    form = RequestToken()
    if form.validate_on_submit():
        flash('A valid email address is required')
        return redirect(url_for('index'))
    return render_template('requesttoken.html', title='Request a new API token', form=form)