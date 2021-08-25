from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from product.models import Product, ProductReview
from product.permissions import IsAuthorOrIsAdmin
from product.serializers import (ProductSerializer, ProductDetailsSerializer, CreateProductSerializer, ReviewSerializer)
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters


def test_view(request):
    return HttpResponse('Hello World')





@api_view(['GET'])
def products_list(request):
    products = Product.objects.all()

#product нам вернет список из экземпляров класса: [product1, product2, product3]

    serializer = ProductSerializer(products, many=True)
#     [{'id':1, 'title':..., 'description':..., 'price':...}]
    return Response(serializer.data)
# 2 вариант вьюшки
class ProductsListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        #     [{'id':1, 'title':..., 'description':..., 'price':...}]
        return Response(serializer.data)

# 3 вариант вьюшки
class ProductsListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailsView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer

class CreateProductView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer

class UpdateProductView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer

class DeleteProductView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer

# CRUD(Create, Retrieve, Update,    Delete)
#         POST    GET     PUT/PATCH   DELETE

class ProductFilter(filters.FilterSet):
    price_from = filters.NumberFilter('price', 'gte')
    price_to = filters.NumberFilter('price', 'lte')
    class Meta:
        model = Product
        fields = ('price_from', 'price_to')

# 5 действий можно заменить одной вьющкой:
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    # def create(self, request, *args, **kwargs):
    #     if not (request.user.is_authenticated and request.user.is_staff):
    #         return Response('Создавать продукты может только админ', status=403)
    #
    #     data = request.data
    #     serializer = self.get_serializer(data=data, context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     print(serializer.data)
    #     return Response(serializer.data, status=201)

    # api/v1/products/
    # api/v1/products/?price_from=10000&price_to=15000
    # фильтрация продуктов: 1 способ
    # def get_queryset(self):
        # queryset = super().get_queryset()
        # print(queryset)
        # print(self.request.query_params)
        # price_from = self.request.query_params.get('price_from')
        # price_to = self.request.query_params.get('price_to')
        # queryset = queryset.filter(price__gte=price_from, price__lte=price_to)
        # return queryset
    # 2 способ фильтрации через библиотеку:
    filter_backends = [filters.DjangoFilterBackend, rest_filters.SearchFilter, rest_filters.OrderingFilter]
    # filterset_fields = ('price')
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'price']
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        elif self.action == 'retrieve':
            return ProductDetailsSerializer
        return CreateProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []

    # api/v1/products/id/
    # api/v1/products/id/reviews/
    @action(['GET'], detail=True)
    def reviews(self, request, pk=None):
        product = self.get_object()
        # reviews = ProductReview.objects.filter(product=product)
        # тоже самое, что и навреху
        reviews = product.reviews.all()
        # [review1, review2]
        # [{}, {}]
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=200)


# создает отзыв только залогиненный пользователь
# редактировать или удалять может либо админ, либо автор
class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrIsAdmin()]
        return []
# TODO: спрятать все важные элементы в окружение
# TODO: Импорт, экспорт данных
# TODO: ограничение количества запросов

# TODO: ViewSet для отзывов, листинг будет в товарах, деталей нет
# TODO: Разобрать взимодействие всех компонентов
# TODO: Сделать обновление товара
# TODO: Удаление товара
# TODO: Отзывы
# TODO: Почитать что такое API (Application programming interface)
# TODO: Почитать MVC
# TODO: Создавать, редактировать и удалять продукты могут только админы (permission)
# TODO: Пагинация (разбивка листинга на страницы)
# TODO: Фильтрация
# TODO: Поиск продуктов по названию и описанию
# TODO: Тесты

# TODO: почитать обязательно django-rest-framework.org/api-guide/views/

