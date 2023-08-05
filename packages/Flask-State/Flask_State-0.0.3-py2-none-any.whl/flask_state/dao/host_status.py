import logging
from ..models.console_host import ConsoleHost, db
from ..utils.date import get_current_ms, get_query_ms


def retrieve_host_status(days='1') -> list:
    """
    Query the status within the time period and flashback

    """
    target_time = get_current_ms() - get_query_ms(days)
    result = ConsoleHost.query.filter(ConsoleHost.ts > target_time).order_by(ConsoleHost.ts.desc()).all()
    return result


def retrieve_one_host_status() -> list:
    """
    Return to the latest status

    """
    result = ConsoleHost.query.order_by(ConsoleHost.id.desc()).first()
    return result


def create_host_status(kwargs):
    """
    Create a new record

    """
    try:
        console_host = ConsoleHost(**kwargs)
        db.session.add(console_host)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        raise e


def retrieve_host_status_yesterday() -> ConsoleHost:
    """
    Returns the closest time status between yesterday and the current

    """
    yesterday_ms = get_current_ms() - get_query_ms('1')
    delta_ms = yesterday_ms - 300000
    yesterday_console_host = ConsoleHost.query.filter(
        ConsoleHost.ts < yesterday_ms, ConsoleHost.ts > delta_ms).order_by(
        ConsoleHost.ts.desc()).first()
    return yesterday_console_host
