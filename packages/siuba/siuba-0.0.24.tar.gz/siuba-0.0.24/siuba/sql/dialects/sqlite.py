# sqlvariant, allow defining 3 namespaces to override defaults
from ..translate import SqlColumn, SqlColumnAgg, base_scalar, base_agg, base_nowin, SqlTranslator, win_agg
import sqlalchemy.sql.sqltypes as sa_types
from sqlalchemy import sql

# Custom dispatching in call trees ============================================

class SqliteColumn(SqlColumn): pass
class SqliteColumnAgg(SqlColumnAgg, SqliteColumn): pass

scalar = SqlTranslator(
        base_scalar,
        )

aggregate = SqlTranslator(
        base_agg
        )

window = SqlTranslator(
        # TODO: should check sqlite version, since < 3.25 can't use windows
        base_nowin,
        sd = win_agg("stddev")
        )

funcs = dict(scalar = scalar, aggregate = aggregate, window = window)

