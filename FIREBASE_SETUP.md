
# Firebase Setup Guide for Snowbird App

## 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project named "snowbird-financial"
3. Enable Google Analytics (optional)

## 2. Enable Authentication

1. In Firebase Console, go to **Authentication** > **Sign-in method**
2. Enable **Email/Password** authentication
3. (Optional) Enable **Google** sign-in for easier login

## 3. Create Firestore Database

1. Go to **Firestore Database** in Firebase Console
2. Click **Create database**
3. Choose **Start in test mode** (we'll secure it later)
4. Select your preferred location

## 4. Get Configuration Keys

### Service Account (for Admin SDK)
1. Go to **Project Settings** > **Service accounts**
2. Click **Generate new private key**
3. Download the JSON file
4. Copy the entire JSON content

### Web App Config (for Client SDK)
1. Go to **Project Settings** > **General**
2. In "Your apps" section, click **Web app** icon
3. Register your app with name "snowbird-web"
4. Copy the `firebaseConfig` object

## 5. Add to Replit Secrets

In Replit, go to **Tools** > **Secrets** and add:

1. **FIREBASE_SERVICE_ACCOUNT**
   ```json
   {"type": "service_account", "project_id": "your-project-id", ...}
   ```

2. **FIREBASE_CONFIG**
   ```json
   {"apiKey": "...", "authDomain": "...", "projectId": "...", ...}
   ```

## 6. Security Rules (Optional)

Update Firestore rules for better security:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only access their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Activities can only be created by authenticated users
    match /activities/{document} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.uid;
    }
  }
}
```

## 7. Test the Setup

1. Run the Snowbird app
2. Try to register a new account
3. Log in and test data synchronization
4. Open the app in another browser/device to test real-time sync

## Troubleshooting

- **Import Error**: Make sure all Firebase packages are installed
- **Auth Error**: Check if your Firebase config is correct
- **Permission Denied**: Update Firestore security rules
- **Sync Issues**: Check browser console for errors

That's it! Your Snowbird app now has full Firebase authentication and real-time sync capabilities.
