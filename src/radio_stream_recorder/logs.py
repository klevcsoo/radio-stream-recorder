from config import AppConfig

C_WELCOME = "\x1b[1;37;40m"
C_HEADER = "\x1b[1;37m"
C_ERROR = "\x1b[1;31m"
C_INFO = "\x1b[1;34m"
C_RESET = "\x1b[0m"


def log_info(message):
    print(f"{C_INFO}[INFO]{C_RESET} {message}{C_RESET}")


def log_error(message):
    print(f"{C_ERROR}[ERROR]{C_RESET} {message}{C_RESET}")


def print_welcome_message(config: AppConfig):
    welcome_header = " RADIO STREAM RECORDER "
    cfg_header = " CONFIGURATION "
    width_multiplier = 1
    line_width = int(max(len(ln) for ln in f"{config}".splitlines()) * width_multiplier)
    shiftby = 1 if line_width % 2 == 0 else 0

    welcome_spacing = int(line_width / 2 - (len(welcome_header) / 2))
    print(C_WELCOME + "-" * (line_width - shiftby) + C_RESET)
    print(C_WELCOME + "|" + " " * (welcome_spacing - 1) + welcome_header + " " * (
            welcome_spacing - 1) + "|" + C_RESET)
    print(C_WELCOME + "-" * (line_width - shiftby) + C_RESET)

    print()

    cfg_header_spacing = int(line_width / 2 - (len(cfg_header) / 2))
    print(C_HEADER + "-" * cfg_header_spacing + cfg_header + "-" * cfg_header_spacing + C_RESET)
    print(config)
    print(C_HEADER + "-" * (line_width - 1) + C_RESET)

    print()

    if config.scheduler_start_at is None:
        log_info(
            f"Recording {C_HEADER}not scheduled{C_RESET}, beginning immediately")
    else:
        log_info(
            f"Recording {C_HEADER}scheduled for every day at {config.scheduler_start_at}{C_RESET}")

    if config.drive_service_account_path is None:
        log_info(
            f"{C_HEADER}Recordings won't be uploaded{C_RESET} (no service account)")
    else:
        log_info(
            f"{C_HEADER}Service account found{C_RESET}")

    if config.drive_keep_local_copy:
        log_info(f"Keeping local files")
    else:
        log_info(f"{C_HEADER}Not{C_RESET} keeping local files")

    print()
