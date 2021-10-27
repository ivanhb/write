# write: from OmekaS to a triplestore

## Export the items of OmekaS in JSONLD and N3
1. Set the configuration values in the file `conf.json`
2. Navigate to the following root directory from your terminal (i.e. `cd`)
3. Run the following command from your terminal `python3 export.py -conf conf.json`
4. The directory **data/** will contain the exported files

## Create your triplestore using blazegraph
### Taken from the quick start tutorial of blazegraph: [https://github.com/blazegraph/database/wiki/Quick_Start](https://github.com/blazegraph/database/wiki/Quick_Start)

1. From the terminal, navigate to the directory **triplestore/** and run the following command to open blazegraph `java -server -Xmx4g -jar blazegraph.jar`
2. Open blazegraph using your browser (usually with the url http://localhost:9999/blazegraph/). Then click on the **UPDATE** section
3. Inside the editor box write: `load <file:///[[N3_FILE_PATH]]>` replace `[[N3_FILE_PATH]]` with the absolute PATH to the N3 file generated in the export step. **Note:** you can move to the directory **data** and type `pwd` on the terminal to get the absolute path to the N3 file
4. The directory **triplestore/** will contain a **blazegraph.jnl** file, and you can query the triplestore from the blazegraph interface.
