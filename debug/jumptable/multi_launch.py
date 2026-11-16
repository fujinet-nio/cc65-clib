import os, time, sys
from pathlib import Path
# Same variables as fn-rom's beebium tests: BEEBIUM_HOME is required; the ROM
# dir and server default to its roms/ and build-release/ trees.
if "BEEBIUM_HOME" not in os.environ: sys.exit("BEEBIUM_HOME must be set to a beebium checkout")
BEEBIUM=os.environ["BEEBIUM_HOME"]
sys.path.insert(0, BEEBIUM+"/clients/beebium-python-client/src")
from beebium.client import Beebium
from beebium.client.screen import screen_contains
ROM=os.environ.get("BEEBIUM_ROM_DIR", BEEBIUM+"/roms")
SERVER=os.environ.get("BEEBIUM_SERVER", BEEBIUM+"/build-release/src/server/beebium-model-b")
CLIB=str(Path(__file__).resolve().parents[2]/"roms"/"clib.rom")  # this repo's build
def once(i):
    ex=["--sideways","slot=12:type=rom:image="+ROM+"/acorn-dfs_2_26.rom","--fdc","acorn-1770","--floppy","0:VECFAIL.ssd","--sideways","slot=13:type=rom:image="+CLIB]
    with Beebium.launch(server=SERVER, mos_filepath=ROM+"/acorn-mos_1_20.rom", basic_filepath=ROM+"/bbc-basic_2.rom", extra_args=ex) as bbc:
        bbc.debugger.reset(); bbc.debugger.run(); time.sleep(1.5)
        # is the CLIB ROM actually loaded in slot 13 this launch?
        try: rom_ok = bbc.sideways.read_slot_data(13,9,9)==b'cc65 CLIB'
        except Exception as e: rom_ok=("ERR:%s"%e)
        bbc.system.set_speed_multiplier(0.0)
        bbc.keyboard.type("*RUN VECFAIL\r"); time.sleep(2.5); bbc.debugger.stop()
        done = screen_contains(bbc,"DONE")
        print("launch %d: clib_rom_in_slot13=%s  program_DONE=%s" % (i, rom_ok, done))
for i in range(6): once(i)
