if __name__ == "__main__":

    import re
    import json
    import tarfile
    import requests

    from pathlib import Path
    from schema import Use, Schema  # type: ignore
    from typing import Any, Dict, Union, Generator

    # numskip:  The number of lines to skip in th database file.
    #           These lines form the header, with version number
    #           and contact information.
    # atnfurl:  URL of the ATNF pulsar database.
    # atnftar:  URL of the ATNF tarball.
    # exfiles:  Paths of the files we need to extract from the tarball.
    #           This includes the database itself, and the "psrcat_ref"
    #           file, which contains all the references.
    # sep:      The separator string.

    numskip = 99
    atnfurl = "https://www.atnf.csiro.au/research/pulsar/psrcat"
    atnftar = "/".join([atnfurl, "downloads", "psrcat_pkg.tar.gz"])
    exfiles = {
        "data": "psrcat_tar/psrcat.db",
        "refs": "psrcat_tar/psrcat_ref",
    }
    sep = "@-----------------------------------------------------------------"

    # A simple regular expression to parse
    # the version number of the database
    # from the header.
    vex = re.compile(
        r"""
        [#]
        CATALOGUE
        \s*
        (?P<version>
            [0-9]+[.][0-9]+
        )
        """,
        re.VERBOSE,
    )

    def download() -> None:

        """
        Download the ATNF tarball, which contains the
        database file, the references, and the `psrcat`
        software.
        """

        tarball = requests.get(atnftar)
        with open(
            "psrcat_pkg.tar.gz",
            "wb+",
        ) as fobj:
            fobj.write(tarball.content)

    def upload() -> Dict:

        """
        Extract the database and the references from
        the tarball into memory for further processing.
        """

        data: Dict = {}

        for abbr, exfile in exfiles.items():
            with tarfile.open(
                "psrcat_pkg.tar.gz",
                mode="r:gz",
            ) as tarball:
                fobj = tarball.extractfile(exfile)
                if fobj is not None:
                    data[abbr] = fobj.read().decode()
        return data

    def parse_cat(data: str) -> Dict:

        """
        Parse the ATNF pulsar database into a dictionary
        of dictionaries and serialise it into a JSON file.
        """

        pcat: Dict = {}

        version = lambda hdr: re.search(  # type: ignore
            vex,
            hdr,
        ).groupdict()["version"]

        refk = lambda k: "_".join([k, "REF"])
        errk = lambda k: "_".join([k, "ERR"])

        def blocks(data: str) -> Generator:

            """
            Split the raw data from the database file into blocks.
            """

            return (
                re.split(
                    r"\n+",
                    block,
                )[1:-1]
                for block in re.split(sep, data)
            )

        def validator(val: Any) -> Union[str, float]:
            try:
                return float(val)
            except ValueError:
                return str(val)

        def parse(row: str) -> Dict:

            """
            Parse each row in a block into a dictionary.
            We also take care to validate each row, so
            that all numeric values are converted into
            float, while the strings are left unchanged.
            """

            cols = re.split(r"\s+", row)
            cols = [i for i in cols if i]
            kvs = Schema({str: Use(validator)})
            pp = {
                2: lambda k, v: {k: v},
                3: lambda k, v, ref: {k: v, refk(k): ref},
                4: lambda k, v, err, ref: {k: v, errk(k): err, refk(k): ref},
            }[len(cols)]
            pd = pp(*cols)  # type: ignore
            pd = kvs.validate(pd)  # type: ignore
            return pd  # type: ignore

        # Now that we have all the tools at hand, time
        # to scrap and parse the ATNF pulsars database!

        header = data[:numskip]
        pcat["version"] = version(header)
        for i, block in enumerate(blocks(data[numskip:])):
            pulsar: Dict = {}
            for line in block:
                pulsar.update(parse(line))
            pcat[str(i + 1)] = pulsar

        return pcat

    def parse_refs(data: str) -> Dict:

        """
        Parse the references from the "psrcat_ref" file
        into a dictionary of dictionaries and serialise
        that into a JSON file.
        """

        return {
            line.split()[0]: " ".join(line.split()[2:])
            for line in data.strip().split("***")
            if len(line) > 0
        }

    def scrap() -> None:

        """
        Scrap the ATNF tarball, extract the files containing the
        pulsars database and the references, and parse that info
        into separate JSON files. The tarball is always deleted.
        """

        download()

        pulsars: Dict = {}
        for key, data in upload().items():
            pulsars[key] = {"data": parse_cat, "refs": parse_refs}[key](data)
        version = pulsars["data"].pop("version")
        with open("pulsars.json", "w+") as fobj:
            json.dump(
                dict(
                    data=pulsars["data"],
                    refs=pulsars["refs"],
                    version=version,
                ),
                fobj,
                indent=4,
            )
        Path("psrcat_pkg.tar.gz").unlink()

    # Scrap the ATNF pulsar database.
    scrap()

    # Get the current version of the database from
    # the JSON file that we have just scraped, and
    # put it into a "v0.01" format.
    with open("pulsars.json", "r") as fobj:
        version = "".join(["v", json.load(fobj)["version"]])

    # Read in the README file.
    with open("README.md", "r") as fobj:
        data = fobj.read()

    # Substitute the version number into the badge,
    # thanks to a nifty regular expression.
    data = re.sub(
        r"[v]\d+[.]\d+",
        version,
        data,
    )

    # Write the file back out.
    with open("README.md", "w+") as fobj:
        fobj.write(data)