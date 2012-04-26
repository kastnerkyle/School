%Metropolis sampling with 
num_samples = 100000;
burnin = 10000;
in = [];
out = [];

%target is N(0,1), or normpdf(x, 0, 1);
%init our mean at 0, and use an arbitrary std deviation of .35
init = 1;
chosen_var = .35;

prev = init;
itr = 1;
for i = 1:num_samples
    candidate = prev + chosen_var*randn(1,1);
    ll_prev = normpdf(prev, 0, 1);
    ll_candidate = normpdf(candidate, 0, 1);
    %new/old * old/new
    cond_candidate = normpdf(prev, candidate, 1);
    cond_prev = normpdf(candidate, prev, 1);
    top = ll_candidate*cond_prev;
    bottom = ll_prev*cond_candidate;
    acceptance = min([ll_candidate/ll_prev, 1]);
    in(i) = candidate;
    if acceptance >= rand(1,1)
        prev = candidate;
        out(itr) = candidate;
        itr = itr + 1;
    end
end

%Use 1000 for better hist resolution
[x1, n1] = hist(out(burnin:length(out)), 1000);
[x2, n2] = hist(in, 1000);

plot(n1, x1, 'r');
hold on;
plot(n2, x2, 'b');

