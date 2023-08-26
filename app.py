
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dbmodels import db, Product, Client, Order, Deliveries, DetailOrder
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir,'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

CORS(app)

with app.app_context():
    db.create_all()

@app.route ("/ping",methods=['GET'])
def pong():
    return{
        "message":"pong"
    }

# Funcion ver todos los productos
@app.route ("/products",methods=['GET'])
def products():
    return jsonify ([
        a_product.serialize() for a_product in Product.query.all()
    ])

#Funcion para ver solo un producto
@app.route("/products/<int:product_id>", methods=['GET'])
def get_product(product_id):
    a_product = Product.query.get_or_404(product_id)
    return jsonify(a_product.serialize())

# Funcion para crear producto
@app.route ("/products",methods=['POST'])
def new_product():
    data = request.json
    try:
        a_product = Product(
            data['name'],
            data['description'],
            data['price'],
            data['availability']
        )
        db.session.add(a_product)
        db.session.commit()
        return jsonify({"message": "success", "id":a_product.id}),200
    except Exception as ex:
        return 400, {
            "message": "No saved",
            'error': str(ex)
        }  
    
# funcion para actualizar producto
@app.route("/products/<int:product_id>", methods=['PUT'])
def update_product(product_id):
    data = request.json
    try:
        product = Product.query.get(product_id)

        if product is None:
            return jsonify({"message": "Product not found"}), 404
        
        if 'name' in data:
            product.product_name = data['name']
        if 'description' in data:
            product.product_description = data['description']
        if 'price' in data:
            product.product_price = data['price']
        if 'availability' in data:
            product.availability = data['availability']

        db.session.commit()

        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as ex:
        return jsonify({
            "message": "Update failed",
            'error': str(ex)
        }), 400

#Funcion para eliminar producto
@app.route("/products/<int:product_id>", methods=['DELETE'])
def delete_product(product_id):
    
    data = request.json
    # Verificar si todos los campos requeridos están presentes en la solicitud
    required_fields = ['availability']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    try:
        product = Product.query.get(product_id)

        if product is None:
            return jsonify({"message": "Product not found"}), 404
        
        product.availability = data['availability']
        db.session.commit()

        return jsonify({"message": "Product update successfully"}), 200
    except Exception as ex:
        return jsonify({
            "message": "Deletion failed",
            'error': str(ex)
        }), 400

# Funcion ver todos los clientes
@app.route ("/clients",methods=['GET'])
def Clients():
    return jsonify ([
        a_client.serialize() for a_client in Client.query.all()

    ])

#Funcion para ver solo un cliente
@app.route("/clients/<int:client_id>", methods=['GET'])
def get_client(client_id):
    a_client = Client.query.get_or_404(client_id)
    return jsonify(a_client.serialize())

# Funcion para crear cliente
@app.route ("/clients",methods=['POST'])
def new_client():
    data = request.json
    try:
        a_client = Client(
            data['name'],
            data['email'],
            data['address']
        )
        db.session.add(a_client)
        db.session.commit()
        return jsonify({"message": "success", "id":a_client.id}),200
    except Exception as ex:
        return 400, {
            "message": "No saved",
            'error': str(ex)
        }  

# funcion para actualizar cliente
@app.route("/clients/<int:client_id>", methods=['PUT'])
def update_client(client_id):
    data = request.json
    try:
        client = Client.query.get(client_id)

        if client is None:
            return jsonify({"message": "Client not found"}), 404
        
        if 'name' in data:
            client.client_name = data['name']
        if 'description' in data:
            client.client_email = data['email']
        if 'price' in data:
            client.client_address = data['address']

        db.session.commit()

        return jsonify({"message": "client updated successfully"}), 200
    except Exception as ex:
        return jsonify({
            "message": "Update failed",
            'error': str(ex)
        }), 400

#Funcion para eliminar cliente
@app.route("/clients/<int:client_id>", methods=['DELETE'])
def delete_client(client_id):
    try:
        client = Client.query.get(client_id)

        if client is None:
            return jsonify({"message": "client not found"}), 404

        db.session.delete(client)
        db.session.commit()

        return jsonify({"message": "Client deleted successfully"}), 200
    except Exception as ex:
        return jsonify({
            "message": "Deletion failed",
            'error': str(ex)
        }), 400

