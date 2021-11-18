import json
import os
import re


LANGUAGE_DIR = "languages"
DEFAULT_LANGUAGE = "en-us"
ALL_PASSED = True

with open(f"{LANGUAGE_DIR}/{DEFAULT_LANGUAGE}.json", "r") as f:
    default_json = json.load(f)


def print_progress(text: str, newline: bool = False):
    print(text, end="\n" if newline else "\r")


for file in os.listdir("languages"):
    if file.endswith(".json"):
        filename = file[:-5]
        any_fails = False

        if filename == DEFAULT_LANGUAGE:
            continue  # Don't check this file, this is for reference

        print_progress(f"Validating {file}...")

        with open(f"{LANGUAGE_DIR}/{file}", encoding="utf-8") as f:
            lang = json.load(f)

        for key in [g for g in default_json]:
            if key not in [g for g in lang]:
                print(f"- Missing JSON key in {file}: {key}")
                any_fails = True

        words_failed = []
        for word in lang["words"]:
            if re.compile("(.* .*)").search(word):
                words_failed.append(word)

        if words_failed:
            all_words_failed = "\n".join([
                f"[{str(i).zfill(2)}] {g}"
                for i, g in enumerate(words_failed, start=1)
            ])
            print(f"- You can't have 2 words inside a string ({file})\n{all_words_failed}")
            any_fails = True

        if any_fails:
            ALL_PASSED = False
        else:
            print_progress(f"Validating {file}: PASSED", newline=True)


if not ALL_PASSED:
    raise SyntaxError("Some of the validation failed, fix those to make it work.")
