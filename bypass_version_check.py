"""
Comprehensive MariaDB 10.4.32 compatibility patch for Django.
This patches Django's MySQL backend to work with older MariaDB versions.
"""

import django.db.backends.mysql.base as mysql_base
import django.db.backends.mysql.features as mysql_features

# Store the original methods
original_check_database_version_supported = mysql_base.DatabaseWrapper.check_database_version_supported

def patched_check_database_version_supported(self):
    """
    Bypass the MariaDB version check to allow MariaDB 10.4.32.
    """
    # Skip the version check entirely
    pass

# Patch database features for MariaDB 10.4.32 compatibility
def patch_database_features():
    """
    Disable features not supported by MariaDB 10.4.32
    """
    # Disable RETURNING clause support for MariaDB 10.4.32
    mysql_features.DatabaseFeatures.can_return_columns_from_insert = False
    mysql_features.DatabaseFeatures.can_return_rows_from_bulk_insert = False
    mysql_features.DatabaseFeatures.supports_over_clause = False
    mysql_features.DatabaseFeatures.supports_frame_range_fixed_distance = False
    
# Apply the patches
mysql_base.DatabaseWrapper.check_database_version_supported = patched_check_database_version_supported
patch_database_features()

print("MariaDB version check bypassed successfully!")
print("MariaDB 10.4.32 compatibility features disabled.")
