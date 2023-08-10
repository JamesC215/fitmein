# Generated by Django 4.2.3 on 2023-08-10 14:04

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0024_delete_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='chosen_activities',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('RU', 'Running'), ('WL', 'Weight Lifting'), ('GC', 'Group Classes'), ('BR', 'Bike Riding'), ('TE', 'Tennis'), ('SQ', 'Squash'), ('BA', 'Badminton'), ('SW', 'Swimming'), ('WA', 'Walking'), ('HI', 'Hiking'), ('P', 'Pilates'), ('SU', 'Surfing'), ('SK', 'Skateboarding')], max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='favorites',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('RU', 'Running'), ('WL', 'Weight Lifting'), ('GC', 'Group Classes'), ('BR', 'Bike Riding'), ('TE', 'Tennis'), ('SQ', 'Squash'), ('BA', 'Badminton'), ('SW', 'Swimming'), ('WA', 'Walking'), ('HI', 'Hiking'), ('P', 'Pilates'), ('SU', 'Surfing'), ('SK', 'Skateboarding')], max_length=50),
        ),
    ]