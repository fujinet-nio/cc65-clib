import os, time, sys
from pathlib import Path
# Same variables as fn-rom's beebium tests: BEEBIUM_HOME is required; the ROM
# dir and server default to its roms/ and build-release/ trees.
if "BEEBIUM_HOME" not in os.environ: sys.exit("BEEBIUM_HOME must be set to a beebium checkout")
BEEBIUM=os.environ["BEEBIUM_HOME"]
sys.path.insert(0, BEEBIUM+"/clients/beebium-python-client/src")
from beebium.client import Beebium
from beebium.client.screen import dump_screen
ROM=os.environ.get("BEEBIUM_ROM_DIR", BEEBIUM+"/roms")
SERVER=os.environ.get("BEEBIUM_SERVER", BEEBIUM+"/build-release/src/server/beebium-model-b")
CLIB=str(Path(__file__).resolve().parents[2]/"roms"/"clib.rom")  # this repo's build
name=sys.argv[1]; ssd=name+".ssd"
ex=["--sideways","12:rom:"+ROM+"/acorn-dfs_2_26.rom","--fdc","acorn-1770","--floppy","0:"+ssd,"--sideways","13:rom:"+CLIB]
with Beebium.launch(server_filepath=SERVER, mos_filepath=ROM+"/acorn-mos_1_20.rom", basic_filepath=ROM+"/bbc-basic_2.rom", extra_args=ex) as bbc:
    bbc.debugger.reset(); bbc.debugger.run(); time.sleep(1.5); bbc.system.set_speed_multiplier(0.0)
    bbc.keyboard.type("*RUN "+name+"\r"); time.sleep(2.0)
    samples=[]
    for _ in range(3):
        bbc.debugger.stop(); samples.append((bbc.cpu.registers.pc, bbc.memory.address.peek[0xF4])); bbc.debugger.run(); time.sleep(0.1)
    bbc.debugger.stop()
    print("=== %s ===" % name)
    for pc,f4 in samples: print("  PC=%04X ROMSEL($F4)=%02X" % (pc,f4))
    print(dump_screen(bbc))
