from utils.Alignment import CosineDistance
from config import QDRANT_HOST, QDRANT_PORT, MODEL, INPUTGRAPH, CODEMETAFILE, SPARQLMUSE, RESULTDIR
import pandas as pd
import json
import os
import re
import argparse

args = argparse.ArgumentParser()
args.add_argument("--query", type=str, default="")
args.add_argument("--input", type=str, default="")
args.add_argument("--output", type=str, default="")
args.add_argument("--debug", type=bool, default=False)
args.add_argument("--dir", type=int, default=0)
args = args.parse_args()

query = args.query
output = args.output
debug = args.debug
dir = args.dir

results = {}
if __name__ == "__main__":
    df = pd.read_csv(CODEMETAFILE)
    mappings = {}
    print("Starting ontology mapping...")
    for index, row in df.iterrows():
        if index: # < 5:
            queries = []
            queries.append(row['Property'])
            split_text = re.sub(r'(?<!^)(?=[A-Z])', ' ', row['Property'])
            if len(split_text.split()) > 1:
                queries.append(split_text)
            for query in queries:
                print(f"query: {query}")
                context = row['Type']
                query+= f" {context} {row['Description']}"
                query = query.replace("/", " ")
                context = CosineDistance(query, debug, SPARQLMUSE)
                context.get_context()
                if debug:
                    print(context.identifiers)
                known_properties = []
                if context.identifiers:
                    results[row['Property']] = context.identifiers
                    print(f"{row['Property']} {context.identifiers}")
                    #https://www.wikidata.org/wiki/Property:
                    for identifier in context.identifiers:
                        if identifier not in known_properties:
                            print(f"\t{identifier} \"{context.labels[identifier]}\" https://www.wikidata.org/wiki/Property:{identifier}")
                            known_properties.append(identifier)

    if output:
        if not os.path.exists(f"{dir}/{output}"):
            os.makedirs(f"{dir}/{output}")
        json.dump(results, open(f"{dir}/{output}/codemeta2wiki.json", 'w'), indent=4)
