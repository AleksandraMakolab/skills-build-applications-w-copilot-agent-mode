from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import settings

from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Usuń istniejących użytkowników
        User.objects.all().delete()

        # Przykładowe dane użytkowników
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': 'marvel'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'team': 'marvel'},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': 'dc'},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': 'dc'},
        ]
        for u in users:
            User.objects.create_user(username=u['username'], email=u['email'], password='password123')

        # Tworzenie kolekcji teams, activities, leaderboard, workouts
        db = connection.cursor().db_conn.client[settings.DATABASES['default']['NAME']]
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        teams = [
            {'name': 'marvel', 'members': ['ironman', 'captainamerica']},
            {'name': 'dc', 'members': ['batman', 'superman']},
        ]
        db.teams.insert_many(teams)

        activities = [
            {'user': 'ironman', 'activity': 'run', 'distance': 5},
            {'user': 'batman', 'activity': 'cycle', 'distance': 10},
        ]
        db.activities.insert_many(activities)

        leaderboard = [
            {'team': 'marvel', 'points': 100},
            {'team': 'dc', 'points': 90},
        ]
        db.leaderboard.insert_many(leaderboard)

        workouts = [
            {'user': 'superman', 'workout': 'pushups', 'reps': 50},
            {'user': 'captainamerica', 'workout': 'situps', 'reps': 40},
        ]
        db.workouts.insert_many(workouts)

        # Unikalny indeks na email w kolekcji users
        db['users'].create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('Baza octofit_db została wypełniona przykładowymi danymi.'))
