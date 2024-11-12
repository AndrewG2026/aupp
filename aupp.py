from itertools import permutations
import re
import argparse
import configparser
import csv
import functools
import gzip
import os
import sys
import multiprocessing
import math
from concurrent.futures import ProcessPoolExecutor
import time
import shutil
import urllib.error
import urllib.parse
import urllib.request
from functools import reduce

CONFIG = {}
CORE_COUNT = multiprocessing.cpu_count()


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
            "netflix-pr": dict(config.items("netflix")),
            "instagram-pr": dict(config.items("instagram")),
            "gmail-pr": dict(config.items("gmail")),
            "apple-pr": dict(config.items("apple")),
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

def write_to_file(target_name, wordlist, password_complextity):
    """
    Lets user choose to append rockyou.txt or create own file
    """
    if password_complextity == 3:
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


def parallel_processing(complete_list, requirements):
    "Will use the filter requirements to go through the passwords"
    chunk_size = math.ceil(len(complete_list) / CORE_COUNT)
    chunks = [
        complete_list[i * chunk_size : (i + 1) * chunk_size] for i in range(CORE_COUNT)
    ]

    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(filter_password, chunk, requirements) for chunk in chunks
        ]
        results = [future.result() for future in futures]

    flattened_results = [item for sublist in results for item in sublist if item is not None]
    return flattened_results


def filter_password(chunk, requirements):
    "Filters the password based on preset or custom requirements"
    def is_valid(item):
        if len(item) < int(requirements["length"]):
            return False

        if  not requirements["uppercase"] and re.search(r'[A-Z]',item):
            return False

        if not requirements["lowercase"] and re.search(r"[a-z]",item):
            return False

        if not requirements["numbers"] and re.search(r"\d",item):
            return False

        if not requirements["special_chars"] and re.search(r"[^a-zA-Z0-9\s]", item):
            return False

        return True

    return [item for item in chunk if is_valid(item)]

def print_sniper():
    """
    Prints team logo, creates profile, and obtains password complexity requirements from user
    """
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
        "> Do you want to add some key words about the victim (Keywords will only be included in Medium/Most Complexity)? Y/[N]: "
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

