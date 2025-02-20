from flaskblog import app


if __name__ == "__main__":
    app.run(debug=True,use_reloader=True) 







'''
agar command line se add karna hai data tho

from flaskblog import db
db.create_all()
from blog import User,Post
user1 = User(username='admin',email='admin@blog.com',password='password')
db.session.add(user1)
db.session.commit()
User.query.all()
User.query.first()   #it will only give first value
User.query.filter_by(username='admin').all()  #it will give all the username with admin
User.query.filter_by(username='admin').first()  #it will give first occurence of the username admin
user = User.query.filter_by(username='admin').first()
user.id  #it will provide id
user = User.query.get(1)
user
db.drop_all()  #that will drop all the data from our database
'''


'''
Hashing is a mathematical process that converts data into a string of characters that is difficult to reverse

for flask we use bcrypt for hashing

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()  #creating instance of Bycrpt
bcrypt.generate_password_hash('testing')
>>>b'$2b$12$GnxIcD77dRqK8O4k0qfrRujc1UIHfrHlXGAiJfts6RX8TzAznbqzq'  # idar starting mein b matlab ye byte mein hai

bcrypt.generate_password_hash('testing').decode('utf-8')  #tho starting ka b hat jayega

hashed_pw = bcrypt.generate_password_hash('testing').decode('utf-8')

bcrypt.check_password_hash(hashed_pw,'testing')  #to check password correct hai ki nhi
>>>True
'''

'''
from itsdangerous import URLSafeTimedSerializer as Serializer
ye hamlog reset password vagere ke liye use karte hai
'''