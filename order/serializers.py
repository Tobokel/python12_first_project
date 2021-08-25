from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ('id', 'order')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    created_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        exclude = ('user', 'products')

    def create(self, validated_data):
        request = self.context.get('request')
        items = validated_data.pop('items')
        user = request.user
        order = Order.objects.create(user=user)
        total = 0
        for item in items:
            total += item['product'].price * item['quantity']
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     quantity=item['quantity']
                                     )
        order.total_sum = total
        order.save()
        return order
