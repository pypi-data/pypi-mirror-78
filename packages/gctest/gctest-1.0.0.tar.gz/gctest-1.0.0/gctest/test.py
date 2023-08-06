from flask import Flask


def main():
    app = Flask(__name__)
    @app.route('/')
    def index():
        return "hello! this is flask sample!!!"

    app.run(port=80)


if __name__ == '__main__':
    main()
