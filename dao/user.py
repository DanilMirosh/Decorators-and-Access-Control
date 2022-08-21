from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(User).get(bid)

    def get_all(self):
        return self.session.query(User).all()

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def create(self, data):
        ent = User(**data)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        user = self.get_one(rid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        if user_d.get("name"):
            user.name = user_d.get("name")
        if user_d.get("role"):
            user.role = user_d.get("role")
        if user_d.get("password"):
            user.password = user_d.get("password")

        self.session.add(user)
        self.session.commit()
