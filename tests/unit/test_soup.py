from bs4 import BeautifulSoup
from graver.soup import (
    get_birth_date,
    get_birth_place,
    get_burial_plot,
    get_death_date,
    get_death_place,
    get_name,
)

soup = BeautifulSoup(open("./tests/unit/asimov.html"), "lxml")


def test_get_name():
    # soup = BeautifulSoup(open("./tests/unit/asimov.html"))
    name = get_name(soup)
    assert name == "Isaac Asimov"


def test_get_birth_date():
    birth = get_birth_date(soup)
    assert birth == "2 Jan 1920"


def test_get_birth_place():
    birth_place = get_birth_place(soup)
    assert birth_place == "Smolensk Oblast, Russia"


def test_get_death_date():
    death = get_death_date(soup)
    assert death == "6 Apr 1992"


def test_get_death_place():
    death_place = get_death_place(soup)
    assert death_place == "New York, New York County, New York, USA"


def test_get_burial_plot():
    plot = get_burial_plot(soup)
    assert plot is None