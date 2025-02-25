import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

load_dotenv()

#crear instancia
app = Flask(__name__)

#Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Componentes(db.Model):
    __tablename__ = 'componentes'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String)
    tipo = db.Column(db.String)
    descripcion = db.Column(db.String)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'descripcion': self.descripcion
        }

#Ruta raiz
@app.route('/')
def index():
    #retornar 
    componentes = Componentes.query.all()
    return render_template('index.html', componentes = componentes)


if __name__ == '__main__':
    app.run(debug=True)