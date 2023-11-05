
from marshmallow import Schema, fields, post_dump
from logic.cell import FireCell, IceCell

class HealingAreaSchema(Schema):
    positions = fields.List(fields.Tuple((fields.Int(), fields.Int())))
    duration = fields.Int()
    healing_rate = fields.Int()
    affected_cell_type = fields.Method("get_affected_cell_type", "load_affected_cell_type")

    #Ty gpt for the code to pass "affected_cell_type\": \"<class 'logic.cell.FireCell'>\" to a correct string representation in affected_cell_type
    def get_affected_cell_type(self, obj):
        return obj.affected_cell_type.__name__ if hasattr(obj.affected_cell_type, '__name__') else obj.affected_cell_type

    def load_affected_cell_type(self, value):
        if value == "IceCell":
            return IceCell
        elif value == "FireCell":
            return FireCell
        return value

    @post_dump(pass_original=True)
    def clean_up(self, data, original_data, **kwargs):
        if 'affected_cell_type' in data and isinstance(data['affected_cell_type'], str):
            if data['affected_cell_type'].startswith("<class '"):
                class_name = data['affected_cell_type'].split("'")[1].split(".")[-1]
                data['affected_cell_type'] = class_name
        return data