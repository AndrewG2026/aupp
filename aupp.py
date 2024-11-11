from itertools import permutations
import re
import configparser
import os
import functools
import sys
import time
import shutil

CONFIG = {}


def read_config(filename):
    """Read the given configuration file and update global variables to reflect
    changes (CONFIG)."""

    if os.path.isfile(filename):
        # global CONFIG

        # Reading configuration file
        config = configparser.ConfigParser()
        config.read(filename)

        CONFIG["global"] = {
            "years": config.get("years", "years").split(","),
            "chars": config.get("specialchars", "chars").split(","),
            "numfrom": config.getint("nums", "from"),
            "numto": config.getint("nums", "to"),
            "wcfrom": config.getint("nums", "wcfrom"),
            "wcto": config.getint("nums", "wcto"),
            "threshold": config.getint("nums", "threshold"),
            "alectourl": config.get("alecto", "alectourl"),
            "dicturl": config.get("downloader", "dicturl"),
            "netflix-pr": config.items("netflix"),
            "instagram-pr": config.items("instagram"),
            "gmail-pr": config.items("gmail"),
            "apple-pr": config.items("apple"),
        }

        # 1337 mode configs, well you can add more lines if you add it to the
        # config file too.
        leet = functools.partial(config.get, "leet")
        leetc = {}
        letters = {"a", "i", "e", "t", "o", "s", "g", "z"}

        for letter in letters:
            leetc[letter] = config.get("leet", letter)

        CONFIG["LEET"] = leetc

        return True

    else:
        print("Configuration file " + filename + " not found!")
        sys.exit("Exiting.")

        return False


def make_leet(x):
    """
    Converts the string to leet"""

    for letter, leetletter in CONFIG["LEET"].items():
        x = x.replace(letter, leetletter)
    return x


def write_to_file(target_name, wordlist):
    """
    Lets user choose to append rockyou.txt or create own file
    """
    append_rockyou = (
        input("Would you like to append rockyou.txt (Y/N): ").lower() == "y"
    )

    if append_rockyou:
        if os.path.exists(f"{target_name}.txt"):
            os.remove(f"{target_name}.txt")
        f = open(f"{target_name}.txt", "a")
        shutil.copy("rockyou.txt", f"{target_name}.txt")
        print("File, target-wordlist.txt has been created, writing now")
        for word in wordlist:
            f.write(f"{word}\n")
            print_loading_animation(idx + 1, wordlist_len)
            time.sleep(0.1)

    else:
        wordlist_len = len(wordlist)
        f = open(f"{target_name}.txt", "w")
        print(f"File {target_name} has been created, writing now")
        for idx, word in enumerate(wordlist):
            f.write(f"{word}\n")
            print_loading_animation(idx + 1, wordlist_len)
            time.sleep(0.1)


def print_loading_animation(current, total):
    """
    Displays a progress bar for the user to see progress of file creation
    """
    percent_complete = (current / total) * 100
    bar_length = 20
    block = int(round(bar_length * percent_complete / 100))
    text = f"\rLoading: [{'#' * block + '-' * (bar_length - block)}] {percent_complete:.2f}%"
    sys.stdout.write(text)
    sys.stdout.flush()


def print_sniper():
    print(
        "          \033[1;31m_________                   _______\033[1;m"
        + 5 * " "
        + "# \033[07mA\033[27mnderson"
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

    profile["phone_number"] = input("> Phone Number (no area code) xxxxxxxxxx: ")
    while (
        len(profile["phone_number"]) != 0 and len(profile["phone_number"]) != 10
    ) or re.search(r"\D+", profile["phone_number"]):
        print("\r\n[-] You must enter 10 digits with no characters for a phone number!")
        profile["phone_number"] = input("> Phone Number (no area code): ")

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
        "> Do you want to add some key words about the victim (Keywords will only be included in Medium Complexity)? Y/[N]: "
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
    return profile


"""
Prints team logo, creates profile, and obtains password complexity requirements from user
"""

# def most_complex():
#     MComplexArr = []

#     max_length = 0


def main():
    read_config("aupp.cfg")

    print_sniper()

    target_profile = create_target_profile()

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

    # Phone number complexity : ran_phone_num = list(itertools.permutations((profile["phone_number"]+rev_name),len(profile["phone_number"])))
    if password_complexity == 1:
        # call least complex function

        print("Least Complex")
    elif password_complexity == 2:
        # call the medium complexity function

        print("Medium Complex")
    else:
        print("Most complex")
        # call the most complex function

    # unique_leet = []
    # for (x) in (ADDRETURN)):  # if you want to add more leet chars, you will need to add more lines in cupp.cfg too...
    #         x = make_leet(x)  # convert to leet
    #         unique_leet.append(x)
    write_to_file(target_profile["name"], complete_wordlist)


if __name__ == "__main__":
    main()
