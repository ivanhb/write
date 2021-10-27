import sys_conf as c
from rdflib.serializer import Serializer
from rdflib import Graph, plugin
from collections import defaultdict, Counter
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from argparse import ArgumentParser
import requests
import json
import os
import sys
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def get_from_omeka(api_url, api_opr, curr_page=1, curr_data=[]):
    response = requests.get(api_url+"/"+api_opr
                            + "?page="+str(curr_page), verify=False)
    if response.status_code == 200:
        l_elems = json.loads(response.text)
        if len(l_elems) == 0:
            return curr_data
        else:
            return get_from_omeka(api_url, api_opr, curr_page+1, curr_data + l_elems)
    else:
        return curr_data


# Backup all the items
def backup_items(api_url=None):
    #if online:
    data_items = get_from_omeka(api_url, "items")

    #in case there is other items then append the given items (i.e. <d>) to the current items
    #if os.path.exists(c.ITEMS_INDEX):
    #    with open(c.ITEMS_INDEX,"r") as created_items_file:
    #        created_items = json.load(created_items_file)
    #        d = d + created_items

    #print all in a json file
    with open(c.ITEMS_INDEX, "w") as items_index_file:
        items_index_file.write(json.dumps(data_items))
    items_index_file.close()
    return data_items


def convert_to_3n():
    #g.serialize(format="json-ld", base, encoding, args)
    with open(c.ITEMS_INDEX, "r") as items:
        items_jsonld = json.load(items)

    g = Graph()
    g.parse(data=str(json.dumps(items_jsonld)), format="json-ld")
    g.serialize(destination=c.ITEMS_INDEX_n3, format="n3")
    return g


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
REQ_SESSION = requests.Session()
retries = Retry(total=10, backoff_factor=1,
                status_forcelist=[502, 503, 504, 524])
REQ_SESSION.mount('http://', HTTPAdapter(max_retries=retries))
REQ_SESSION.mount('https://', HTTPAdapter(max_retries=retries))

########################
############ Things to do manually
########################

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        "omeka_export.py", description="Export all the items from OmekaS")
    arg_parser.add_argument("-conf", "--configuration", required=True,
                            dest="conf", help="Specify the configuration file (JSON format)")
    args = arg_parser.parse_args()

    ## -------
    ## Args Conf and definitions
    ## -------
    args_conf = None
    with open(args.conf) as json_file:
        args_conf = json.load(json_file)
        params = {
            'key_identity': args_conf["key_identity"],
            'key_credential': args_conf["key_credential"]
        }

    items_json = backup_items(args_conf["omeka_api_url"])
    print("Backup of all items in: "+c.ITEMS_INDEX+". Done!")

    convert_to_3n()
    print("Backup of all items in: "+c.ITEMS_INDEX_n3+". Done!")
