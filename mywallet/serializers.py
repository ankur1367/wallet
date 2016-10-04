from .models import Wallet
from rest_framework import serializers


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wallet
        fields = ('title',)
