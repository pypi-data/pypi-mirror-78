import csv
from pathlib import Path
from typing import IO, Optional, Union

PathLike = Union[str, Path]


def _write(f_in: IO, f_out: IO, *, delimiter=","):
    csv.writer(f_out, delimiter="\t", lineterminator="\n").writerows(
        csv.reader(f_in, delimiter=delimiter)
    )


def _to_tsv(
    src: PathLike, dist: Optional[PathLike] = None, *, encoding="utf-8", delimiter=","
):
    src = Path(src)
    if not src.is_file():
        raise ValueError(f"{str(src)} is not files. src only allows files, not dir.")
    if src.exists():
        with open(src, "r", encoding=encoding, errors="replace") as f_in:
            dist = (
                src.resolve().parent / f"{src.stem}_tsv.csv"
                if dist is None
                else Path(dist)
            )
            if dist.is_dir():
                dist = dist / src.name
            dist.parent.mkdir(parents=True, exist_ok=True)
            stem = dist.stem
            i: int = 0
            while dist.exists():
                print(f"{str(dist)} is exists.")
                i += 1
                dist = dist.parent / f"{stem}_{i}.csv"
            with open(dist, "x", encoding=encoding, newline="\n") as f_out:
                _write(f_in, f_out, delimiter=delimiter)
                print(f"{str(src.resolve())} -> {str(dist.resolve())}")
    else:
        raise FileNotFoundError(f"{str(src)} is not exists.")


def to_tsv(
    src: PathLike, dist: Optional[PathLike] = None, *, encoding="utf-8", delimiter=","
):
    src = Path(src)
    if src.is_dir():
        dist = src.resolve().parent / "tsv" if dist is None else Path(dist)
        for fs in src.glob("**/*.csv"):
            fd: Path = dist / fs.relative_to(src)
            _to_tsv(fs, fd, encoding=encoding, delimiter=delimiter)
    else:
        _to_tsv(src, dist, encoding=encoding, delimiter=delimiter)
    print("done.")


if __name__ == "__main__":
    _to_tsv(f"{Path(__file__).parent}/test.csv")
