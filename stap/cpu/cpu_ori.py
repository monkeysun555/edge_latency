global cputimes;
global cmdline;
global oncpu;
global usage;
global NS_PER_SEC = 1000000000;

# global tcp_send = 0;
# global udp_send = 0;
global process = @1;


probe begin {
    printf("Monitoring CPU usage of %s", process)
}
probe scheduler.cpu_on {
    if (isinstr(cmdline_str(), process)) {
        oncpu[pid()] = local_clock_ns();
    }
}

probe scheduler.cpu_off {
    if(oncpu[pid()] == 0)
        next;

    cmdline[pid()] = cmdline_str();
    cputimes[pid(), cpu()] <<< local_clock_ns() - oncpu[pid()];

    delete oncpu[pid()];
}

# probe tcp.sendmsg {
#     if (isinstr(execname(), process)){
#         tcp_send += 1
#     }
# }

# probe udp.sendmsg {
#     if (dport == 22222){
#         udp_send += 1
#     }
# }


probe timer.s(1) {
    printf("%6s %3s %6s %s\n", "PID", "CPU", "PCT", "CMDLINE");
    foreach([pid+, cpu] in cputimes) {
        cpupct = @sum(cputimes[pid, cpu]) * 10000 / NS_PER_SEC;
        usage += cpupct
        # printf("%6d %3d %3d.%02d %s\n", pid, cpu, 
        #     cpupct / 100, cpupct % 100, cmdline[pid]);
    }
    printf("%6d %3s %3d.%02d %s\n", pid, "sum", 
            usage / 100, usage % 100, cmdline[pid]);

    delete cputimes;
    delete usage;

}