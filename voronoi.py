from delaunay import *

class Voronoi:
    def __init__(self, tri, boundary = None):
        self.tri = tri
       
        self.__do(boundary)
        
    def __do(self, boundary):
        self.edges = []
        self.points = []
        self.pdict = {}
        
        for e in self.tri.edges:
            a = self.tri.points[e.a]
            b = self.tri.points[e.b]
            
            if e.l is not None and e.r is not None:
                ca = Circle(a, b, self.tri.points[e.l])
                cb = Circle(a, b, self.tri.points[e.r])
                atu = (ca.c.x, ca.c.y)
                btu = (cb.c.x, cb.c.y)
                
                if atu in self.pdict:
                    aidx = self.pdict[atu]
                else:
                    aidx = len(self.points)
                    self.points.append(Point(atu[0], atu[1]))
                    self.pdict[atu] = aidx
                    
                if btu in self.pdict:
                    bidx = self.pdict[btu]
                else:
                    bidx = len(self.points)
                    self.points.append(Point(btu[0], btu[1]))
                    self.pdict[btu] = bidx
                    
                self.edges.append(Edge(aidx, bidx))
            elif boundary is not None and (e.l is not None or e.r is not None):
                mid = (a+b)/2
                if e.l is not None:
                    c = Circle(a, b, self.tri.points[e.l])
                    p = c.c
                else:
                    c = Circle(a, b, self.tri.points[e.r])
                    p = c.c
                v = mid - p
                tx = -1
                ty = -1
                
                if v.x>0:
                    # pozitiv x fele lep ki
                    tx = (boundary[2]-p.x)/v.x
                elif v.x<0:
                    # negativ x fele lep ki
                    tx = (boundary[0]-p.x)/v.x
                if v.y>0:
                    # pozitiv y fele lep ki
                    ty = (boundary[3]-p.y)/v.y
                elif v.y<0:
                    # negativ y fele lep ki
                    ty = (boundary[1]-p.y)/v.y
                
                if tx > 0 or ty > 0:
                    if tx>ty and ty>0:
                        t = ty
                    else:
                        t = tx
                    p = p+v*t
                    ptu = (p.x, p.y)
                    ctu = (c.c.x, c.c.y)
                    if ptu in self.pdict:
                        pidx = self.pdict[ptu]
                    else:
                        pidx = len(self.points)
                        self.points.append(p)
                        self.pdict[ptu] = pidx
                    if ctu in self.pdict:
                        cidx = self.pdict[ctu]
                    else:
                        cidx = len(self.points)
                        self.points.append(c.c)
                        self.pdict[ctu] = cidx
                    self.edges.append(Edge(pidx, cidx))

    def saveSVG(self, filename, points = None):
        head = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <svg
           xmlns:svg="http://www.w3.org/2000/svg"
           xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
           xmlns="http://www.w3.org/2000/svg"
           version="1.0"
           width="1000"
           height="1000"
           id="svg2">

            <g inkscape:groupmode="layer" id="layer1" inkscape:label="Layer">
        """
        tail = """
            </g>
        </svg>
        """

        f = open(filename, "w")
        f.write(head)

        t = self.tri
        f.write("    <g id=\"Delaunay\">\n")
        for e in t.edges:
            a = t.points[e.a]
            b = t.points[e.b]
            line ="\t<path d=\"M %f, %f L %f, %f\" stroke=\"lavender\" />\n" % (a.x, a.y, b.x, b.y)
            f.write(line)
        f.write("    </g>\n")

        if points is not None:
            f.write("    <g id=\"Points\">\n")
            for p in points:
                dot = "\t<circle cx=\"%f\" cy=\"%f\" r=\"3\" fill=\"red\" stroke=\"red\" />\n" % (p.x, p.y)
                f.write(dot)
            f.write("    </g>\n")
            
        f.write("    <g id=\"Voronoi\">\n")
        for e in self.edges:
            a = self.points[e.a]
            b = self.points[e.b]
            line ="\t<path d=\"M %f, %f L %f, %f\" stroke=\"green\" />\n" % (a.x, a.y, b.x, b.y)
            f.write(line)
        f.write("    </g>\n")

        f.write(tail)
        f.close()

    
