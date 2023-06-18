# observer/user_observer.py
from models.user import User

class UserObserver:
    """
    An observer class for the User. It updates its state when the state of the User changes.
    """
    def __init__(self, user: User):
        """
        Initializes a new instance of the UserObserver class.

        Arguments:
        user: the User to observe
        """
        self.user = user
        self.user.attach(self)

    def update(self):
        """
        Updates the state of the observer. 
        This method is called when the state of the User changes.

        Returns:
        None
        """
        print(f'The state of the User {self.user.userUID} has changed.')

    def __del__(self):
        """
        Detaches the observer from the User when the observer is deleted.

        Returns:
        None
        """
        self.user.detach(self)
