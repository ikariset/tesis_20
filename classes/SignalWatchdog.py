import signal


class SignalWatchdog:
    def __init__(self, recovery_class):
        signal.signal(signal.SIGHUP, recovery_class)
        signal.signal(signal.SIGINT, recovery_class)
        signal.signal(signal.SIGQUIT, recovery_class)
        signal.signal(signal.SIGILL, recovery_class)
        signal.signal(signal.SIGTRAP, recovery_class)
        signal.signal(signal.SIGABRT, recovery_class)
        signal.signal(signal.SIGBUS, recovery_class)
        signal.signal(signal.SIGFPE, recovery_class)
        signal.signal(signal.SIGKILL, recovery_class)
        signal.signal(signal.SIGUSR1, recovery_class)
        signal.signal(signal.SIGSEGV, recovery_class)
        signal.signal(signal.SIGUSR2, recovery_class)
        signal.signal(signal.SIGPIPE, recovery_class)
        signal.signal(signal.SIGALRM, recovery_class)
        signal.signal(signal.SIGTERM, recovery_class)