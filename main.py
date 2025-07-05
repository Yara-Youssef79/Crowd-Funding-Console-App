from user import User
from project import Project

def main():
    current_user = None

    while True:
        if not current_user:
            print("\n=== Main Menu ===")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Choose option: ")

            if choice == "1":
                User.register()
            elif choice == "2":
                user = User.login()
                if user:
                    current_user = user
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        else:
            print(f"\n=== User Menu (Logged in as {current_user.email}) ===")
            print("1. Create New Project")
            print("2. View All Projects")
            print("3. Edit My Projects")
            print("4. Delete My Projects")
            print("5. Search Projects By Date")
            print("6. Logout")

            choice = input("Choose option: ")

            if choice == "1":
                Project.create_project(current_user.email)
            elif choice == "2":
                Project.view_all_projects()
            elif choice == "3":
                Project.edit_project(current_user.email)
            elif choice == "4":
                Project.delete_project(current_user.email)
            elif choice == "5":
                Project.search_by_date()
            elif choice == "6":
                current_user = None
                print("Logged out successfully.")
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()
