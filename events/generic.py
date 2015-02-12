'''
Description:
	A generic event-driven design for Python.

Usage:
	1. Inherit in the class which you want to listen for events
	2. Make sure Observer's initializer gets called!
	3. Register events to listen to with .observe(event_name, callback_function)
	   event_name is just a string-identifier for a certain event
	   
	After this you can instansiate the class Event() anywhere in the project
	and if someone is listening for that event, the according callback
	will run.

'''


class Observer():
	_observers = []
	def __init__(self):
		self._observers.append(self)
		self._observed_events = []
	def observe(self, event_name, callback_fn):
		self._observed_events.append({'event_name' : event_name, 'callback_fn' : callback_fn})


class Event():
	def __init__(self, event_name, *callback_args):
		for observer in Observer._observers:
			for observable in observer._observed_events:
				if observable['event_name'] == event_name:
					observable['callback_fn'](*callback_args)







############################### EXAMPLE ################################

if __name__ == "__main__":
	
	class Room(Observer):
	    def __init__(self):
	        print("Room is ready.")
	        Observer.__init__(self) # DON'T FORGET THIS
	    def someone_arrived(self, who):
	        print(who + " has arrived!")
	
	# Observe for specific event
	room = Room()
	room.observe('someone arrived',  room.someone_arrived)
	
	# Fire some events
	Event('someone left',    'John')
	Event('someone arrived', 'Lenard') # will output "Lenard has arrived!"
	Event('someone Farted',  'Lenard')
