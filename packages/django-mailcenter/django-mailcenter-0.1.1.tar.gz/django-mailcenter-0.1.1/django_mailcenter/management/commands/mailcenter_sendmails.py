import time
import djclick as click
from fastutils import sysutils

from django_mailcenter.models import MailForDelivery

@click.command()
@click.option("-n", "--number", type=int, default=10, help="Fetch tasks to do at one time.")
def sendmails(number):
    worker = sysutils.get_worker_id("Django.Management.commands.Mailcenter.Sendmails")
    while True:
        info = MailForDelivery.do_tasks(worker, number)
        total = info["total"]
        print(info)
        if total < 1:
            break
        time.sleep(5)

if __name__ == "__main__":
    sendmails()
