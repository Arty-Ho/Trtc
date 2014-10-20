from trtc_check import Trtc
import unittest


class Trtc_test(unittest.TestCase):

    def setUp(self):
        self.test = Trtc(pir=1000, pbs=2000, cir=500, cbs=1000)

    def tearDown(self):
        self.test = None

    def test_metering_yellow(self):
        self.test.tp = 600
        self.test.tc = 300
        self.assertEqual(self.test.metering(500), 'yellow')

    def test_metering_red(self):
        self.test.tp = 600
        self.test.tc = 300
        self.assertEqual(self.test.metering(800), 'red')

    def test_metering_green(self):
        self.test.tp = 600
        self.test.tc = 300
        self.assertEqual(self.test.metering(200), 'green')

    def test_metering_undersize(self):
        self.test.tp = 600
        self.test.tc = 300
        self.assertEqual(self.test.metering(0), 'error')

    def test_token_buckets_update_tp_tc_add(self):
        self.test.tp = 200
        self.test.tc = 100
        self.test.token_buckets_update(1001)
        self.assertEqual(200 + self.test.pir, self.test.tp)
        self.assertEqual(100 + self.test.cir, self.test.tc)

    def test_token_buckets_update_tp_max(self):
        self.test.tp = 1200
        self.test.tc = 300
        self.test.token_buckets_update(1001)
        self.assertEqual(self.test.pbs, self.test.tp)
        self.assertEqual(300 + self.test.cir, self.test.tc)

    def test_token_buckets_update_tc_max(self):
        self.test.tp = 900
        self.test.tc = 800
        self.test.token_buckets_update(1001)
        self.assertEqual(900 + self.test.pir, self.test.tp)
        self.assertEqual(self.test.cbs, self.test.tc)

    def test_check_packet_size_undersize(self):
        self.assertEqual(-1, self.test.check(1, 20, None, None, None))

    def test_check_packet_size_green_error_red(self):
        self.assertEqual(-1, self.test.check(1, 80, 'red', 1920, 920))

    def test_check_packet_size_green_error_yellow(self):
        self.assertEqual(-1, self.test.check(1, 80, 'yellow', 1920, 920))

    def test_check_packet_size_green_correct(self):
        self.assertEqual(0, self.test.check(1, 80, 'green', 1920, 920))

    def test_check_token_bucket_mismatch_tp(self):
        self.assertEqual(-1, self.test.check(1, 80, 'green', 1980, 920))

    def test_check_token_bucket_mismatch_tc(self):
        self.assertEqual(-1, self.test.check(1, 80, 'green', 1920, 980))

if __name__ == '__main__':
    unittest.main()
