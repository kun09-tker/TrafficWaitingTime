import logging

# =========================
# Setup logging
# =========================
logging.basicConfig(
    level=logging.DEBUG,   # mức thấp nhất hiển thị (DEBUG → INFO → WARNING → ERROR → CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()  # in ra console
        # logging.FileHandler("app.log")  # có thể bật nếu muốn lưu ra file
    ]
)

logger = logging.getLogger(__name__)


# =========================
# Wrapper functions
# =========================
def log_debug(message: str):
    """Ghi log mức DEBUG"""
    logger.debug(message)


def log_info(message: str):
    """Ghi log mức INFO"""
    logger.info(message)


def log_warning(message: str):
    """Ghi log mức WARNING"""
    logger.warning(message)


def log_error(message: str):
    """Ghi log mức ERROR"""
    logger.error(message)