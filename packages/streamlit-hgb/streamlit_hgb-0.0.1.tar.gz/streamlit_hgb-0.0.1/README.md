# Streamlit-HGB

A streamlit component for a hybrid genome browser

* virtualenv

```bash
$ python3 -m venv venv  # create venv
$ . venv/bin/activate   # activate venv
$ pip install streamlit # install streamlit
$ pip install pyyaml    # install pyyaml
```

* frontend

```bash
$ cd hgb/frontend
$ npm install    # Initialize the project and install npm dependencies
$ npm run start  # Start the Webpack dev server
```

* backend

```bash
export STREAMLIT_HOST=$(hostname -i)
export HGB_BIN=/*location_to_hgb_binary*/

streamlit run hgb/__init__.py 
```

## Example of `config.yaml`

```yaml
hg38:
  range: 
    - chr1:1-1000001
  default:
    - "/path/to/bamfile1.bam"
  samples: 
    - "/path/to/bamfile1.bam"
    - "/path/to/bamfile2.bam"
```

* Range: a default range to visualize
* Default: a default set of BAM file to be loaded
* Samples: a list of BAM file

All input bam files must be indexed by `samtools index` or compatibles.
