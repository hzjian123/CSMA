% This function takes an input vector of probabilities, p, where:
    % p(1): the probability that a STA transmits in a certain time slot,
    % denoted by \tau in Bianchi's model
    % p(2): the conditional probability of a transmission collision,
    % denoted by p in Binachi's model
    % p(3): the conditional probability of a transmission failure, either 
    % due to transmission collision or channel error
% The output of this function is a three dimensional vector, F, where: 
    % F(1): the value of the difference between the LHS and RHS of eqn [7] 
    % in Bianchi's paper
    % F(2): the value of the difference between the LHS and RHS of eqn [9] 
    % in Bianchi's paper
    % F(3): the value of p(3) - ( 1 - (1-p(2))(1-p_channel) ) 
% the entries of the F vector are evaluated at the values of p input to the
% function

function F = Bianchi_eqns(p)

global n_nodes w m p_channel n c%W=2^3 m=(2^5-2^2) = 2
tau = p(1); 
p_c = p(2); 
p_e = p(3); 
F(1) = p(1) - 2*(1-2*p_e)/((1-2*p_e)*(w+1)+p_e*w*(1-(2*p_e)^m));
F(2) = p_c-(1-(1-tau)^(n_nodes(n)-1));
F(3) = p_e-(1-(1-p_c)*(1-p_channel(c)));

end

% parameters, w, m , p_channel