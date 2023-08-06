# csv-to-tsv

Convert CSV file to tab-delimited TSV file.

## Installation and Usage

python is installed, install with pip

```sh
pip install csv2tsv
```

```python
from csv2tsv import to_csv

to_csv(src_dir)
```

or copy csv2tsv folder and run

```sh
py -m csv2tsv [src_dir]
```

python is NOT installed, download from release and run batch file.

## API

### Use python

* to_csv(src, [dist_dir], [encoding="utf-8"], [delimiter=","])
    * src: Source csv directory or csv file path.
    * dist_dir: Output directory. If None, a folder named tsv will be created in the same hierarchy as the src folder. (default=None)
    * encoding: Character encoding of src/dist csv. (default="utf-8")
    * delimiter: Delimiter of src csv. (default=",")

### Use command

See help.

```sh
py -m csv2tsv --help
```

## License

MIT License
