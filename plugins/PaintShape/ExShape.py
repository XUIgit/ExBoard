from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import Qt

import math

class ExShape:

    def __init__(self):
        self.color = QColor(Qt.black)#默认颜色
        self.penStyle = Qt.SolidLine
        self.__selected = False
        self.visible = True

    def setColor(self, color):
        self.color = color

    def setPenStyle(self, style):
        self.penStyle = style

    def draw(self, QPainter, MainPlugin):
        pass

    def getPoints(self):
        return []

    def setVisible(self, b):
        self.visible = b

    def isVisible(self):
        return self.visible


    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, b):
        if b:
            #在这个设置选中颜色
            self.color = QColor(Qt.green)
        else:
            self.color = QColor(Qt.black)
        self.__selected = b

    def isPointOnShape(self, pt, MainPlugin):
        pass

    def isPointNearShape(self,pt,r,MainPlugin):
        pass

class ExPoint(ExShape):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.x = None
        self.y = None
        if not kwargs:
            if len(args) == 0:#无参
                return
            if len(args) == 1:#该参数为QPoint
                if isinstance(args[0], QPoint):
                    self.x = args[0].x()
                    self.y = args[0].y()
                elif isinstance(args[0], ExPoint):
                    self.x = args[0].x
                    self.y = args[0].y
                return
            if len(args)!=2:
                raise TypeError("ExPoine只需要两个参数")
            self.x = args[0]#两个参数
            self.y = args[1]
            return
        else:
            if not args:
                self.x = kwargs['x']#用x,y指定的两个参数
                self.y = kwargs['y']
                return
            else:
                raise TypeError("不能混用 指定参数的方式")

    def isPointNearShape(self,pt,r,MainPlugin):
        v = (pt.x - self.x)*(pt.x - self.x) + (pt.y - self.y)*(pt.y - self.y)
        if v <= r*r:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False


