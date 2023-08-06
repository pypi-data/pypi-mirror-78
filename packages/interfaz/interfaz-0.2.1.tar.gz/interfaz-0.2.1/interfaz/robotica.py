import socketio
import time
# standard Python
socket = socketio.Client()

MAX_ANALOG_VALUE = 1023 

__all__ = ["interfaz", "_OUTPUT", "_SERVO", "_ANALOG", "_DIGITAL", "_LCD", "_PING", "_PIXEL", "_I2C", "_DEVICE"];

class _OUTPUT:
    """
    # Class Output
    # @constructor
    #
    # @param index {Integer} output number
    """
    def __init__(self, index):
        self.index = index

    def on(self):
        """
        # On(): Turns ouput on
        """
        socket.emit('OUTPUT', {"index": self.index, "method": 'on'})

    def off(self):
        """
        # Off(): Turns ouput off
        """
        socket.emit('OUTPUT', {"index": self.index, "method": 'off'})

    def brake(self):
        """
        # Brake(): Applies brake
        #
        """
        socket.emit('OUTPUT', {"index": self.index, "method": 'brake'})

    def inverse(self):
        """
        # Inverse(): Inverts direction
        """
        socket.emit('OUTPUT', {"index": self.index, "method": 'inverse'})

    def direction(self, dir):
        """
        # Direction(): Sets direction
        #
        # @param dir {Integer} direction: 0, 1
        """
        socket.emit('OUTPUT', {"index": self.index, "method": 'direction', "param": dir})

    def power(self, pow):
        """
        # Power(): Sets pwm power
        #
        # @param pow {Integer} power: 0 to 255
        """
        socket.emit('OUTPUT', {"index": self.index, "method": 'power', "param": pow})


class _SERVO:
    """
    # class Servo
    # @constructor
    #
    # @param index {Integer} motor number
    #
    """
    def __init__(self, index):
        self.index = index

    def position(self, value):
        """
        # Position(): Sets position
        #
        # @param value {Integer}servo position: 0 to 180
        #
        """
        socket.emit('SERVO', {"index": self.index, "method": 'position', "param": value})


class _ANALOG:
    """
    # class Analog
    # @constructor
    #
    # @param index {Integer} analog number
    #
    """
    def __init__(self, index):
        self.index = index
        self.status = 0;
        self.value = 0;
        self.type = "analog";
        self.callback = None;
        self.whenCallbacks = {"high" : None, "low": None};
        self.threshold = 100;

    def get(self):
        """
        # value(): returns analog value
        #
        """
        return self.value


    def when(self, event, callback):
        """
        # when(): sets when callback
        #
        # @param event {string} evento to trigger callback: "high", "low"
        # @param callback {Function} callback function
        """
        self.whenCallbacks[event] = callback

    def data(self, callback):
        """
        # data(): sets data callback
        #
        # @param callback {Function} callback function
        """
        self.callback = callback

    def on(self):
        """
        # On(): Turns reporting on
        #
        """
        self.status = 1;
        socket.emit('ANALOG', { "index": self.index, "method": 'on' });

    def off(self):
        """
        # Off(): Turns reporting off
        #
        """
        self.status = 0;
        socket.emit('ANALOG', { "index": self.index, "method": 'off' });


class _DIGITAL:
    """
    # class Digital
    # @constructor
    #
    # @param index {Integer} digital port number
    #
    """
    def __init__(self, index):
        self.index = index
        self.status = 0;
        self.value = 0;
        self.type = "digital";
        self.callback = None;
        self.whenCallbacks = {"high" : None, "low": None};

    def get(self):
        """
        # value(): returns analog value
        #
        """
        return self.value

    def when(self, event, callback):
        """
        # when(): sets when callback
        #
        # @param event {string} evento to trigger callback: "high", "low"
        # @param callback {Function} callback function
        """
        self.whenCallbacks[event] = callback


    def data(self, callback):
        """
        # data(): sets data callback
        #
        # @param callback {Function} callback function
        """
        self.callback = callback

    def on(self):
        """
        # On(): Turns reporting on
        #
        """
        self.status = 1;
        socket.emit('DIGITAL', { "index": self.index, "method": 'on' });

    def off(self):
        """
        # Off(): Turns reporting off
        #
        """
        self.status = 0;
        socket.emit('DIGITAL', { "index": self.index, "method": 'off' });

    def pullup(self, enable):
        """
        # Pullup(): Set input pullup
        #
        """
        socket.emit('DIGITAL', { "index": self.index, "method": 'pullup', "param": enable })


