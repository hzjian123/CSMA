global p_channel n_nodes n c w m;
[p_channel,n_nodes,c,n,w,m] = deal(0:0.05:0.95, 2:20,2,7,8,3);%m=3,  w=8
ret = fsolve(@Bianchi_eqns,zeros(1,3),optimset('Display','off'))