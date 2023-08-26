from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer,primary_key=True)
    product_name = db.Column(db.String(100),unique=True)
    product_description = db.Column(db.String(100))
    product_price = db.Column(db.Integer)
    availability = db.Column(db.Integer)

    def __init__ (self,name,description,price,availability):
        self.product_name = name
        self.product_description = description
        self.product_price = price
        self.availability = availability
    
    def __repr__(self):
        return '<Product %r, %r>' % self.id, self.product_name
    
    def serialize(self):
        return {
            'product_id' : self.id,
            'product_name' : self.product_name,
            'product_description' :self.product_description,
            'product_price' : self.product_price,
            'availability' : self.availability,
        }
    
class Client(db.Model):
    __tablename__ = "clients"   

    id = db.Column(db.Integer,primary_key=True)
    client_name = db.Column(db.String(100),unique=False)
    client_email = db.Column(db.String(100),unique=False)
    client_address = db.Column(db.String(100),unique=False)

    def __init__ (self,name,email,address):
        self.client_name = name
        self.client_email = email
        self.client_address = address

    def __repr__(self):
        return '<Client %r, %r>' % self.id, self.client_name

    def serialize(self):
        return {
            'client_id' :   self.id,
            'client_name' : self.client_name,
            'client_email' :self.client_email,
            'client_address' : self.client_address,
        }

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer,primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    client_id = db.Column(db.Integer,db.ForeignKey('clients.id'),nullable=False)
    client = relationship("Client", foreign_keys=[client_id])
    order_status = db.Column(db.Integer)

    def __init__ (self,client_id,status):
        #self.order_date = date
        ecuador_tz = pytz.timezone('America/Guayaquil')
        current_time_ecuador = datetime.now(ecuador_tz)

        self.order_date = current_time_ecuador
        self.client_id = client_id
        self.order_status = status

    def __repr__(self):
        return '<Orders %r, %r, %r, %r>' % self.id, self.order_date, self.client_id, self.order_status

    def serialize(self):
        return {
            'Order_id' :   self.id,
            'Order_date' : self.order_date,
            'client_id' : self.client_id,
            'order_status' : self.order_status
        }

class Deliveries(db.Model):
    __tablename__ = "delivery"

    id = db.Column(db.Integer,primary_key=True)
    delivery_address = db.Column(db.String(100))
    delivery_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    delivery_status = db.Column(db.String(100))
    order_id = db.Column(db.Integer,db.ForeignKey('orders.id'),nullable=False,unique=True)
    order = relationship("Order", foreign_keys=[order_id])

    def __init__ (self,address,status,order_id):
        ecuador_tz = pytz.timezone('America/Guayaquil')
        current_time_ecuador = datetime.now(ecuador_tz)

        self.delivery_address = address
        self.delivery_date = current_time_ecuador
        self.delivery_status = status
        self.order_id = order_id

    def __repr__(self):
        return '<Shipping %r, %r, %r, %r, %r>' % self.id, self.delivery_address, self.delivery_date, self.delivery_status, self.order_id

    def serialize(self):
        return {
            'delivery_id' :   self.id,
            'delivery_address' : self.delivery_address,
            'delivery_date' : self.delivery_date,
            'delivery_status' :self.delivery_status,
            'order_id' :self.order_id,
        }

class DetailOrder(db.Model):
    __tablename__ = "detail_orders"
    
    id = db.Column(db.Integer,primary_key=True)
    order_id = db.Column(db.Integer,db.ForeignKey('orders.id'),nullable=False)
    order = relationship("Order", foreign_keys=[order_id])
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'),nullable=False)
    product = relationship("Product", foreign_keys=[product_id])
    detailorder_count = db.Column(db.Integer)
    detailorder_price_uni = db.Column(db.Integer)
    detailorder_price_total = db.Column(db.Integer)

    # Crea una restricción única para order_id y product_id
    __table_args__ = (
        db.UniqueConstraint('order_id', 'product_id', name='_order_product_uc'),
    )

    def __init__ (self,order_id,product_id,count,price_uni,price_total):
        self.order_id = order_id
        self.product_id = product_id
        self.detailorder_count = count
        self.detailorder_price_uni = price_uni
        self.detailorder_price_total = price_total

    def __repr__(self):
        #return '<DetailOrder %r, %r, %r, %r, %r, %r>' % self.id, self.order_id, self.product_id, self.detailorder_count, self.detailorder_price_uni, self.detailorder_price_total
        return f'<DetailOrder {self.id}, {self.order_id}, {self.product_id}, {self.detailorder_count}, {self.detailorder_price_uni}, {self.detailorder_price_total}>'

    def serialize(self):
        return {
            'detailorder_id' : self.id,
            'order_id' :   self.order_id,
            'product_id' : self.product_id,
            'detailorder_count' : self.detailorder_count,
            'detailorder_price_uni' :self.detailorder_price_uni,
            'detailorder_price_total' :self.detailorder_price_total,
        }


