from flask_server import app

with app.app_context():
    print('LOADING START')
    from term_loading import load_index, load_url_map
    load_index()
    load_url_map()
    print('LOADING DONE')

def run():
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    run()