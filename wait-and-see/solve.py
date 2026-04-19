import xdis.load
import xdis.std as dis

ver, ts, magic, co, *_ = xdis.load.load_module('waiting_game_extracted/waiting_game.pyc')
dis.disassemble(co)
