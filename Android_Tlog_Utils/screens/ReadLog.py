from kivy.uix.widget import Widget
from kivy.properties import Property


class Reader(Widget):
    log = None
    log_text = Property('<Log_Text>')
    packetlimit = 150

    def DisplayLog(self):
        log_text = ''
        for i in range(len(self.log)):
            if i < self.packetlimit:
                log_text += str(self.log[i])
                log_text += '\n'

            if i >= self.packetlimit:
                log_text += "\n \n \n  ... Output truncated to " +
                str(self.packetlimit) + " packets"
                break
        self.log_text.text = log_text
