import time
import djclick as click
from fastutils import sysutils

from django_fastadmin.services import SimpleTaskService
from django_db_lock.client import get_default_lock_service

from django_mailcenter.models import MailForDelivery

@click.command()
@click.option("-n", "--number", type=int, default=10, help="How many tasks to fetch at one time.")
def sendmails(number):
    lock_service = get_default_lock_service()
    mail_delivery_service = SimpleTaskService(MailForDelivery, lock_service)
    worker = sysutils.get_worker_id("Django.Management.Commands.django-mailcenter-sendmails")
    while True:
        info = mail_delivery_service.do_tasks(worker, number)
        total = info["total"]
        print(info)
        if total < 1:
            break
        time.sleep(5)

if __name__ == "__main__":
    sendmails()
