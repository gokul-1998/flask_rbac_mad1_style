
from flask_restful import Resource, Api, marshal, reqparse, fields, marshal_with

from database import AddProduct, DeleteCategory, DeleteProduct, EditCategory, ProductUpdate, addcart, cartProducts, \
    deleteProductCart, product, profileItems, updateQuantity, validateCategory_id, \
    validateCategory_name, validateProduct, Adminsignin, Managersignin, fetch_all_user, AddCategory, all_product, \
    validateProduct_name, fetch_category, fetch_category_unapproved, EditCategory_ia, EditCategory_name, \
    fetch_cat_by_id, get_all_prod_by_cat_id, validateCategoryApproved, fetch_pending_user, validateManager, deleteUser
from flask import abort, jsonify, request

from models import db, Product
# from task import send_welcome_msg, generate_csv

from flask_security import SQLAlchemySessionUserDatastore, Security, login_user, logout_user
from flask_security import current_user, auth_required, login_required, roles_required, roles_accepted,login_user, logout_user,auth_token_required

api = Api(prefix='/api')





class Homepage(Resource):
    def get(self):
        return {"hello": "World"}

user_data= reqparse.RequestParser()

user_data.add_argument('fname')
user_data.add_argument('lname')
user_data.add_argument('mobile')
user_data.add_argument('email')
user_data.add_argument('id')
user_fields= {
    'id': fields.Integer,
    'fname': fields.String,
    'lname': fields.String,
    'email': fields.String,
}

class UserApi(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self):
        # print(request.headers)
        # print(current_user)
        return marshal(fetch_pending_user(), user_fields)

    @marshal_with(user_fields)
    @auth_required('token')
    @roles_required('admin')
    def patch(self):
        args=user_data.parse_args()
        user_id=args['id']
        if validateManager(user_id):
            return {"message": "Manager verified"}
        else:
            return {"message": "Something went wrong"}

    @auth_required('token')
    @roles_required('admin')
    def delete(self):
        args=user_data.parse_args()
        user_id=args['id']
        if deleteUser(user_id):
            return {"message": "Requested Rejected"}
        else:
            return {"message": "Something went wrong"}



login_data= reqparse.RequestParser()

login_data.add_argument('email')
login_data.add_argument('password')

def get_user_roles(roles):
    return [role.name for role in roles]



#Admin Functionalities

cat=reqparse.RequestParser()
cat.add_argument('old_name')
cat.add_argument('new_name')
cat.add_argument('is_approved')

update_cat= reqparse.RequestParser()
update_cat.add_argument('old_name')
update_cat.add_argument('new_name')
update_cat.add_argument('is_approved')

cat_is_approved= reqparse.RequestParser()
cat_is_approved.add_argument('is_approved')

cat_name= reqparse.RequestParser()
cat_name.add_argument('old_name')
cat_name.add_argument('new_name')

catName={
    "oldName": fields.String,
    "newName": fields.String
}

cat_fields = {
    'name': fields.List(fields.Nested(catName)),
    'id': fields.Integer,
    'is_approved': fields.Integer
}
cat_is_approved_fields={
    'is_approved': fields.Integer
}
prod= reqparse.RequestParser()
prod.add_argument('prod_name')
prod.add_argument('mdate')
prod.add_argument('edate')
prod.add_argument('rate')
prod.add_argument('quantity')
prod.add_argument('cat_id')
# prod.add_argument('edit_prod')



class Category_Pending(Resource):
    @auth_required('token')
    @roles_accepted('admin', 'manager')
    def get(self):
        result=fetch_category_unapproved()
        # print(result)
        return jsonify(marshal(result, cat_fields))




