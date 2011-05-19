'''
push a newline onto the stack (assumes a valid document)
start in the data state
read some data; push that onto the stack.
look through the stack for \r
 then check for successive characters from the boundary
  when one doesn't match: pop the stack to the output
  if it does, keep pushing on to the stack
 if we're out of boundary characters, change state to IN_MIME
  (parse headers, until we see \r\n\r\n)
'''

# States
IN_DATA = 1
IN_HEADERS = 2

class Streamime(object):

    def __init__(self, boundary):
        self.stop_after = -1
        self.stopped = False
        self.state = IN_DATA
        self.boundary = boundary
        self.stack = ["\r", "\n"]
        self.output = [] 
        self.boundary_match = "\r\n--%s\r\n" % boundary
        self.end_of_headers = "\r\n\r\n"
        self.body = ''
        self.times_in_header = 0

    def push(self, data):
        if self.stopped:
            return
        for character in data:
            if self.state == IN_HEADERS:
                if character == self.end_of_headers[len(self.stack)]:
                    # could still be an end of header sequence
                    self.stack.append(character)
                    if len(self.stack) == len(self.end_of_headers):
                        self.state = IN_DATA
                        self.stack = []
                else:
                    self.stack = []
            else:
                if character == self.boundary_match[len(self.stack)]:
                    # might still be boundary
                    self.stack.append(character)
                    if len(self.stack) == len(self.boundary_match):
                        self.state = IN_HEADERS
                        self.times_in_header += 1
                        if self.times_in_header > self.stop_after:
                            self.stopped = True
                            return
                        self.stack = []
                else:
                    self.output.extend(self.stack)
                    self.stack = []
                    self.output.append(character)

    def get_body(self):
        return ''.join(self.output)
