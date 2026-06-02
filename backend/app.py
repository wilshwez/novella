import os
from flask import Flask, render_template, request

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static',
    static_url_path='/static'
)

# Custom template context processor to pass variables if needed
@app.context_processor
def inject_global_vars():
    return {
        'version': '1.0.0'
    }

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/library')
def library():
    # Supports optional query params like ?book=echoes
    book = request.args.get('book', '')
    return render_template('library.html', book=book)

@app.route('/reader')
def reader():
    # Supports optional query params like ?book=echoes&chapter=1
    book = request.args.get('book', '')
    chapter = request.args.get('chapter', 1)
    return render_template('reader.html', book=book, chapter=chapter)

@app.route('/memberships')
def memberships():
    return render_template('memberships.html')

@app.route('/community')
def community():
    # Supports optional query params like ?tab=polls
    tab = request.args.get('tab', 'discussions')
    return render_template('community.html', tab=tab)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/dashboard')
def dashboard():
    # Supports optional query params like ?tab=bookmarks
    tab = request.args.get('tab', 'overview')
    return render_template('dashboard/author_admin.html', tab=tab)

# Health check route
@app.route('/health')
def health():
    return {'status': 'healthy', 'version': '1.0.0'}, 200

if __name__ == '__main__':
    # Listen on all interfaces so it runs seamlessly inside Docker or local workspace environments
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