class _LCD:

    def on():
        """
        # encender(): Turns on
        #
        """
        socket.emit('LCD', {"method": 'on', "param": False, "param2": False})

    def off():
        """
        # apagar(): Turns off
        #
        """
        socket.emit('LCD', {"method": 'off', "param": False, "param2": False})

    def silence():
        """
        # silenciar(): Turns silent
        #
        """
        socket.emit('LCD', {"method": 'silence', "param": False, "param2": False})


class _PING:
    """
    # class Ping
    # @constructor
    #
    # @param index {Integer} analog number
    #
    """
    def __init__(self, index):
        self.index = index
        self.status = 0
        self.type = "ping"
        self.cm = 0
        self.inches = 0
        self.callback = None

    def getCm(self):
        """
        # value(): returns value in cm
        #
        """
        return self.cm

    def getInches(self):
        """
        # value(): returns value in inches
        #
        """
        return self.inches


    def data(self, callback):
        """
        # data(): sets data callback
        #
        # @param callback {Function} callback function
        """
        self.callback = callback


    def on(self):
        """
        # On(): Turns reporting on
        #
        """
        self.status = 1;
        socket.emit('PING', { "index": self.index, "method": 'on' });

    def off(self):
        """
        # Off(): Turns reporting off
        #
        """
        self.status = 0;
        socket.emit('PING', { "index": self.index, "method": 'off' });


class _PIXEL:
    """
    # class Pixel
    # @constructor
    #
    # @param index {Integer} motor number
    #
    """
    def __init__(self, index):
        self.index = index;
        self.type = "pixel";

    def create(self, length):
        """
        # create(length): Create strip
        #
        """
        socket.emit('PIXEL', {"index": self.index, "method": 'create', "param": length, "param2": False, "param3": False })

    def on(self, n = None):
        """
        # on(): Turns on
        #
        """
        socket.emit('PIXEL', {"index": self.index, "method": 'on', "param": n, "param2": False, "param3": False })

    def off(self, n = None):
        """
        # off(): Turns off
        #
        """
        socket.emit('PIXEL', {"index": self.index, "method": 'off', "param": n, "param2": False, "param3": False })

    def color(self, color, i):
        """
        # color(): Change color to strip or pixel
        #
        """
        socket.emit('PIXEL', {"index": self.index, "method": 'color', "param": color, "param2": i, "param3": False })

    def shift(self, offset, direction, wrap):
        """
        # shift(): Shift amount of pixels
        #
        """
        socket.emit('PIXEL', {"index": self.index, "method": 'shift', "param": offset, "param2": direction, "param3": wrap })


class _I2C:
    """
    # class I2C
    # @constructor
    #
    # @param address {Integer} device address
    #
    """
    def __init__(self, address):
        self.address = address;
        self.callback = None;

    def data(self, callback):
        """
        # data(): sets data callback
        #
        # @param callback {Function} callback function
        """
        self.callback = callback

    def on(self, register, bytes):
        """
        # On(): Turns reporting on
        #
        # @param register {Integer} register to read
        # @param bytes {Integer} amount of bytes to read
        """
        socket.emit('I2C', { "address": self.address, "register": register, "method": 'on', "param": bytes })

    def off(self, register):
        """
        # Off(): Turns reporting off
        #
        """
        socket.emit('I2C', { "address": self.address, "register": register, "method": 'off' });

    def read(self, register, bytes):
        """
        # Read(): Reads register once
        #
        # @param register {Integer} register to read
        # @param bytes {Integer} amount of bytes to read
        """
        socket.emit('I2C', { "address": self.address, "register": register, "method": 'read', "param": bytes });

    def write(self, register, data):
        """
        # Write(): Writes data into register
        #
        # @param register {Integer} register to read
        # @param data {Integer} data to write
        """
        socket.emit('I2C', { "address": self.address, "register": register, "method": 'write', "param": data });


