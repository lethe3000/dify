import logging

from events.message_event import message_was_created
from extensions.ext_database import db
from models.billing import Balance
from services.billing_service import BillingService


@message_was_created.connect
def handle(sender, **kwargs):
    logging.info(f'balance deduction, total_price={sender.total_price}, account={sender.from_account_id}')
    db.session.query(Balance).filter_by(
        account_id=sender.from_account_id
    ).update(
        {'point': Balance.point - BillingService.consumption_point(sender.total_price)}
    )
