import re
import datetime
from pathlib import Path
from enum import Enum


Band10 = Enum("Band", "AOT B02 B03 B04 B08 TCI WVP")
Band20 = Enum("Band", "AOT B02 B03 B04 B05 B06 B07 B11 B12 B8A SCL TCI WVP")
Band60 = Enum("Band", "AOT B01 B02 B03 B04 B05 B06 B07 B09 B11 B12 B8A SCL TCI WVP")

BandResolution = {Band10: "10", Band20: "20", Band60: "60"}


class Tile:
    def __init__(self, path):
        self.path = Path(path)

        pattern = (
            r"^S2[AB]_MSIL2A_"
            r"(?P<start>\d{8}T(\d{6}))_"
            r"N(\d{4})_"
            r"(?P<orbit>R(\d{3}))_"
            r"(?P<name>[A-Z0-9]{6})_"
            r"(?P<stop>\d{8}T(\d{6}))"
            r"\.SAFE$"
        )

        match = re.match(pattern, self.path.name, re.IGNORECASE)

        if not match:
            raise RuntimeError("unable to parse tile name")

        self.props = match.groupdict()

    @property
    def name(self):
        return self.props["name"]

    @property
    def orbit(self):
        return self.props["orbit"]

    @property
    def start(self):
        return datetime.datetime.strptime(self.props["start"], "%Y%m%dT%H%M%S")

    @property
    def stop(self):
        return datetime.datetime.strptime(self.props["stop"], "%Y%m%dT%H%M%S")

    def get_band(self, band):
        res = BandResolution[type(band)]
        tif = next(self.path.glob(f"GRANULE/*/IMG_DATA/R{res}m/*_{band.name}_{res}m.jp2"))
        return tif