class ExLine(ExShape):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.pt0 = ExPoint()
        self.pt1 = ExPoint()
        self.threshold = 1.5
        if not kwargs:
            if len(args) == 0:
                return
            if len(args) == 4:#我这里没有判断参数的类型
                self.pt0.x = args[0]
                self.pt0.y = args[1]
                self.pt1.x = args[2]
                self.pt1.y = args[3]
                return
            if len(args) == 2:
                self.pt0 = args[0]
                self.pt1 = args[1]
                return
        else:
            if args:
                raise TypeError("不能混用参数")
            else:
                self.pt0 = kwargs["pt0"]
                self.pt1 = kwargs["pt1"]
    def setThreshold(self, threshold):
        self.threshold = threshold

    def setValue(self, *args):
        if len(args) == 2:
            self.pt0 = args[0]
            self.pt1 = args[1]
        elif len(args) == 4:
            self.pt0.x = args[0]
            self.pt0.y = args[1]
            self.pt1.x = args[2]
            self.pt1.y = args[3]
        else:
            raise TypeError("参数不正确")

    def getPoints(self):
        return [self.pt0, self.pt1]

    def setPt0(self,x,y):
        self.pt0.x = x
        self.pt0.y = y

    def setPt1(self,x,y):
        self.pt1.x = x
        self.pt1.y = y

    def draw(self, QPainter, MainPlugin):
        if self.visible:
            QPainter.save()
            #定义画笔
            pen = QPen()
            pen.setColor(self.color)
            pen.setWidth(MainPlugin.line_width)
            pen.setStyle(self.penStyle)
            pen.setCapStyle(Qt.RoundCap)
            QPainter.setPen(pen)

            #绘制图形
            QPainter.drawLine(self.pt0.x*MainPlugin.unit_pixel,self.pt0.y*MainPlugin.unit_pixel,self.pt1.x*MainPlugin.unit_pixel,self.pt1.y*MainPlugin.unit_pixel)
            QPainter.restore()

    def isPointOnShapeNoLimit(self, pt, MainPlugin):

        # 判断的阈值
        self.threshold = 1.5

        # 计算直线的一般方程
        a = self.pt1.y - self.pt0.y
        b = self.pt0.x - self.pt1.x
        c = self.pt1.x * self.pt0.y - self.pt0.x * self.pt1.y

        result = False

        if a == 0 and b == 0:
            result = False
        elif a == 0:
            if pt.y < (-c) / b + self.threshold and pt.y > (-c) / b - self.threshold:
                result = True
            else:
                result = False
        elif b == 0:
            if pt.x < (-c) / a + self.threshold and pt.x > (-c) / a - self.threshold:
                result = True
            else:
                result = False
        else:
            y = ((-c) - a * pt.x) / b
            # 因为斜率不同时 其单位距离相差的值会不同 所以阈值不应该保持不变
            k = (-a) / b
            k = k if k > 0 else -k  # 变为正值
            if k >= 1.5:  # 当直线变得相对垂直的时候增大阈值
                if pt.y < y + k and pt.y > y - k:
                    result = True
                else:
                    result = False
            else:
                if pt.y < y + self.threshold and pt.y > y - self.threshold:
                    result = True
                else:
                    result = False

        return result


    def isPointOnShape(self, pt,MainPlugin):

        #判断的阈值
        self.threshold = 1.5

        #计算直线的一般方程
        a = self.pt1.y - self.pt0.y
        b = self.pt0.x - self.pt1.x
        c = self.pt1.x*self.pt0.y - self.pt0.x*self.pt1.y

        result = False

        if a == 0 and b == 0:
            result = False
        elif a == 0:
            if pt.y < (-c)/b + self.threshold and pt.y > (-c)/b - self.threshold:
                result = True
            else:
                result = False
        elif b == 0:
            if pt.x < (-c)/a + self.threshold and pt.x  > (-c)/a  - self.threshold:
                result = True
            else:
                result = False
        else:
            y = ((-c) - a * pt.x) / b
            # 因为斜率不同时 其单位距离相差的值会不同 所以阈值不应该保持不变
            k = (-a)/b
            k = k if k>0 else -k#变为正值
            if k >= 1.5:#当直线变得相对垂直的时候增大阈值
                if pt.y < y + k and pt.y > y - k:
                    result = True
                else:
                    result = False
            else:
                if pt.y < y + self.threshold and pt.y > y - self.threshold:
                    result = True
                else:
                    result = False


        #上面验证了 点在直线附近 还要验证 是否在线段内
        if result:
            maxX,minX = (self.pt0.x, self.pt1.x) if self.pt0.x > self.pt1.x else (self.pt1.x, self.pt0.x)
            maxY,minY = (self.pt0.y, self.pt1.y) if self.pt0.y > self.pt1.y else (self.pt1.y, self.pt0.y)

            if a == 0:
                if pt.x <= maxX and pt.x >= minX:
                    result = True
                else:
                    result = False
            elif b == 0:
                if pt.y <= maxY and pt.y >= minY:
                    result = True
                else:
                    result = False
            else:
                if pt.x <= maxX+self.threshold and pt.x >= minX-self.threshold:
                    if pt.y <= maxY+self.threshold and pt.y >= minY-self.threshold:
                        result = True
                    else:
                        result = False
                else:
                    result = False

        return result


