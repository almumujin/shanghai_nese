from exts import db


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    head_image = db.Column(db.Text, nullable=False)
    sex = db.Column(db.Boolean, nullable=False)
    nickname = db.Column(db.String(15), nullable=False)
    cid = db.relationship('Collection', backref='user')


class Passage(db.Model):
    __tablename__ = 'passage'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ptitle = db.Column(db.String(15), nullable=False)
    ppic = db.Column(db.Text, nullable=False)
    purl = db.Column(db.String(100), nullable=False)
    cpid = db.relationship('Collection', backref='passage')


class Collection(db.Model):
    __tablename__ = 'collection'
    cpid = db.Column(db.Integer, db.ForeignKey('passage.pid'), primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    date = db.Column(db.String(10), primary_key=True)


class Scene(db.Model):
    __tablename__ = 'scene'
    sid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sname = db.Column(db.String(20), nullable=False)
    spic = db.Column(db.String(100), nullable=False)


class Dialogue(db.Model):
    __tablename__ = 'dialogue'
    did = db.Column(db.Integer, primary_key=True, autoincrement=True)
    durl = db.Column(db.String(100), nullable=False)
    dlyric = db.Column(db.Text, nullable=False)
    dname = db.Column(db.String(20), nullable=False)
    dsid = db.Column(db.Integer, db.ForeignKey('scene.sid'))
# class ImageFile(db.Model):
#     __tablename__ = 'ImageFile'
#     id = db.Column(db.Integer, primary_key=True)
#     image_name = db.Column(db.String(30), index=True)
#     image = db.Column(db.LargeBinary(length=2048))

