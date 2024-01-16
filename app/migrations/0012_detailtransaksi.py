# Generated by Django 4.2.5 on 2023-12-22 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_delete_detailtransaksi'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailTransaksi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('harga_barang', models.IntegerField(null=True)),
                ('quantity_sales', models.IntegerField(null=True)),
                ('kode_barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.databarang')),
                ('kode_sales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.salestransactions')),
                ('kode_satuan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.satuanbarang')),
            ],
        ),
    ]