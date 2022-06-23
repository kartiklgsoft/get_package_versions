import requests
import urllib3
import argparse
import sys
import lxml.html
from pkg_resources import parse_version

urllib3.disable_warnings()

repo_base_url = "https://repo1.maven.org/maven2/"


def main():
    
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-ga", required=True, help="Specify the group ID and artifact ID in the following format - 'groupID:artifactID'. Eg. - 'org.cometd.java:cometd-java-oort'")
    arg_parser.add_argument("-vr", required=True, nargs="+", help="Specify the vulnerable version range(s) in the following format: -vr 4.12 5.17")
    arg_parser.add_argument("-c", action="store_true", help="Specify the -c flag if you want the version list suitable for adding to json file")
    args = arg_parser.parse_args()
    
    repo_path_list = args.ga.split(":")
    repo_path = "/".join(repo_path_list[0].split(".")) + "/" + repo_path_list[1]
    repo_url = repo_base_url + repo_path
    repo_version_request = requests.get(repo_url)
    
    if repo_version_request.status_code != 200:
        print("[!] Package not found\nkindly check the group ID and the artifact ID for the package")
        sys.exit(0)
    
    tree = lxml.html.fromstring(repo_version_request.text)
    links = tree.xpath("//a")
    links = links[1:]
    complete_version_list = list()
    
    for link in links:
        if "/" in link.text_content():
            complete_version_list.append(link.text_content().strip("/"))
    for i in range(0, len(args.vr), 2):
        for version in complete_version_list:
            if parse_version(args.vr[i]) <= parse_version(version) <= parse_version(args.vr[i+1]):
                if args.c:
                    print("\"{}\",".format(version))
                else:
                    print(version)


try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    print("\nReceived KeyboardInterrupt - Exiting...")
    sys.exit(0)
