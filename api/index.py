import os
from flask import Flask, request, send_file, render_template
import markdown
from xhtml2pdf import pisa
import io
from xhtml2pdf.files import pisaFileObject

app = Flask(__name__)
a = os.getcwd()
style = """<style type="text/css">
    body {font-family: STSong-Light, Times New Roman; word-wrap: break-word; word-break: normal; white-space: pre-wrap; -pdf-word-wrap: CJK;}
    </style>"""

@app.route('/')
def convert_page():
    return render_template("index.html")

@app.route('/upload',methods=['POST','GET'])
def upload():
    print(request.args)
    fila = io.BytesIO()
    f = request.files['file'].read()
    fp = str(f, encoding="utf-8")
    html = markdown.markdown(fp)+style
    # print(html)
    pisaFileObject.getNamedFile = lambda self: self.uri
    pisa_stats = pisa.CreatePDF(html, dest=fila, encoding='utf-8')
    # print(fila.getvalue())
    # print(pisa_stats.err)
    # pisa.showLogging()
    # with open("a.html","wt", encoding="utf-8") as g:
    #     g.write(html)
    # with open("a.pdf","wb") as g:
    #     g.write(fila.getvalue())
    fila.seek(0)
    return send_file(fila, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)