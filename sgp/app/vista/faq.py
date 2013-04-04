#faq.py
from flask import render_template, flash, redirect
from app import app

@app.route('/faq')
def faq():
    return "FAQ"
