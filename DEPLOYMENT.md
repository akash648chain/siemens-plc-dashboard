# PLC QA Dashboard - Deployment Guide

This guide will help you deploy your Siemens PLC QA Dashboard to the cloud for global access.

## 🚀 Quick Deploy Options

### Option 1: Railway (Recommended - Free & Easy)

1. **Push to GitHub:**
   ```bash
   # Create a new repository on GitHub first, then:
   git remote add origin https://github.com/yourusername/plc-qa-dashboard.git
   git push -u origin main
   ```

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign up/Login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect and deploy your app
   - Your app will be live at: `https://your-app-name.railway.app`

### Option 2: Render (Free Tier Available)

1. **Push to GitHub** (same as above)

2. **Deploy to Render:**
   - Go to [render.com](https://render.com)
   - Sign up/Login with GitHub
   - Click "New" → "Web Service"
   - Connect your GitHub repo
   - Use these settings:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT production_dashboard:app`
   - Your app will be live at: `https://your-app-name.onrender.com`

### Option 3: Heroku

1. **Install Heroku CLI:**
   ```bash
   brew install heroku/brew/heroku
   ```

2. **Deploy:**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

## 🔧 Configuration

### Environment Variables
Set these in your deployment platform:

- `SECRET_KEY`: A random secret key (generate one)
- `PORT`: Usually auto-set by the platform
- `DEBUG`: Set to `False` for production
- `ALLOWED_ORIGINS`: Your domain (e.g., `https://your-app.railway.app`)

### For Railway/Render:
These platforms will automatically set `PORT`. You just need to add:
- `SECRET_KEY`: Generate a secure random string
- `ALLOWED_ORIGINS`: Your deployed URL

## 🌐 Custom Domain (Optional)

1. **Buy a domain** (e.g., from Namecheap, GoDaddy)
2. **Configure DNS** in your deployment platform
3. **Enable SSL** (usually automatic)

## 📱 Access Your Dashboard

Once deployed, your dashboard will be accessible from:
- Any device (phone, tablet, computer)
- Any network (home, office, mobile data)
- Anywhere in the world

## 🔒 Security Features Included

- ✅ Rate limiting (prevents abuse)
- ✅ CORS protection
- ✅ Input validation
- ✅ Error handling
- ✅ Secure headers

## 🛠️ Local Testing

Test the production version locally:
```bash
# Install production dependencies
pip install -r requirements.txt

# Run production server
python production_dashboard.py
```

## 📊 Monitoring

Most platforms provide built-in monitoring:
- View logs
- Monitor performance
- Track errors
- See usage statistics

## 💡 Tips

1. **Start with Railway** - it's the easiest for beginners
2. **Use a custom domain** for a professional look
3. **Monitor your usage** to stay within free tier limits
4. **Keep your repository updated** for easy redeployments

## 🆘 Troubleshooting

**App won't start?**
- Check the logs in your platform dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify environment variables are set

**Can't access the app?**
- Check if the URL is correct
- Ensure the app is deployed and running
- Try accessing from different devices/networks

## 🔄 Updates

To update your deployed app:
1. Make changes locally
2. Commit and push to GitHub
3. Most platforms auto-deploy from main branch
