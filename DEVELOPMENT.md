## Architecture

Since multiple editions with overlapping code are maintained, the code is split into two datapacks in `src/`. The editions are build by `build.py`. Mod versions are build with the files of `wrapper/` and metadata provided by `meta.yaml`.

To build use Beet (Python 3.14+ required):
```sh
pip install -r requirements.txt
beet build
```
All datapack and mod artifacts are to be found in `build/`.

## 26.3 Support TODO
- Add Flat Dimensions support for 26.3+
- Verify Overworldify support for 26.3+
- ✅ Check whether pre-26.3 Tectonic support should be updated
- ✅ Verify that overlays work in mod versions
- ✅ Verify Tectonic support
