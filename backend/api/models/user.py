from ..db import db


followers = db.Table(
    'followers',
    # 나를 팔로우하는 사람들의 id
    db.Column('follower_id', db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True),
    # 내가 팔로우한 사람들의 id
    db.Column('followed_id', db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True)
)

class UserModel(db.Model):
    """
    Flastagram 사용자 모델
     
    username   : 사용자 이름, 80자 제한, 중복된 값을 가질 수 없음
    password   : 사용자 비밀번호, 80자 제한
    email      : 이메일, 중복된 값을 가질 수 없음
    created_at : 사용자가 가입한 날짜
    """
    __tablename__ = "User"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    followed = db.relationship(                             # 본인이 팔로우한 유저들
        'UserModel',                                        # User 모델 스스로를 참조
        secondary=followers,                                # 연관 테이블 이름을 지정
        primaryjoin=(followers.c.follower_id==id),          # followers 테이블에서 특정 유저를 팔로우하는 유저들을 찾음
        secondaryjoin=(followers.c.followed_id==id),        # followers 테이블에서 특정 유저가 팔로우한 모든 유저들을 찾음
        backref=db.backref('follower_set', lazy='dynamic'), # 역참조 관계 설정
        lazy='dynamic' 
    )
    
    def follow(self, user):
        """
        특정 사용자를 팔로우
        """
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        """
        특정 사용자를 언팔로우
        """
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        """
        현재 사용자가 특정 사용자를 팔로우하고 있는지에 대한 여부 반환 (True or False)
        """
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    @classmethod
    def find_by_username(cls, username):
        """
        데이터베이스에서 이름으로 특정 사용자 찾기
        """
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, id):
        """
        데이터베이스에서 id 로 특정 사용자 찾기
        """        
        return cls.query.filter_by(id=id).first()
    
    def save_to_db(self):
        """
        사용자를 데이터베이스에 저장
        """
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        """
        사용자를 데이터베이스에서 삭제
        """
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<User Object : {self.username}>'