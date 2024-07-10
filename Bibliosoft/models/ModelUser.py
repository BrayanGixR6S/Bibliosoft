from .entities.User import User


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT user_id, username, password, fullname FROM user WHERE username = %s",(user.username,))
            row = cursor.fetchone()
            if row != None:
                print(user.password)
                if User.check_password(row[2], user.password):
                    return row
                else:
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, username):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT user_Id, username, fullname FROM user WHERE username = %s ",(username,))
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)