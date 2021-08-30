F=readmatrix("cd.txt")';
F=lowpass(F,0.001);
plot(F)
Fs = 1/0.005;
L = length(F);
len = 5;
l = floor(L/len);
f = Fs*(0:(l/2))/l;
for q=1:len
    s = F((q-1)*l+1:q*l);
    s = fft(s);
    P2 = abs(s/l);
P1 = P2(1:l/2+1);
P1(2:end-1) = 2*P1(2:end-1);
  subplot(len,1,q)
plot(f,P1)
if q == 3
    title("Merge")
end
ylim([0,0.1])
xlabel('f (Hz)')
end
%title('Single-Sided Amplitude Spectrum of X(t)')

%ylabel('|P1(f)|')