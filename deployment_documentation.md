# Spotify Music Search Bot - Deployment Documentation

This document provides comprehensive documentation for the deployment of the Spotify Music Search Bot as a permanent website.

## Overview

The Spotify Music Search Bot has been deployed as a web application using Render, a cloud platform that offers free hosting suitable for applications with moderate traffic (approximately 100 simultaneous users). The application is connected to GitHub for continuous deployment, allowing for easy updates and maintenance.

## Deployment Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  User Browser   │────▶│  Render Server  │────▶│  Spotify API    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │
                              │
                              ▼
                        ┌─────────────────┐
                        │                 │
                        │   AudD API      │
                        │                 │
                        └─────────────────┘
```

## Components

1. **Web Application**: Flask-based Python application hosted on Render
2. **Database**: File-based session storage on Render's persistent disk
3. **External APIs**: 
   - Spotify API for music search and playlist management
   - AudD API for audio recognition and humming matching
4. **Source Control**: GitHub repository for code storage and continuous deployment

## Environment Configuration

The application uses environment variables for configuration to keep sensitive information secure:

- `SPOTIPY_CLIENT_ID`: Spotify API client ID
- `SPOTIPY_CLIENT_SECRET`: Spotify API client secret
- `SPOTIPY_REDIRECT_URI`: Callback URL for Spotify authentication
- `AUDD_API_KEY`: API key for AudD music recognition service
- `SECRET_KEY`: Secret key for Flask session encryption
- `FLASK_ENV`: Set to "production" for the deployed environment

## Deployment Process

The application was deployed using the following process:

1. **Preparation**:
   - Modified the application code to use environment variables
   - Created a requirements.txt file for dependencies
   - Added a Procfile for process management
   - Created a render.yaml file for Render configuration
   - Added setup scripts for production environment

2. **GitHub Setup**:
   - Created a repository on GitHub under the user's account (Mia-Ping)
   - Pushed the application code to the repository

3. **Render Configuration**:
   - Created a new web service on Render
   - Connected to the GitHub repository
   - Configured environment variables
   - Set up persistent disk storage
   - Configured build and start commands

4. **Spotify Developer Dashboard**:
   - Updated the redirect URI in the Spotify Developer Dashboard to match the Render URL

5. **Deployment**:
   - Triggered the initial deployment on Render
   - Verified the application was running correctly
   - Ran automated and manual tests to ensure functionality

## File Structure

```
spotify-search-bot/
├── app.py                 # Main application file
├── audio_processor.py     # Audio processing module
├── requirements.txt       # Python dependencies
├── Procfile               # Process configuration for web servers
├── render.yaml            # Render configuration
├── setup_production.py    # Production environment setup script
├── start.sh               # Startup script
├── static/                # Static assets (CSS, JS)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── templates/             # HTML templates
    ├── index.html
    └── login.html
```

## Maintenance Procedures

### Updating the Application

1. Make changes to the code in the GitHub repository
2. Commit and push the changes
3. Render will automatically detect the changes and redeploy the application

### Monitoring

1. Use the Render dashboard to monitor application performance
2. Check logs for errors or issues
3. Set up notifications for service status changes (available in paid plans)

### Backup Procedures

1. The code is backed up in the GitHub repository
2. User data is stored in Spotify, not in the application
3. Session data is stored on Render's persistent disk but is not critical

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Verify that the Spotify redirect URI is correctly set in both Render environment variables and the Spotify Developer Dashboard
   - Check that the Spotify API credentials are correct

2. **Audio Processing Errors**:
   - Verify that the AudD API key is correctly set
   - Check that the audio processing dependencies are installed

3. **Performance Issues**:
   - Monitor CPU and memory usage in the Render dashboard
   - Consider upgrading to a paid plan if the free tier is insufficient

### Accessing Logs

1. In the Render dashboard, select the web service
2. Click on "Logs" to view application logs
3. Use the filter options to find specific types of logs

## Security Considerations

1. **API Keys and Secrets**:
   - Stored as environment variables, not in the code
   - Not exposed to client-side code

2. **User Data**:
   - Authentication handled by Spotify OAuth
   - No user passwords stored in the application
   - Session data encrypted with SECRET_KEY

3. **HTTPS**:
   - Render provides HTTPS by default
   - All communication is encrypted

## Scaling Considerations

The free tier of Render has limitations that may affect the application as it grows:

1. **Resource Limits**:
   - Limited CPU and memory
   - May slow down with heavy usage

2. **Scaling Options**:
   - Upgrade to a paid plan for more resources
   - Consider horizontal scaling for very high traffic

## Cost Analysis

Current deployment costs:

- Render Free Tier: $0/month
- Spotify API: Free
- AudD API: Varies based on usage (free tier available)

Potential future costs:

- Render Standard Tier: $7/month (if more resources needed)
- Additional disk storage: $0.10/GB/month
- AudD API paid plan: Varies based on usage

## Conclusion

The Spotify Music Search Bot has been successfully deployed as a permanent website on Render, with continuous deployment from GitHub. The application is configured for production use with proper security measures and can handle approximately 100 simultaneous users on the free tier.
