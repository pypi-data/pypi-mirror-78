from app import db
from avatar_utils.db.mixins.time_cast import TimeCastMixin


class CreatedAtMixin:

    created_at = db.Column(db.DateTime(timezone=True),
                           default=TimeCastMixin.utc_now)
    updated_at = db.Column(db.DateTime(timezone=True),
                           default=TimeCastMixin.utc_now,
                           onupdate=TimeCastMixin.utc_now)
