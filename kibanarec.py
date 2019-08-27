import shodan
import time
import requests
import argparse
import configparser

from termcolor import colored

__author__ = "lekssays"
__license__ = "GPLv3"
__version__ = "1.0.0"

def banner():
    print('''
         _    _ _                                     
        | | _(_) |__   __ _ _ __   __ _ _ __ ___  ___ 
        | |/ / | '_ \ / _` | '_ \ / _` | '__/ _ \/ __|
        |   <| | |_) | (_| | | | | (_| | | |  __/ (__ 
        |_|\_\_|_.__/ \__,_|_| |_|\__,_|_|  \___|\___|
                                                      
        ''')
    print(colored("Author: Ahmed Lekssays (@Lekssays)", "magenta"))
    print(colored("Version {} \n\n", "magenta").format(__version__))

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o','--output',
                        dest = "output",
                        help = "Name of the file where results will be stored.",
                        default = "kibana_results.txt",
                        required = False)
    return parser.parse_args()

def write(entry, filename):
    out = open(filename, "a")
    out.write(entry + "\n")
    out.close()

def checkValidity(host, issued_to, filename):
    print(colored("[*] INFO: Checking " + host + "...", 'cyan'))
    url = "https://" + host + "/app/kibana#/home?_g=()"
    try:
        r = requests.get(url, allow_redirects=False, verify=False, timeout=10)
        body = str(r.content)
        entry = host + ", " + issued_to
        if "APM" in body:
            print(colored("[+] SUCCESS: " + entry, 'green'))
            write(entry, filename)
        else:
            print(colored("[+] FAILED: " + entry, 'red'))
    except Exception as e:
        print('Error: {}'.format(e))
        pass

def getHosts(filename):
    secret = configparser.RawConfigParser()
    secret.read('.env')
    SHODAN_API_KEY = secret["shodan"]["key"]
    api = shodan.Shodan(SHODAN_API_KEY)

    try:
        for p in range(1, 150):
            query = 'title:"kibana" port:"443"'
            results = api.search(query, page=p)
            for result in results['matches']:
                host = str(result['ip_str'])
                print(colored("[*] INFO: Parsing " + host + "...", "cyan"))
                issued_to = "Unknown"
                try:
                    if 'ssl' in str(result):
                        issued_to = result['ssl']['cert']['subject']['CN']
                except Exception as e:
                    print('Error: {}'.format(e))
                    pass
                checkValidity(host, issued_to, filename)
            time.sleep(1)
    except shodan.APIError as e:
        print('Error: {}'.format(e))
        pass

def main():
    banner()
    filename = parse_args().output
    getHosts(filename)

if __name__ == '__main__':
    main()
