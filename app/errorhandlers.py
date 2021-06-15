from flask import render_template

def page_not_found(e):
    return render_template('404.html'), 404


def method_not_allowed(e):
    return render_template('405.html'), 405


def internal_server_error(e):
    return render_template('500.html'), 500


def forbidden(e):
    return render_template('403.html'), 403