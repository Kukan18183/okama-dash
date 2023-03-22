from app import app

server = app.server

if __name__ == "__main__":
    app.run(port=8050, debug=True, host="0.0.0.0", dev_tools_silence_routes_logging=True)
