from sqlalchemy.dialects.postgresql import UUID

from extensions.ext_database import db


class Balance(db.Model):
    __tablename__ = 'balances'
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='balance_pkey'),
        db.Index('balance_account_id_idx', 'account_id'),
    )

    id = db.Column(UUID, server_default=db.text('uuid_generate_v4()'))
    point = db.Column(db.Integer, nullable=False, default=0)
    account_id = db.Column(UUID, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.text('CURRENT_TIMESTAMP(0)'))
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.text('CURRENT_TIMESTAMP(0)'))


class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='order_pkey'),
        db.Index('order_account_id_idx', 'account_id'),
    )

    id = db.Column(UUID, server_default=db.text('uuid_generate_v4()'))
    currency = db.Column(db.Numeric(10, 4), nullable=False, default=0)
    point = db.Column(db.Integer, nullable=False, default=0)
    account_id = db.Column(UUID, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.text('CURRENT_TIMESTAMP(0)'))
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.text('CURRENT_TIMESTAMP(0)'))
