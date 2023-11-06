import logging
from functools import wraps
from flask import current_app
from flask_login import current_user

from extensions.ext_database import db
from libs.exception import BaseHTTPException
from models.account import Account, TenantAccountJoin
from models.billing import Balance, Order

DEFAULT_CHARGE_WEIGHT = 100
DEFAULT_CONSUMPTION_WEIGHT = 300


class InsufficientPointError(BaseHTTPException):
    error_code = 'insufficient_point'
    description = "Points is insufficient. Please contract admin to charge."
    code = 403


class BillingService:
    @staticmethod
    def create_balance(account_id: str):
        balance = Balance()
        balance.account_id = account_id
        db.session.add(balance)
        db.session.commit()

    @staticmethod
    def charge(account_id: str, currency: float):
        order = Order()
        order.account_id = account_id
        order.currency = currency
        order.point = BillingService.charge_point(currency)
        db.session.add(order)
        db.session.commit()

        db.session.query(Balance).filter_by(
            account_id=account_id
        ).update(
            {'point': Balance.point + order.point}
        )

    @staticmethod
    def charge_point(currency: float) -> int:
        charge_weight = current_app.config.get('CHARGE_WEIGHT', DEFAULT_CHARGE_WEIGHT)
        return int(currency * charge_weight)

    @staticmethod
    def consumption_point(total_price: float) -> int:
        consumption_weight = current_app.config.get('CONSUMPTION_WEIGHT', DEFAULT_CONSUMPTION_WEIGHT)
        return int(total_price * 7 * consumption_weight)

    @staticmethod
    def get_balance(account_id: str) -> Balance:
        balance = db.session.query(Balance).filter_by(
            account_id=account_id
        ).first()
        return balance


def points_required(view):
    @wraps(view)
    def decorated(*args, **kwargs):
        account, role = db.session.query(Account, TenantAccountJoin.role).join(
            TenantAccountJoin, Account.id == TenantAccountJoin.account_id
        ).filter(Account.id == current_user.id).first()

        if role != 'owner':
            balance = BillingService.get_balance(account.id)
            logging.info(f'{balance.point if balance else "NAN"} points remains for {account.id}')
            if not balance or balance.point <= 0:
                raise InsufficientPointError()

        return view(*args, **kwargs)

    return decorated
