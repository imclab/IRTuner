#!/usr/bin/python
# Generate data for program
note_hz = [
    82.407,
    110.000,
    146.832,
    195.998,
    246.942,
    329.628,    
]

# 16*10^6 / 128 / 13 / D / 2  *  (32/128) = f
def error(f, dest_B=32, presc=128, scale=128):
        D = 615384.6153846154 * dest_B / f / presc / scale
        Di = round(D)
        Bar = 1.6249999999999998e-6 * f * Di * presc * scale
        Bari = round(Bar)
        real_hz = 615384.6153846154 * Bari / Di / presc / scale
#        print D, Di, Bar, Bari, real_hz
        return abs(f - real_hz), Di, Bari


def table(dest_B=32, presc=128):
    for f in note_hz:
    
        D = 4807.692307692308 * dest_B / f / presc
        Di = round(D)
        Bar = 2.0799999999999996e-4 * f * Di * presc
        Bari = round(Bar)
        real_hz = 4807.692307692308 * Bari / Di / presc
        print "%10f %10.2f (%2d) %10.2f (%2d) Real Hz: %5.3f Error: %5.2f" % (f, D, Di, Bar, Bari, real_hz, f - real_hz)
    print

table(dest_B=32, presc=64)
table(dest_B=45, presc=64)
table(dest_B=64, presc=64)


for f in note_hz:
    sm_err = 300
    sm_bar = 0
    for bar in range(30, 60):
        er, div, real_bar = error(f, dest_B=bar)
        if er < sm_err:
            sm_err = er
            sm_bar = real_bar
    print f, "bar:", sm_bar, "err:", sm_err


for f in note_hz:
    sm_err = 300
    sm_bar = 0
    sm_presc = 0
    sm_div = 0
    presc = 128
    scale = 64
    bar = 48 #scale/2 

    er, div, real_bar = error(f, dest_B=bar, presc=presc, scale=scale)
    if er < sm_err:
        sm_err = er
        sm_bar = real_bar
        sm_div = div
        sm_presc = presc
        
    print "	/* f=%.3f presc=%d div=%d bar=%d err=%.5f scale=%d  */" % (f, sm_presc, sm_div, sm_bar, sm_err, scale)
    print "	{%d, %dU}, " % (sm_div, f * 100)



for i in range(1,41):
        print "i:", i, "spaces:", (i-1)/5, "char:", ((i-1)%5)
