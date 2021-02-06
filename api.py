from flask import Flask
from flask_restful import request, reqparse, abort, Api, Resource
import json

app = Flask(__name__)
api = Api(app)

Notebooks = {
    'Notebook1': {'task1': 'build an API','task2':'write documentation','task3':'test api'},
    'Notebook2': {'task1': 'make software','task2':'test it','task3':'publish it'},
}


def abort_if_note_doesnt_exist(notebook_id):
    if notebook_id not in Notebooks:
        abort(404, message="{} doesn't exist".format(notebook_id))

parser = reqparse.RequestParser()
parser.add_argument('task')

class Note(Resource):
    def get(self, notebook_id):
        abort_if_note_doesnt_exist(notebook_id)
        return Notebooks[notebook_id],200

    def delete(self, notebook_id):
        print(notebook_id)
        abort_if_note_doesnt_exist(notebook_id)
        del Notebooks[notebook_id]
        return '', 204



class BookList(Resource):
    def get(self):
        return Notebooks,200
        

class addNote(Resource):
    def post(self):
        ndata=request.json
        note_id=request.args.get('note')
        if(note_id in Notebooks.keys()):
            abort(404,message="Invalid Input")
        Notebooks[note_id]={}
        Notebooks[note_id].update(ndata)
        return note_id,201


api.add_resource(BookList, '/Notebooks')
api.add_resource(Note, '/Notebooks/<notebook_id>')
api.add_resource(addNote,'/Notebooks/Add')


if __name__ == '__main__':
    app.run(debug=True)