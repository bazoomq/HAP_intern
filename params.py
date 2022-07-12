from scipy.special import hyp2f1

g = 9.8065
L0 = 24.06031 * g
wp = 0.229158
rp_max = 6.122831
l = 2 * hyp2f1(1/4, 1/2, 5/4, 1) * rp_max
ds = 0.002
