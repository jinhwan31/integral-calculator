from flask import Flask, render_template, request, send_from_directory
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_integral():
    try:
        # 사용자 입력 받기
        expr_str = request.form['function']
        x_start = float(request.form['x_start'])
        x_end = float(request.form['x_end'])

        # SymPy로 수식 변환
        x = sp.symbols('x')
        expr = sp.sympify(expr_str)

        # 정적분 계산
        area = sp.integrate(expr, (x, x_start, x_end))

        # 그래프 생성 및 저장
        graph_path = os.path.join('static', 'images', 'integral_plot.png')
        plot_function_and_integral(expr, x, x_start, x_end, graph_path)

        return render_template('index.html', result=round(float(area), 4), graph_url=graph_path)

    except Exception as e:
        return render_template('index.html', error=str(e))

def plot_function_and_integral(expr, x, x_start, x_end, save_path):
    f = sp.lambdify(x, expr, "numpy")

    x_vals = np.linspace(x_start - 2, x_end + 2, 400)
    y_vals = f(x_vals)

    integral_expr = sp.integrate(expr, x)
    f_integral = sp.lambdify(x, integral_expr, "numpy")
    integral_vals = f_integral(x_vals)

    plt.figure(figsize=(6, 4))
    plt.plot(x_vals, y_vals, label=f'f(x) = {expr}', color='blue')
    plt.plot(x_vals, integral_vals, label=f"F(x) = ∫f(x)dx", linestyle='--', color='orange')
    plt.fill_between(x_vals, 0, y_vals, where=((x_vals >= x_start) & (x_vals <= x_end)), color='skyblue', alpha=0.4, label="적분 구간")
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.title("f(x)와 정적분 그래프")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)

    plt.savefig(save_path)
    plt.close()

if __name__ == '__main__':
    app.run(debug=True)