# REST -архитектурный подход
# 1. Модель клиент- сервер (Серверная часть отделяется от клиентской)
# 2. Отсутсвие состояния
# 3. Кэширование (данные ответа хранятся в темплейте какое-то время)
# 4. Единообразие интерфейса:
# a. определение ресурсов-rest ресурсом может быть любой объект например: json, media, csv и т.д
# б. управление ресурсами через предстваление
# в. самодостаточные сообщения
# г. гипермедия
# 5. Слои
# 6. Код по требованию
#  'GET', отвечает за list (много объектов), retrieve (получаем один объект)
#  'POST', создание (create)
#  'PUT', редактирование (update)
#  'PATCH', частичное редактирование (partial update)
#  'DELETE' destroy (удаление)

#all() - выдает весь список записей объектов этого класса (список объектов модели)
# SELECT * FROM product;
#create() - создает новый объект
# INSERT INTO product ...

#Product.objects.update() - обновляет объекты
#UPDATE product...

# Product.objects.delete() - удаляет объекты
# DELETE FROM product;

# Product.objects.filter(условие)
# SELECT * FROM product WHERE условие;

#Операции сравнения
# Product.objects.filter(price=10000)
# SELECT * FROM product WHERE price = 10000

#'>'
# Product.objects.filter(price__gt=10000)
# SELECT * FROM product WHERE price > 10000;


#'<'
# Product.objects.filter(price__lt=10000)
# SELECT * FROM product WHERE price < 10000;

#'>='
# Product.objects.filter(price__gte=10000)
# SELECT * FROM product WHERE price >= 10000;

#'<='
# Product.objects.filter(price__lte=10000)
# SELECT * FROM product WHERE price <= 10000;

#BETWEEN
# Product.objects.filter(price__range=[50000, 80000])
# SELECT * FROM product WHERE price BETWEEN 50000 and 80000;

#IN
# Product.objects.filter(price__in=[50000, 80000])
# SELECT * FROM product WHERE price IN (50000, 80000);

#Like
#ILIKE

# 'work%' -начинается
# Product.objects.filter(title__startswith='Apple')
# SELECT * FROM product WHERE title LIKE '&Apple';
# Product.objects.filter(title__istartswith='Apple')
# SELECT * FROM product WHERE title ILIKE '&Apple';

#'%work'-заканчивается
# Product.objects.filter(title__endswith='GB')
# SELECT * FROM product where title like '%GB';
# Product.objects.filter(title__iendswith='GB')
# SELECT * FROM product where title ilike '%GB';

# '%work%'
# Product.objects.filter(title__contains='Samsung')
# SELECT * FROM product where title like '%GB%';
# Product.objects.filter(title__icontains='Samsung')
# SELECT * FROM product where title ilike '%GB%';

# 'work'
# Product.objects.filter(title__exact='Apple Iphone 12')
# SELECT * FROM product WHERE title LIKE 'Apple Iphone 12';
# Product.objects.filter(title__iexact='Apple Iphone 12')
# SELECT * FROM product WHERE title ILIKE 'Apple Iphone 12';

# Сортировка
#ORDER BY
# Product.objects.order_by('price')
# SELECT * FROM product ORDER BY price ASC;
# Product.objects.order_by('-price')
# SELECT * FROM product ORDER BY price DESC;

# Product.objects.order_by('-price', 'title')
# SELECT * FROM product ORDER BY price  title ASC;

#LIMIT
# Product.objects.all()[:2]
# SELECT * FROM product limit 2;

# Product.objects.all()[3:6]
# SELECT * FROM product LIMIT 3 OFFSET 3;

# Product.objects.first()
# SELECT* FROM products LIMIT 1;


#get() - возвращает один объект
# Product.objects.get(id=1)
# SELECT * FROM product WHERE id = 1;

# DoesNotExist - возникает, если по условию не найден ни один объект
# MultipleObjectsReturned - возникает, когда найдено больше одного объекта

#count() - возвращает количество результатов
# Product.objects.count()
# SELECT COUNT(*) FROM product;

# Product.objects.filter(...).count()
# SELECT COUNT (*) FROM product WHERE ...;

#exclude() -
# Product.objects.filter(price__gt=10000)
# SELECT * FROM product where price > 10000;
#
# Product.objects.exclude(price__gt=10000)
# SELECT * FROM product WHERE NOT price > 10000;

# QuerySet - список объектов модели (класс), все запросы которые мы писали выше

# HTTP методы ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')