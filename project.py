from datetime import datetime
from utils import load_data, save_data

class Project:
    projects_file = "projects.json"

    def __init__(self, title, details, target, start_date, end_date, owner_email):
        self.title = title
        self.details = details
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.owner_email = owner_email

    @staticmethod
    def validate_date_format(date_str):
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_end_after_start(start_date, end_date):
        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")
        return end > start

    @classmethod
    def create_project(cls, user_email):
        print("\n=== Create New Project ===")
        title = input("Project Title: ")
        details = input("Project Details: ")
        target_input = input("Total Target Amount (EGP): ")
        if not target_input.isdigit():
            print("Target amount must be a number.")
            return

        target = int(target_input)
        start_date = input("Start Date (dd-mm-yyyy): ")
        if not cls.validate_date_format(start_date):
            print("Invalid date format.")
            return

        end_date = input("End Date (dd-mm-yyyy): ")
        if not cls.validate_date_format(end_date):
            print("Invalid date format.")
            return

        if not cls.is_end_after_start(start_date, end_date):
            print("End date must be after start date.")
            return

        project = cls(title, details, target, start_date, end_date, user_email)
        projects = load_data(cls.projects_file)
        projects.append(project.__dict__)
        save_data(cls.projects_file, projects)
        print("Project created successfully!")

    @classmethod
    def view_all_projects(cls):
        print("\n=== All Projects ===")
        projects = load_data(cls.projects_file)
        if not projects:
            print("No projects found.")
            return
        for idx, project in enumerate(projects, 1):
            print(f"\nProject #{idx}")
            print(f"Title: {project['title']}")
            print(f"Details: {project['details']}")
            print(f"Target: {project['target']} EGP")
            print(f"Start Date: {project['start_date']}")
            print(f"End Date: {project['end_date']}")
            print(f"Owner: {project['owner_email']}")

    @classmethod
    def edit_project(cls, user_email):
        projects = load_data(cls.projects_file)
        user_projects = [
            proj for proj in projects if proj["owner_email"] == user_email
        ]

        if not user_projects:
            print("You have no projects to edit.")
            return

        print("\n=== Your Projects ===")
        for idx, project in enumerate(user_projects, 1):
            print(f"{idx}. {project['title']}")

        choice = input("Select project number to edit: ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(user_projects):
            print("Invalid choice.")
            return

        index = int(choice) - 1
        selected_project = user_projects[index]

        print("Leave field blank to keep current value.")

        new_title = input(f"New Title [{selected_project['title']}]: ") or selected_project["title"]
        new_details = input(f"New Details [{selected_project['details']}]: ") or selected_project["details"]
        new_target_input = input(f"New Target [{selected_project['target']}]: ")
        if new_target_input:
            if not new_target_input.isdigit():
                print("Target must be a number.")
                return
            new_target = int(new_target_input)
        else:
            new_target = selected_project["target"]

        new_start_date = input(f"New Start Date [{selected_project['start_date']}]: ") or selected_project["start_date"]
        if not cls.validate_date_format(new_start_date):
            print("Invalid date format.")
            return

        new_end_date = input(f"New End Date [{selected_project['end_date']}]: ") or selected_project["end_date"]
        if not cls.validate_date_format(new_end_date):
            print("Invalid date format.")
            return

        if not cls.is_end_after_start(new_start_date, new_end_date):
            print("End date must be after start date.")
            return

        for proj in projects:
            if proj == selected_project:
                proj["title"] = new_title
                proj["details"] = new_details
                proj["target"] = new_target
                proj["start_date"] = new_start_date
                proj["end_date"] = new_end_date
                break

        save_data(cls.projects_file, projects)
        print("Project updated successfully.")

    @classmethod
    def delete_project(cls, user_email):
        projects = load_data(cls.projects_file)
        user_projects = [
            proj for proj in projects if proj["owner_email"] == user_email
        ]

        if not user_projects:
            print("You have no projects to delete.")
            return

        print("\n=== Your Projects ===")
        for idx, project in enumerate(user_projects, 1):
            print(f"{idx}. {project['title']}")

        choice = input("Select project number to delete: ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(user_projects):
            print("Invalid choice.")
            return

        index = int(choice) - 1
        selected_project = user_projects[index]

        projects = [proj for proj in projects if proj != selected_project]
        save_data(cls.projects_file, projects)
        print("Project deleted successfully.")

    @classmethod
    def search_by_date(cls):
        projects = load_data(cls.projects_file)
        if not projects:
            print("No projects found.")
            return

        date = input("Enter date to search (dd-mm-yyyy): ")
        if not cls.validate_date_format(date):
            print("Invalid date format.")
            return

        found = False
        for project in projects:
            if project["start_date"] == date or project["end_date"] == date:
                found = True
                print("\nProject Found:")
                print(f"Title: {project['title']}")
                print(f"Details: {project['details']}")
                print(f"Target: {project['target']} EGP")
                print(f"Start Date: {project['start_date']}")
                print(f"End Date: {project['end_date']}")
                print(f"Owner: {project['owner_email']}")
        if not found:
            print("No projects found for that date.")
