#!/usr/bin/env python3
"""
Database Sync Script
Sync data between localhost and cloud databases
"""

import os
import sys
import subprocess
from datetime import datetime

class DatabaseSync:
    def __init__(self):
        self.local_config = {
            'host': '127.0.0.1',
            'port': '3306',
            'user': 'root',
            'password': '',
            'database': 'django_it_help'
        }
        
    def get_cloud_config(self):
        """Get cloud database configuration from user input"""
        print("🔧 Enter your cloud database details:")
        return {
            'host': input("Cloud DB Host: "),
            'user': input("Cloud DB User: "),
            'password': input("Cloud DB Password: "),
            'port': input("Cloud DB Port (3306): ") or "3306",
            'database': input("Cloud DB Name (django_it_help): ") or "django_it_help"
        }
    
    def create_dump(self, config, filename):
        """Create database dump"""
        password_part = f"-p{config['password']}" if config['password'] else ""
        
        dump_command = (
            f'mysqldump -h {config["host"]} '
            f'-u {config["user"]} '
            f'{password_part} '
            f'-P {config["port"]} '
            f'{config["database"]} > {filename}'
        )
        
        try:
            subprocess.run(dump_command, shell=True, check=True)
            print(f"✅ Dump created: {filename}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Dump failed: {e}")
            return False
    
    def restore_dump(self, config, filename):
        """Restore database from dump"""
        password_part = f"-p{config['password']}" if config['password'] else ""
        
        restore_command = (
            f'mysql -h {config["host"]} '
            f'-u {config["user"]} '
            f'{password_part} '
            f'-P {config["port"]} '
            f'{config["database"]} < {filename}'
        )
        
        try:
            subprocess.run(restore_command, shell=True, check=True)
            print(f"✅ Restore completed from: {filename}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Restore failed: {e}")
            return False
    
    def sync_local_to_cloud(self):
        """Sync local database to cloud"""
        print("📤 Syncing LOCAL → CLOUD")
        
        cloud_config = self.get_cloud_config()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_file = f"local_to_cloud_{timestamp}.sql"
        
        if self.create_dump(self.local_config, dump_file):
            if self.restore_dump(cloud_config, dump_file):
                print("🎉 Local data synced to cloud successfully!")
                return True
        return False
    
    def sync_cloud_to_local(self):
        """Sync cloud database to local"""
        print("📥 Syncing CLOUD → LOCAL")
        
        cloud_config = self.get_cloud_config()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_file = f"cloud_to_local_{timestamp}.sql"
        
        if self.create_dump(cloud_config, dump_file):
            if self.restore_dump(self.local_config, dump_file):
                print("🎉 Cloud data synced to local successfully!")
                return True
        return False
    
    def backup_both(self):
        """Create backups of both databases"""
        print("💾 Creating backups of both databases")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Backup local
        local_backup = f"local_backup_{timestamp}.sql"
        if self.create_dump(self.local_config, local_backup):
            print(f"✅ Local backup: {local_backup}")
        
        # Backup cloud
        cloud_config = self.get_cloud_config()
        cloud_backup = f"cloud_backup_{timestamp}.sql"
        if self.create_dump(cloud_config, cloud_backup):
            print(f"✅ Cloud backup: {cloud_backup}")
        
        print("💾 Backups completed!")

def main():
    """Main sync function"""
    sync = DatabaseSync()
    
    print("🔄 Django IT Helpdesk Database Sync Tool")
    print("=" * 45)
    
    while True:
        print("\nChoose an option:")
        print("1. 📤 Sync Local → Cloud (Upload your local data)")
        print("2. 📥 Sync Cloud → Local (Download cloud data)")
        print("3. 💾 Backup Both Databases")
        print("4. ❌ Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            sync.sync_local_to_cloud()
        elif choice == '2':
            sync.sync_cloud_to_local()
        elif choice == '3':
            sync.backup_both()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
