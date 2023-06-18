from abc import ABC, abstractmethod

# states/request_state.py
class RequestState(ABC):
    """
    An abstract base class that defines an interface for all states.
    """
    @abstractmethod
    def process_request(self, request):
        pass


class NewState(RequestState):
    """
    The state of a new request.
    """
    def process_request(self, request):
        print(f"Processing a new request: {request}")

# Implement more states as needed...


class PendingState(RequestState):
    """
    The state of a pending request.
    """
    def process_request(self, request):
        print(f"Processing a pending request: {request}")


class ApprovedState(RequestState):
    """
    The state of an approved request.
    """
    def process_request(self, request):
        print(f"Processing an approved request: {request}")


class RejectedState(RequestState):
    """
    The state of a rejected request.
    """
    def process_request(self, request):
        print(f"Processing a rejected request: {request}")


class CompletedState(RequestState):
    """
    The state of a completed request.
    """
    def process_request(self, request):
        print(f"Processing a completed request: {request}")
