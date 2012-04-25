%Metropolis sampling with 
num_samples = 100000;
burnin = 2000;
in = [];
out = [];

%target is N(0,1), or normpdf(x, 0, 1);
%init our mean at 0, and use an arbitrary std deviation of .35
init = 1;
chosen_var = .35;

prev = 0;
itr = 1;
for i = 1:num_samples
    candidate = prev + chosen_var*randn(1,1);
    ll_prev = normpdf(prev, 0, 1);
    ll_candidate = normpdf(candidate, 0, 1);
    acceptance = min([ll_candidate/ll_prev, 1]);
    in(i) = candidate;
    if acceptance >= rand(1,1)
        prev = candidate;
        out(itr) = candidate;
        itr = itr + 1;
    end
end

%Use 1000 for better hist resolution
hist(out(burnin:length(out)), 1000);
figure();
hist(in, 1000);

%plot(x1, n1, 'r');
%hold on;
%plot(x2, n2, 'b');

