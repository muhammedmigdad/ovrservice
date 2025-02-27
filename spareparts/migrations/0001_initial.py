# Generated by Django 5.1.4 on 2025-02-19 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.FloatField()),
            ],
            options={
                'verbose_name': 'cart item',
                'verbose_name_plural': 'cart items',
                'db_table': 'cart_item',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='CartTotal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_total', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('tax_charge', models.FloatField()),
            ],
            options={
                'verbose_name': 'carttotal',
                'verbose_name_plural': 'carttotals',
                'db_table': 'Customer_CartTotal',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('order_id', models.CharField(max_length=35)),
                ('sub_total', models.FloatField(default=0)),
                ('tax_charge', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('phone_number', models.BigIntegerField()),
                ('order_status', models.CharField(choices=[('IN', 'In Progress'), ('SH', 'Shipped'), ('DL', 'Delivered'), ('CN', 'Cancelled')], default='IN', max_length=25)),
                ('city', models.CharField(blank=True, max_length=25, null=True)),
                ('state', models.CharField(blank=True, max_length=25, null=True)),
                ('pincode', models.CharField(blank=True, max_length=25, null=True)),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'db_table': 'customers_order',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('amount', models.FloatField(default=0)),
            ],
            options={
                'verbose_name': 'order item',
                'verbose_name_plural': 'order items',
                'db_table': 'customers_order_item',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('regular_price', models.FloatField()),
                ('sale_price', models.FloatField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'items_product',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='ProductDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('regular_price', models.FloatField()),
                ('sale_price', models.FloatField(blank=True, null=True)),
                ('rating', models.FloatField(default=0)),
                ('stock', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'verbose_name': 'productdetail',
                'verbose_name_plural': 'productdetails',
                'db_table': 'items_productdetail',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='review')),
                ('rating', models.FloatField(default=0)),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'reviews',
                'db_table': 'customers_review',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='services/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(max_length=15)),
                ('details', models.TextField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'service_request',
                'verbose_name_plural': 'service_requests',
                'db_table': 'customers_service_request',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='store')),
            ],
            options={
                'verbose_name': 'store',
                'verbose_name_plural': 'stores',
                'db_table': 'store',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='StoreCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'store_category',
                'verbose_name_plural': 'store_categories',
                'db_table': 'store_category',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='StoreUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('storeuser_id', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'storeuser',
                'verbose_name_plural': 'storeusers',
                'db_table': 'storeusers_StoreUser',
                'ordering': ['-id'],
            },
        ),
    ]
