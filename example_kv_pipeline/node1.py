import rclpy
from rclpy.node import Node

from kv_interfaces.msg import Ki

class Node1(Node):
    def __init__(self):
        super().__init__("pipeline_step1")
        self.pub_   = self.create_publisher(Ki, "data1", 300)
        self.timer_ = self.create_timer(1.0, self.publish_data)
        self.v_     = 0
        self.crc_table = dict()
        self.gen_crc8()

    def gen_crc8(self):
        CRC_POLY = 0x8c #CRC-8-Dallas/Maxim. right shift. x^8+x^5+x^4+1
        for i in range(256):
            result = i
            for j in range(8):
                if(result & 1):
                    result = CRC_POLY ^ (result >> 1)
                else:
                    result = result >> 1
            self.crc_table[i] = result & 0xFF

    def calc_crc8(self, data):
        result = 0
        for item in data:
            result = self.crc_table[result ^ item]
            #self.get_logger().info("in:%02x,crc:%02x" % (item,result))
        return result
    
    def publish_data(self):
        self.get_logger().info('===========%d============' % self.v_)
        for i in range(100):
            msg = Ki()
            msg.key = "key" + str(i)
            msg.val = ((self.v_ + i + 6) << 24) + \
                      ((self.v_ + i + 5) << 16) + \
                      ((self.v_ + i + 4) <<  8) + \
                      ((self.v_ + i + 3) <<  0)
            msg.status = ((self.v_ + i + 2) << 24) + \
                         ((self.v_ + i + 1) << 16) + \
                         ((self.v_ + i + 0) <<  8) + \
                           self.calc_crc8([
                                        self.v_ + i + 6, \
                                        self.v_ + i + 5, \
                                        self.v_ + i + 4, \
                                        self.v_ + i + 3, \
                                        self.v_ + i + 2, \
                                        self.v_ + i + 1, \
                                        self.v_ + i + 0])
            self.pub_.publish(msg)
            self.get_logger().info("%s:0x%08x,0x%08x" % (msg.key,msg.val,msg.status))
        self.v_ = (self.v_ + 1) % 128 #avoid overflow

def main(args=None):
    rclpy.init(args=args)

    data1_publisher = Node1()

    rclpy.spin(data1_publisher)

    data1_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
