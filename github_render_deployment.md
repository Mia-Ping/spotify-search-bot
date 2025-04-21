# GitHub Repository Setup and Render Deployment Guide

This document provides step-by-step instructions for deploying the Spotify Music Search Bot to Render using GitHub.

## 1. GitHub Repository Setup

1. Create a new repository on GitHub:
   - Go to https://github.com/Mia-Ping
   - Click on "New" to create a new repository
   - Name it "spotify-search-bot"
   - Set it to Public (or Private if you prefer)
   - Initialize with a README
   - Click "Create repository"

2. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Mia-Ping/spotify-search-bot.git
   cd spotify-search-bot
   ```

3. Copy all the deployment files to the repository:
   - app.py
   - audio_processor.py
   - requirements.txt
   - Procfile
   - render.yaml
   - setup_production.py
   - start.sh
   - static/ directory
   - templates/ directory

4. Make the start script executable:
   ```bash
   chmod +x start.sh
   ```

5. Commit and push the files to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit of Spotify Music Search Bot"
   git push origin main
   ```

## 2. Render Deployment

1. Create a Render account:
   - Go to https://render.com/
   - Sign up for a free account (you can use your GitHub account for signup)

2. Connect your GitHub repository:
   - In the Render dashboard, click "New +"
   - Select "Web Service"
   - Connect your GitHub account if not already connected
   - Select the "spotify-search-bot" repository

3. Configure the web service:
   - Name: spotify-search-bot
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt && python setup_production.py`
   - Start Command: `gunicorn app:app`
   - Select the Free plan

4. Add environment variables:
   - Click on "Advanced" to expand additional options
   - Add the following environment variables:
     - SPOTIPY_CLIENT_ID: 112198efe8bc4ae49492ad78031679a8
     - SPOTIPY_CLIENT_SECRET: 9deeb3255e3d4d7187903c8b5ae2dd90
     - SPOTIPY_REDIRECT_URI: https://spotify-search-bot.onrender.com/callback
     - AUDD_API_KEY: (your AudD API key)
     - SECRET_KEY: (generate a random string or leave blank for Render to generate)
     - FLASK_ENV: production

5. Configure disk storage:
   - Under "Disks", click "Add Disk"
   - Name: spotify-data
   - Mount Path: /data
   - Size: 1 GB

6. Deploy the service:
   - Click "Create Web Service"
   - Render will automatically build and deploy your application
   - This process may take a few minutes

7. Update the Spotify Developer Dashboard:
   - Go to https://developer.spotify.com/dashboard/
   - Select your Spotify application
   - Click "Edit Settings"
   - Add the Render URL to the Redirect URIs:
     - https://spotify-search-bot.onrender.com/callback
   - Save the changes

## 3. Testing the Deployment

1. Once the deployment is complete, Render will provide a URL for your application
   (e.g., https://spotify-search-bot.onrender.com)

2. Open the URL in your browser to test the application

3. Verify that all features are working:
   - Spotify authentication
   - Text-based search
   - Audio recognition
   - Humming search
   - Adding songs to Liked Songs

## 4. Troubleshooting

If you encounter issues with the deployment:

1. Check the Render logs for error messages:
   - In the Render dashboard, select your web service
   - Click on "Logs" to view the application logs

2. Common issues and solutions:
   - Authentication errors: Verify that the Spotify redirect URI is correctly set in both Render environment variables and the Spotify Developer Dashboard
   - File storage errors: Check that the disk is properly mounted and the application has write permissions
   - Audio processing errors: Ensure that all required dependencies are installed

3. For persistent issues, you can SSH into the Render instance:
   - In the Render dashboard, select your web service
   - Click on "Shell" to access a terminal
   - Use commands like `ls`, `cd`, and `cat` to inspect files and directories

## 5. Maintenance

To update the application:

1. Make changes to your local repository
2. Commit and push the changes to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
3. Render will automatically detect the changes and redeploy the application

## 6. Monitoring

Render provides basic monitoring for free tier services:

1. In the Render dashboard, select your web service
2. Click on "Metrics" to view CPU and memory usage
3. Set up notifications for service status changes (available in paid plans)

## 7. Scaling

If you need to scale beyond the free tier:

1. In the Render dashboard, select your web service
2. Click on "Settings"
3. Under "Instance Type", select a higher tier
4. Note that this will incur charges according to Render's pricing
