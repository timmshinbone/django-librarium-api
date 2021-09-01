from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from ..models.copy import Copy
# from ..serializers import CopySerializer, CopyReadSerializer
from ..models.trade import Trade
from ..serializers import TradeSerializer, TradeReadSerializer


class Trades(generics.ListCreateAPIView):
    serializer_class = TradeSerializer

    def get(self, request):
        """Index request"""
        # Get all the trades:
        trades = Trade.objects.all()

        data = TradeSerializer(trades, many=True).data
        print('THIS IS THE DATA', data)

        return Response({'trades': data})

    def post(self, request):
        """Create request"""
        print('this is the request', request.data['trade'])

        c_from_oid = Copy.objects.filter(id=request.data['trade']['copy_from'])[0].owner.id
        c_to_oid = Copy.objects.filter(id=request.data['trade']['copy_to'])[0].owner.id

        # print('copy_from', c_from[0].owner.id)
        # print('copy_to', c_to[0].owner.id)
        print('copy_from', c_from_oid)
        print('copy_to', c_to_oid)

        request.data['trade']['from_user'] = c_from_oid
        request.data['trade']['to_user'] = c_to_oid

        # ADD CHECK TO MAKE SURE COPY FROM IS OWNED BY CURRENT USER

        trade = TradeSerializer(data=request.data['trade'])

        if((c_from_oid == request.user.id) and (c_from_oid != c_to_oid)):
          if trade.is_valid():
            trade.save()
            return Response({'trade': trade.data}, status=status.HTTP_201_CREATED)
          return Response(trade.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
          raise PermissionDenied('Unauthorized, Cant trade away a copy that aint yours, and ya cant trade with yourself')


class TradeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        print('this is the request', request)
        # Locate the copy to show
        trade = get_object_or_404(Trade, pk=pk)

        # Run the data through the serializer so it's formatted
        data = TradeReadSerializer(trade).data
        # data['book'] = the_book
        return Response({'trade': data})

    # LAY DOWN SOME CODE FOR ACCEPT AND REJECT TRADES
    # DELETE REQUEST TO TAKE THE TRADE BACK SHOULD HAVE REQUEST OWNER PERMISSION ONLY
        # @user_passes_test(lambda u: u.is_superuser)
    def delete(self, request, pk):
        """Delete request"""
        # Locate book to delete
        trade = get_object_or_404(Trade, pk=pk)

        if((trade.from_user.id == request.user.id) or (request.user.is_superuser)):
          # Only delete if the user sent the trade
          trade.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
        else:
          raise PermissionDenied('Unauthorized, you do not have permission to delete this trade')
