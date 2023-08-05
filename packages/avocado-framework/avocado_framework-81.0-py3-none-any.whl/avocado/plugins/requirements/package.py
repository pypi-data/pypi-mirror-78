from avocado.utils.software_manager import SoftwareManager


def check(requirement):
    """Requirement so far is just a package name."""
    sm = SoftwareManager()
    return sm.check_installed(requirement)
