"""
Custom MySQL backend to bypass MariaDB version check for Django.
This allows Django to work with MariaDB 10.4.32 by skipping the version validation.
"""

from django.db.backends.mysql import base


class DatabaseWrapper(base.DatabaseWrapper):
    """
    Custom MySQL database wrapper that bypasses MariaDB version checks.
    """
    
    def check_database_version_supported(self):
        """
        Override the version check to allow MariaDB 10.4.32.
        This bypasses Django's requirement for MariaDB 10.5+.
        """
        # Skip the version check entirely
        pass
    
    def init_connection_state(self):
        """
        Initialize connection state with custom settings for MariaDB 10.4.32.
        """
        assignments = []
        
        # Set SQL mode for compatibility
        assignments.append("sql_mode = 'STRICT_TRANS_TABLES'")
        
        # Set character set
        assignments.append("character_set_connection = 'utf8mb4'")
        assignments.append("collation_connection = 'utf8mb4_unicode_ci'")
        
        if assignments:
            with self.cursor() as cursor:
                cursor.execute('SET ' + ', '.join(assignments))
