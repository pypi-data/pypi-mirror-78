import serial as s
import time
import logging

logger = logging.getLogger(__name__)


class DPPort():
    """Class that extends the functionality of :class:`Serial` for use with the Agilis controller commands.
    Creates an instance of :class:`Serial`
    
    :param portName: Serial port (Uses pySerial serial_for_url)
    :portName type: str
    """
    
    def __init__(self, portName=None):
        """Constructor method
        """
        if portName == None:
            self.soul = None
            return None
        try:
            logger.debug('Opening serial communication..')
            self.portName = portName
            self.ser = s.serial_for_url(self.portName,9600,s.EIGHTBITS,s.PARITY_NONE,s.STOPBITS_ONE,timeout=1)
            self.soul = 'p'
            logger.info('Serial communcation opened with ' + self.portName)
        except Exception as e:
            print('I could not find or open the port you specified: {0}'.format(portName))
            self.soul = None
            return None
    
        
    def amInull(self):
        """Returns whether port has been successfully opened.

        :return: True if port is open. False if not.
        :rtype: bool
        """
        return self.soul is None
    
    
    def isAquery(self,command):
        """Returns whether command is a query, as defined by Agilis command reference.

        :param command: Command to check
        :command type: str
        :return: True if command is a query. False if not.
        :rtype: bool
        """
        
        if self.amInull():
            return False
        
        queryOnly=["?"]
        command = command.upper()
        for q in queryOnly:
            if command.find(q) != -1:
                return True
        return False
    
    
    def sendString(self, command):
        """Sends a serial command to the device.
        Returns a response if command is a query. Else returns 0.

        :param command: Command to send
        :command type: str
        :return: Return reponse if command is a query. Else returns 0.
        :rtype: str or int
        """
        
        response = ''
        bCommand = command.encode('utf-8')
        self.ser.write(bCommand)
        logger.debug('sent: ' + repr(command))
        if self.isAquery(command):
            try:
                response = self.ser.readline().decode('utf-8')
                logger.debug('received: ' + repr(response))
                return response[:-1]
            except:
                print('Serial Timeout')
                return 0

    def close(self):
        """Close serial connection.
        """
        logger.debug('Closing serial communication..')
        self.ser.close()
        logger.info('Serial communication with ' + self.portName + ' is closed.')
    
 