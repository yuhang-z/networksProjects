import statistics
import matplotlib.pyplot as plt

size = [32, 64, 128, 256, 512]
dft_mean = list()
dft_std = list()
fft_mean = list()
fft_std = list()

dft32 = [
    0.2854188000000004,
    0.24196779999999984,
    0.22641540000000004,
    0.23377360000000014,
    0.2443276000000001,
    0.24465540000000008,
    0.21904160000000017,
    0.22423099999999963,
    0.22613470000000024,
    0.2233723999999997,
    0.23506859999999996,
    0.24060389999999998,
    0.1953232000000007,
    0.09563379999999988,
    0.09540930000000003
]
dft_mean.append(statistics.mean(dft32))
dft_std.append(statistics.stdev(dft32))
dft64 = [
    0.9933639000000003,
    1.8389115999999994,
    0.8472989000000002,
    1.6989459999999994,
    1.6839405999999997,
    0.83812,
    0.8514326000000008,
    1.664095999999999,
    1.6778613000000018,
    0.8072052999999997,
    1.7833220999999995,
    1.6322089999999996,
    0.8430664000000014,
    0.8473657999999986,
    1.7962933999999997
]
dft_mean.append(statistics.mean(dft64))
dft_std.append(statistics.stdev(dft64))
dft128 = [
    11.458069300000002,
    10.4317019,
    10.706633199999999,
    9.785723599999997,
    9.630841499999988,
    9.943233400000011,
    15.666832299999996,
    14.183601799999991,
    12.554642400000006,
    11.419924199999997,
    9.984897499999988,
    13.996764099999979,
    12.273065500000001,
    12.128517299999999,
    12.824860900000004
]
dft_mean.append(statistics.mean(dft128))
dft_std.append(statistics.stdev(dft128))
dft256 = [
    92.66005290000001,
    97.78487890000002,
    89.4728518,
    100.73381710000007,
    90.47773480000001,
    99.97272180000004,
    96.9173151,
    89.71772770000007,
    95.26000339999996,
    113.45563179999999,
    94.66993120000006,
    108.64297140000008,
    95.5755959999999,
    98.33220719999986,
    92.96268179999993
]
dft_mean.append(statistics.mean(dft256))
dft_std.append(statistics.stdev(dft256))
dft512 = [
    731.4017257999999,
    760.0898778000001,
    794.7715177,
    782.0835031000001,
    694.1314087000001,
    658.6156046999995,
    700.3555162000002,
    800.7066695000003,
    756.5604688000003,
    758.1042029,
    732.1335953999987,
    685.9723685999998,
    694.8230378000007,
    701.9032060000009,
    715.7291456999992
]
dft_mean.append(statistics.mean(dft512))
dft_std.append(statistics.stdev(dft512))

fft32 = [
    0.10475709999999994,
    0.09611259999999988,
    0.09682499999999994,
    0.10375979999999996,
    0.10646480000000014,
    0.10262409999999988,
    0.0965395,
    0.10278770000000015,
    0.10748000000000002,
    0.10960129999999979,
    0.16815249999999993,
    0.2268577999999999,
    0.22742050000000003,
    0.21953150000000043,
    0.2485858000000003
]
fft_mean.append(statistics.mean(fft32))
fft_std.append(statistics.stdev(fft32))
fft64 = [
    0.9190741999999998,
    0.9494769000000001,
    0.5513928999999997,
    0.4282545000000004,
    0.7789885999999999,
    0.9363016999999996,
    0.8906948999999988,
    0.7799081999999995,
    0.4529318,
    0.505075699999999,
    0.9215758000000012,
    0.9139559999999989,
    0.9428450000000002,
    0.5411314000000012,
    0.4128936000000003
]
fft_mean.append(statistics.mean(fft64))
fft_std.append(statistics.stdev(fft64))
fft128 = [
    3.332033899999999,
    1.5435371000000018,
    3.181268899999999,
    2.283337200000002,
    2.799144899999998,
    1.8994822000000013,
    2.9822321999999986,
    3.3281477000000024,
    1.8012805999999983,
    3.2158727000000056,
    2.262334299999999,
    3.4210825999999983,
    2.9814328000000003,
    2.2992188999999996,
    2.9677910999999995
]
fft_mean.append(statistics.mean(fft128))
fft_std.append(statistics.stdev(fft128))
fft256 = [
    9.995969600000002,
    10.031781699999996,
    12.073452799999998,
    9.9516943,
    10.780687200000003,
    10.749400499999993,
    9.928137399999997,
    10.163141900000014,
    12.250875500000006,
    10.005870799999997,
    10.922043200000019,
    11.516809599999988,
    9.973730900000021,
    12.230565899999988,
    11.509925199999998
]
fft_mean.append(statistics.mean(fft256))
fft_std.append(statistics.stdev(fft256))
fft512 = [
    41.2932211,
    42.5951857,
    41.042766400000005,
    41.050893,
    40.078670500000015,
    41.27331369999999,
    41.94865610000002,
    42.03450950000001,
    41.66601490000005,
    41.738072699999975,
    40.85942180000001,
    42.998015699999996,
    43.07122059999995,
    41.526408100000026,
    42.33222760000001
]
fft_mean.append(statistics.mean(fft512))
fft_std.append(statistics.stdev(fft512))

plt.figure("Mode_4")

some = plt.subplot(121)

plt.plot(size, dft_mean, label = "DFT")
plt.plot(size, fft_mean, label = "FFT")
plt.xlabel('Size')
plt.ylabel('Runtime Mean')
plt.title('Mean')
plt.legend()

plt.subplot(122)
plt.plot(size, dft_std, label = "DFT")
plt.plot(size, fft_std, label = "FFT")
plt.xlabel('Size')
plt.ylabel('Runtime Std. Dev.')
plt.title('Standard Deviation')
plt.legend()
plt.show()