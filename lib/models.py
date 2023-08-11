from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


class Audition(Base):
    __tablename__ = "auditions"

    id = Column(Integer(), primary_key=True)
    actor = Column(String())
    location = Column(String())
    phone = Column(Integer())
    hired = Column(Boolean())

    role_id = Column(Integer(), ForeignKey("roles.id"))
    role = relationship("Role", back_populates="auditions")

    def call_back(self):
        self.hired = not self.hired

    def __repr__(self) -> str:
        return (
            f"<{self.actor}>"
            + f"<{self.location}>"
            + f"<{self.phone}>"
            + f"<{self.location}>"
            + f"<{self.hired}>"
        )


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer(), primary_key=True)
    character_name = Column(String())
    auditions = relationship("Audition", back_populates="role")

    @property
    def actors(self):
        return [audition.actor for audition in self.auditions]

    @property
    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        for audition in self.auditions:
            if audition.hired:
                return audition
        else:
            return "No actor has been hired for this role."

    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) > 1:
            return hired_auditions[1]
        else:
            return "no actor has been hired for understudy for this role."


# Sample roles
role1 = Role(character_name="King Lear")
role2 = Role(character_name="Macbeth")

# Sample auditions
audition1 = Audition(
    actor="John Doe", location="New York", phone=123456789, hired=False
)
audition2 = Audition(
    actor="Jane Smith", location="Los Angeles", phone=987654321, hired=True
)
audition3 = Audition(actor="Alice", location="Chicago", phone=123123123, hired=True)
role1.auditions.append(audition1)
role1.auditions.append(audition2)
role1.auditions.append(audition3)
# print(audition1.role())
# print(audition1.hired)
# audition1.call_back()
# print(audition1.hired)
# print(role1.auditions)
# print(role1.actors)
# print(role1.locations)
# print(role1.lead())
print(role1.understudy())
