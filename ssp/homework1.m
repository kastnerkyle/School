vsigs = [.01,.5,1];
for idx=1:length(vsigs)
    wmean = 0;
    wsig = .6;
    wcount = 1000;
    
    xmult = .8;
    xr = @(xmult, xp, wsig) ...
        xmult*xp + wsig*randn(1, 1);
    
    %Generate signal for 1:1000, using random value as initial Xr-1
    x(1) = 0;
    for t=2:wcount
        x(t) = xr(xmult,x(t-1),wsig);
    end
    
    %Remove initializer
    x = x(2:end);
    
    vmean = 0;
    vsig = vsigs(idx);
    
    ymult = .9;
    yk = @(ymult, xk, vsig) ...
        ymult*xk + vsig*randn(1,1);
    
    %Generate received waveform, given x
    for t=1:length(x)
        y(t) = yk(ymult, x(t), vsig);
    end
    
    %Kalman Filtering
    %Init and function definitions
    last_mean = wmean;
    last_sig = wsig;
    last_mean_k = wmean;
    last_sig_k = wsig;
    
    pred_mean = @(last_mean) ...
        xmult*last_mean;
    pred_sig = @(last_sig) ...
        sqrt(xmult^2*last_sig^2+wsig^2);

    %Different Approach - trouble shooting
    k_gain = @(pred_sig) ...
        pred_sig*ymult/(ymult^2*pred_sig+vsig);
    k_post_mean = @(pred_mean, pred_sig, meas_val) ...
        pred_mean+k_gain(pred_sig)*(meas_val-ymult*pred_mean);
    k_post_sig = @(pred_sig) ...
        pred_sig - k_gain(pred_sig)*ymult*pred_sig;
    
    %Class Approach
    post_mean = @(pred_mean, pred_sig, meas_val, meas_sig) ...
        ((pred_mean/(pred_sig^2))+(meas_val/(meas_sig^2)))/((1/(pred_sig^2))+(1/(meas_sig^2)));
    post_sig = @(pred_sig, meas_sig) ...
        (sqrt((1/(pred_sig^2))+(1/(meas_sig^2))))^-1;
    
    %Generate all predictions and update
    ye = zeros([1,length(x)]);
    yek = zeros([1,length(x)]);
    for i=1:length(x)
        temp_mean_k = pred_mean(last_mean_k);
        temp_sig_k = pred_sig(last_sig_k);
        
        temp_mean = pred_mean(last_mean);
        temp_sig = pred_sig(last_sig);
        
        ye(i) = normrnd(temp_mean, temp_sig);
        yek(i) = normrnd(temp_mean_k, temp_sig_k);
        
        last_mean_k = k_post_mean(temp_mean_k, temp_sig_k, y(i));
        last_sig_k = k_post_sig(temp_sig_k);
        
        last_mean = post_mean(temp_mean, temp_sig, y(i), vsig);
        last_sig = post_sig(temp_sig, vsig);
    end
    
    figure();
    hold on;
    plot(x, 'red');
    %plot(y, 'green');
    plot(ye, 'blue');
    %plot(yek, 'black');
    hold off;
end
