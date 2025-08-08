# InBrief News Backend - Railway Deployment

🚀 **Fresh Railway deployment for InBrief News Application with enhanced admin dashboard**

## 🌟 Features

### ✅ Core Features
- **Flask REST API** for mobile app integration
- **PostgreSQL Database** with Supabase integration
- **Admin Dashboard** with create/edit/delete functionality
- **CORS Enabled** for mobile app access
- **Health Check Endpoints** for monitoring
- **Publish/Unpublish Toggle** for post management

### ✅ Railway Optimizations
- **Production-ready configuration** 
- **Auto-scaling support**
- **Environment variable management**
- **Custom domain support**
- **Database connection pooling**

## 🚂 Railway Deployment Instructions

### Step 1: Repository Setup
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial Railway deployment setup"

# Add remote repository (replace with your repo URL)
git remote add origin https://github.com/your-username/inbrief-railway-backend.git
git push -u origin main
```

### Step 2: Railway Project Creation
1. Go to [Railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose this repository
5. Railway will auto-detect the Flask app

### Step 3: Environment Variables
Add these in Railway Dashboard → Variables:
```
DATABASE_URL=postgresql://postgres.iwzmixjdzjdukkrkwyxh:InBrief2025!@aws-0-ap-south-1.pooler.supabase.com:5432/postgres
SECRET_KEY=inbrief-railway-production-key-2025
FLASK_ENV=production
FLASK_DEBUG=false
```

### Step 4: Custom Domain (Optional)
To avoid `.up.railway.app` blocking:
1. Railway Dashboard → Settings → Custom Domain
2. Add your custom domain (e.g., `api.yourdomain.com`)
3. Update DNS records as instructed
4. Or use Railway's alternative domains

## 📡 API Endpoints

### Public Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `GET /api/news` - Get all published news
- `GET /api/news/<id>` - Get single news post

### Admin Endpoints
- `GET /admin` - Admin dashboard
- `GET /admin/create` - Create post form
- `POST /admin/create` - Create new post
- `POST /admin/delete/<id>` - Delete post
- `POST /admin/toggle/<id>` - Toggle publish status

## 🏗️ Project Structure
```
railway-backend-fresh/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment config
├── railway.toml          # Railway build config
├── .env.example          # Environment variables template
├── templates/            # HTML templates
│   ├── admin_dashboard.html
│   └── create_post.html
└── README.md             # This file
```

## 🔧 Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="your_database_url"
export SECRET_KEY="your_secret_key"

# Run application
python app.py
```

## 📱 Mobile App Integration

Update your Flutter app's `NetworkService` with the new Railway URL:

```dart
class NetworkService {
  static const String baseUrl = 'https://your-app-name.railway.app';
  // Or your custom domain: 'https://api.yourdomain.com'
  
  static const String newsEndpoint = '$baseUrl/api/news';
  static const String healthEndpoint = '$baseUrl/health';
}
```

## 🎯 Key Improvements

### Database
- ✅ PostgreSQL with connection pooling
- ✅ Timezone-aware timestamps
- ✅ Indexed columns for performance
- ✅ Publish/unpublish functionality

### Admin Dashboard
- ✅ Modern responsive design
- ✅ Real-time statistics
- ✅ Post management (CRUD)
- ✅ Status toggles
- ✅ Image preview support

### API
- ✅ RESTful design
- ✅ Error handling
- ✅ CORS configuration
- ✅ Health monitoring
- ✅ Mobile-optimized responses

### Railway Features
- ✅ Auto-deployment from GitHub
- ✅ Environment variable management
- ✅ Custom domain support
- ✅ Auto-scaling
- ✅ Build optimization

## 🌐 Domain Solutions

### Option 1: Custom Domain
- Buy a domain (e.g., `yourdomain.com`)
- Point `api.yourdomain.com` to Railway
- No blocking issues

### Option 2: Railway Alternative Domains
Railway provides multiple domain patterns:
- `your-app.railway.app` (instead of `.up.railway.app`)
- Custom subdomains
- Regional domains

### Option 3: Subdomain Setup
If you have an existing domain:
- `news-api.yourdomain.com`
- `backend.yourdomain.com`
- `api.yourdomain.com`

## 🚀 Deployment Checklist

- [ ] Repository created and pushed
- [ ] Railway project connected
- [ ] Environment variables set
- [ ] Custom domain configured (optional)
- [ ] Database connection tested
- [ ] Admin dashboard accessible
- [ ] API endpoints working
- [ ] Mobile app updated with new URL

## 📞 Support

If you encounter any issues:
1. Check Railway logs in Dashboard
2. Verify environment variables
3. Test database connection
4. Check API endpoints manually

## 🎉 Success Metrics

After deployment, you should have:
- ✅ Working admin dashboard at `/admin`
- ✅ API responding at `/api/news`
- ✅ Health check passing at `/health`
- ✅ Mobile app connecting successfully
- ✅ Posts persisting in database
- ✅ No domain blocking issues
