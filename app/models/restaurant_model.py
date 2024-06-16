from app.database import db

# Define la clase `Restaurant` que hereda de `db.Model`
# `Restaurant` representa la tabla `restaurants` en la base de datos
class Restaurant(db.Model):
    __tablename__ = "restaurants"

    # Define las columnas de la tabla `restaurants`
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Float, nullable=False)

    # Inicializa la clase `Restaurant`
    def __init__(self, name, address, city, phone, description, rating):
        self.name = name
        self.address = address
        self.city = city
        self.phone = phone
        self.description = description
        self.rating = rating

    # Guarda un restaurante en la base de datos
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Obtiene todos los restaurantes de la base de datos
    @staticmethod
    def get_all():
        return Restaurant.query.all()

    # Obtiene un restaurante por su ID
    @staticmethod
    def get_by_id(id):
        return Restaurant.query.get(id)

    # Actualiza un restaurante en la base de datos
    def update(self, name=None, address=None, city=None, phone=None, description=None, rating=None):
        if name is not None:
            self.name = name
        if address is not None:
            self.address = address
        if city is not None:
            self.city = city
        if phone is not None:
            self.phone = phone
        if description is not None:
            self.description = description
        if rating is not None:
            self.rating = rating
        db.session.commit()

    # Elimina un restaurante de la base de datos
    def delete(self):
        db.session.delete(self)
        db.session.commit()
