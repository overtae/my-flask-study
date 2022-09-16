from ..db import db

followers = db.Table(
  'followers',
  db.Column('follower_id', db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True),
  db.Column('followed_id', db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True)
)

class UserModel(db.Model):
  __tablename__ = 'User'
  
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(80), nullable=False, unique=True)
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
  
  followed = db.relationship(
    'User',
    secondary=followers,
    primaryjoin=(followers.c.follower_id==id),
    secondaryjoin=(followers.c.followed_id==id),
    backref=db.backref('follower_set', lazy='dynamic'),
    lazy='dynamic'
  )
  
  def follow(self, user):
    if not self.is_following(user):
      self.followed.append(user)
      return self

  def unfollow(self, user):
    if self.is_following(user):
      self.followed.remove(user)
      return self

  def is_following(self, user):
    return self.followed.filter(followers.c.followed_id == user.id).count() > 0
  
  @classmethod
  def find_by_username(cls, username):
    return cls.query.filter_by(username=username).first()
  
  @classmethod
  def find_by_id(cls, id):
    return cls.query.filter_by(id=_id).first()
  
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()
    
  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()