class _DEVICE:
    """
    # Device object to connect to device class
    # class Device
    #
    # @this .device {String} Name of class.
    # @this .options {Object} Options to pass as parameters of class
    #
    # example:
    #      light = new Device('Light', { controller: "BH1750"});
    #      led = new Device('Led', { pin: 13});
    """

    def __init__(self, device, options):
        self.device = device;
        self.options = options;
        self.id = None;
        @socket.on('DEVICE_ID')
        def onMessage(data):
            if data['device'] == self.device:
                self.id = data['id']
        socket.emit('DEVICE', {  "device": device, "options": options})


    def on(self, event, attributes = None, callback = None):
        """
        # On(): Create event listener
        #
        # @param event {String} Event to listen
        # @param attributes {Object} Attributes to receive from device
        # @param callback {myCallback} Callback to execute on data received
        #
        # example:
        #  gps.on("change", ["latitude","longitude"] , function(d) { console.log(d) });
        """
        socket.emit('DEVICE_EVENT', { "id": self.id, "event": event, "attributes": attributes})
        if callback != None:
            @socket.on(event + self.id)
            def onMessage(data):
                callback(data);

    def call(self, method):
        """
        # Call(): Call method on device
        #
        # @param method {String} method to run with parenthesis and parameters
        #
        # example:
        #    led.call('on(10)');
        """
        socket.emit('DEVICE_CALL', { "id": self.id, "method": method })

class _JOYSTICK:
    """
    # class Joystick
    # @constructor
    #
    # @param index {Integer} digital port number
    #
    """
    def __init__(self, index):
        self.index = index
        self.status = 0;
        self.value = None
        self.callback = None
        self.whenCallbacks = {"high" : None, "low": None};

    def get(self):
        """
        # value(): returns joystick values
        #
        """
        return self.value

    def when(self, event, callback):
        """
        # when(): sets when callback
        #
        # @param event {string} evento to trigger callback: "high", "low"
        # @param callback {Function} callback function
        """
        self.whenCallbacks[event] = callback


    def data(self, callback):
        """
        # data(): sets data callback
        #
        # @param callback {Function} callback function
        """
        self.callback = callback

    def on(self):
        """
        # On(): Turns reporting on
        #
        """
        self.status = 1;
        socket.emit('I2CJOYSTICK', { "index": self.index, "method": 'on' });




