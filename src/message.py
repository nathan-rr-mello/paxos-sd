import uuid

class Message:
    """
    Base class for all messages used in Paxos.
    Every message has a source.
    """
    def __init__(self, src):
        self.src = src
        self.debug = True

    def __str__(self):
        return str(self.__dict__)

    def print_message(self, message):
        if self.debug:
            print(message)

class P1aMessage(Message):
    """
    Sent by Scouts to Acceptors in Phase 1 of Paxos.
    Carries a ballot number.
    """
    def __init__(self, src, ballot_number):
        Message.__init__(self, src)
        self.ballot_number = ballot_number
        # self.print_message("P1aMessage: %s" % (self.__dict__))

class P1bMessage(Message):
    """
    Sent by Acceptors to Scouts in Phase 1 of Paxos.
    Carries a ballot number and the set of accepted pvalues.
    """
    def __init__(self, src, ballot_number, accepted):
        Message.__init__(self, src)
        self.ballot_number = ballot_number
        self.accepted = accepted
        # self.print_message("P1bMessage: %s" % (self.__dict__))

class P2aMessage(Message):
    """
    Sent by Commanders to Acceptors in Phase 2 of Paxos.
    Carries a ballot number, a slot number and a command.
    """
    def __init__(self, src, ballot_number, slot_number, command):
        Message.__init__(self, src)
        self.ballot_number = ballot_number
        self.slot_number = slot_number
        self.command = command
        self.print_message("P2aMessage: %s" % (self.__dict__))

class P2bMessage(Message):
    """
    Sent by Acceptors to Commanders in Phase 2 of Paxos.
    Carries a ballot number and a slot number.
    """
    def __init__(self, src, ballot_number, slot_number):
        Message.__init__(self, src)
        self.ballot_number = ballot_number
        self.slot_number = slot_number
        self.print_message("P2bMessage: %s" % (self.__dict__))

class PreemptedMessage(Message):
    """
    Sent by Scouts or Commanders to Leaders.
    Carries a ballot number.
    """
    def __init__(self, src, ballot_number):
        Message.__init__(self, src)
        self.ballot_number = ballot_number
        # self.print_message("PreemptedMessage: %s" % (self.__dict__))

class AdoptedMessage(Message):
    """
    Sent by Scouts to Leaders.
    Carries a ballot number and the set of accepted pvalues.
    """
    def __init__(self, src, ballot_number, accepted):
        Message.__init__(self, src)
        self.ballot_number = ballot_number
        self.accepted = accepted
        self.print_message("AdoptedMessage: %s" % (self.__dict__))

class DecisionMessage(Message):
    """
    Sent by Commanders to Replicas.
    Carries a slot number and a command.
    """
    def __init__(self, src, slot_number, command):
        Message.__init__(self, src)
        self.slot_number = slot_number
        self.command = command
        self.print_message("DecisionMessage: %s" % (self.__dict__))

class RequestMessage(Message):
    """
    Sent by Clients to Replicas.
    Carries a command.
    """
    def __init__(self, src, command):
        Message.__init__(self, src)
        self.command = command
        self.print_message("RequestMessage: %s" % (self.__dict__))

class ResponseMessage(Message):
    """
    Sent by Replicas to Client.
    Carries a slot number and a command.
    """
    def __init__(self, src, command, slot_number):
        Message.__init__(self, src)
        self.slot_number = slot_number
        self.command = command
        self.print_message("ResponseMessage: %s" % (self.__dict__))

class ProposeMessage(Message):
    """
    Sent by Replicas to Leaders.
    Carries a slot number and a command.
    """
    def __init__(self, src, slot_number, command):
        Message.__init__(self, src)
        self.slot_number = slot_number
        self.command = command
        self.print_message("ProposeMessage: %s" % (self.__dict__))
