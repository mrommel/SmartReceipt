# Generated by Django 3.0.4 on 2020-06-16 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0018_auto_20151212_1708'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='receiptcategory',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='receiptcategoryrelation',
            options={'ordering': ['receipt__name']},
        ),
        migrations.AlterField(
            model_name='receipt',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/receipts'),
        ),
        migrations.AlterField(
            model_name='receiptcategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/category'),
        ),
        migrations.RenameModel(
            old_name='IntegrientType',
            new_name='IngredientType',
        ),
        migrations.RenameModel(
            old_name='Integrient',
            new_name='Ingredient',
        ),
        migrations.RenameModel(
            old_name='ReceiptIntegrientRelation',
            new_name='ReceiptIngredientRelation',
        ),
    ]
