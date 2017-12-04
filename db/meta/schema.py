from sqlalchemy.sql.functions import FunctionElement
from sqlalchemy.types import DateTime


class utcnow(FunctionElement):
    key = 'utcnow'
    type = DateTime(timezone=True)


@compiles(utcnow)
def _default_utcnow(element, compiler, **kw):
    """default compilation handler.

    Note that there is no SQL "utcnow()" function; this is a
    "fake" string so that we can produce SQL strings that are dialect-agnostic,
    such as within tests.

    """
    return "utcnow()"
    

@compiles(utcnow, 'sqlite')
def _sqlite_utcnow(element, compiler, **kw):
    """SQLite-specific compilation handler."""
    return "datetime('now', 'utc')"


@event.listens_for(Table, "after_parent_attach")
def timestamp_cols(table, metadata):
    from .base import Base

    if metadata is Base.metadata:
        table.append_column(
            Column('created_at',
                        DateTime(timezone=True),
                        nullable=False, default=utcnow())
        )
        table.append_column(
            Column('updated_at',
                        DateTime(timezone=True),
                        nullable=False,
                        default=utcnow(), onupdate=utcnow())
        )

