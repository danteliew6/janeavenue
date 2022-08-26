from src.splitbill import db


class User(db.Model):
    # Start of DB model
    __tablename__ = 'users'
    __mapper_args__ = {'polymorphic_identity': 'users'}
    __table_args__={'mysql_engine':'InnoDB', 'mysql_auto_increment': '1'}

    bid = db.Column(db.Integer(), primary_key = True)
    id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    name = db.Column(db.String(50))
    to_pay = db.Column(db.Float())


    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result


        