class _INTERFAZ:

    def __init__(self, address = "localhost"):
        @socket.on('ANALOG_MESSAGE')
        def onMessage(data):
            a = self._analogs[data['index'] - 1]
            v = data['value']
            # DATA CALLBACK
            if a.callback != None:
                a.callback(v)
            for w in ["low", "high"]:
                if a.whenCallbacks[w] != None:
                    if w == "low" and v <= a.threshold and a.value > a.threshold: a.whenCallbacks[w]()
                    if w == "high" and v >= MAX_ANALOG_VALUE - a.threshold and a.value < MAX_ANALOG_VALUE - a.threshold: a.whenCallbacks[w]()
            a.value = v

        @socket.on('DIGITAL_MESSAGE')
        def onMessage(data):
            a = self._digitals[data['index'] - 1]
            v = data['value']
            # DATA CALLBACK
            if a.callback != None:
                a.callback(v)
            for w in ["low", "high"]:
                if a.whenCallbacks[w] != None:
                    if w == "low" and v == 0 and a.value == 1: a.whenCallbacks[w]()
                    if w == "high" and v == 1 and a.value == 0: a.whenCallbacks[w]()
            a.value = v


        @socket.on('PING_MESSAGE')
        def onMessage(data):
            a = self._pings[data['index'] - 1]
            if a.callback != None:
                a.callback({"cm": data["cm"], "inches": data["inches"]})
            a.cm = data['cm']
            a.inches = data['inches']

        @socket.on('I2C_MESSAGE')
        def onMessage(data):
            a = self._i2c[data['address']]
            if a.callback != None:
                a.callback(data)

        @socket.on('I2CJOYSTICK_MESSAGE')
        def onMessage(data):
            a = self._joystick
            if a.callback != None:
                a.callback(data)
            a.value = data

        if socket.connected:
            socket.disconnect();
        socket.connect('http://'+address+':4268')

    def sensor(self, port):
        if self._analogs_map.index(port) is not None:
            return self._analogs[self._analogs_map.index(port)]
        return self._analogs[port - 1]

    def digital(self, port):
        if self._digitals_map.index(port) is not None:
            return self._digitals[self._digitals_map.index(port)]
        return self._digitals[port - 1]

    def ping(self, port):
        if self._digitals_map.index(port) is not None:
            return self._pings[self._digitals_map.index(port)]
        return self._pings[port - 1]

    def output(self, port):
        if self._outputs_map.index(port) is not None:
            return self._outputs[self._outputs_map.index(port)]
        return self._outputs[port - 1]

    def servo(self, port):
        if self._digitals_map.index(port) is not None:
            return self._servos[self._digitals_map.index(port)]
        return self._servos[port - 1]

    def pixel(self, port):
        if self._digitals_map.index(port) is not None:
            return self._pixels[self._digitals_map.index(port)]
        return self._pixels[port - 1]

    def lcd(self):
        return self._lcd;

    def joystick(self):
        return self._joystick;

    def i2c(self, address):
        self._i2c[address] = _I2C(address)
        return self._i2c[address]


class interfaz(_INTERFAZ):

    def __init__(self, address = "localhost"):
        self._analogs = [_ANALOG(1), _ANALOG(2), _ANALOG(3), _ANALOG(4)]
        self._digitals = [_DIGITAL(1), _DIGITAL(2), _DIGITAL(3), _DIGITAL(4)]
        self._pings = [_PING(1), _PING(2), _PING(3), _PING(4)]
        self._outputs = [_OUTPUT(1), _OUTPUT(2), _OUTPUT(3), _OUTPUT(4)]
        self._servos = [_SERVO(1), _SERVO(2)]
        self._pixels = [_PIXEL(1), _PIXEL(2)]
        self._devices = []
        self._joystick = _JOYSTICK(1)
        self._i2c = []
        self._lcd = _LCD();
        super().__init__(address)

class rasti(_INTERFAZ):

    def __init__(self, address = "localhost"):
        self._analogs = [_ANALOG(1), _ANALOG(2), _ANALOG(3), _ANALOG(4), _ANALOG(5)]
        self._digitals = [_DIGITAL(1), _DIGITAL(2), _DIGITAL(3), _DIGITAL(4)]
        self._pings = [_PING(1), _PING(2), _PING(3), _PING(4)]
        self._outputs = [_OUTPUT(1), _OUTPUT(2)]
        self._servos = [_SERVO(1), _SERVO(2), _SERVO(3), _SERVO(4)]
        self._pixels = [_PIXEL(1), _PIXEL(2)]
        self._devices = []
        self._joystick = _JOYSTICK(1)
        self._i2c = []
        self._lcd = None
        super().__init__(address)

        self._outputs_map = ["G", "H"];
        self._analogs_map = ["C", "F", "B", "A", "D"];
        self._digitals_map = ["F", "C", "A", "B"];

