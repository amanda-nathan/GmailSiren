#!/usr/bin/env python3
import os
import pickle
import time
import subprocess
import sys
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CHECK_INTERVAL = 1800

def get_gmail_service():
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def check_for_new_emails(service, start_timestamp, domain):
    try:
        query = f'from:*@{domain} after:{start_timestamp}'
        
        response = service.users().messages().list(userId='me', q=query).execute()
        messages = response.get('messages', [])

        if not messages:
            return False, []
        
        senders = []
        for message in messages:
            msg = service.users().messages().get(
                userId='me', 
                id=message['id'], 
                format='metadata', 
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()
            
            headers = msg['payload']['headers']
            sender = subject = email_date = ''
            
            for header in headers:
                if header['name'] == 'From':
                    sender = header['value']
                elif header['name'] == 'Subject':
                    subject = header['value']
                elif header['name'] == 'Date':
                    email_date = header['value']
            
            senders.append({
                'from': sender, 
                'subject': subject,
                'date': email_date
            })
        
        return True, senders

    except Exception as e:
        print(f"Error checking emails: {e}")
        return False, []

def play_alarm():
    print("\n" + "="*70)
    print("🚨 NEW EMAIL DETECTED! 🚨")
    print("="*70)
    
    subprocess.run(['say', 'Alert! You have new email'], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print("\n⏰ ALARM IS PLAYING!")
    print("\nOptions:")
    print("  - Press ENTER to stop alarm and continue monitoring")
    print("  - Press Ctrl+C to stop alarm and quit program\n")
    
    sound_file = "/System/Library/Sounds/Sosumi.aiff"
    alarm_process = None
    
    try:
        alarm_process = subprocess.Popen(
            ['sh', '-c', f'while true; do afplay "{sound_file}"; sleep 0.5; done'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        input()
        
    except KeyboardInterrupt:
        print("\n\n👋 Stopping program. Goodbye!")
        if alarm_process:
            alarm_process.terminate()
        sys.exit(0)
    finally:
        if alarm_process:
            alarm_process.terminate()
            time.sleep(0.5)

def main():
    print("="*70)
    print("📧 Gmail Email Alert Monitor")
    print("="*70)
    
    domain = input("\nEnter the email domain to monitor (e.g., icloud.com, gmail.com): ").strip()
    
    if not domain:
        print("❌ No domain entered. Exiting.")
        return
    
    print(f"\n✓ Monitoring emails from: @{domain}")
    print(f"✓ Checking every {CHECK_INTERVAL // 60} minutes for NEW emails")
    print("✓ Will only alert on emails received AFTER program starts")
    print("✓ Press Ctrl+C anytime to quit\n")
    
    print("Authenticating with Gmail...")
    service = get_gmail_service()
    
    if not service:
        print("❌ Could not connect to Gmail. Exiting.")
        return
    
    print("✓ Successfully connected to Gmail!\n")
    
    start_timestamp = int(time.time())
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"📅 Program started at: {start_time}")
    print(f"✓ Will only alert on emails received after this time\n")
    
    while True:
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Checking for new emails from @{domain}...")
            
            has_emails, senders = check_for_new_emails(service, start_timestamp, domain)
            
            if has_emails:
                print(f"\n✉️  Found {len(senders)} NEW email(s) from @{domain}:\n")
                
                for i, email_info in enumerate(senders, 1):
                    print(f"  {i}. From: {email_info['from']}")
                    print(f"     Subject: {email_info['subject'][:60]}{'...' if len(email_info['subject']) > 60 else ''}")
                    print(f"     Received: {email_info['date']}")
                    print()
                
                play_alarm()
                
                print("✅ Alarm stopped. Continuing to monitor...\n")
            else:
                print(f"   ✓ No new emails from @{domain}\n")
            
            print(f"   Next check in {CHECK_INTERVAL // 60} minutes...\n")
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n\n👋 Stopping Gmail checker. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("   Retrying in 1 minute...\n")
            time.sleep(60)

if __name__ == '__main__':
    main()