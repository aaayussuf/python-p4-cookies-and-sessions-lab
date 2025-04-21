#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    articles_list = [{
        'id': article.id,
        'title': article.title,
        'content': article.content
    } for article in articles]
    return jsonify(articles_list)

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize page_views to 0 if not set
    session['page_views'] = session.get('page_views', 0) + 1

    # Check if page_views exceeds limit
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    # Query the article by id
    article = Article.query.get(id)
    if not article:
        return jsonify({'message': 'Article not found'}), 404

    # Return article data as JSON
    return jsonify({
        'id': article.id,
        'title': article.title,
        'content': article.content
    })

if __name__ == '__main__':
    app.run(port=5556)
