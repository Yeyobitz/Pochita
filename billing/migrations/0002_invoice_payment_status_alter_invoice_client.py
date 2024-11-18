# Generated by Django 5.1.3 on 2024-11-18 06:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
        ('users', '0003_alter_client_id_alter_vet_id_pet'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='payment_status',
            field=models.CharField(choices=[('paid', 'Pagado'), ('pending', 'Pendiente'), ('overdue', 'Vencido')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='users.client'),
        ),
    ]