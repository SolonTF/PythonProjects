% a code for simulation of Brown noise

R=randn(1000,50)
K=cumsum(R)
plot(K)
