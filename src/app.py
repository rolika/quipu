from pathlib import Path
import bottle


btl = bottle.Bottle()

cwd = Path.cwd()  # current directory
html_path = cwd / "html"
img_path = cwd / "img"
css_path = cwd / "css"
tpl_path = cwd / "tpl"


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


btl.run(reloader=True, debug=True)