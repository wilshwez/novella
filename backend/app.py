import os
import json
import datetime
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
    book = request.args.get('book', 'echoes')
    chapter = request.args.get('chapter', 1)
    
    # Load chapters from JSON file
    chapters_path = os.path.join(os.path.dirname(__file__), 'data/chapters.json')
    try:
        with open(chapters_path, 'r') as f:
            chapters = json.load(f)
    except Exception:
        chapters = []
        
    # Filter chapters by book key (e.g. 'echoes' or 'neon')
    book_chapters = [c for c in chapters if c.get('book') == book]
    
    # If someone requested a chapter ID that doesn't exist in the filtered book, default to first chapter ID
    chapter_ids = [c['id'] for c in book_chapters]
    current_chapter_id = int(chapter)
    if current_chapter_id not in chapter_ids and len(chapter_ids) > 0:
        current_chapter_id = chapter_ids[0]
        
    return render_template(
        'reader.html', 
        book=book, 
        chapter=current_chapter_id, 
        chapters_json=json.dumps(book_chapters)
    )

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

# ── API ENDPOINTS FOR PERSISTENCE ──

@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    books_path = os.path.join(os.path.dirname(__file__), 'data/books.json')
    
    if request.method == 'POST':
        data = request.get_json() or {}
        if not data.get('title'):
            return {'error': 'Missing required field: title'}, 400
            
        try:
            with open(books_path, 'r') as f:
                books = json.load(f)
        except Exception:
            books = []
            
        title = data.get('title')
        # Generate unique key from title
        key = "".join([c for c in title.lower() if c.isalnum() or c == ' ']).strip().replace(' ', '-')
        
        # Check if already exists
        if any(b['key'] == key for b in books):
            return {'error': 'A book with this title or key already exists'}, 400
            
        new_book = {
            'key': key,
            'title': title,
            'genre': data.get('genre', 'General Fiction'),
            'status': 'Ongoing',
            'reads': '0',
            'sales': '$0.00',
            'cover': data.get('cover') or 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=600&auto=format&fit=crop',
            'rating': 5.0,
            'desc': data.get('desc', '')
        }
        
        books.append(new_book)
        
        with open(books_path, 'w') as f:
            json.dump(books, f, indent=2)
            
        return {'success': True, 'book': new_book}, 201
        
    else: # GET
        try:
            with open(books_path, 'r') as f:
                books = json.load(f)
        except Exception:
            books = []
        return json.dumps(books), 200

@app.route('/api/chapters', methods=['POST'])
def add_chapter():
    data = request.get_json() or {}
    if not data.get('title') or not data.get('content'):
        return {'error': 'Missing required fields (title, content)'}, 400
        
    chapters_path = os.path.join(os.path.dirname(__file__), 'data/chapters.json')
    try:
        with open(chapters_path, 'r') as f:
            chapters = json.load(f)
    except Exception:
        chapters = []
        
    # Map input book choice to key
    raw_book = data.get('book', 'echoes')
    if 'abyss' in raw_book.lower() or raw_book.lower() == 'echoes':
        book_key = 'echoes'
    elif 'whispers' in raw_book.lower() or raw_book.lower() == 'neon':
        book_key = 'neon'
    elif 'caf' in raw_book.lower() or 'clockwork' in raw_book.lower() or raw_book.lower() == 'autumn':
        book_key = 'autumn'
    else:
        # Create standard key from any custom title
        book_key = "".join([c for c in raw_book.lower() if c.isalnum() or c == ' ']).strip().replace(' ', '-')
        
    new_id = max([c['id'] for c in chapters], default=0) + 1
    try:
        new_seq = int(data.get('seq') or (max([c['seq'] for c in chapters if c.get('book') == book_key], default=0) + 1))
    except ValueError:
        new_seq = max([c['seq'] for c in chapters if c.get('book') == book_key], default=0) + 1
        
    # Calculate approximate reading time
    word_count = len(data.get('content').split())
    read_time = max(1, round(word_count / 180))
    
    new_ch = {
        'id': new_id,
        'book': book_key,
        'seq': new_seq,
        'title': data.get('title'),
        'time': f"{read_time} min read",
        'isPremium': bool(data.get('isPremium')),
        'content': data.get('content').replace('\r\n', '<br><br>').replace('\n', '<br><br>')
    }
    
    chapters.append(new_ch)
    chapters.sort(key=lambda x: x['seq'])
    
    with open(chapters_path, 'w') as f:
        json.dump(chapters, f, indent=2)
        
    return {'success': True, 'chapter': new_ch}, 201

@app.route('/api/tickets', methods=['POST'])
def add_ticket():
    data = request.get_json() or {}
    if not data.get('name') or not data.get('email') or not data.get('message'):
        return {'error': 'Missing required fields (name, email, message)'}, 400
        
    tickets_path = os.path.join(os.path.dirname(__file__), 'data/tickets.json')
    try:
        with open(tickets_path, 'r') as f:
            tickets = json.load(f)
    except Exception:
        tickets = []
        
    new_ticket = {
        'id': len(tickets) + 1,
        'name': data.get('name'),
        'email': data.get('email'),
        'subject': data.get('subject', 'General Support'),
        'message': data.get('message'),
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    tickets.append(new_ticket)
    with open(tickets_path, 'w') as f:
        json.dump(tickets, f, indent=2)
        
    return {'success': True, 'ticket_id': new_ticket['id']}, 201

# ── LOGGING INTERCEPTOR FOR ALL API CALLS ──

@app.after_request
def log_api_call(response):
    if request.path.startswith('/api/'):
        log_path = os.path.join(os.path.dirname(__file__), 'data/api_calls.json')
        try:
            try:
                with open(log_path, 'r') as f:
                    logs = json.load(f)
            except Exception:
                logs = []
                
            log_entry = {
                'timestamp': datetime.datetime.now().isoformat(),
                'method': request.method,
                'path': request.path,
                'ip': request.remote_addr,
                'status_code': response.status_code,
                'payload': request.get_json(silent=True) or {}
            }
            logs.append(log_entry)
            
            with open(log_path, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            app.logger.error(f"Failed to log API call: {e}")
            
    return response

# Health check route
@app.route('/health')
def health():
    return {'status': 'healthy', 'version': '1.0.0'}, 200

if __name__ == '__main__':
    # Listen on all interfaces so it runs seamlessly inside Docker or local workspace environments
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
