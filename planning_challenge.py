from midca import plans, base

import json
import numpy as np

class WaypointPlanner(base.BaseModule):

    """
    The challenge is to survey the Qroute and remove the maximum mines to provide safe passage to the ships.
    
    input : Two dictionaries "remus_location" and "hazard_location" which gives information about the submarine and the mines detected

            remus_location format:
                        remus_location =  {"X": x,
                                           "Y": y,
                                           "speed": speed,
                                           "direction": speed})
                        x and y are the location coordinates
                        speed is the velocity with which the remus is heading towards
                        ignore direction

            hazard_location format:
                        hazard_location =  {"X": mine_x,
                                            "Y": mine_y}
                        x and y are the location coordinates of the mine

    output : The list "way_point" to make the remus go to certain way_points
             way_point format:
                    way_point = [ [2,2],
                                  [3,3]]
    """
    def sample_behavior(self):
        """

        :return: a list of way_points
        """
        way_points = [[-49,-1],[49, -27],[49,-150], [80,-27], [80,-150]
                      ]



        return way_points

    def init(self, world, mem):
        """
        This is executed during the initialization of midca.
        Feel free to create any number of variables to store information
        """
        self.world = world
        self.mem = mem
        self.previous_way_points = []
        self.hazardMemory={}
        self.mayBeCircle = {}
        self.k =0
        self.insertPostion = 0
        self.lock = 0
        self.way_points = self.sample_behavior()

    def get_remus_location(self):
        """

        :return: the dictionary of remus location
        """
        return self.mem.get(self.mem.REMUS_LOCATION)


    def get_mine_location(self):
        """

        :return: the dictionary of mine location
        """

        return self.mem.get(self.mem.HAZARD_LOCATION)



    def define_circle(self, p1, p2, p3):
        """
        Returns the center and radius of the circle passing the given 3 points.
        In case the 3 points form a line, returns (None, infinity).
        """
        temp = p2[0] * p2[0] + p2[1] * p2[1]
        bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
        cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
        det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])

        if abs(det) < 1.0e-6:
            return None, np.inf
        # Center of circle
        cx = (bc * (p2[1] - p3[1]) - cd * (p1[1] - p2[1])) / det
        cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det

        radius = np.sqrt((cx - p1[0]) ** 2 + (cy - p1[1]) ** 2)
        return (cx, cy), radius

    def set_way_points(self,way_points):
        """

        :param way_points: the list of way_points
         sets the memory variable "WAY_POINTS"
        """
        if self.previous_way_points == way_points:
                return

        self.mem.set(self.mem.WAY_POINTS, way_points)
        self.previous_way_points = way_points

    def calculate_index(self, location):

        x = location[0]
        y = location[1]
        distances = []
        a = np.array((x,y))
        for each_point in self.previous_way_points:
            b = np.array((each_point[0], each_point[1]))
            distances.append(np.linalg.norm(a-b))

        return distances.index(min(distances))

   
    def run(self, cycle, verbose=2):
        """
        run function is executed in a cyclic fashion
        """

        remus_location = self.get_remus_location()
        hazard_location = self.get_mine_location()

        # a simple behaviour for understanding the output format feel free to rempve the below code


        """
        Your Code should start here
        """

        #   if hazard_location != null:
        if hazard_location:
            print self.previous_way_points
            #self.insertPostion = way_points.index("bar")
            print "Arjun"
            print hazard_location
            y = hazard_location["Y"]
            x = hazard_location["X"]
            self.hazardMemory[x] = y;
            for x_loc in self.hazardMemory.keys():
                if (x+5) < x_loc:
                #if x in dict.keys():
                    self.mayBeCircle[x_loc]=self.hazardMemory.get(x_loc)
                    print "is y correct"
                    print y
                    self.mayBeCircle[x] = self.hazardMemory.get(x)
                    print "point may be a circle"
                if (x-5)>x_loc:
                    self.mayBeCircle[x_loc] = self.hazardMemory.get(x_loc)
                    print "point may be circle"
                    self.mayBeCircle[x] = self.hazardMemory.get(x)
          #  hazard_location
           # print zipped
            print self.mayBeCircle
            if len(self.mayBeCircle)>=3:
                p1 = [0,0]
                p2 = [0,0]
                p3 = [0,0]
                p4 = [0,0]
                p5 = [0,0]
                p6 = [0,0]
                x = list(self.mayBeCircle.keys())[0]
                y = self.mayBeCircle.get(x)
                #print x
                #print y
                p1[0] = x
                p1[1] = y
                ##delete key once processed
                x = list(self.mayBeCircle.keys())[1]
                y = self.mayBeCircle.get(x)
                #print x
                #print y
                p2[0] = x
                p2[1] = y
                x = list(self.mayBeCircle.keys())[2]
                y = self.mayBeCircle.get(x)
                #print x
                #print y
                p3[0] = x
                p3[1] = y
                k = self.define_circle(p1, p2, p3)
               # if p3[0]+5 >
                print k
               # a.insert(i, x)
                #k[1] is the found radius
                #finding chord mirror points and trying to navigate to them
                p4[0] = p1[0]+k[1]*1.414
                p4[1] = p1[1]+k[1]



                print p4
                p5[0]=p1[0]+2*k[1]
                p5[1]=p1[1]
                print p5
                p6[0] = p1[0] + k[1]
                p6[1] = p1[1] - k[1]*1.414
                print p6
                indexnew = self.calculate_index(p1)
                #print indexnew
                #print self.way_points
                self.way_points = self.way_points[indexnew:]
                #print self.way_points
                self.way_points.insert(indexnew+1,p6)
                #print self.way_points
                self.way_points.insert(indexnew+1,p5)
                #print self.way_points
                self.way_points.insert(indexnew+1, p4)
                #print self.way_points
                #print self.way_points
                #del self.hazardMemory[se]
                self.mayBeCircle={}
               # self.hazardMemory = {}
                #del self.hazardMemory[p1[o]]
                #del self.hazardMemory[p2[o]]
                #del self.hazardMemory[p3[o]]
                print indexnew
            #raw_input("Enter")




        self.set_way_points(self.way_points)
