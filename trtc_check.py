import argparse
import re
import sys
# definition:
#     four traffic parameters:
#         PIR:    Peak Information Rate.(byte of IP packets per second)
#         PBS:    Peak Burst Size.
#         CIR:    Committed Information Rate.(byte of IP packets per second)
#         CBS:    Committed Burst Size.
#
#     limited:
#         PIR >= CIR
#         PBS > 0
#         CBS > 0
#         It is recommended that they be configured to be equal to or greater
#         than the size of the largest possible IP packet in the stream.
#


class Trtc:
    def __init__(self, pir = None, pbs = None, cir = None, cbs = None):
        if pir is not None:
            self.pir = pir

        if pbs is not None:
            self.pbs = pbs

        if cir is not None:
            self.cir = cir

        if cbs is not None:
            self.cbs = cbs

        self.tp = self.pbs
        self.tc = self.cbs
        self.time = 0


    def token_buckets_update(self, arrive_time):
        unit_second = 1000
        if arrive_time - self.time >= unit_second:
            if self.tp + self.pir > self.pbs:
                self.tp = self.pbs
            else:
                self.tp = self.tp + self.pir

            if self.tc + self.cir > self.cbs:
                self.tc = self.cbs
            else:
                self.tc = self.tc + self.cir
            self.time = self.time + unit_second


    def metering(self, packet_size):
        if self.tp - packet_size < 0:
            color = "red"
        if self.tc - packet_size < 0:
            color = "yellow"
            self.tp = self.tp - packet_size
        else:
            color = "green"
            self.tp = self.tp - packet_size
            self.tc = self.tc - packet_size

        return color

    def check(self, arrive_time = None, packet_size = None, trtc_color = None,
              trtc_tp = 0, trtc_tc = 0):

        error_print = 0

        if packet_size < 64:
            return -1

        self.token_buckets_update(arrive_time)

        self.color = self.metering(packet_size)

        if self.color != trtc_color:
            print "color not match"
            error_print = 1


        if (self.tp != trtc_tp) or (self.tc != trtc_tc):
            print "token buckets not match"
            error_print = 1

        if error_print == 1:
            print "trtc:  " + trtc_color
            print "check: " + self.color
            print "trtc_tp:  %d" % trtc_tp
            print "check_tp: %d" % self.tp
            print "trtc_tc:  %d" % trtc_tc
            print "check_tc: %d" % self.tc
            sys.exit()

        return 0

def main(file_name = None, pir = None, pbs = None, cir = None, cbs = None):
    trtc = Trtc(pir = pir, pbs = pbs, cir = cir, cbs = cbs)
    trtc_file = open(file_name, 'r')
    # skip first line
    line = trtc_file.readline()
    while True:
        line = trtc_file.readline()
        if len(line) == 0:
            break
        line_list = re.findall(r"[\w']+", line)
        # assign parameters
        arrive_time = int(line_list[0], 10)
        index = int(line_list[1], 10)
        packet_size = int(line_list[2], 10)
        trtc_color = line_list[3]
        trtc_tp = int(line_list[4], 10)
        trtc_tc = int(line_list[5], 10)
        ret = trtc.check(arrive_time = arrive_time, packet_size = packet_size,
                         trtc_color = trtc_color, trtc_tp = trtc_tp,
                         trtc_tc = trtc_tc)
        if ret < 0:
            break

    print "PASS"
def args_parser():
    parser = argparse.ArgumentParser(description='Trtc function check.')
    # option
    parser.add_argument('-version','-v', action='version',
                        version='%(prog)s 1.0.0')
    # must
    parser.add_argument('trtc_file', metavar='trtc_file', type=str, nargs=1,
                        help="The trtc file.")
    parser.add_argument('pir', metavar='pir', type=int, nargs=1,
                        help="The Peak Information Rate.")
    parser.add_argument('pbs', metavar='pbs', type=int, nargs=1,
                        help="The Peak Burst Size.")
    parser.add_argument('cir', metavar='cir', type=int, nargs=1,
                        help="The Committed Information Rate.")
    parser.add_argument('cbs', metavar='cbs', type=int, nargs=1,
                        help="The Committed Burst Size.")
    args = parser.parse_args()
    return args





if __name__ == '__main__':
    args = args_parser()
    main(file_name = args.trtc_file[0], pir = args.pir[0], pbs = args.pbs[0],
         cir = args.cir[0], cbs = args.cbs[0])
    sys.exit()
