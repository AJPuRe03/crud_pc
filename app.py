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
    

@app.route('/componentes/new', methods=['GET','POST'])
def create_componente():
    if request.method == 'POST':
        #Agregar Componente
        id = request.form['id']
        nombre = request.form['nombre']
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']

        nvo_componente = Componentes(id=id, nombre=nombre, tipo=tipo, descripcion=descripcion)

        db.session.add(nvo_componente)
        db.session.commit()
    
        return redirect(url_for('index'))
    return render_template('create_componente.html')

#Eliminar componente
@app.route('/componentes/delete/<int:id>')
def delete_componente(id):
    componente = Componentes.query.get(id)
    if componente:
        db.session.delete(componente)
        db.session.commit()
    return redirect(url_for('index'))

#Actualizar componente
@app.route('/componentes/update/<int:id>', methods=['GET','POST'])
def update_componente(id):
    componente = Componentes.query.get(id)
    if request.method == 'POST':
        componente.nombre = request.form['nombre']
        componente.tipo = request.form['tipo']
        componente.descripcion = request.form['descripcion']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_componente.html', componente=componente)

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(debug=True)