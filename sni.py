from auth.database_manager import DatabaseManager

db = DatabaseManager()

success = db.update_user_role(
    "finance_user",
    "finance_employee"
)

print("Updated:", success)