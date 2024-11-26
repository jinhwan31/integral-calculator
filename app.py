from flask import Flask, render_template, request
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            expr_str = request.form["function"]
            x_start = float(request.form["x_start"])
            x_end = float(request.form["x_end"])

            x = sp.symbols("x")
            expr = sp.sympify(expr_str)
            result = sp.integrate(expr, (x, x_start, x_end))
        except Exception as e:
            result = f"오류 발생: {e}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

