from werkzeug.security import check_password_hash, generate_password_hash
from hashlib import scrypt

class User():

   def __init__(self, user_id, username, password, fullname="") -> None:
      self.user_id = user_id
      self.username = username
      self.password = password
      self.fullname = fullname


   @classmethod
   def check_password(self, hashed_password,passwords):
      return check_password_hash(hashed_password, passwords)

   def create_password(self, password):
      return generate_password_hash(password, method='scrypt',salt_length=16);