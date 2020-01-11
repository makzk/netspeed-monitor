from flask import Flask, render_template, jsonify

from lib.speedtest_result import SpeedtestResult
from lib.common import size_scale as size_scale

app = Flask(__name__)


@app.route('/')
def hello_world():
    sp_results = SpeedtestResult.get(16)
    for i, result in enumerate(sp_results):
        if len(sp_results) <= (i + 1):
            continue

        result.add_comparison(sp_results[i+1])

    return render_template('results.html', results=sp_results[:15])


@app.route('/api/results')
def results():
    sp_results = SpeedtestResult.get(16)
    for i, result in enumerate(sp_results):
        if len(sp_results) <= (i + 1):
            continue

        result.add_comparison(sp_results[i+1])

    return jsonify([r.data for r in sp_results[:15]])


@app.template_filter()
def size_scaler(val):
    return size_scale(val)


if __name__ == '__main__':
    app.run()
