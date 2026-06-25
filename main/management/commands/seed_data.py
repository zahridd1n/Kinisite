from django.core.management.base import BaseCommand
from main.models import Category, Actor, Rejissor
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Seed database with 10 genres, 10 actors and 10 directors'

    def handle(self, *args, **kwargs):
        # Create media directories if they don't exist
        categories_dir = os.path.join(settings.MEDIA_ROOT, 'categories')
        actors_dir = os.path.join(settings.MEDIA_ROOT, 'rejissors')
        
        os.makedirs(categories_dir, exist_ok=True)
        os.makedirs(actors_dir, exist_ok=True)

        # 10 Genres with sample data
        genres_data = [
            {"name": "Action", "icon": "categories/action.jpg"},
            {"name": "Comedy", "icon": "categories/comedy.jpg"},
            {"name": "Drama", "icon": "categories/drama.jpg"},
            {"name": "Horror", "icon": "categories/horror.jpg"},
            {"name": "Romance", "icon": "categories/romance.jpg"},
            {"name": "Sci-Fi", "icon": "categories/scifi.jpg"},
            {"name": "Thriller", "icon": "categories/thriller.jpg"},
            {"name": "Adventure", "icon": "categories/adventure.jpg"},
            {"name": "Animation", "icon": "categories/animation.jpg"},
            {"name": "Fantasy", "icon": "categories/fantasy.jpg"},
        ]

        # 10 Actors with sample data
        actors_data = [
            {"name": "Robert Downey Jr.", "photo": "rejissors/robert.jpg", "year": 1965},
            {"name": "Scarlett Johansson", "photo": "rejissors/scarlett.jpg", "year": 1984},
            {"name": "Leonardo DiCaprio", "photo": "rejissors/leonardo.jpg", "year": 1974},
            {"name": "Angelina Jolie", "photo": "rejissors/angelina.jpg", "year": 1975},
            {"name": "Brad Pitt", "photo": "rejissors/brad.jpg", "year": 1963},
            {"name": "Tom Cruise", "photo": "rejissors/tom.jpg", "year": 1962},
            {"name": "Jennifer Lawrence", "photo": "rejissors/jennifer.jpg", "year": 1990},
            {"name": "Dwayne Johnson", "photo": "rejissors/dwayne.jpg", "year": 1972},
            {"name": "Emma Stone", "photo": "rejissors/emma.jpg", "year": 1988},
            {"name": "Chris Evans", "photo": "rejissors/chris.jpg", "year": 1981},
        ]

        # 10 Directors with sample data
        directors_data = [
            {"name": "Christopher Nolan", "photo": "rejissors/nolan.jpg", "year": 1970},
            {"name": "Steven Spielberg", "photo": "rejissors/spielberg.jpg", "year": 1946},
            {"name": "Quentin Tarantino", "photo": "rejissors/tarantino.jpg", "year": 1963},
            {"name": "Martin Scorsese", "photo": "rejissors/scorsese.jpg", "year": 1942},
            {"name": "James Cameron", "photo": "rejissors/cameron.jpg", "year": 1954},
            {"name": "Ridley Scott", "photo": "rejissors/scott.jpg", "year": 1937},
            {"name": "David Fincher", "photo": "rejissors/fincher.jpg", "year": 1962},
            {"name": "Denis Villeneuve", "photo": "rejissors/villeneuve.jpg", "year": 1967},
            {"name": "Greta Gerwig", "photo": "rejissors/gerwig.jpg", "year": 1983},
            {"name": "Jordan Peele", "photo": "rejissors/peele.jpg", "year": 1979},
        ]

        # Add Genres
        for genre_data in genres_data:
            genre, created = Category.objects.get_or_create(
                name=genre_data["name"],
                defaults={"icon": genre_data["icon"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created genre: {genre.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Genre already exists: {genre.name}'))

        # Add Actors
        for actor_data in actors_data:
            actor, created = Actor.objects.get_or_create(
                name=actor_data["name"],
                defaults={
                    "photo": actor_data["photo"],
                    "year": actor_data["year"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created actor: {actor.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Actor already exists: {actor.name}'))

        # Add Directors
        for director_data in directors_data:
            director, created = Rejissor.objects.get_or_create(
                name=director_data["name"],
                defaults={
                    "photo": director_data["photo"],
                    "year": director_data["year"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created director: {director.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Director already exists: {director.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with 10 genres, 10 actors and 10 directors'))
