
num_samples = 10000;
burnin = 1000;
in = [];
out = [];
i = 1;
j = 1;
prev = randn(1,1);
for i = 1:burnin
    
    epsilon = prev + randn(1,1);
end
for i = 1:num_samples
    
    epsilon = prev + randn(1,1);    
end
[n1, x1] = hist(in, 1000);
[n2, x2] = hist(out, 1000);
plot(x1, n1, 'r');
hold on;
plot(x2, n2, 'b');
show();
