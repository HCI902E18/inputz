from inputz.controllers import XboxController


class XboxEliteController(XboxController):
    """
    Xbox controller mappings

    """

    @staticmethod
    def validate(name: str) -> bool:
        """
        Used to validate if the name of the controller matches this controller

        :param name: The name of the input controller
        :return: bool, if the controller matches
        """
        return name == 'Microsoft X-Box One Elite pad'
