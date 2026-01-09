import time
from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Train, Booking
from .serializers import UserSerializer, TrainSerializer, BookingSerializer
from .mongodb_utils import logs_collection  # Utility for MongoDB logging [cite: 9]
from rest_framework_simplejwt.tokens import RefreshToken

# --- Authentication APIs ---

class RegisterView(APIView):
    """Register a new user and return JWT tokens [cite: 12]"""
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """Login with email/password and return JWT tokens [cite: 13]"""
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# --- Train APIs ---

class TrainCreateView(APIView):
    """Admin only: Create or update train details [cite: 19]"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = TrainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TrainSearchView(APIView):
    """Search trains and log request to MongoDB [cite: 16, 18]"""
    def get(self, request):
        source = request.query_params.get('source')
        destination = request.query_params.get('destination')
        
        start_time = time.time()
        trains = Train.objects.filter(source__icontains=source, destination__icontains=destination)
        serializer = TrainSerializer(trains, many=True)
        execution_time = time.time() - start_time
        
        # Log to MongoDB [cite: 18]
        logs_collection.insert_one({
            "endpoint": "/api/trains/search/",
            "params": {"source": source, "destination": destination},
            "user_id": request.user.id if request.user.is_authenticated else "Anonymous",
            "execution_time": execution_time
        })
        
        return Response(serializer.data)

# --- Booking APIs ---

class BookingView(APIView):
    """Book seats and validate availability [cite: 21]"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        train_id = request.data.get('train_id')
        seats_to_book = int(request.data.get('seats_booked', 0))
        
        try:
            with transaction.atomic():
                train = Train.objects.select_for_update().get(id=train_id)
                if train.available_seats >= seats_to_book:
                    train.available_seats -= seats_to_book
                    train.save()
                    booking = Booking.objects.create(
                        user=request.user, train=train, seats_booked=seats_to_book
                    )
                    return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
                return Response({"error": "No seats available"}, status=status.HTTP_400_BAD_REQUEST)
        except Train.DoesNotExist:
            return Response({"error": "Train not found"}, status=status.HTTP_404_NOT_FOUND)

class UserBookingsView(APIView):
    """Return all bookings of the logged-in user [cite: 22]"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

# --- Analytics API ---

class AnalyticsView(APIView):
    """Aggregate MongoDB logs for top 5 routes [cite: 24]"""
    def get(self, request):
        pipeline = [
            {"$group": {"_id": {"s": "$params.source", "d": "$params.destination"}, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        results = list(logs_collection.aggregate(pipeline))
        formatted = [{"route": f"{i['_id']['s']} to {i['_id']['d']}", "count": i['count']} for i in results]
        return Response(formatted)