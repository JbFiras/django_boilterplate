from django.core.management.base import BaseCommand


def success(cmd, msg):
    cmd.stdout.write(cmd.style.SUCCESS(msg))


def warn(cmd, msg):
    cmd.stdout.write(cmd.style.WARNING(msg))


def info(cmd, msg):
    """Print a styled WARNING message"""
    cmd.stdout.write(cmd.style.HTTP_NOT_MODIFIED(msg))


def error(cmd, msg):
    """Print a styled WARNING message"""
    cmd.stdout.write(cmd.style.NOTICE(msg))


class Command(BaseCommand):
    """
    Command Class

    custom command example
    """

    def handle(self, *args, **options):
        success(self, "custom command example")