class ExArc(ExShape):
    '''角度的单位为度'''

    def __init__(self, *args):
        super().__init__()
        self.x = None
        self.y = None
        self.width = None
        self.height = None
        self.startAngle = None
        self.spanAngle = None
        self.pt0 = None
        self.pt1 = None
        self.pt2 = None
        if len(args) == 6:
            self.x = args[0]
            self.y = args[1]
            self.width = args[2]
            self.height = args[3]
            self.startAngle = args[4]
            self.spanAngle = args[5]

    def setValue(self,*args):
        if len(args) != 6:
            raise TypeError("不支持的参数数量")
        self.x = args[0]
        self.y = args[1]
        self.width = args[2]
        self.height = args[3]
        self.startAngle = args[4]
        self.spanAngle = args[5]

    def setRect(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def setStartAngle(self,angle):
        self.startAngle = angle

    def setSpanAngle(self, angle):
        self.spanAngle = angle

    def setPt0(self, pt0):
        self.pt0 = pt0

    def setPt1(self, pt1):
        self.pt1 = pt1

    def setPt2(self, pt2):
        self.pt2 = pt2

    def calculate(self):

        #先判断一下三个点是否 在阈值下 为一条直线 如果是 则返回False
        line = ExLine(self.pt0,self.pt1)
        line.setThreshold(2.5)
        if line.isPointOnShapeNoLimit(self.pt2, None):
            return False


        # 计算直线的一般方程
        a = self.pt1.y - self.pt0.y
        b = self.pt0.x - self.pt1.x
        #c = self.pt1.x * self.pt0.y - self.pt0.x * self.pt1.y

        # 计算直线的一般方程
        a1 = self.pt1.y - self.pt2.y
        b1 = self.pt2.x - self.pt1.x
        #c1 = self.pt1.x * self.pt2.y - self.pt2.x * self.pt1.y

        D = -a1*b + a*b1
        if D == 0:
            return False
        k = (a*(self.pt1.y+self.pt0.y) - b*(self.pt1.x + self.pt0.x))/2
        k1 = (a1*(self.pt2.y+self.pt1.y) - b1*(self.pt2.x + self.pt1.x))/2
        D1 = k*a1 - a*k1
        D2 = -b*k1 + k*b1

        centerPt = ExPoint(D1/D, D2/D)
        r = math.sqrt((centerPt.x - self.pt0.x)**2+(centerPt.y - self.pt0.y)**2)

        self.x = centerPt.x - r
        self.y = centerPt.y - r
        self.width = 2* r
        self.height = 2*r

        angle0 = ExArc.calculateAngel(self.pt0, centerPt, r)
        angle2 = ExArc.calculateAngel(self.pt2, centerPt, r)

        if angle0 > angle2:
            startPt = self.pt2
            endPt = self.pt0
        else:
            endPt = self.pt2
            startPt = self.pt0

        minAngel, maxAngle = (angle0, angle2) if angle0 < angle2 else (angle2, angle0)

        angle1 = ExArc.calculateAngel(self.pt1, centerPt, r)

        if angle1 < maxAngle and angle1 > minAngel:
            self.spanAngle = maxAngle - minAngel
        else:
            temp = startPt
            startPt = endPt
            endPt = temp
            self.spanAngle = 360 - (maxAngle - minAngel)

        if startPt is self.pt0:
            self.startAngle = angle0
        else:
            self.startAngle = angle2

        return True

    @staticmethod
    def calculateAngel(pt,centerPt, r):#计算以centerPt为圆心 pt和x轴的角度
        angle = math.asin((pt.y - centerPt.y) / r) * (180 / math.pi)

        if pt.y > centerPt.y:
            if pt.x >= centerPt.x:
                angle = 360 - angle
            else:
                angle += 180
        else:
            if pt.x >= centerPt.x:
                angle = -angle
            else:
                angle = 180 + angle
        return angle

    def getPoints(self):
        if self.pt0 and self.pt1 and self.pt2:
            return [self.pt0, self.pt2]
        else:
            return []

    def clear(self):
        self.x = None
        self.y = None
        self.startAngle = None
        self.spanAngle = None

    def isPointOnShape(self, pt, MainPlugin):
        return False

    def draw(self, QPainter, MainPlugin):
        if self.visible:
            QPainter.save()
            #定义画笔
            pen = QPen()
            pen.setColor(self.color)
            pen.setWidth(MainPlugin.line_width)
            pen.setStyle(self.penStyle)
            pen.setCapStyle(Qt.RoundCap)
            QPainter.setPen(pen)
            # 绘制图形
            if self.x!=None and self.y!=None and self.width !=None and self.height!=None and self.startAngle!=None and self.spanAngle!=None:
                QPainter.drawArc(self.x*MainPlugin.unit_pixel,self.y*MainPlugin.unit_pixel,self.width*MainPlugin.unit_pixel,self.height*MainPlugin.unit_pixel,self.startAngle*16,self.spanAngle*16)

            QPainter.restore()



class ExCircle(ExShape):

    def __init__(self,*args):
        super().__init__()
        self.centerPt = ExPoint()
        self.r = None
        if len(args) == 3:
            self.centerPt.x = args[0]
            self.centerPt.y = args[1]
            self.r = args[2]
        elif len(args) == 2:
            self.centerPt.x = args[0].x
            self.centerPt.y = args[0].y
            self.r = args[1]
        else:
            if len(args) != 0:
                raise TypeError("参数错误")

    def setValue(self,x,y,r):
        self.centerPt.x = x
        self.centerPt.y = y
        self.r = r

    def setRadius(self, r):
        self.r = r

    def setCenter(self,x,y):
        self.centerPt.x = x
        self.centerPt.y = y

    def isPointOnShape(self, pt, MainPlugin):
        threhold = 2
        rr = (pt.x - self.centerPt.x)*(pt.x - self.centerPt.x) + (pt.y - self.centerPt.y)*(pt.y - self.centerPt.y)
        if rr >= self.r*self.r - threhold and rr <= self.r*self.r + threhold:
            return True
        else:
            return False


    def getPoints(self):
        return [self.centerPt]

    def draw(self, QPainter, MainPlugin):
        if self.visible:
            QPainter.save()
            pen = QPen()
            pen.setWidth(MainPlugin.line_width)
            pen.setStyle(self.penStyle)
            pen.setColor(self.color)
            QPainter.setPen(pen)
            QPainter.drawEllipse((self.centerPt.x - self.r) * MainPlugin.unit_pixel, (self.centerPt.y - self.r) * MainPlugin.unit_pixel,
                                 2 * self.r * MainPlugin.unit_pixel, 2 * self.r * MainPlugin.unit_pixel)

            QPainter.restore()

#下面是一些 特殊图形 不是表示数据的图形 比如 坐标系的十字箭头等

class CirclePoint(ExPoint):

    HOVER = 0
    PRESSED = 1
    NONE = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r = 2
        self.state = CirclePoint.HOVER

    def draw(self, QPainter, MainPlugin):
        if self.visible:
            QPainter.save()
            if self.state == CirclePoint.HOVER:
                self.setColor(Qt.green)
            elif self.state == CirclePoint.PRESSED:
                self.setColor(Qt.red)
            pen = QPen()
            pen.setColor(self.color)
            pen.setWidth(MainPlugin.line_width)
            QPainter.setPen(pen)
            #绘制一个圆圈
            QPainter.drawEllipse((self.x-self.r)*MainPlugin.unit_pixel, (self.y-self.r)*MainPlugin.unit_pixel, 2*self.r*MainPlugin.unit_pixel, 2*self.r*MainPlugin.unit_pixel)
            #再绘制一下中心点
            QPainter.drawPoint(self.x*MainPlugin.unit_pixel,self.y*MainPlugin.unit_pixel)

        QPainter.restore()

class FreeLine(ExLine):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.pen = QPen()
        self.pen.setColor(Qt.gray)
        self.pen.setStyle(Qt.DotLine)
        self.pen.setCapStyle(Qt.RoundCap)
        self.pen.setWidth(2)

    def setPen(self, pen):
        if pen:
            self.pen = pen

    def draw(self, QPainter, MainPlugin):
        if self.visible:
            QPainter.save()
            if self.pen:
                QPainter.setPen(self.pen)
            # 绘制图形
            QPainter.drawLine(self.pt0.x * MainPlugin.unit_pixel, self.pt0.y * MainPlugin.unit_pixel,
                                  self.pt1.x * MainPlugin.unit_pixel, self.pt1.y * MainPlugin.unit_pixel)
            QPainter.restore()