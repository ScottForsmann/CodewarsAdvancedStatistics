from methods import *

Page = PageData()


def Menu():
    menu = True
    while menu:
        print("""
Please select an option:

        1. Overall Stats
        2. Specific Language Stats
        3. All Stats
        4. Kyu until Overall Level up 
        5. Kyu until Specific Level up  
        
        6. Set a Default Username
        
or type exit
        """)
        ans = input("Option: ")
        print()

        if ans == "1":
            # Prints Overall stats
            Page.printOverallStats()
            print()
            waitTillContinue()

        elif ans == "2":
            # Prints specific language stats
            Page.promptLanguages()
            waitTillContinue()

        elif ans == "3":
            # Prints all stats
            Page.printOverallStats()
            print()
            Page.printAllLanguageStats()
            waitTillContinue()

        if ans == "4":
            # Overall EXP to level up
            Page.overallEXPLevel()
            print()
            waitTillContinue()

        if ans == "5":
            # Specific EXP to level up
            Page.specificEXPLevel()
            waitTillContinue()

        if ans == "6":
            # Set Default Username
            setDefaultUsername()
            waitTillContinue()

        elif ans.lower() == "exit":
            # Exits
            print("\nGoodbye")
            menu = None

        else:
            pass
