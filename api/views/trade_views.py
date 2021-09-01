from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from ..models.copy import Copy
from ..serializers import CopySerializer
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

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate Trade
        trade = get_object_or_404(Trade, pk=pk)
        # Check if user is the same as the request.user.id
        if not (request.user.id == trade.to_user.id):
            raise PermissionDenied('Unauthorized, you cannot update this trade')

        # Ensure the copies and sender/reciever remain the same
        request.data['trade']['to_user'] = trade.to_user.id
        request.data['trade']['from_user'] = trade.from_user.id
        request.data['trade']['copy_from'] = trade.copy_from.id
        request.data['trade']['copy_to'] = trade.copy_to.id
        # Validate updates with serializer
        data = TradeSerializer(trade, data=request.data['trade'], partial=True)
        print('this is the trade data', data)
        print('this is request data', request.data)
        if(request.data['trade']['status'] == 'approved'):
          if data.is_valid():
              # get the actual copies from the database
              c_from = get_object_or_404(Copy, pk=trade.copy_from.id)
              c_to = get_object_or_404(Copy, pk=trade.copy_to.id)

              # partial update on copies that changes ownership
              c_from_serial = CopySerializer(c_from, data={"owner": trade.to_user.id}, partial=True)
              c_to_serial = CopySerializer(c_to, data={"owner": trade.from_user.id}, partial=True)

              if c_from_serial.is_valid():
                print('c_from valid')
                c_from_serial.save()
              else:
                print('c_from failed valid')

              if c_to_serial.is_valid():
                print('c_to valid')
                c_to_serial.save()
              else:
                print('c_to failed valid')

              # Save & send a 204 no content
              data.save()
              return Response(status=status.HTTP_204_NO_CONTENT)
          # If the data is not valid, return a response with the errors
          return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        elif(request.data['trade']['status'] == 'declined'):
          if data.is_valid():
              data.save()
              return Response(status=status.HTTP_204_NO_CONTENT)
          return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        elif(request.data['trade']['status'] == 'pending'):
          if data.is_valid():
              data.save()
              return Response(status=status.HTTP_204_NO_CONTENT)
          return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
          return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

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
