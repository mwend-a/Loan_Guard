import jinja2

# Create jinja template object from file

template= jinja2.Environment(
    loader= jinja2.FileSystemLoader("./templates"),
    autoescape=jinja2.select_autoescape
).get_template("home.html")