import rclpy
from rclpy.node import Node

from kv_interfaces.msg import Ki

class Node3(Node):
    def __init__(self):
        super().__init__('pipeline_node3')
        self.sub_ = self.create_subscription(
                Ki,
                'data2',
                self.subscription_callback,
                300)
        self.crc_table = dict()
        self.gen_crc8()
        self.sub_num_ = 0
        self.err_num_ = 0

    def gen_crc8(self):
        CRC_POLY = 0x8c #CRC-8-Dallas/Maxim. right shift. x^8+x^5+x^4+1
        for i in range(256):
            result = i
            for j in range(8):
                if(result & 1):
                    result = CRC_POLY ^ (result >> 1)
                else:
                    result = result >> 1
            self.crc_table[i] = result

    def calc_crc8(self, data):
        result = 0
        for item in data:
            result = self.crc_table[result ^ item]
            #self.get_logger().info("in:%02x,crc:%02x" % (item,result))
        return result

    def subscription_callback(self, msg):
        self.sub_num_ += 1
        data = [(msg.val    >> 24) & 0xFF,
                (msg.val    >> 16) & 0xFF,
                (msg.val    >>  8) & 0xFF,
                (msg.val         ) & 0xFF,
                (msg.status >> 24) & 0xFF,
                (msg.status >> 16) & 0xFF,
                (msg.status >>  8) & 0xFF,
                (msg.status      ) & 0xFF]
        result = self.calc_crc8(data)
        if(result != 0):
            self.err_num_ += 1
            self.get_logger().info('error!key:%x,val:%08x,status:%08x' % (msg.key, msg.val))
        self.get_logger().info('key:%s,val:0x%08x,status:0x%08x,received:%d,err:%d' % (msg.key,msg.val,msg.status,self.sub_num_,self.err_num_))

def main(args=None):
    rclpy.init(args=args)

    node3 = Node3()

    rclpy.spin(node3)

    node3.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