def least_complex(profile):
    """ Generates a wordlist from a given profile """

    chars = CONFIG["global"]["chars"]
    years = CONFIG["global"]["years"]
    numfrom = CONFIG["global"]["numfrom"]
    numto = CONFIG["global"]["numto"]

    profile["spechars"] = []

    if profile["spechars1"] == "y":
        for spec1 in chars:
            profile["spechars"].append(spec1)
            for spec2 in chars:
                profile["spechars"].append(spec1 + spec2)
                for spec3 in chars:
                    profile["spechars"].append(spec1 + spec2 + spec3)

    print("\r\n[+] Now making a dictionary...")

    # Now me must do some string modifications...

    # Birthdays first

    birthdate_yy = profile["birthdate"][-2:]
    birthdate_yyy = profile["birthdate"][-3:]
    birthdate_yyyy = profile["birthdate"][-4:]
    birthdate_xd = profile["birthdate"][1:2]
    birthdate_xm = profile["birthdate"][3:4]
    birthdate_dd = profile["birthdate"][:2]
    birthdate_mm = profile["birthdate"][2:4]

    wifeb_yy = profile["wifeb"][-2:]
    wifeb_yyy = profile["wifeb"][-3:]
    wifeb_yyyy = profile["wifeb"][-4:]
    wifeb_xd = profile["wifeb"][1:2]
    wifeb_xm = profile["wifeb"][3:4]
    wifeb_dd = profile["wifeb"][:2]
    wifeb_mm = profile["wifeb"][2:4]

    kidb_yy = profile["kidb"][-2:]
    kidb_yyy = profile["kidb"][-3:]
    kidb_yyyy = profile["kidb"][-4:]
    kidb_xd = profile["kidb"][1:2]
    kidb_xm = profile["kidb"][3:4]
    kidb_dd = profile["kidb"][:2]
    kidb_mm = profile["kidb"][2:4]

    # Convert first letters to uppercase...

    nameup = profile["name"].title()
    surnameup = profile["surname"].title()
    nickup = profile["nick"].title()
    wifeup = profile["wife"].title()
    wifenup = profile["wifen"].title()
    kidup = profile["kid"].title()
    kidnup = profile["kidn"].title()
    petup = profile["pet"].title()
    companyup = profile["company"].title()

    wordsup = []
    wordsup = list(map(str.title, profile["words"]))

    word = profile["words"] + wordsup

    # reverse a name

    rev_name = profile["name"][::-1]
    rev_nameup = nameup[::-1]
    rev_nick = profile["nick"][::-1]
    rev_nickup = nickup[::-1]
    rev_wife = profile["wife"][::-1]
    rev_wifeup = wifeup[::-1]
    rev_kid = profile["kid"][::-1]
    rev_kidup = kidup[::-1]

    reverse = [
        rev_name,
        rev_nameup,
        rev_nick,
        rev_nickup,
        rev_wife,
        rev_wifeup,
        rev_kid,
        rev_kidup,
    ]
    rev_n = [rev_name, rev_nameup, rev_nick, rev_nickup]
    rev_w = [rev_wife, rev_wifeup]
    rev_k = [rev_kid, rev_kidup]
    # Let's do some serious work! This will be a mess of code, but... who cares? :)

    # Birthdays combinations

    bds = [
        birthdate_yy,
        birthdate_yyy,
        birthdate_yyyy,
        birthdate_xd,
        birthdate_xm,
        birthdate_dd,
        birthdate_mm,
    ]

    bdss = []

    for bds1 in bds:
        bdss.append(bds1)
        for bds2 in bds:
            if bds.index(bds1) != bds.index(bds2):
                bdss.append(bds1 + bds2)
                for bds3 in bds:
                    if (
                        bds.index(bds1) != bds.index(bds2)
                        and bds.index(bds2) != bds.index(bds3)
                        and bds.index(bds1) != bds.index(bds3)
                    ):
                        bdss.append(bds1 + bds2 + bds3)

                # For a woman...
    wbds = [wifeb_yy, wifeb_yyy, wifeb_yyyy, wifeb_xd, wifeb_xm, wifeb_dd, wifeb_mm]

    wbdss = []

    for wbds1 in wbds:
        wbdss.append(wbds1)
        for wbds2 in wbds:
            if wbds.index(wbds1) != wbds.index(wbds2):
                wbdss.append(wbds1 + wbds2)
                for wbds3 in wbds:
                    if (
                        wbds.index(wbds1) != wbds.index(wbds2)
                        and wbds.index(wbds2) != wbds.index(wbds3)
                        and wbds.index(wbds1) != wbds.index(wbds3)
                    ):
                        wbdss.append(wbds1 + wbds2 + wbds3)

                # and a child...
    kbds = [kidb_yy, kidb_yyy, kidb_yyyy, kidb_xd, kidb_xm, kidb_dd, kidb_mm]

    kbdss = []

    for kbds1 in kbds:
        kbdss.append(kbds1)
        for kbds2 in kbds:
            if kbds.index(kbds1) != kbds.index(kbds2):
                kbdss.append(kbds1 + kbds2)
                for kbds3 in kbds:
                    if (
                        kbds.index(kbds1) != kbds.index(kbds2)
                        and kbds.index(kbds2) != kbds.index(kbds3)
                        and kbds.index(kbds1) != kbds.index(kbds3)
                    ):
                        kbdss.append(kbds1 + kbds2 + kbds3)

                # string combinations....

    kombinaac = [profile["pet"], petup, profile["company"], companyup]

    kombina = [
        profile["name"],
        profile["surname"],
        profile["nick"],
        nameup,
        surnameup,
        nickup,
    ]

    kombinaw = [
        profile["wife"],
        profile["wifen"],
        wifeup,
        wifenup,
        profile["surname"],
        surnameup,
    ]

    kombinak = [
        profile["kid"],
        profile["kidn"],
        kidup,
        kidnup,
        profile["surname"],
        surnameup,
    ]

    kombinaa = []
    for kombina1 in kombina:
        kombinaa.append(kombina1)
        for kombina2 in kombina:
            if kombina.index(kombina1) != kombina.index(kombina2) and kombina.index(
                kombina1.title()
            ) != kombina.index(kombina2.title()):
                kombinaa.append(kombina1 + kombina2)

    kombinaaw = []
    for kombina1 in kombinaw:
        kombinaaw.append(kombina1)
        for kombina2 in kombinaw:
            if kombinaw.index(kombina1) != kombinaw.index(kombina2) and kombinaw.index(
                kombina1.title()
            ) != kombinaw.index(kombina2.title()):
                kombinaaw.append(kombina1 + kombina2)

    kombinaak = []
    for kombina1 in kombinak:
        kombinaak.append(kombina1)
        for kombina2 in kombinak:
            if kombinak.index(kombina1) != kombinak.index(kombina2) and kombinak.index(
                kombina1.title()
            ) != kombinak.index(kombina2.title()):
                kombinaak.append(kombina1 + kombina2)

    kombi = {}
    kombi[1] = list(komb(kombinaa, bdss))
    kombi[1] += list(komb(kombinaa, bdss, "_"))
    kombi[2] = list(komb(kombinaaw, wbdss))
    kombi[2] += list(komb(kombinaaw, wbdss, "_"))
    kombi[3] = list(komb(kombinaak, kbdss))
    kombi[3] += list(komb(kombinaak, kbdss, "_"))
    kombi[4] = list(komb(kombinaa, years))
    kombi[4] += list(komb(kombinaa, years, "_"))
    kombi[5] = list(komb(kombinaac, years))
    kombi[5] += list(komb(kombinaac, years, "_"))
    kombi[6] = list(komb(kombinaaw, years))
    kombi[6] += list(komb(kombinaaw, years, "_"))
    kombi[7] = list(komb(kombinaak, years))
    kombi[7] += list(komb(kombinaak, years, "_"))
    "ADD TO MEDIUM COMPLEXITY"
    # kombi[8] = list(komb(word, bdss))
    # kombi[8] += list(komb(word, bdss, "_"))
    # kombi[9] = list(komb(word, wbdss))
    # kombi[9] += list(komb(word, wbdss, "_"))
    # kombi[10] = list(komb(word, kbdss))
    # kombi[10] += list(komb(word, kbdss, "_"))
    # kombi[11] = list(komb(word, years))
    # kombi[11] += list(komb(word, years, "_"))
    kombi[8] = [""]
    kombi[9] = [""]
    kombi[10] = [""]
    kombi[11] = [""]
    kombi[12] = [""]
    kombi[17] = [""]
    if profile["randnum"] == "y":
        "ADD TO MEDIUM COMPLEXITY"
        # kombi[12] = list(concats(word, numfrom, numto))
        kombi[13] = list(concats(kombinaa, numfrom, numto))
        kombi[14] = list(concats(kombinaac, numfrom, numto))
        kombi[15] = list(concats(kombinaaw, numfrom, numto))
        kombi[16] = list(concats(kombinaak, numfrom, numto))
        kombi[17] = list(concats(reverse, numfrom, numto))
    kombi[13] = list(komb(reverse, years))
    kombi[13] += list(komb(reverse, years, "_"))
    kombi[14] = list(komb(rev_w, wbdss))
    kombi[14] += list(komb(rev_w, wbdss, "_"))
    kombi[15] = list(komb(rev_k, kbdss))
    kombi[15] += list(komb(rev_k, kbdss, "_"))
    kombi[16] = list(komb(rev_n, bdss))
    kombi[16] += list(komb(rev_n, bdss, "_"))
    komb001 = [""]
    komb002 = [""]
    komb003 = [""]
    komb004 = [""]
    komb005 = [""]
    komb006 = [""]
    if len(profile["spechars"]) > 0:
        komb001 = list(komb(kombinaa, profile["spechars"]))
        komb002 = list(komb(kombinaac, profile["spechars"]))
        komb003 = list(komb(kombinaaw, profile["spechars"]))
        komb004 = list(komb(kombinaak, profile["spechars"]))
        "ADD TO MEDIUM COMPLEXITY"
        # komb005 = list(komb(word, profile["spechars"]))
        komb006 = list(komb(reverse, profile["spechars"]))

    print("[+] Sorting list and removing duplicates...")

    komb_unique = {}
    for i in range(1, 18):
        komb_unique[i] = list(dict.fromkeys(kombi[i]).keys())

    komb_unique01 = list(dict.fromkeys(kombinaa).keys())
    komb_unique02 = list(dict.fromkeys(kombinaac).keys())
    komb_unique03 = list(dict.fromkeys(kombinaaw).keys())
    komb_unique04 = list(dict.fromkeys(kombinaak).keys())
    "ADD TO MEDIUM COMPLEXITY"
    # komb_unique05 = list(dict.fromkeys(word).keys())
    komb_unique07 = list(dict.fromkeys(komb001).keys())
    komb_unique08 = list(dict.fromkeys(komb002).keys())
    komb_unique09 = list(dict.fromkeys(komb003).keys())
    komb_unique010 = list(dict.fromkeys(komb004).keys())
    komb_unique011 = list(dict.fromkeys(komb005).keys())
    komb_unique012 = list(dict.fromkeys(komb006).keys())

    uniqlist = (
        bdss
        + wbdss
        + kbdss
        + reverse
        + komb_unique01
        + komb_unique02
        + komb_unique03
        + komb_unique04
        # + komb_unique05
    )

    for i in range(1, 18):
        uniqlist += komb_unique[i]

    uniqlist += (
        komb_unique07
        + komb_unique08
        + komb_unique09
        + komb_unique010
        + komb_unique011
        + komb_unique012
    )
    unique_lista = list(dict.fromkeys(uniqlist).keys())
    unique_leet = []

    for (
            x
        ) in (
            unique_lista
        ):  # if you want to add more leet chars, you will need to add more lines in cupp.cfg too...

            x = make_leet(x)  # convert to leet
            unique_leet.append(x)

    unique_list = unique_lista + unique_leet

    unique_list_finished = []
    unique_list_finished = [
        x
        for x in unique_list
        if len(x) < CONFIG["global"]["wcto"] and len(x) > CONFIG["global"]["wcfrom"]
    ]
    return unique_list

