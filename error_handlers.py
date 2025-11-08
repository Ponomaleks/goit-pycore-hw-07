from colorama import Fore


class ValidationError(Exception):
    def __init__(self, message="Validation failed"):
        super().__init__(message)


class DataError(Exception):
    def __init__(self, message="Data error occurred"):
        super().__init__(message)


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return f"{Fore.RED}{str(e)}{Fore.RESET}"
        except DataError as e:
            return f"{Fore.RED}{str(e)}{Fore.RESET}"
        except ValueError:
            return f"{Fore.RED}Give me name and phone please.{Fore.RESET}"
        except IndexError:
            return f"{Fore.RED}Enter user name{Fore.RESET}"
        except KeyError:
            return f"{Fore.RED}Contact not found.{Fore.RESET}"

    return inner
