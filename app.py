from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
import pytz
import cloudinary
import cloudinary.uploader
import cloudinary.api
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Cloudinary Configuration
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', 'dhktf9m25'),
    api_key=os.environ.get('CLOUDINARY_API_KEY', '159532712964974'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET', 'DssDwgjlFynfrU2V8sFZzt3ixF8')
)

# Railway Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
                        'postgresql://postgres.iwzmixjdzjdukkrkwyxh:InBrief2025!@aws-0-ap-south-1.pooler.supabase.com:5432/postgres'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_timeout': 20,
    'max_overflow': 0
}

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'inbrief-railway-secret-2025'
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Initialize database
db = SQLAlchemy(app)

# Configure CORS with specific origins
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "supports_credentials": True
    }
})

# Database Model
class NewsPost(db.Model):
    __tablename__ = 'news_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    content = db.Column(db.Text)
    image_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(pytz.UTC), index=True)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(pytz.UTC), onupdate=lambda: datetime.now(pytz.UTC))
    author = db.Column(db.String(200), default='Admin')
    source_url = db.Column(db.Text)
    is_published = db.Column(db.Boolean, default=True, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'author': self.author,
            'source_url': self.source_url,
            'is_published': self.is_published
        }

# API Routes
@app.route('/')
def home():
    """API information and health status"""
    return jsonify({
        "app": "InBrief News API",
        "version": "2.0",
        "status": "healthy",
        "deployment": "railway",
        "endpoints": {
            "news_api": "/api/news",
            "admin_dashboard": "/admin", 
            "health_check": "/health",
            "create_post": "/admin/create"
        },
        "database": "postgresql_connected",
        "cors": "enabled"
    })

@app.route('/health')
def health_check():
    """Comprehensive health check"""
    try:
        # Database connection test
        post_count = NewsPost.query.count()
        latest_post = NewsPost.query.order_by(NewsPost.created_at.desc()).first()
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "total_posts": post_count,
            "latest_post_id": latest_post.id if latest_post else None,
            "timestamp": datetime.now(pytz.UTC).isoformat(),
            "railway_deployment": True
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy", 
            "error": str(e),
            "timestamp": datetime.now(pytz.UTC).isoformat()
        }), 500

@app.route('/api/news')
@app.route('/api/news/all')
def get_all_news():
    """Get all published news posts for mobile app"""
    try:
        posts = NewsPost.query.filter_by(is_published=True)\
                             .order_by(NewsPost.created_at.desc())\
                             .all()
        
        return jsonify({
            "success": True,
            "total_posts": len(posts),
            "posts": [post.to_dict() for post in posts]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/news/<int:post_id>')
def get_single_news(post_id):
    """Get single news post by ID"""
    try:
        post = NewsPost.query.filter_by(id=post_id, is_published=True).first()
        if not post:
            return jsonify({"error": "Post not found"}), 404
            
        return jsonify({
            "success": True,
            "post": post.to_dict()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Admin Routes
@app.route('/admin')
def admin_dashboard():
    """Admin dashboard to manage posts"""
    try:
        posts = NewsPost.query.order_by(NewsPost.created_at.desc()).all()
        return render_template('admin_dashboard.html', posts=posts)
    except Exception as e:
        return f"Database error: {str(e)}", 500

@app.route('/admin/upload-image', methods=['POST'])
def upload_image():
    """Upload image to Cloudinary"""
    try:
        if 'image' not in request.files:
            return jsonify({"success": False, "error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"success": False, "error": "No image selected"}), 400
        
        if file:
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                file,
                folder="inbrief-news",  # Dynamic folder in Cloudinary
                transformation=[
                    {'width': 800, 'height': 600, 'crop': 'fill', 'quality': 'auto:good'},
                    {'fetch_format': 'auto'}
                ]
            )
            
            return jsonify({
                "success": True,
                "image_url": result['secure_url'],
                "public_id": result['public_id']
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Upload failed: {str(e)}"
        }), 500

@app.route('/admin/create', methods=['GET', 'POST'])
def create_post():
    """Create new news post"""
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            image_url = request.form.get('image_url', '').strip()
            author = request.form.get('author', 'Admin').strip()
            source_url = request.form.get('source_url', '').strip()
            
            if not title:
                flash('Title is required!', 'error')
                return redirect(url_for('create_post'))
            
            post = NewsPost(
                title=title,
                content=content,
                image_url=image_url if image_url else None,
                author=author,
                source_url=source_url if source_url else None,
                is_published=True
            )
            
            db.session.add(post)
            db.session.commit()
            
            flash(f'Post "{title}" created successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating post: {str(e)}', 'error')
            return redirect(url_for('create_post'))
    
    return render_template('create_post.html')

@app.route('/admin/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    """Delete a news post"""
    try:
        post = NewsPost.query.get_or_404(post_id)
        title = post.title
        db.session.delete(post)
        db.session.commit()
        flash(f'Post "{title}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting post: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/toggle/<int:post_id>', methods=['POST'])
def toggle_post_status(post_id):
    """Toggle post published status"""
    try:
        post = NewsPost.query.get_or_404(post_id)
        post.is_published = not post.is_published
        post.updated_at = datetime.now(pytz.UTC)
        db.session.commit()
        
        status = "published" if post.is_published else "unpublished"
        flash(f'Post "{post.title}" {status} successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating post: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

# Database initialization
def init_database():
    """Initialize database with tables and sample data"""
    try:
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Add sample data if no posts exist
            if NewsPost.query.count() == 0:
                sample_posts = [
                    NewsPost(
                        title="Welcome to InBrief - Railway Deployment!",
                        content="Your news application is now running on Railway with a completely fresh setup and enhanced admin dashboard.",
                        author="System",
                        is_published=True
                    ),
                    NewsPost(
                        title="Enhanced Admin Dashboard",
                        content="The new admin panel includes post management, publish/unpublish toggles, and better mobile app integration.",
                        author="Admin",
                        is_published=True
                    ),
                    NewsPost(
                        title="Mobile App Ready",
                        content="All API endpoints are optimized for your Flutter mobile application with proper CORS and error handling.",
                        author="DevOps",
                        is_published=True
                    ),
                    NewsPost(
                        title="Database Persistence",
                        content="Your news posts are now permanently stored in PostgreSQL database with automatic backups.",
                        author="System",
                        is_published=True
                    )
                ]
                
                for post in sample_posts:
                    db.session.add(post)
                
                db.session.commit()
                print("✅ Sample data added successfully")
                print(f"✅ Created {len(sample_posts)} sample posts")
                
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

# Initialize database on startup
init_database()

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )
