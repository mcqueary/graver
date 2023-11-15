import logging as log
import os
import re
import sys
from typing import Optional

import typer
from tqdm import tqdm
from typing_extensions import Annotated

import graver
from graver.memorial import Memorial, MemorialMergedException
from graver.parsers import MemorialParser

# Constants
DEFAULT_DB_FILE_NAME = "graves.db"
DEFAULT_OUTPUT_FILE = sys.stdout
DEFAULT_LOG_LINE_FMT = "%(asctime)s %(levelname)s %(message)s"
DEFAULT_LOG_DATE_FMT = "%m/%d/%Y %I:%M:%S %p"
DEFAULT_LOG_LEVEL = "INFO"
COLUMNS = [
    "id",
    "url",
    "name",
    "birth",
    "birthplace",
    "death",
    "deathplace",
    "burial",
    "plot",
    "coords" "more_info",
]

log_level = DEFAULT_LOG_LEVEL
csvwriter = None
problemchilds = []
parsed_args = None

app = typer.Typer(add_completion=False)

# TODO: Add support for log level DEBUG, INFO, WARNING, ERROR, CRITICAL
# Configure logging
# log_level = DEFAULT_LOG_LEVEL
# if log is not None:
#     log_level = parsed_args.log
# log.basicConfig(
#     format=DEFAULT_LOG_LINE_FMT, datefmt=DEFAULT_LOG_DATE_FMT, level=log_level
# )
# log.debug("Log level is " + str(log_level))

# TODO: Add support for output CSV
# TODO: Add init command
# TODO: Configure output database name


def get_id_from_url(url: str):
    result = None
    old_style = ".*?GRid=([0-9]+)$"
    new_style = MemorialParser.DEFAULT_URL_FORMAT.format("([0-9]+)")
    if "GRid=" in url:  # oldstyle URL format
        result = re.match(old_style, url).group(1)
    elif re.match(new_style, url):
        result = re.match(new_style, url).group(1)
    return result


def get_urls_from_gedcom(gedfile: str):
    # TODO add gedcom input support
    # # read from gedcom
    # with open('tree.ged', encoding='utf8') as ged:
    #     for line in ged.readlines():
    #         num_memorials+=1
    #         if '_LINK ' in line and 'findagrave.com' in line:
    #             for unit in line.split('&'):
    #                 if 'GRid=' in unit:
    #                     if unit[5:-1] not in graveids:
    #                         graveids.append(unit[5:-1])
    #                         #print(graveids[numids])
    #                         numids+=1
    return


@app.command()
def version():
    """Return version of graver application"""
    print(graver.__version__)


@app.command()
def scrape(input_filename: str, db: Annotated[Optional[str], typer.Argument()] = None):
    """Scrape URLs from a file"""
    print(f"Input file: {input_filename}")

    urls = []

    if db is None:
        db = os.getenv("DATABASE_NAME")
        if db is None:
            db = DEFAULT_DB_FILE_NAME
    else:
        os.environ["DATABASE_NAME"] = db
    Memorial.create_table(db)

    # Main loop
    with open(input_filename) as file:
        while line := file.readline():
            # currid = re.match(".*?([0-9]+)$", line).group(1)
            # currid = get_id_from_url(line)
            line = line.strip()
            if line not in urls:
                urls.append(line)

    parsed = 0
    failed_urls = []
    for url in (pbar := tqdm(urls)):
        try:
            pbar.set_postfix_str(url)
            MemorialParser().parse(url).save()
            parsed += 1
        except MemorialMergedException as ex:
            log.warn(ex)
        except Exception as ex:
            out = "Unable to parse Memorial []" + url + "]!"
            log.error(out, ex)
            failed_urls.append(url)

    msg = "Successfully parsed {total} of {expected}"
    print(msg.format(total=parsed, expected=len(urls)))
    # out = "Successfully parsed " + str(parsed) + " of "
    # out += str(len(urls))
    # print(out)
    if len(problemchilds) > 0:
        out = "Problem childz were:" + problemchilds
        print(out)


if __name__ == "__main__":
    typer.run(app)