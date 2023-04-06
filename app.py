from flask import Flask, render_template, request, redirect, url_for, flash, send_file, get_flashed_messages
import ezdxf
import time
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"

ALLOWED_EXTENSIONS_MODEL = {'dxf'}
ALLOWED_EXTENSIONS_POINTS = {'txt'}


def arquivo_permitido(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/processar", methods=["POST"])
def processar_arquivos():
    if request.method == "POST":
        model_file = request.files.get("model_file")
        points_file = request.files.get("points_file")

        if model_file and arquivo_permitido(model_file.filename,
                                            ALLOWED_EXTENSIONS_MODEL) and points_file and arquivo_permitido(
            points_file.filename, ALLOWED_EXTENSIONS_POINTS):
            model_filename = secure_filename(model_file.filename)
            points_filename = secure_filename(points_file.filename)
            model_file.save(os.path.join("uploads", model_filename))
            points_file.save(os.path.join("uploads", points_filename))

            # Processar os arquivos e criar o arquivo de saída
            output_filename = processar_blocos_cad(model_filename, points_filename)

            if output_filename:
                flash("Blocos CAD criados com sucesso.")
                return send_file(os.path.join("uploads", output_filename), as_attachment=True)
            else:
                flash("Ocorreu um erro ao criar os Blocos CAD.")
        else:
            flash("Arquivos inválidos. Verifique as extensões e tente novamente.")
    return redirect(url_for("index"))


def processar_blocos_cad(model_filename, points_filename):
    model_filepath = os.path.join("uploads", model_filename)
    points_filepath = os.path.join("uploads", points_filename)
    output_filename = "blocos.dxf"
    output_filepath = os.path.join("uploads", output_filename)

    try:
        doc = ezdxf.readfile(model_filepath)
        msp = doc.modelspace()

        with open(points_filepath, encoding='utf-8') as points_file:
            points = [tuple(map(float, line.strip().split(','))) for line in points_file]

        for point in points:
            msp.add_blockref('PT_E', point)

        doc.saveas(output_filepath)
        return output_filename

    except Exception as e:
        print(f"Erro ao processar arquivos: {e}")
        return None


if __name__ == "__main__":
    app.run(debug=True)
