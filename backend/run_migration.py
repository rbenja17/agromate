"""Script to run database migrations on Supabase."""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import logging
from database import get_supabase_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def run_migration():
    """Execute the database migration SQL."""
    print("\n" + "="*80)
    print("🗄️  AGROMATE - Running Database Migration")
    print("="*80 + "\n")
    
    # Read migration SQL
    migration_file = Path(__file__).parent.parent / "supabase" / "migrations" / "001_create_news_table.sql"
    
    print(f"📄 Reading migration file: {migration_file.name}\n")
    
    try:
        with open(migration_file, 'r', encoding='utf-8') as f:
            sql = f.read()
        
        print(f"✅ Migration SQL loaded ({len(sql)} characters)\n")
        
    except FileNotFoundError:
        print(f"❌ Migration file not found: {migration_file}\n")
        return
    
    print("-" * 80 + "\n")
    
    # Connect to Supabase
    print("📡 Connecting to Supabase...\n")
    
    try:
        client = get_supabase_client(use_service_key=True)
        print(f"✅ Connected to: {client.supabase_url}\n")
    except Exception as e:
        print(f"❌ Failed to connect: {e}\n")
        return
    
    print("-" * 80 + "\n")
    
    # Execute migration
    print("🚀 Executing migration...\n")
    
    try:
        # Execute the SQL using Supabase RPC
        response = client.rpc('exec_sql', {'sql_query': sql}).execute()
        
        print("✅ Migration executed successfully!\n")
        
    except Exception as e:
        # If RPC doesn't work, provide manual instructions
        print("⚠️  Automatic migration failed. Please run manually:\n")
        print("="*80)
        print("\nOPTION 1: Supabase Dashboard")
        print("-" * 80)
        print("1. Go to: https://supabase.com/dashboard/project/ctzrzelnfjcrefuqerow/editor/sql")
        print("2. Paste the SQL from: supabase/migrations/001_create_news_table.sql")
        print("3. Click 'Run'\n")
        
        print("OPTION 2: SQL Code")
        print("-" * 80)
        print("\n```sql")
        print(sql)
        print("```\n")
        
        print("="*80)
        print(f"\nError details: {e}\n")
        return
    
    print("="*80)
    print("✅ Database migration completed!")
    print("="*80 + "\n")
    
    print("📋 Next steps:")
    print("   1. Run: python test_database.py")
    print("   2. Verify the 'news' table was created in Supabase\n")


if __name__ == "__main__":
    run_migration()
