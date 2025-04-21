# Manual Testing Checklist for Deployed Spotify Music Search Bot

Use this checklist to manually verify all functionality of the deployed application.

## Authentication Testing

- [ ] Homepage loads correctly and displays login button
- [ ] Clicking "Login with Spotify" redirects to Spotify authentication page
- [ ] After authentication, user is redirected back to the application
- [ ] User information and playlists are displayed correctly
- [ ] Logout button works and clears the session

## Text-based Search Testing

- [ ] Search form accepts input
- [ ] Searching for descriptive terms (e.g., "delighted female vocal") returns relevant results
- [ ] Results are displayed correctly with track name, artist, and album art
- [ ] Play button opens the track in Spotify
- [ ] Add button adds the track to Liked Songs

## Audio Recognition Testing

- [ ] Audio recording interface loads correctly
- [ ] Microphone access is requested when clicking "Start Recording"
- [ ] Recording timer works correctly
- [ ] Stopping recording processes the audio and returns results
- [ ] File upload interface works correctly
- [ ] Uploading an audio file processes the audio and returns results

## Humming Search Testing

- [ ] Humming interface loads correctly
- [ ] Microphone access is requested when clicking "Start Humming"
- [ ] Recording timer works correctly
- [ ] Stopping humming processes the audio and attempts to match songs
- [ ] Results are displayed correctly

## Playlist Management Testing

- [ ] User's playlists are displayed correctly
- [ ] Clicking on a playlist loads its tracks
- [ ] Tracks are displayed correctly with track name, artist, and album art

## Performance Testing

- [ ] Application loads within a reasonable time (< 5 seconds)
- [ ] Search results are returned within a reasonable time (< 5 seconds)
- [ ] Audio processing completes within a reasonable time (< 10 seconds)
- [ ] Application remains responsive with multiple users (if possible to test)

## Security Testing

- [ ] Unauthenticated users cannot access protected endpoints
- [ ] Session persists correctly between page refreshes
- [ ] Session expires after logout
- [ ] API keys and secrets are not exposed in client-side code

## Cross-browser Testing

- [ ] Application works correctly in Chrome
- [ ] Application works correctly in Firefox
- [ ] Application works correctly in Safari
- [ ] Application works correctly in Edge

## Mobile Testing

- [ ] Application displays correctly on mobile devices
- [ ] All functionality works on mobile devices
- [ ] Audio recording works on mobile devices

## Error Handling Testing

- [ ] Application handles invalid search queries gracefully
- [ ] Application handles audio recording errors gracefully
- [ ] Application handles authentication errors gracefully
- [ ] Error messages are clear and helpful

## Notes

- Record any issues or observations here
- Note any performance concerns
- Document any browser-specific issues
- Record any mobile-specific issues

## Test Results

- Date of testing: ________________
- Tester: ________________
- Overall result: ________________
- Action items: ________________
