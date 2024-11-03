from itertools import permutations
import re
import configparser
import os
import functools
import sys

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


def transform_word(word):
    return {
        "capitalize": word.capitalize(),
        "title": word.title(),
        "swapcase": word.swapcase(),
        "lower": word.lower(),
        "upper": word.upper(),
    }


def transform_words(words):
    return {
        word: {
            method: getattr(transform_word(word), method)
            for method in ["capitalize", "title", "swapcase", "lower", "upper"]
        }
        for word in words
    }


"""
Converts the string to leet
"""


def make_leet(x):
    for letter, leetletter in CONFIG["LEET"].items():
        x = x.replace(letter, leetletter)
    return x


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
Provides additional complextiy to the wordlist utilizing the target's keywords
"""


def medium_complexity(target_profile):
    # This is psuedo code! Need to wait until least complex is created
    # Get every combination of the birthdays, names of target, wife, and kid,
    med_comp_list = []
    least_comp_wl = least_complextity()
    wbd = least_comp_wl["wife_birthday"]  # combination of wifes b-day
    kidb = least_comp_wl["kid_birthday"]  # combination of kid b-day
    tbd = least_comp_wl["target_birthday"]  # combinations of targets b-day

    # Take the key words and perform uppercase, lowercase, title case, capitalize case, and swapcase

    transformed_words = transform_words(target_profile["words"])

    # Using the birthdays of the target, as well as nicknames, names, and surnames

    # Will need to partition the list into different sections
    # and make threads per each partition
    # Using math we can combine the parts of the transformed words list +the complete list of the birthdays
    # If the length of transformed_words = 150, we can divide it into partitions of 10 elements each + complete list of target info
    # Or just use the permustaion command once and really brute force it

    # In config file, you can increase the number of leet characters
    for x in med_comp_list:
        x = make_leet(x)
        med_comp_list.append(x)

    return med_comp_list


"""
Prints team logo, creates profile, and obtains password complexity requirements from user
"""


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
        med_comp_wl = medium_complexity(target_profile)
    else:
        print("Most complex")
        # call the most complex function


if __name__ == "__main__":
    main()
