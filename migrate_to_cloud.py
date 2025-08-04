#!/usr/bin/env python3
"""
Database Migration Script
Migrate data from localhost MySQL to cloud MySQL database
"""

import os
import sys
import subprocess
from datetime import datetime

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def backup_local_database():
    """Create backup of local database"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"django_it_help_backup_{timestamp}.sql"
    
    print("📦 Creating backup of local database...")
    
    # XAMPP MySQL dump command
    dump_command = f'mysqldump -u root -p --host=127.0.0.1 --port=3306 django_it_help > {backup_file}'
    
    if run_command(dump_command, f"Creating backup: {backup_file}"):
        print(f"✅ Backup created: {backup_file}")
        return backup_file
    else:
        print("❌ Failed to create backup")
        return None

def restore_to_cloud(backup_file, cloud_config):
    """Restore backup to cloud database"""
    print("☁️ Restoring to cloud database...")
    
    restore_command = (
        f'mysql -h {cloud_config["host"]} '
        f'-u {cloud_config["user"]} '
        f'-p{cloud_config["password"]} '
        f'-P {cloud_config["port"]} '
        f'{cloud_config["database"]} < {backup_file}'
    )
    
    if run_command(restore_command, "Restoring to cloud database"):
        print("✅ Data successfully migrated to cloud database")
        return True
    else:
        print("❌ Failed to restore to cloud database")
        return False

def main():
    """Main migration function"""
    print("🚀 Django IT Helpdesk Database Migration Tool")
    print("=" * 50)
    
    print("\n📋 This script will help you migrate your local database to the cloud")
    print("Make sure you have:")
    print("1. ✅ XAMPP MySQL running with your data")
    print("2. ✅ Cloud MySQL database created and accessible")
    print("3. ✅ Cloud database credentials ready")
    
    # Get cloud database configuration
    print("\n🔧 Enter your cloud database details:")
    cloud_config = {
        'host': input("Database Host: "),
        'user': input("Database User: "),
        'password': input("Database Password: "),
        'port': input("Database Port (default 3306): ") or "3306",
        'database': input("Database Name: ") or "django_it_help"
    }
    
    # Create backup
    backup_file = backup_local_database()
    if not backup_file:
        sys.exit(1)
    
    # Restore to cloud
    if restore_to_cloud(backup_file, cloud_config):
        print("\n🎉 Migration completed successfully!")
        print(f"\n📝 Update your .env.vercel with these settings:")
        print(f"DB_HOST={cloud_config['host']}")
        print(f"DB_USER={cloud_config['user']}")
        print(f"DB_PASSWORD={cloud_config['password']}")
        print(f"DB_PORT={cloud_config['port']}")
        print(f"DB_NAME={cloud_config['database']}")
        
        print(f"\n💾 Local backup saved as: {backup_file}")
        print("Keep this backup file safe for future reference!")
    else:
        print("\n❌ Migration failed. Please check your cloud database settings.")

if __name__ == '__main__':
    main()
