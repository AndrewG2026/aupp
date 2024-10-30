from itertools import permutations
import re


def print_sniper():
    print(
        "          \033[1;31m_________                   _______\033[1;m"
        + 5 * " "
        + "# \033[07mC\033[27mommon"
    )
    print(
        "\033[1;31m_-----____/   ========================|______|\033[1;m"
        + 4 * " "
        + "# \033[07mU\033[27mser"
    )
    print(
        "\033[1;31m|           ______________/\033[1;m"
        + 23 * " "
        + "# \033[07mP\033[27masswords"
    )
    print(
        "\033[1;31m|    ___--_/(_)       ^\033[1;m"
        + 27 * " "
        + "# \033[07mP\033[27mrofiler"
    )
    print("\033[1;31m|___ ---\033[1;m")
    print("This branch was created by the students at Anderson University")
    print(18 * " " + "[ Muris Kurgas | j0rgan@remote-exploit.org ]")
    print(25 * " " + "[ Mebus | https://github.com/Mebus/ ]\r\n")


def create_target_profile():
    """Implementation of the -i switch. Interactively question the user and
    create a password dictionary file based on the answer."""

    print("\r\n[+] Insert the information about the victim to make a dictionary")
    print("[+] If you don't know all the info, just hit enter when asked! ;)\r\n")

    # We need some information first!

    profile = {}

    name = input("> First Name: ").lower()
    while len(name) == 0 or name == " " or name == "  " or name == "   ":
        print("\r\n[-] You must enter a name at least!")
        name = input("> Name: ").lower()
    profile["name"] = str(name)

    profile["surname"] = input("> Surname: ").lower()
    profile["nick"] = input("> Nickname: ").lower()
    birthdate = input("> Birthdate (DDMMYYYY): ")
    while len(birthdate) != 0 and len(birthdate) != 8:
        print("\r\n[-] You must enter 8 digits for birthday!")
        birthdate = input("> Birthdate (DDMMYYYY): ")
    profile["birthdate"] = str(birthdate)

    print("\r\n")

    profile["wife"] = input("> Partners) name: ").lower()
    profile["wifen"] = input("> Partners) nickname: ").lower()
    wifeb = input("> Partners) birthdate (DDMMYYYY): ")
    while len(wifeb) != 0 and len(wifeb) != 8:
        print("\r\n[-] You must enter 8 digits for birthday!")
        wifeb = input("> Partners birthdate (DDMMYYYY): ")
    profile["wifeb"] = str(wifeb)
    print("\r\n")

    profile["kid"] = input("> Child's name: ").lower()
    profile["kidn"] = input("> Child's nickname: ").lower()
    kidb = input("> Child's birthdate (DDMMYYYY): ")
    while len(kidb) != 0 and len(kidb) != 8:
        print("\r\n[-] You must enter 8 digits for birthday!")
        kidb = input("> Child's birthdate (DDMMYYYY): ")
    profile["kidb"] = str(kidb)
    print("\r\n")

    profile["pet"] = input("> Pet's name: ").lower()
    profile["company"] = input("> Company name: ").lower()
    print("\r\n")

    profile["words"] = [""]
    words1 = input(
        "> Do you want to add some key words about the victim? Y/[N]: "
    ).lower()
    words2 = ""
    if words1 == "y":
        words2 = input(
            "> Please enter the words, separated by comma. [i.e. hacker,juice,black], spaces will be removed: "
        ).replace(" ", "")
    profile["words"] = words2.split(",")

    profile["spechars1"] = input(
        "> Do you want to add special chars at the end of words? Y/[N]: "
    ).lower()

    profile["randnum"] = input(
        "> Do you want to add some random numbers at the end of words? Y/[N]:"
    ).lower()
    profile["leetmode"] = input("> Leet mode? (i.e. leet = 1337) Y/[N]: ").lower()


"""
Prints team logo, creates profile, and obtains password complexity requirements from user
"""


def main():
    print_sniper()
    create_target_profile()

    password_complexity = int(
        input(
            "How complex is the password (1 => Least Complexity, 2 => Medium Complexity, 3 => Most Complex): "
        )
    )

    while password_complexity > 3 or password_complexity == 0:
        password_complexity = int(
            input(
                "Enter a value that is between 1 and 3! (1 => Least Complexity, 2 => Medium Complexity, 3 => Most Complex): "
            )
        )

    if password_complexity == 1:
        # call least complex function
        print("Least Complex")
    elif password_complexity == 2:
        # call the medium complexity function
        print("Medium Complex")
    else:
        print("Most complex")
        # call the most complex function


if __name__ == "__main__":
    main()
