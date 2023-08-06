from logging import getLogger

logger = getLogger(__name__)


def read_version(path):
    try:
        with open(path, encoding='utf-8') as f:
            version = f.readline().strip()
            logger.info('Current version: %s', version)

            if version.count('.') != 2:
                logger.warning('Version number is not in "major.minor.fix" format')

            return version
    except FileNotFoundError as err:
        logger.warning(err)

    return None
