from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from django.contrib.auth import get_user_model

from apps.account.views import LoginView
from apps.category.models import Category
from apps.product.models import Product
from apps.product.views import ProductViewSet

User = get_user_model()

class ProductTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = self.setup_user()
        self.setup_category()
        self.access_token = self.setup_user_token()
        self.setup_product()

    def setup_category(self):
        Category.objects.create(name='category1')
        Category.objects.create(name='category2')
        Category.objects.create(name='category3')


    def setup_user(self):
        return User.objects.create_superuser('test@gmail.com', '1')



    def setup_product(self):
        product = [
            Product(owner=self.user, title='first product', category=Category.objects.first(),
                                   image=None, price=10.5, stock='in_stock'),
            Product(owner=self.user, title='second product', category=Category.objects.first(),
                                   image=None, price=10.5, stock='in_stock'),
            Product(owner=self.user, title='third product', category=Category.objects.first(),
                                   image=None, price=10.5, stock='in_stock')

        ]
        Product.objects.bulk_create(product)


    def setup_user_token(self):
        data = {
            'email': 'test@gmail.com',
            'password': '1'

        }
        request = self.factory.post('api/v1/account/login', data)
        view = LoginView.as_view()
        response = view(request)
        return response.data['access']


    def test_get_product(self):
        requests = self.factory.get('api/v1/product')
        view = ProductViewSet.as_view({'get': 'list'})
        response = view(requests)
        print(response)
        assert response.status_code == 200
        assert Product.objects.count() == 3


    def test_post_product(self):
        image = open('/home/adik/PycharmProjects/project/deploy2/media/products/Screenshot_from_2023-11-07_14-24-54.png', 'rb')
        data = {

            'owner': self.user.id,
            'category': Category.objects.first().slug,
            'title': 'test_post',
            'price': 20,
            'image': image,
            'stock': 'in_stock'

        }
        request = self.factory.post('api/v1/product/', data, HTTP_AUTHORIZATION='Bearer '+self.access_token)
        view = ProductViewSet.as_view({'post': 'create'})
        response = view(request)
        # print(response.status_code, response.data)
        assert response.status_code == 201

