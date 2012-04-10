
num_samples = 10000;
in = [];
out = [];
i = 1;
j = 1;
while length(out) < num_samples
    sample = 4*(rand(1,1)-.5);
    in(j) = sample;
    j = j + 1;
    target_dist = normpdf(sample,0,1)/(2*pi);
    if rand(1,1) < abs(target_dist/sample)
        out(i) = sample;
        i = i + 1;
    end
end
[n1, x1] = hist(in, 1000)
[n2, x2] = hist(out, 1000)
plot(x1, n1, 'r')
hold on
plot(x2, n2, 'b')
show()
