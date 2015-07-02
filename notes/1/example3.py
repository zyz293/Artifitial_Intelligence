import math

class polygon:
    """This polygon class is here to show you how to use classes in python."""
    
    def __init__(self, ed, color = "none", length = 1):
        """This is a special method - with __ before and after its name,
        meaning that you are not to call it directly.  This method that is
        called when you create an instance of the polygon object. ed is a
        required parameter and color and length are optional."""
        self.edges = ed
        self.color = color
        self.length = length

    def __str__(self):
        """Another special method, str should not be called directly. Instead
        simple print an instance of the polygon object and str will be called.
        It is critical that str RETURNS a string."""
        return  "A " + self.color + " polygon with " + str(self.edges) + \
               " edges of length " + str(self.length)

    def area(self):
        """Calculate the area of the object."""
        return (self.edges*self.length**2)/(4*math.tan(math.pi/self.edges))

    def paint(self, newColor):
        """Change the color of the object to newColor."""
        self.color = newColor

    def multArea(self, n):
        """Create (and returns) a new polygon with a multiple of the area of
        the old one. """
        newArea = self.area() * n
        oldEdges = self.edges
        oldColor = self.color
        newLength = math.sqrt((newArea*4*math.tan(math.pi/oldEdges))/oldEdges)
        return polygon(oldEdges, oldColor, length = newLength)


class box:
    def __init__(self):
        """Creates an instance of the box class."""
        # boxes always start empty
        box.contents = []

    def __str__(self):
        """Returns a string representation of the box."""
        return "This is a box of " + str(len(box.contents)) + " polygons."

    def listContents(self):
        """Prints the contents of the box."""
        print "This box contains:"
        for p in box.contents:
            #note - this calls the __str__ function for the polygon
            print p

    def putin(self, item):
        """Can put in either a single polygon or another box of polygons."""
        if isinstance(item, box):
            for p in box:
                self.contents[:0] = [item]
        elif isinstance(item, polygon):
            self.contents[:0] = [item]
        else:
            print "This box is only for polygons."

    def howMany(self, edges = 0, color = ""):
        count = 0
        if edges == 0 and color == "":
            print "Please specify what you want to count."
        elif edges != 0 and color != "":
            print "Please be more specific about what you want to count."
        else:
            for p in box.contents:
                if edges == p.edges or color == p.color:
                    count = count + 1
            if count == 0:
                print "No polygons in this box matched your criteria."
            else:
                return count

    def paint(self, newColor):
        """Paint every polygon in the box a new color."""
        for p in box.contents:
            p.paint(newColor)


#INSTANTIATION (making INSTANCES of a CLASS)
blueTriangle = polygon(3, length = 3, color="blue")#order doesn't matter for optionals
yellowSquare = polygon(4, "yellow", 2) #however, u don't need names if in order
redPentagon = polygon(5, "red")#don't need to specify all if in order

#METHODS - self
#self in a param list basically says:
#"this is a method that can act upon an instance of this class" 
#(aka - use the dotted method notation) 
#you don't pass in self as an argument, but it must be in the param list in order 
#for the dotted method notation to work

#CALLING A METHOD ON AN OBJECT - DOTTED METHOD NOTATION
#even though no params - still need parens - that makes it a function
yellowSquare.area()

#STR
#why might you want a string representation of your class? 
#in debugging if you wanted to print it out, but didn't feel like printing messages 
#each time
print yellowSquare

# #create a new square, twice the size of the yellow one, and paint it orange
newSquare = yellowSquare.multArea(2)
newSquare.area()
yellowSquare.area()#the yellowsquare's size didn't change because multArea 
#					returned a new instance of the polygon class
newSquare.paint("orange")
print yellowSquare
print newSquare

#COPY
import copy
ys = copy.copy(yellowSquare)
yellowSquare.length = 20
print ys
print yellowSquare

#classes interacting with each other
aBox = box()
aBox.putin(newSquare)
aBox.putin(yellowSquare)
aBox.putin(blueTriangle)
aBox.putin(redPentagon)
print aBox

#point out LISTCONTENTS - called print polygon - str fun
aBox.listContents()

#you can do things to the polygons when they're inside the box
aBox.paint("blue")
