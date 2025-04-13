import tarfile
import os

def create_archive():
    # Create a tar.gz archive
    with tarfile.open("dogtea_bot_project.tar.gz", "w:gz") as tar:
        # Add all important directories and files
        directories = [
            "games",
            "handlers",
            "locales",
            "static",
            "templates",
            "utils"
        ]
        
        files = [
            "app.py",
            "bot.py",
            "config.py",
            "main.py",
            "models.py",
            "simple_bot.py",
            "standalone_bot.py",
            "create_archive.py"
        ]
        
        # Add directories
        for directory in directories:
            if os.path.exists(directory):
                tar.add(directory)
                print(f"Added directory: {directory}")
        
        # Add individual files
        for file in files:
            if os.path.exists(file):
                tar.add(file)
                print(f"Added file: {file}")
    
    print(f"Archive created: dogtea_bot_project.tar.gz")

if __name__ == "__main__":
    create_archive()