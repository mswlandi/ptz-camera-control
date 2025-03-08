from flask import Flask, request

app = Flask(__name__)

@app.route('/<path:path>', methods=['GET'])
def print_path(path):
    if (path == 'favicon.ico'):
        return 'Favicon requested'
    
    print(f'\033[92m{path}\033[0m')
    return f'Requested path: {path}'

if __name__ == '__main__':
    app.run(debug=True)