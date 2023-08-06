#!/usr/bin/env python
# -*- coding: utf-8 -*-


import statefulfirewall


fw = statefulfirewall.StateFulFireWall()

print(fw.protobynumber)
for log in fw.yield_logs(limit=100):
    if 'conntrack_type' in log:
        #print('%-8s %s' % (log['conntrack_type'], log['id']))
        continue
    else:
        if 'DPT' not in log:
            log['DPT'] = ''
        if log['PROTO'].isnumeric():
            log['PROTO'] = fw.protobynumber[int(log['PROTO'])]
        print('packet   %-16s %-16s %4s %5s %-15s' % (
                    log['SRC'],
                    log['DST'],
                    log['PROTO'],
                    log['DPT'],
                    str(log['LOG_DATE']),
        ))