# Funcion ver todas las ordenes
@app.route ("/orders",methods=['GET'])
def Orders():
    return jsonify ([
        a_order.serialize() for a_order in Order.query.all()

    ])

#Funcion para ver una sola orden
@app.route("/orders/<int:order_id>", methods=['GET'])
def get_order(order_id):
    a_order = Order.query.get_or_404(order_id)
    return jsonify(a_order.serialize())

# Funcion para crear orden
@app.route ("/orders",methods=['POST'])
def new_order():
    data = request.json

    # Verificar si todos los campos requeridos están presentes en la solicitud
    required_fields = ['client_id', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
        
    try:
        client = db.session.query(Client).filter_by(id=data['client_id']).first()

        if client is None:
            return jsonify({"message": "client does not exist"}), 404
        
        a_order = Order(
            #order_date=data['date'],
            data['client_id'],
            data['status']
        )

        db.session.add(a_order)
        db.session.commit()

        return jsonify({"message": "Order created successfully"}),201
    except Exception as ex:
        return jsonify({
            "message": "Deletion failed",
            'error': str(ex)
        }), 400

# funcion para actualizar orden
@app.route("/orders/<int:order_id>", methods=['PUT'])
def update_order(order_id):
    data = request.json
    try:
        order = Orders.query.get(order_id)

        if order is None:
            return jsonify({"message": "Order not found"}), 404
        
        if 'date' in data:
            order.order_date = data['date']
        if 'client_id' in data:
            order.client_id = data['client_id']
        if 'status' in data:
            order.order_status = data['status']

        db.session.commit()

        return jsonify({"message": "order updated successfully"}), 200
    except Exception as ex:
        return jsonify({
            "message": "Update failed",
            'error': str(ex)
        }), 400

#Funcion para inactivar orden
@app.route("/orders/<int:order_id>", methods=['DELETE'])
def disable_order(order_id):
    try:
        order = Order.query.get(order_id)

        if order is None:
            return jsonify({"message": "order not found"}), 404

        order.order_status = 0
        db.session.commit()

        return jsonify({"message": "Disable order successfully"}), 200
    except Exception as ex:
        return jsonify({
            "message": "Deletion failed",
            'error': str(ex)
        }), 400

# Funcion ver todas los envios
@app.route ("/deliveries",methods=['GET'])
def get_Deliveries():
    return jsonify ([
        a_delivery.serialize() for a_delivery in Deliveries.query.all()
    ])

#Funcion para ver un solo envio por id_envio
@app.route("/deliveries/<int:delivery_id>", methods=['GET'])
def get_delivery(delivery_id):
    a_delivery = Deliveries.query.get_or_404(delivery_id)
    return jsonify(a_delivery.serialize())

# Funcion para crear envio
@app.route ("/deliveries",methods=['POST'])
def new_deliveries():
    data = request.json

    # Verificar si todos los campos requeridos están presentes en la solicitud
    required_fields = ['address', 'status', 'order_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
        
    try:
        order = db.session.query(Order).filter_by(id=data['order_id']).first()

        if order is None:
            return jsonify({"message": "order does not exist"}), 404
        
        a_delivery = Deliveries(
            #order_date=data['date'],
            data['address'],
            data['status'],
            data['order_id']
        )

        db.session.add(a_delivery)
        db.session.commit()

        return jsonify({"message": "Delivery created successfully"}),201
    except Exception as ex:
        return jsonify({
            "message": "Deletion failed",
            'error': str(ex)
        }), 400
    
#Funcion para cambiar estado de envio
@app.route("/deliveries/<int:delivery_id>", methods=['DELETE'])
def update_delivery(delivery_id):
    data = request.json

    # Verificar si todos los campos requeridos están presentes en la solicitud
    required_fields = ['status']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
        

    try:
        delivery = Deliveries.query.get(delivery_id)

        if delivery is None:
            return jsonify({"message": "delivery not found"}), 404

        delivery.delivery_status = data['status']
        db.session.commit()

        return jsonify({"message": "Delivery update successfully"}), 200
    except Exception as ex:
        return jsonify({
            "message": "Deletion failed",
            'error': str(ex)
        }), 400    

# Funcion ver todos los detalles de ordenes
@app.route ("/detailorders",methods=['GET'])
def get_DetailOrders():
    return jsonify ([
        a_detailorder.serialize() for a_detailorder in DetailOrder.query.all()
    ])

#Funcion para ver detalle de order por id_detailorder
@app.route("/detailorders/<int:detailorder_id>", methods=['GET'])
def get_detailOrders(detailorder_id):
    a_detailorder = DetailOrder.query.get_or_404(detailorder_id)
    return jsonify(a_detailorder.serialize())

# Funcion para crear detalle de orden
@app.route ("/detailorders",methods=['POST'])
def new_detailOrder():
    data = request.json

    # Verificar si todos los campos requeridos están presentes en la solicitud
    required_fields = ['order_id', 'product_id', 'count']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
        
    try:
        # Verificar si existe la orden y el producto
        order = Order.query.get(data['order_id'])
        product = Product.query.get(data['product_id'])

        if not order or not product:
            return jsonify({'error': 'Order or product not found'}), 404

        detailorder_count = data['count']

        # Obtener el precio unitario del producto
        detailorder_price_uni = product.product_price 

        existing_detail_order = DetailOrder.query.filter_by(order_id=data['order_id'], product_id=data['product_id']).first()

        # Si el detalle de orden ya existe, actualizarlo
        if existing_detail_order:

            countCurrent = existing_detail_order.detailorder_count
            countBefore =  detailorder_count - countCurrent 

            print("Cantidad actual:")
            print(existing_detail_order.detailorder_count)
            print(countBefore)

            if product.availability >= countBefore:

                existing_detail_order.detailorder_count = detailorder_count
                existing_detail_order.detailorder_price_uni = detailorder_price_uni 
                existing_detail_order.detailorder_price_total = detailorder_count * detailorder_price_uni

                # Resta cantidad disponible de producto
                product.availability = product.availability - countBefore

                db.session.commit()
                return jsonify({"message": "Order detail update successfully"}),201  
            else:
                return jsonify({"message": "Product not available in sufficient quantity for udpate"}),201  
            
        else:
            if product.availability < detailorder_count:
                return jsonify({'error': 'Product not available in sufficient quantity'}), 400

            a_detailorder = DetailOrder(
                data['order_id'],
                data['product_id'],
                count=detailorder_count,
                price_uni=detailorder_price_uni,
                price_total=detailorder_count * detailorder_price_uni
                )

            # Resta cantidad disponible de producto
            product.availability = product.availability - detailorder_count
            
            db.session.add(a_detailorder)

            db.session.commit()
            return jsonify({"message": "Order detail created successfully"}),201
    
    except Exception as ex:
        return jsonify({
            "message": "Deletion failed",
            'error': str(ex)
        }), 400

# Funcion para borrar producto  de orden
@app.route ("/detailorders",methods=['DELETE'])
def removeProductId_detailOrder():
    data = request.json

    # Verificar si todos los campos requeridos están presentes en la solicitud
    required_fields = ['order_id', 'product_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
        
    try:
        existing_detail_order = DetailOrder.query.filter_by(order_id=data['order_id'], product_id=data['product_id']).first()

        # Verifica que el producto y la orden exista
        if existing_detail_order:

            product = Product.query.get(data['product_id'])
            countCurrent = existing_detail_order.detailorder_count

            #Retorna cantidad de inventario del producto borrado
            product.availability = product.availability + countCurrent
            db.session.commit()

            #Elimina el registro de la orden
            db.session.delete(existing_detail_order)
            db.session.commit()

            return jsonify({"message": "Product removed from order successfully"}), 200
        
        else:

            return jsonify({"message": "Product could not be removed from the order"}), 400

    except Exception as ex:
        return jsonify({
            "message": "Deletion failed",
            'error': str(ex)
        }), 400

app.run(host="0.0.0.0", debug=True, port=9030)

