import sqlalchemy as sa
from CheckList.repositories.user_repository import UserRepository
from CheckList.objects.user import User

engine = sa.create_engine("sqlite:///tasks.db")

ur = UserRepository(engine=engine)
ur.ensure_table_exists()

u = User(repository=ur, email_address="test@test.com", password_hash="blah")
u.save()

print(repr(ur.fetch(u.id)))

u.email_address = "changed@change.com"
u.save()

print(repr(ur.fetch(u.id)))



