from faker import Faker

fake = Faker("ru_RU")

def generate_user() -> dict:
    return{
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.unique.email(),
        "password": fake.password(length=12),
        "phone": fake.phone_number(),
    }