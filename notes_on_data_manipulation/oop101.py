#  game that will have several players moving on a grid and interacting with each other

class Player:
    # create class attribute
    MAX_POSITION = 10
    # the constructor is automatically called every time an object is created
    def __init__(self):
        # instance attributes to be assigned when the instance is created
        self.position = 0

    # Add a method with steps parameter
    def move(self, steps):
        if (self.position + steps) < Player.MAX_POSITION:
            self.position = self.position + steps
        else:
            self.position = Player.MAX_POSITION
    

    # This method provides a rudimentary visualization in the console    
    def draw(self):
        drawing = "x" * self.position + "|" +"-"*(Player.MAX_POSITION - self.position)
        print(drawing)

p = Player(); p.draw()
p.move(4); p.draw()
p.move(5); p.draw()
p.move(3); p.draw()

# customize pandas DataFrame class

# Imports
import pandas as pd
from datetime import datetime

# Define LoggedDF inherited from pd.DataFrame and add the constructor
class LoggedDF(pd.DataFrame):
  # Use *args and **kwargs not to worry about keeping the signature of your 
  # customized method compatible.
  def __init__(self, *args, **kwargs):
    pd.DataFrame.__init__(self, *args, **kwargs)
    self.created_at = datetime.today()
    
  def to_csv(self, *args, **kwargs):
    # Copy self to a temporary DataFrame
    temp = self.copy()
    
    # Create a new column filled with self.created at
    temp["created_at"] = self.created_at
    
    # Call pd.DataFrame.to_csv on temp with *args and **kwargs
    pd.DataFrame.to_csv(temp, *args, **kwargs)
    

    