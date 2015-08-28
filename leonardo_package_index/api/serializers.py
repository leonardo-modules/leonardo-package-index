from rest_framework import serializers

from leonardo_package_index.models import Package, Category


class PackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
