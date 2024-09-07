'''
File: H45H-VeriFinder-v3.8.py
Author: Ocean-PI (Sagar Mondal)
Date: 07-09-2024
Description: H45H Verifinder is a versatile tool for file integrity verification.
'''
import hashlib
import subprocess
import sys
import os

# Function to check if 'rich' is installed, if not ask to install
def check_rich():
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.prompt import Prompt
        from rich.text import Text
        return True, Console, Table, Panel, Prompt, Text
    except ImportError:
        return False, None, None, None, None, None

# Function to install rich if the user agrees
def install_rich():
    install = input("The 'rich' module is not installed. Would you like to install it now? (y/n): ").strip().lower()
    if install == 'y':
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
            print("Rich has been installed successfully. Please re-run the program.")
            sys.exit()  # Exit so the user can restart the program with 'rich' installed
        except Exception as e:
            print(f"Failed to install 'rich'. Error: {e}")
            print("Running program in basic mode...")
            return False
    else:
        print("Running program in basic mode without 'rich'...")
        return False

# Function to calculate the hash for a file using different algorithms
def calculate_hash(file_path, hash_type):
    hash_func = hashlib.new(hash_type)
    
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):  # Read the file in chunks of 8192 bytes
                hash_func.update(chunk)
    except PermissionError:
        print(f"Permission denied: {file_path}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

    return hash_func.hexdigest()

# Function to check all hash types and verify the file
def verify_file(file_path, provided_hash, use_rich, Console=None):
    hash_types = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']
    computed_hashes = {}
    provided_hash_type = None

    for hash_type in hash_types:
        computed_hash = calculate_hash(file_path, hash_type)
        computed_hashes[hash_type] = computed_hash
        if computed_hash == provided_hash:
            provided_hash_type = hash_type
            return True, provided_hash_type, computed_hash, computed_hashes

    # If no match found, determine the provided hash type from the computed hashes
    if provided_hash_type is None:
        for hash_type, hash_value in computed_hashes.items():
            if hash_value == provided_hash:
                provided_hash_type = hash_type
                break

    # Check provided hash type against known hash types
    if provided_hash_type is None:
        for hash_type in hash_types:
            test_hash = hashlib.new(hash_type)
            test_hash.update(provided_hash.encode())
            if len(test_hash.hexdigest()) == len(provided_hash):
                provided_hash_type = hash_type
                break

    # Set provided_hash_type to "Unknown" if not determined
    if provided_hash_type is None:
        provided_hash_type = "Unknown"

    return False, provided_hash_type, None, computed_hashes

# Main program
if __name__ == "__main__":
    use_rich, Console, Table, Panel, Prompt, Text = check_rich()

    if not use_rich:
        # Try installing 'rich' if the user wants
        if not install_rich():
            use_rich = False  # Proceed with basic mode if installation failed or declined

    author_name = "Dev: Ocean-PI"  # Author name

    if use_rich:
        console = Console()

        # Define the main content and the author's name
        main_content = Text("Welcome to the H45H VeriFinder Progname!!", style="bold blue")
        author_text = Text(author_name, style="bold blue")

        # Print the welcome message
        console.print(
            Panel(
                main_content + Text(" " * (console.width - len(str(main_content)) - len(str(author_text)) - 4)) + author_text,
                title="H45H VeriFinder",
                subtitle="v3.8",
                style="bold cyan",
                width=console.width
            )
        )

        # Prompt for file path and check if it's empty
        file_path = os.path.normpath(Prompt.ask("[bold yellow]Enter the file path[/bold yellow]")).strip()
        if not file_path:
            print("No file path provided. Exiting...")
            sys.exit()

        # Check if the file exists
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            sys.exit()

        provided_hash = Prompt.ask("[bold yellow]Enter the hash value to verify or (Leave empty)[/bold yellow]").strip()

        if provided_hash:
            console.print(Panel(f"Verifying [bold magenta]{file_path}[/bold magenta] with the provided hash...", style="bold blue", border_style="bright_blue"))

            is_valid, provided_hash_type, matched_hash_value, computed_hashes = verify_file(file_path, provided_hash, use_rich, Console)

            if is_valid:
                # Create a table to display the provided hash
                provided_hash_table = Table()
                provided_hash_table.add_column("Hash Type", justify="center")
                provided_hash_table.add_column("Provided Hash Value", justify="center")
                provided_hash_table.add_row(provided_hash_type, provided_hash)

                # Create a table to display the actual file hash
                actual_hash_table = Table()
                actual_hash_table.add_column("Hash Type", justify="center")
                actual_hash_table.add_column("Actual File Hash Value", justify="center")
                actual_hash_table.add_row(provided_hash_type, matched_hash_value)

                # Print the tables with a small space before the provided hash table
                console.print("")  # Add a small space before printing the table
                console.print(provided_hash_table)
                console.print("")  # Add a blank line between tables
                console.print(actual_hash_table)
                
                # Add success message
                console.print(Panel("[bold green]✅ Verification Successful! The file hash matches.[/bold green]", style="green", border_style="bold green"))
            else:
                # Create tables to display provided hash and computed hashes
                provided_hash_table = Table()
                provided_hash_table.add_column("Hash Type", justify="center")
                provided_hash_table.add_column("Provided Hash Value", justify="center")
                provided_hash_table.add_row(provided_hash_type, provided_hash)

                comparison_table = Table()
                comparison_table.add_column("Hash Type", justify="center")
                comparison_table.add_column("Actual File Hash Values", justify="center")
                for hash_type, hash_value in computed_hashes.items():
                    comparison_table.add_row(hash_type, hash_value)

                # Print the tables with a small space before the provided hash table
                console.print("")  # Add a small space before printing the panel
                console.print(Panel("[bold red]❌ Verification Failed! No matching hash found.[/bold red]", title="Verification Failed", style="bold red"), justify="center")
                console.print("")  # Add a small space before printing the table
                console.print(provided_hash_table)
                console.print("")  # Add a blank line between tables
                console.print(comparison_table)

            # Add a pause before the program exits
            console.print("\n[bold cyan]Press Enter to exit...[/bold cyan]")
            console.input()  # Waits for the user to press Enter
        else:
            # If no hash value is provided, just show the file hash values
            computed_hashes = {}
            for hash_type in ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']:
                computed_hashes[hash_type] = calculate_hash(file_path, hash_type)
            
            # Create a table to display the computed hashes
            hash_table = Table()
            hash_table.add_column("Hash Type", justify="center")
            hash_table.add_column("Computed Hash Value", justify="center")
            for hash_type, hash_value in computed_hashes.items():
                hash_table.add_row(hash_type, hash_value)

            # Print the table
            console.print("")  # Add a small space before printing the table
            console.print(hash_table)

            # Add a pause before the program exits
            console.print("\n[bold cyan]Press Enter to exit...[/bold cyan]")
            console.input()  # Waits for the user to press Enter
    else:
        # Basic mode without 'rich'
        print("\nWelcome to the H45H VeriFinder Progname!!")
        print(author_name)  # Print the author's name in basic mode

        # Prompt for file path and check if it's empty
        file_path = os.path.normpath(input("Enter the file path: ")).strip()
        if not file_path:
            print("No file path provided. Exiting...")
            sys.exit()

        # Check if the file exists
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            sys.exit()

        provided_hash = input("Enter the hash value to verify or (Leave empty): ").strip()

        if provided_hash:
            is_valid, provided_hash_type, matched_hash_value, computed_hashes = verify_file(file_path, provided_hash, use_rich)

            if is_valid:
                print(f"\nFile is real. Hash type: {provided_hash_type}")
                print(f"Provided hash: {provided_hash}")
                print(f"Computed hash: {matched_hash_value}")
                print("✅ Verification Successful! The file hash matches.")
            else:
                print("❌ Verification Failed! No matching hash found.")
                print(f"Provided hash: {provided_hash}")
                print("Computed hashes:")
                for hash_type, hash_value in computed_hashes.items():
                    print(f"{hash_type}: {hash_value}")

            # Add a pause before the program exits
            input("\nPress Enter to exit...")
        else:
            # If no hash value is provided, just show the file hash values
            computed_hashes = {}
            for hash_type in ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']:
                computed_hashes[hash_type] = calculate_hash(file_path, hash_type)
            
            # Display computed hashes
            print("\nComputed Hash Values:")
            for hash_type, hash_value in computed_hashes.items():
                print(f"{hash_type}: {hash_value}")

            # Add a pause before the program exits
            input("\nPress Enter to exit...")