def komb(seq, start, special=""):
    for mystr in seq:
        for mystr1 in start:
            yield mystr + special + mystr1

def concats(seq, start, stop):
    for mystr in seq:
        for num in range(start, stop):
            yield mystr + str(num)




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
        complete_wordlist = least_complex(target_profile)

    elif password_complexity == 2:
        # call the medium complexity function
        print("Medium Complex")
    else:
        print("Most complex")
        # call the most complex function

    # Will take the complete list and filter it
    will_filter = str(input("Do you want to filter for password requirements? (Y/N): "))

    if will_filter.lower() == "y":
        is_custom = int(
            input(
                "Do you want to add your own custom password requirements (1) or use pre-set ones listed in aupp.cfg (2)? : "
            )
        )
        while is_custom > 2 or is_custom == 0:
            is_custom = int(
            input(
                "Number is out of range! Do you want to add your own custom password requirements (1) or use pre-set ones listed in aupp.cfg (2)? : "
            )
        )
        if is_custom == 1:
            custom_password_requirements = {
                "length": 0,
                "uppercase": True,
                "lowercase": True,
                "numbers": True,
                "special_chars": True,
            }
            custom_password_requirements["length"] = int(
                input("What is the minimum length of the password: ")
            )
            custom_password_requirements["uppercase"] = (
                str(input("Are there any uppercase characters (Y/N): ")).lower() == "y"
            )
            custom_password_requirements["lowercase"] = (
                str(input("Are there any lowercase characters (Y/N): ")).lower() == "y"
            )
            custom_password_requirements["numbers"] = (
                str(input("Are there any numbers (Y/N): ")).lower() == "y"
            )
            custom_password_requirements["special_chars"] = (
                str(input("Are there any special characters: (Y/N): ")).lower() == "y"
            )

            # Using this string filter out each string in the wordlist
            filtered_list = parallel_processing(
                complete_wordlist, custom_password_requirements
            )
            "Prompt user to create own requirements based on aupp.cfg"
        else:
            "Prompt user to pick which of the 4 preset password requirements to pick from and use that as reference"
            preset_password_requirements = int(
                input(
                    "Which of the preset password requirements would you like to select (Netflix=1, Instagram=2, gmail=3, apple=4): "
                )
            )

            while preset_password_requirements == 0 or preset_password_requirements > 4:
                preset_password_requirements = int(
                    input(
                        "Number is out of range please select (Netflix=1, Instagram=2, gmail=3, apple=4): "
                    )
                )

            if preset_password_requirements == 1:
                filtered_list = parallel_processing(
                    complete_wordlist, CONFIG["global"]["netflix-pr"]
                )
            elif preset_password_requirements == 2:
                filtered_list = parallel_processing(
                    complete_wordlist, CONFIG["global"]["instagram-pr"]
                )
            elif preset_password_requirements == 3:
                filtered_list = parallel_processing(
                    complete_wordlist, CONFIG["global"]["gmail-pr"]
                )
            else:
                filtered_list = parallel_processing(
                    complete_wordlist, CONFIG["global"["apple-pr"]]
                )

    write_to_file(target_profile["name"], filtered_list, password_complexity)

if __name__ == "__main__":
    main()

