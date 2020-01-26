from flask import Flask, render_template
import data

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 Not Found</h1>"

@app.errorhandler(500)
def server_error(e):
    return "<h1>Internal Server Error</h1>"

@app.route('/')
def main():
    keys=sorted(data.tours, key=lambda x: (data.tours[x]['price']))[:6]
    return render_template("index.html", tours = data.tours, departures=data.departures,
     keys=keys)

@app.route('/from/<direction>')
def direction(direction):
    
    tours = dict()
    pricemin = min(data.tours[tour]["price"] for tour in data.tours 
                    if data.tours[tour]["departure"] == direction)
    pricemax = max(data.tours[tour]["price"] for tour in data.tours 
                    if data.tours[tour]["departure"] == direction)
    nightsmin = min(data.tours[tour]["nights"] for tour in data.tours
                    if data.tours[tour]["departure"] == direction)
    nightsmax = max(data.tours[tour]["nights"] for tour in data.tours 
                    if data.tours[tour]["departure"] == direction)
    for tour in data.tours:
        if data.tours[tour]["departure"] == direction:
            tours[tour] = data.tours[tour]
    return render_template("direction.html", departure = data.departures[direction], 
    tours = tours, pricemin = pricemin, pricemax = pricemax, nightsmin = nightsmin, 
    nightsmax = nightsmax, departures=data.departures)

@app.route('/tours/', defaults={'id':1})
@app.route('/tours/<int:id>')
def tours(id):
    tour = data.tours[id]
    return render_template("tour.html", tour=tour, departures=data.departures)


if __name__ == '__main__':
    app.run()

