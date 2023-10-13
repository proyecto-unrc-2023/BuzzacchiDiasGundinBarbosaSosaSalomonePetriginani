from flask import jsonify, request
from flask_restful import Resource
from api.games.board_schema import BoardSchema
from api.games.board_model import BoardModel
from api.games import api
from logic.board import Board
from api import db
import json

class BoardResource(Resource):
    def get(self):
        board_schema = BoardSchema()
        board = Board(50,50)
        board_json = board_schema.dump(board)

        return jsonify(board_json)

    def post(self):
        data = request.json

        board_data = {
            'rows': data.get('rows'),
            'columns': data.get('columns'),
            'board': data.get('board')
        }

        board_schema = BoardSchema()
        logic_board = Board(**board_schema.load(board_data))

        # Convertir logic Board a Board Model
        api_board = BoardModel(
            rows=logic_board.rows,
            columns=logic_board.columns,
            board=json.dumps(logic_board.board)  
        )

        db.session.add(api_board)
        db.session.commit()
        return jsonify({'success': 'true'})
    
api.add_resource(BoardResource, '/board')

# Hit endpoint with, and first board will be added to the DB:
# {
#     "board": [
#         [
#             [],
#             [
#                 {
#                     "level": 1,
#                     "life": 18,
#                     "position": [
#                         0,
#                         1
#                     ],
#                     "type": "FireCell"
#                 }
#             ]
#         ],
#         [
#             [],
#             []
#         ]
#     ],
#     "columns": 2,
#     "rows": 2
# }
#