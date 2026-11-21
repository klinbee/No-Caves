import shutil
import zipfile
import yaml
from pathlib import Path
from string import Template
from beet import Context, DataPack, TextFile
from beet.contrib.worldgen import WorldgenDensityFunction, WorldgenConfiguredCarver


# For some reason Beet does not have the new carvers
class WorldgenCarver(WorldgenConfiguredCarver):
    scope = ("worldgen", "carver")


ROOT = Path(__file__).parent
BUILD = ROOT / "build"
SOURCE = ROOT / "src"
WRAPPER = ROOT / "wrapper"


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


    with open(ROOT / "meta.yaml") as f:
        metadata: dict = yaml.load(f, Loader=yaml.SafeLoader)

    for edition in (NoCaves, NoNewCaves, NoOldCaves):

        edition.name += f"-{metadata["version"]}" # NOTE: This leads to the mods' names containing the version number
        edition.save(BUILD)
        edition.save(BUILD, zipped=True)


        with (
            zipfile.ZipFile(BUILD / (edition.name + ".zip"), "r") as datapackbuild,
            zipfile.ZipFile(BUILD / (edition.name + ".jar"), "w", compression=zipfile.ZIP_DEFLATED) as modbuild
            ):

            for item in datapackbuild.infolist():
                modbuild.writestr(item, datapackbuild.read(item.filename))

            for file in WRAPPER.rglob("*"):
                if file.is_file():
                    rel_path = file.relative_to(WRAPPER).as_posix()
                    template = file.read_text(encoding="utf-8")
                    rendered = Template(template).safe_substitute(metadata | {
                        "id": "mr_" + edition.name.lower().replace(" ", "_").split("-")[0],
                        "name": edition.name.replace("_", " "),
                        "description": edition.mcmeta.data["pack"]["description"][0], # TODO: Formatting-wise this is very unsafe
                    })
                    modbuild.writestr(rel_path, rendered.encode("utf-8"))