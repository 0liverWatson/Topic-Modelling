import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
        data = pd.read_csv("C:/Users/Subhashree/Documents/data.csv")
        event_list = data.Group.unique()
        el = event_list.tolist()
        return render_template("map.html", event_list = el)

if __name__ == '__main__':
  app.run(host='0.0.0.0')