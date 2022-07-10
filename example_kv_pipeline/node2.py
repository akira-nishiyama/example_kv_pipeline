import rclpy
from rclpy.node import Node

from kv_interfaces.msg import Ki

class Node2(Node):
    def __init__(self):
        super().__init__('pipeline_step2')
        self.sub_ = self.create_subscription(
                Ki,
                'data1',
                self.subscription_callback,
                300
                )
        self.pub_ = self.create_publisher(Ki, 'data2', 300)
        timer_period = 1
        self.timer = self.create_timer(timer_period, self.publish_data)
        self.table = dict()
        self.st_table = dict()

        self.sub_ # prevent unused variable warning

    def subscription_callback(self, msg):
        self.table[msg.key] = msg.val
        self.st_table[msg.key] = msg.status

    def publish_data(self):
        for k,v in self.table.items():
            msg = Ki()
            msg.key = k
            msg.val = v
            msg.status = self.st_table[k]
            self.pub_.publish(msg)
            self.get_logger().info('%s:%08x,%08x' % (msg.key, msg.val, msg.status))

def main(args=None):
    rclpy.init(args=args)

    node2 = Node2()

    rclpy.spin(node2)

    node2.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
