from flask import Flask, request, redirect, url_for, send_file, render_template, make_response,flash
import colorgram, webcolors, os, time
from colormap import rgb2hex


app = Flask(__name__)

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(rgb):
    requested_colour = (rgb.r, rgb.g, rgb.b)
    hex_code = rgb2hex(rgb.r, rgb.g, rgb.b)
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name, hex_code


@app.route("/", methods=['GET', 'POST'])
def index():
    resp = make_response(render_template('index.html', title='Home'))
    return resp

@app.route("/upload/", methods=['POST'])
def upload():
    color_data = []
    if request.method == 'POST':
        f = request.files['file']

        colors = colorgram.extract(f, 6)
        for item in colors:
            actual_name, closest_name, hex_code = get_colour_name(item.rgb)
            proportion = str(format(item.proportion * 100, '.2f')) + '%'
            color_data.append({'name': closest_name, 'hex_approx': hex_code, 'hex_actual': webcolors.name_to_hex(closest_name), 'proportion': proportion})

    return render_template('index.html', data = color_data, title='Home')




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