class Category_resource(Resource):
    #@auth_required('token')
    #@roles_required('user')

    def get(self): #fetch all cat
        # print(current_user)
        result=fetch_category()
        # print(result)
        # print(jsonify(marshal(result, cat_fields)))
        return jsonify(marshal(result, cat_fields))

    @auth_required('token')
    @roles_accepted('admin', 'manager')
    def post(self):
        args=cat.parse_args()
        old_name = args['old_name']
        new_name = args['new_name']
        name = {
            "oldName": old_name,
            "newName": new_name
        }
        # print("sdcscsd", cat_name)
        is_approved=args['is_approved']
        if validateCategory_name(old_name, is_approved):

            return marshal( AddCategory(name, is_approved),cat_fields)
        else:
            return jsonify({"message": "something went wrong"})

class CategoryCRUD(Resource):
    @marshal_with(cat_fields)
    @roles_required('user')
    @auth_required('token')

    def get(self, id):
        return fetch_cat_by_id(id)

    @marshal_with(cat_fields)
    @auth_required('token')
    @roles_accepted('admin', 'manager')
    def put(self, id):
        args=update_cat.parse_args()
        old_name=args['old_name']
        new_name=args['new_name']
        name={
            "oldName": old_name,
            "newName": new_name
        }
        is_approved=args['is_approved']
        if validateCategory_id(id):
            return EditCategory(name, is_approved,id)
        else:
            return "Error"

    @marshal_with(cat_is_approved_fields)
    @auth_required('token')
    @roles_required('admin')
    def patch(self, id):
        args=cat_is_approved.parse_args()

        is_approved=args['is_approved']
        if validateCategory_id(id):
            return EditCategory_ia(is_approved,id)
        else:
            return "Error"

    # @marshal_with(catName)
    # def patch(self, id):
    #     args=cat_name.parse_args()
    #     old_name=args['old_name']
    #     new_name=args['new_name']
    #     name={
    #         "oldName": old_name,
    #         "newName": new_name
    #     }
    #     if validateCategory_id(id):
    #         return EditCategory(name,is_approved, id)

    @auth_required('token')
    @roles_accepted('admin', 'manager')
    def delete(self, id):
        if validateCategory_id(id):
            return DeleteCategory(id)
        else:
            return "Error"


prod_fields={
    'id': fields.Integer,
    'name': fields.String,
    'manufacture_date': fields.String,
    'expiry_date': fields.String,
    'rate_per_unit': fields.Float,
    'quantity': fields.Integer,
    'category_id': fields.Integer
}

class Product_API(Resource):
    @marshal_with(prod_fields)

    def get(self,cat_id):
        return get_all_prod_by_cat_id(cat_id)

    @marshal_with(prod_fields)
    @auth_required('token')
    @roles_required('manager')
    def post(self, cat_id):
        args=prod.parse_args()
        prod_name=args['prod_name']
        mdate=args['mdate']
        edate= args['edate']
        rate= args['rate']
        quantity= args['quantity']
        if validateCategoryApproved(cat_id):
            if validateProduct_name(prod_name):
                return AddProduct(prod_name, mdate, edate, rate, cat_id, quantity)
            else:
                return jsonify({"message": "something went wrong"})

class Products(Resource):
    @marshal_with(prod_fields)
    def get(self):
        return all_product()


class ProductCRUD(Resource):
    @marshal_with(prod_fields)
    def get(self, prod_id):
        return product(prod_id)

    @auth_required('token')
    @roles_required('manager')
    def put(self, prod_id):
        args=prod.parse_args()
        prod_name = args['prod_name']
        mdate = args['mdate']
        edate = args['edate']
        rate = args['rate']
        quantity = args['quantity']
        cat_id = args['cat_id']

        if validateProduct(prod_id):
            return ProductUpdate(prod_id, prod_name, mdate, edate, rate, quantity, cat_id)
        else:
            return "Error"

    @auth_required('token')
    @roles_required('manager')
    def delete(self, prod_id):
        if validateProduct(prod_id):
            return DeleteProduct(prod_id)
        else:
            return "Error"

cart_data=reqparse.RequestParser()
cart_data.add_argument('product_id')


