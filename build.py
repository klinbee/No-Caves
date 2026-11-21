import shutil
import zipfile
from pathlib import Path
from beet import Context, DataPack, TextFile
from beet.contrib.worldgen import WorldgenDensityFunction, WorldgenConfiguredCarver


# For some reason Beet does not have the new carvers
class WorldgenCarver(WorldgenConfiguredCarver):
    scope = ("worldgen", "carver")


ROOT = Path(__file__).parent
BUILD = ROOT / "build"
SOURCE = ROOT / "src"


def beet_default(ctx: Context):

    NoNewCaves = DataPack(path=SOURCE / "No_New_Caves", extend_namespace=[WorldgenDensityFunction], extend_extra={"LICENSE": TextFile})
    NoOldCaves = DataPack(path=SOURCE / "No_Old_Caves", extend_namespace=[WorldgenConfiguredCarver, WorldgenCarver], extend_extra={"LICENSE": TextFile})

    NoCaves = DataPack(name="No_Caves")
    NoCaves.merge(NoNewCaves)
    NoCaves.merge(NoOldCaves)
    NoCaves.mcmeta.data["pack"]["description"][0] = "Removes All Caves"


    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True, exist_ok=True)


    for edition in (NoCaves, NoNewCaves, NoOldCaves):

        edition.save(BUILD)
        edition.save(BUILD, zipped=True)


        with (
            zipfile.ZipFile(BUILD / (edition.name + ".zip"), "r") as datapackbuild,
            zipfile.ZipFile(BUILD / (edition.name + ".jar"), "w", compression=zipfile.ZIP_DEFLATED) as modbuild
            ):

            for item in datapackbuild.infolist():
                modbuild.writestr(item, datapackbuild.read(item.filename))

            ... # TODO