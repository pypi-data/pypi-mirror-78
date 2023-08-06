import time
import json
from flask import Flask, request, render_template
from flask_restful import Api, Resource

idle_time = {}


class IDLEResource(Resource):
    def get(self, ):
        return "hello"

    def post(self):
        """Insert new task."""
        remote_ip = request.remote_addr
        request_body = request.get_data(as_text=True)
        print("{} sends the data:{}".format(remote_ip, request_body))
        data = json.loads(request_body)
        name = data.get("name").upper()
        t = int(data.get("idle_time"))
        idle_time[name] = {}
        idle_time[name]["time_h"] = str(t // 3600)
        idle_time[name]["time_m"] = str(t % 3600 // 60)
        idle_time[name]["time_s"] = str(t % 60)
        idle_time[name]["color"] = "#F0F8FF" if t <= 3600 else "#fc3"
        idle_time[name]["update_time"] = time.time()
        idle_time[name]["ip"] = remote_ip
        return "OK", 201


def main():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(IDLEResource, "/idle")

    @app.route('/')
    def index():
        ctime = time.time()
        for host in idle_time:
            if ctime - idle_time[host].get("update_time") > 60:
                idle_time[host]["time"] = "OFFLINE"
                idle_time[host]["color"] = "lightgray"
        return render_template("index.html", data=idle_time)

    app.run(port=80, debug=True, host="0.0.0.0", threaded=True)


if __name__ == "__main__":
    main()