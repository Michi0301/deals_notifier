# Generated by Django 3.2.9 on 2023-06-09 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_rm_unused_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('branch_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Posting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('posting_id', models.CharField(max_length=36)),
                ('product_id', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('branch_id', models.IntegerField()),
                ('image_url', models.TextField()),
                ('shipping_type', models.CharField(max_length=255)),
                ('shipping_cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deal_search.provider')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('product_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('search_type', models.CharField(max_length=10)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deal_search.provider')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='IndexedPosting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posting_id', models.CharField(max_length=255)),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deal_search.notification')),
            ],
        ),
        migrations.CreateModel(
            name='BranchSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deal_search.branch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.AddField(
            model_name='branch',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deal_search.provider'),
        ),
    ]