cart_fields={
    "user_id": fields.Integer,
    "product_id": fields.Integer,
    "quantity": fields.Integer
}
class Cart(Resource):
    @auth_required('token')
    @roles_required('user')
    def get(self):
        from models import Cart, Product
        userid=current_user.id
        cart_items = db.session.query(Cart).filter_by(user_id=userid).all()
        # Fetch corresponding product details for cart items
        products_info = []
        for item in cart_items:
            product_info = db.session.query(Product).filter_by(id=item.product_id).first()
            if product_info:
                product_data = {
                    'product_id': item.product_id,
                    'user_id': item.user_id,
                    'name': product_info.name,
                    'manufacture_date': product_info.manufacture_date,
                    'expiry_date': product_info.expiry_date,
                    'rate_per_unit': product_info.rate_per_unit,
                    'quantity': product_info.quantity,
                    'cart_quantity': item.quantity
                }
                products_info.append(product_data)

        return products_info

    @marshal_with(cart_fields)
    @auth_required('token')
    @roles_required('user')
    def post(self):
        user_id=current_user.id
        args=cart_data.parse_args()
        product_id= args['product_id']

        return addcart(user_id, product_id)




cart_update=reqparse.RequestParser()
cart_update.add_argument('quantity')
class CartCRUD(Resource):



    @auth_required('token')
    @roles_required('user')
    def put(self, prod_id):
        userid=current_user.id
        args= cart_update.parse_args()
        quantity= args['quantity']

        updateQuantity(userid, prod_id, quantity)
        return "Quantity Updated"

    @auth_required('token')
    @roles_required('user')
    def delete(self, prod_id):
        userid=current_user.id
        deleteProductCart(userid, prod_id)
        return "Deleted successfully"

# product_name_field = fields.String(attribute=lambda x: x.name)
# export_details={
#     "product_name": product_name_field,
#     "user_id":fields.Integer,
#     "product_id":fields.Integer,
#     "quantity":fields.Integer,
#     "date_purchased": fields.String
# }
export_details = {
    "product_name": fields.String,
    "user_id": fields.Integer,
    "product_id": fields.Integer,
    "quantity": fields.Float,
    "date_purchased": fields.String
}
export_data= reqparse.RequestParser()
# export_data.add_argument()
class exports(Resource):
    # @auth_required('token')
    # @roles_required('manager')
    def get(self):
        data = generate_csv.delay()
        return "CSV file is being generated, you will receive a mail once done."

class Celery_API(Resource):
    def get(self):
        data = send_welcome_msg.delay("Hello Celery")
        return "Task completed"

class Buy(Resource):
    @auth_required('token')
    @roles_required('user')
    def get(self):
        userid=current_user.id
        profile_items = profileItems(userid)
        print(profile_items)
        resp=[]
        for product,profile in profile_items:
            print(product.name,product.rate_per_unit,profile.quantity,profile.date_purchased)
            resp.append({
                "product_name": product.name,
                "rate_per_unit": product.rate_per_unit,
                "quantity": profile.quantity,
                "date_purchased": profile.date_purchased
            })
        return jsonify(resp)
        

    @auth_required('token')
    @roles_required('user')
    def post(self):
        from database import buyAll
        userid=current_user.id
        if buyAll(userid):
            return jsonify({"message": "Bought successfully"})
        else:
            raise abort(400, "Something went wrong")

api.add_resource(Homepage,'/')
api.add_resource(UserApi, '/pending-managers')

api.add_resource(Category_Pending,'/pending-category')
api.add_resource(Category_resource, '/category') # get and post
api.add_resource(CategoryCRUD, "/category/<id>")

api.add_resource(Products, '/products')
api.add_resource(Product_API, '/product/cat/<int:cat_id>')
api.add_resource(ProductCRUD,'/product/<prod_id>')


api.add_resource(Cart, '/cart')
api.add_resource(CartCRUD, '/cart/<prod_id>')

api.add_resource(exports, "/export")
api.add_resource(Celery_API, "/celery")

api.add_resource(Buy, "/buy")
