from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

RYU_REST_API = 'http://localhost:8080'

@app.route('/')
def index():
    try:
        switches = requests.get(f'{RYU_REST_API}/stats/switches').json()
        flows = {}
        for dpid in switches:
            flows[str(dpid)] = requests.get(f'{RYU_REST_API}/stats/flow/{dpid}').json().get(str(dpid), [])
        return render_template('index.html', flows=flows)
    except Exception as e:
        return render_template('index.html', error=str(e), flows={})

@app.route('/add', methods=['GET', 'POST'])
def add_flow():
    if request.method == 'POST':
        try:
            data = {
                "dpid": int(request.form['dpid']),
                "priority": int(request.form['priority']),
                "match": {
                    "in_port": int(request.form['in_port']),
                    "dl_src": request.form['dl_src'],
                    "dl_dst": request.form['dl_dst']
                },
                "actions": [
                    {
                        "type": "OUTPUT",
                        "port": int(request.form['out_port'])
                    }
                ]
            }
            response = requests.post(f'{RYU_REST_API}/stats/flowentry/add', data=json.dumps(data))
            flash('Règle ajoutée avec succès', 'success')
        except Exception as e:
            flash(f'Erreur : {e}', 'danger')
        return redirect(url_for('index'))
    return render_template('add_flow.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_flow():
    if request.method == 'POST':
        try:
            data = {
                "dpid": int(request.form['dpid']),
                "match": {
                    "in_port": int(request.form['in_port']),
                    "dl_src": request.form['dl_src'],
                    "dl_dst": request.form['dl_dst']
                }
            }
            response = requests.post(f'{RYU_REST_API}/stats/flowentry/delete', data=json.dumps(data))
            flash('Règle supprimée avec succès', 'success')
        except Exception as e:
            flash(f'Erreur : {e}', 'danger')
        return redirect(url_for('index'))
    return render_template('delete_flow.html')

if __name__ == '__main__':
    app.run(debug=True)
