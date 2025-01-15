from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from users.services import create_stripe_product, create_stripe_price, create_stripe_session
from course_platform.models import Course
from users.models import CustomUser, Payments
from users.serializers import UserSerializer, PaymentsSerializer, CustomsUserDetailSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save()


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('payment_method', 'paid_course', 'paid_lesson')
    ordering_fields = ('payment_date',)

    def create(self, request, *args, **kwargs):
        """Creates a new payment and interacts with Stripe."""
        amount = request.data.get("amount")
        product_name = request.data.get("product_name")
        course_id = request.data.get("course_id")

        if not product_name or amount is None:
            return Response(
                {"error": "Invalid input: product_name and amount are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if course_id:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Course ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = create_stripe_product(course)

            price = create_stripe_price(amount, product.id)

            session_id, session_url = create_stripe_session(price.id)

            payment = Payments.objects.create(
                user=request.user,
                payment_amount=amount,
                payment_method="Stripe",
                paid_course=course,
            )

            return Response(
                {"session_id": session_id, "payment_id": payment.id, "url": session_url},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomsUserViewSet(viewsets.ModelViewSet):
    """User view endpoint."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomsUserDetailSerializer


class CustomUserCreateAPIView(generics.CreateAPIView):
    """User creation endpoint."""
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
