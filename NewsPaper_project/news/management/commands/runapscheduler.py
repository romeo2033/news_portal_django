import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from ...jobs import weekly_digest

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Запускает планировщик задач"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_digest,
            trigger=CronTrigger(day_of_week="mon", hour="6", minute="30"),
            id="weekly_digest",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена задача weekly_digest")

        try:
            logger.info("Запуск планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка планировщика...")
            scheduler.shutdown()
            logger.info("Планировщик остановлен")
