from http import client
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

@app.route("/")
def clients():

    f = open("data/clients.json", "r")
    clients_str = f.read()
    all_clients = json.loads(clients_str)     

    return render_template("clients.html", clients=all_clients)


@app.route("/clients/add", methods=['GET', 'POST'])
def create():

    f = open("data/clients.json", "r")
    clients_str = f.read()
    f.close()
    all_clients = json.loads(clients_str)

    next_id = 1
    if len(all_clients) > 0:
        next_id = all_clients[-1]["id"] + 1


    if request.method == 'POST':
        client_name = request.form["client_name"]

        if client_name == "":
            return "Name is required"

        all_clients.append(
            {
                "id": next_id,
                "name": client_name
            }
        )

        updated_clients = json.dumps(all_clients)
        f = open("data/clients.json", "w")
        f.write(updated_clients)
        f.close()

    return redirect("/")


@app.route("/clients/<id>")
def client(id):

    f = open("data/clients.json", "r")
    clients_str = f.read()
    f.close()
    all_clients = json.loads(clients_str)

    client_by_id = list(filter(lambda x: (x["id"] == int(id)), all_clients))
    client_by_id = client_by_id[0]

    return render_template("client.html", client=client_by_id)


@app.route("/clients/edit/<id>", methods=['GET', 'POST'])
def client_edit(id):

    f = open("data/clients.json", "r")
    clients_str = f.read()
    f.close()
    all_clients = json.loads(clients_str)

    client_by_id = list(filter(lambda x: (x["id"] == int(id)), all_clients))
    client_by_id = client_by_id[0]
    client_index = all_clients.index(client_by_id)

    if request.method == 'POST':
        client_name = request.form["client_name"]
        all_clients[client_index] = {"id": client_by_id["id"], "name": client_name }

        updated_clients = json.dumps(all_clients)
        f = open("data/clients.json", "w")
        f.write(updated_clients)
        f.close()

        return redirect('/')

    return render_template("edit.html", client_id=id, client=client_by_id)


@app.route("/clients/delete")
def client_delete():

    f = open("data/clients.json", "r")
    clients_str = f.read()
    f.close()
    all_clients = json.loads(clients_str)

    client_id = request.args.get("id")
    client_by_id = list(filter(lambda x: (x["id"] == int(client_id)), all_clients))
    client_by_id = client_by_id[0]
    client_index = all_clients.index(client_by_id)

    del all_clients[client_index]
    updated_clients = json.dumps(all_clients)

    f = open("data/clients.json", "w")
    f.write(updated_clients)
    f.close()

    return redirect("/")