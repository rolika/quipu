from pathlib import Path
import bottle
from quipu import Quipu

from szemely import Szemely


cwd = Path.cwd()  # current directory
html_path = cwd / "html"
img_path = cwd / "img"
css_path = cwd / "css"
db_path = cwd / "db"
tpl_path = cwd / "tpl"


btl = bottle.Bottle()
kipu = Quipu(db_path)


@btl.route("/")
def main():
    return bottle.static_file("index.html", root=html_path)


@btl.route("/img/<filename>")
def serve_image(filename):
    return bottle.static_file(filename, root=img_path)


@btl.route("/css/<filename>")
def serve_css(filename):
    return bottle.static_file(filename, root=css_path)


@btl.route("/insider")
def insider():
    return bottle.static_file("insider.html", root=html_path)


@btl.get("/insider/szemely")
def uj_szemely():
    req = bottle.request.query
    if req.save:
        del req["save"]
        szemely = Szemely(kon=kipu.kon, **req)
        uj_id = szemely.ment()
        return "<p>{} elmentve, {} azonosítószám alatt.</p>".format(str(szemely), uj_id)
    else:
        return bottle.static_file("szemelyform.html", root=html_path)


btl.run(reloader=True, debug=True)