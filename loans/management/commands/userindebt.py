import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from datetime import date
from loans.models import Loan
from users.models import User
from django.shortcuts import get_object_or_404


logger = logging.getLogger(__name__)


def get_late_users():
    list_loans = Loan.objects.filter(devolutions_date=date.today())

    for loan in list_loans:
        if not loan.copy.is_free:
            user = get_object_or_404(User, id=loan.user.id)
            user.situation = "debt"
            user.save()


class Command(BaseCommand):
    help = "Check debit users"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            get_late_users,
            trigger=CronTrigger(hour="*/18"),
            id="get_late_users",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
