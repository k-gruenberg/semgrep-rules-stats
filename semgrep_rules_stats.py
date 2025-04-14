import yaml
import sys
import os
import statistics
from collections import defaultdict
from typing import List, Dict


def generate_semgrep_rules_stats(semgrep_rules_repo_dir: str):
    no_of_yaml_files: int = 0
    no_of_erroneous_yaml_files: int = 0
    no_of_misc_exceptions: int = 0
    no_of_rules_per_yaml_file: List[int] = []
    no_of_yaml_files_with_more_than_one_rule: int = 0
    no_of_rules: int = 0
    no_of_rules_with_fix: int = 0
    no_of_rules_with_fix_regex: int = 0
    no_of_rules_without_a_language: int = 0
    no_of_rules_per_language: Dict[str, int] = defaultdict(lambda: 0)
    no_of_rules_with_fix_per_language: Dict[str, int] = defaultdict(lambda: 0)
    no_of_rules_with_fix_regex_per_language: Dict[str, int] = defaultdict(lambda: 0)

    for subdir, dirs, files in os.walk(semgrep_rules_repo_dir):
        for file in files:
            if file.endswith(".yaml"):
                yaml_path: str = os.path.join(subdir, file)
                no_of_yaml_files += 1
                with open(yaml_path) as yaml_file:
                    try:
                        yaml_content = yaml.safe_load(yaml_file)
                        # Example:
                        # {'rules': [{'id': 'eqeq-is-bad', 'pattern': '$X == $X', 'message':
                        #  '$X == $X is a useless equality check', 'languages': ['python'], 'severity': 'ERROR'}]}
                        rules = yaml_content["rules"]
                        no_of_rules_per_yaml_file.append(len(rules))
                        if len(rules) > 1:
                            no_of_yaml_files_with_more_than_one_rule += 1
                        for rule in rules:
                            no_of_rules += 1
                            if "fix" in rule:
                                no_of_rules_with_fix += 1
                            if "fix-regex" in rule:
                                no_of_rules_with_fix_regex += 1
                            #####
                            if "languages" in rule:
                                for language in rule["languages"]:
                                    no_of_rules_per_language[language] += 1
                                    if "fix" in rule:
                                        no_of_rules_with_fix_per_language[language] += 1
                                    if "fix-regex" in rule:
                                        no_of_rules_with_fix_regex_per_language[language] += 1
                            else:
                                no_of_rules_without_a_language += 1
                    except yaml.YAMLError as exc:
                        no_of_erroneous_yaml_files += 1
                    except:
                        no_of_misc_exceptions += 1

    print("")
    print(f"Total no. of YAML files: {no_of_yaml_files}")
    print(f"No. of erroneous YAML files: {no_of_erroneous_yaml_files}")
    print(f"No. of YAML files raising other exceptions: {no_of_misc_exceptions}")
    print(f"Avg. no. of rules per YAML file: {statistics.mean(no_of_rules_per_yaml_file)}")
    print(f"No. of YAML files with >1 rule: {no_of_yaml_files_with_more_than_one_rule}")
    print("")
    print(f"No. of rules: {no_of_rules}")
    print(f"No. of rules with a 'fix': {no_of_rules_with_fix}")
    print(f"No. of rules with a 'fix-regex': {no_of_rules_with_fix_regex}")
    print(f"No. of rules w/o a language: {no_of_rules_without_a_language}")
    print("")
    print("Languages, sorted by number of rules (note that a rule can apply to multiple languages):")
    for language, no_of_rules in sorted(no_of_rules_per_language.items(), key=lambda x: x[1], reverse=True):
        print(f"{language}: {no_of_rules}")
    print("")
    print("Languages, sorted by number of rules with a 'fix':")
    for language, no_of_rules in sorted(no_of_rules_with_fix_per_language.items(), key=lambda x: x[1], reverse=True):
        print(f"{language}: {no_of_rules}")
    print("")
    print("Languages, sorted by number of rules with a 'fix-regex':")
    for language, no_of_rules in sorted(no_of_rules_with_fix_regex_per_language.items(), key=lambda x: x[1], reverse=True):
        print(f"{language}: {no_of_rules}")
    print("")


def main():
    if len(sys.argv) < 2:
        print("Usage: semgrep_rules_stats.py <semgrep-rules repo>")
    else:
        generate_semgrep_rules_stats(sys.argv[1])


if __name__ == "__main__":
    main()
