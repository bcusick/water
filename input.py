import working

def display_menu():
    print("1. 2024")
    print("2. 2023")
    print("3. 2022")
    print("4. Exit")

def get_choice():
    return input("Choose a Year (1-4): ")

def main():
    display_menu()
    while True:
        choice = get_choice()

        if choice == '1':
            working.plot_water(2024)
        elif choice == '2':
            working.plot_water(2023)
        elif choice == '3':
            working.plot_water(2022)
        elif choice == '4':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

        # Pause and wait for user to continue
        #input("Press Enter to continue...")

if __name__ == "__main__":
    main()
